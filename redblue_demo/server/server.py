"""
This module implements the server class for the RedBlue consistency protocol.
"""

import threading
import xmlrpc.client
from xmlrpc.server import SimpleXMLRPCServer

from queue import Queue
from collections import deque
from typing import List, NamedTuple
from redblue_demo.common.bank_storage import BankStorage
from redblue_demo.common.shadow_op import ShadowOP
from redblue_demo.common.vector_clock import VectorClock
from redblue_demo.common.common import Request


class ServerConfig:
    """
    Represents the configuration for a server.
    """

    def __init__(self, index: int, addr: List[str]) -> None:
        self.index = index
        self.addr = addr


# A NamedTuple to hold request and response queue
class RequestItem(NamedTuple):
    """
    Represents an item in the request queue.

    Attributes:
        req (Request): The request object.
        res_queue (Queue): The response queue.
    """

    req: Request
    res_queue: Queue


class Server:
    """
    Represents a server in the system.

    Attributes:
        id (int): The index of the server.
        bank (BankStorage): The storage for the server's bank.
        now (VectorClock): The vector clock for the server.
        max_r (int): The maximum red value seen by the server.
        has_token (bool): Indicates whether the server has the token.
        peers (List[ServerProxy]): The list of server proxies representing the peers.
        token_queue (Queue): The queue for token messages.
        req_queue (Queue): The queue for request messages.
        shadow_queue (Queue): The queue for shadow operation messages.
        op_list (deque): The list of shadow operations.
        red_list (deque): The list of red requests.
        addrs (List[str]): The list of server addresses.
    """

    def __init__(self, index: int, addrs: List[str]) -> None:
        """
        Initializes a new instance of the Server class.

        Args:
            index (int): The index of the server.
            addrs (List[str]): The list of server addresses.
        """
        num_server = len(addrs)

        self.id = index
        self.bank = BankStorage()
        self.now = VectorClock(num_server)
        self.max_r = 0
        self.has_token = False
        self.peers = [None] * num_server
        self.token_queue = Queue()
        self.req_queue = Queue()
        self.shadow_queue = Queue()
        self.op_list = deque()
        self.red_list = deque()

        self.addrs = addrs

    @classmethod
    def from_config(cls, config: ServerConfig) -> "Server":
        """
        Creates a new Server instance from a ServerConfig object.

        Args:
            config (ServerConfig): The ServerConfig object.

        Returns:
            Server: The new Server instance.
        """
        return cls(config.index, config.addr)

    def run(self):
        """
        Runs the server.

        This method sets up the RPC server, establishes peer connections,
        and starts the main loop.
        """
        # Setup RPC server
        server = SimpleXMLRPCServer((self.addrs[self.id], 8000), allow_none=True)
        server.register_instance(self)

        # Setup peer connection
        def setup_peers():
            for i, addr in enumerate(self.addrs):
                if i == self.id:
                    continue
                self.peers[i] = xmlrpc.client.ServerProxy(addr)
            print(f"server {self.id}: peer connection established")
            self.main_loop()

        peer_thread = threading.Thread(target=setup_peers)
        peer_thread.start()
        server.serve_forever()

    def set_token_timeout(self) -> None:
        """
        Sets the token timeout.

        This method is responsible for implementing the functionality
        to set the token timeout.
        """
        raise NotImplementedError("TODO: Implement this functionality")

    def primary(self) -> bool:
        """
        Checks if the server is the primary server.

        Returns:
            bool: True if the server is the primary server, False otherwise.
        """
        raise NotImplementedError("TODO: Implement this functionality")

    def do_request(self, req_item: RequestItem) -> bool:
        """
        Processes a request item.

        Args:
            req_item (RequestItem): The request item to process.

        Returns:
            bool: True if the request item was processed successfully, False otherwise.
        """
        raise NotImplementedError("TODO: Implement this functionality")

    def main_loop(self) -> None:
        """
        The main loop of the server.

        This method is responsible for processing the token queue, shadow queue,
        request queue, operation list, and red list.
        """
        if self.id == 0:
            self.set_token_timeout()
            self.has_token = True

        while True:
            try:
                # Process token_queue
                while not self.token_queue.empty():
                    max_r = self.token_queue.get()
                    if self.has_token:
                        self.has_token = False
                        next_id = (self.id + 1) % len(self.peers)
                        if self.peers[next_id] is not None:
                            self.peers[next_id].pass_token(self.max_r)
                    else:
                        self.max_r = max_r
                        self.has_token = True
                        self.set_token_timeout()

                # Process shadow_queue
                while not self.shadow_queue.empty():
                    shadow: ShadowOP = self.shadow_queue.get()
                    self.op_list.append(shadow)

                # Process req_queue
                while not self.req_queue.empty():
                    req_item = self.req_queue.get()
                    if not self.do_request(req_item):
                        self.red_list.append(req_item)

                # Process op_list
                while True:
                    todo = False
                    for shadow in list(self.op_list):
                        if shadow.depend.ready(self.now):
                            shadow.apply(self.bank)
                            self.now.tick(shadow.server_id, shadow.color)
                            self.now.print(self.id)
                            if self.now.red() > self.max_r:
                                self.max_r = self.now.red()

                            todo = True
                            self.op_list.remove(shadow)

                    if not todo:
                        break

                # Process red_list if primary
                if self.primary():
                    for req_item in list(self.red_list):
                        ok = self.do_request(req_item)
                        if not ok:
                            raise ValueError(f"server {self.id}: process redList fail")
                    # Clear red_list after processing all items
                    self.red_list.clear()

            except ValueError as e:
                print(f"ValueError in main_loop: {e}")
