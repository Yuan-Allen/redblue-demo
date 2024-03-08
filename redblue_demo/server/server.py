"""
This module implements the server class for the RedBlue consistency protocol.
"""

from socketserver import ThreadingMixIn
import threading
import copy
import time
from xmlrpc.server import SimpleXMLRPCServer

from queue import Queue
from collections import deque
from typing import List, NamedTuple, Optional, Tuple
from redblue_demo.client.client import Client
from redblue_demo.common.bank_storage import NUM_ACCOUNTS, BankStorage
from redblue_demo.common.shadow_op import ShadowOp
from redblue_demo.common.vector_clock import VectorClock
from redblue_demo.common.common import COLOR, REQ, Request, Response


class ThreadXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer):
    """
    A subclass of SimpleXMLRPCServer that supports threading.

    This class combines the functionality of the ThreadingMixIn class
    and the SimpleXMLRPCServer class to create a threaded XML-RPC server.
    """


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
        ip, port = self.addrs[self.id].split(":")
        port = int(port)
        # server = SimpleXMLRPCServer((ip, port), allow_none=True)
        server = ThreadXMLRPCServer((ip, port), allow_none=True)
        server.register_instance(self)

        # Setup peer connection
        def setup_peers():
            for i, addr in enumerate(self.addrs):
                if i == self.id:
                    continue
                self.peers[i] = Client(f"http://{addr}")
            print(f"server {self.id}: peer connection established")
            self._main_loop()

        peer_thread = threading.Thread(target=setup_peers)
        peer_thread.start()
        server.serve_forever()

    def _set_token_timeout(self) -> None:
        def timeout():
            time.sleep(1)
            self.token_queue.put(0)

        threading.Thread(target=timeout).start()

    def _primary(self) -> bool:
        return self.has_token and self.max_r == self.now.red()

    def _generate_shadow(
        self, req: Request, primary: bool
    ) -> Tuple[ShadowOp, Optional[Response], bool]:
        shadow = ShadowOp(
            aid=req.aid, depend=copy.deepcopy(self.now), server_id=self.id
        )
        balance = self.bank.get_account(req.aid).get_balance()
        res = None

        if req.op == REQ.DEPOSIT:
            shadow.amount = req.amount
            shadow.color = COLOR.BLUE
            res = Response(status=0, balance=balance + req.amount)
            ok = True
        elif req.op == REQ.WITHDRAW:
            if primary:
                if balance >= req.amount:
                    shadow.amount = -req.amount
                    shadow.color = COLOR.RED
                    res = Response(status=0, balance=balance - req.amount)
                else:
                    shadow.amount = 0
                    shadow.color = COLOR.BLUE
                    res = Response(
                        status=-1, balance=balance, message="Insufficient balance"
                    )
                ok = True
            else:
                ok = False
        elif req.op == REQ.INTEREST:
            delta = self.bank.get_account(req.aid).compute_interest()
            shadow.amount = delta
            shadow.color = COLOR.BLUE
            res = Response(status=0, balance=balance + delta)
            ok = True
        elif req.op == REQ.CHECK:
            shadow.amount = 0
            shadow.color = COLOR.BLUE
            res = Response(status=0, balance=balance)
            ok = True
        else:
            raise ValueError("Unknown operation")
        return shadow, res, ok

    def _do_request(self, req_item: RequestItem) -> bool:
        primary = self._primary()
        req = req_item.req
        # verify request
        if req.aid < 0 or req.aid >= NUM_ACCOUNTS:
            req_item.res_queue.put(Response(status=-1, message="Invalid Account Id"))
            return True

        # try generate shadow op
        shadow, res, ok = self._generate_shadow(req, primary)
        if ok:
            assert isinstance(res, Response)
            req_item.res_queue.put(res)
            self._dispatch_shadow_op(shadow)
            return True
        if not ok and primary:
            print(f"failed {req.op}: ")
        return False

    def _dispatch_shadow_op(self, shadow: ShadowOp):
        if shadow.amount == 0:
            return  # read only, no need to dispatch shadow op
        shadow.apply(self.bank)
        self.now.tick(shadow.server_id, shadow.color)
        self.now.print(self.id)
        if self.now.red() > self.max_r:
            self.max_r = self.now.red()

        for peer in self.peers:
            if peer is not None:
                assert isinstance(peer, Client)
                peer.add_shadow_op_async(shadow)

    def _main_loop(self) -> None:
        if self.id == 0:
            self._set_token_timeout()
            self.has_token = True

        while True:
            try:
                # Process token_queue
                while not self.token_queue.empty():
                    max_r = self.token_queue.get()
                    if self.has_token:
                        next_id = (self.id + 1) % len(self.peers)
                        if self.peers[next_id] is not None:
                            self.has_token = False
                            self.peers[next_id].pass_token(self.max_r)
                            # print(f"server {self.id}: pass token to {next_id}")
                    else:
                        self.max_r = max_r
                        self.has_token = True
                        self._set_token_timeout()
                        # print(f"server {self.id}: received token")

                # Process shadow_queue
                while not self.shadow_queue.empty():
                    shadow: ShadowOp = self.shadow_queue.get()
                    self.op_list.append(shadow)

                # Process req_queue
                while not self.req_queue.empty():
                    req_item = self.req_queue.get()
                    if not self._do_request(req_item):
                        self.red_list.append(req_item)
                        # print(f"server {self.id}: add to redList")

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
                    # print(f"server {self.id}: process shadowOp")

                # Process red_list if primary
                if self._primary():
                    for req_item in list(self.red_list):
                        ok = self._do_request(req_item)
                        if not ok:
                            raise ValueError(f"server {self.id}: process redList fail")
                    # Clear red_list after processing all items
                    self.red_list.clear()

            except ValueError as e:
                print(f"ValueError in main_loop: {e}")

    def pass_token(self, max_r: int) -> None:
        """
        This method is a RPC handler provided by the server.
        Passes the token to the next server.

        Args:
            max_r (int): The maximum red value seen by the server.
        """
        self.token_queue.put(max_r)

    def add_shadow_op(self, shadow: dict) -> None:
        """
        This method is a RPC handler provided by the server.
        Adds a shadow operation to the queue.

        Args:
            shadow (ShadowOp): The shadow operation to add.
        """
        self.shadow_queue.put(ShadowOp.from_dict(shadow))

    def request(self, req_dict: dict) -> dict:
        """
        This method is a RPC handler provided by the server.
        It puts the request into the request queue and returns the response.

        Args:
            req (Request): The request object to be processed.

        Returns:
            Response: The response object generated by processing the request.

        Raises:
            ValueError: If the request processing fails.
        """
        res_queue = Queue()
        req = None
        if len(req_dict) == 3:
            aid = req_dict["aid"]
            amount = req_dict["amount"]
            if req_dict["cmd"] == "DEPOSIT":
                op = REQ.DEPOSIT
            elif req_dict["cmd"] == "WITHDRAW":
                op = REQ.WITHDRAW

            req = Request(aid, op, amount)

        elif len(req_dict) == 2:
            if req_dict["cmd"] == "INTEREST":
                op = REQ.INTEREST
                aid = req_dict["aid"]
                req = Request(aid, op)
            elif req_dict["cmd"] == "CHECK":
                op = REQ.CHECK
                aid = req_dict["aid"]
                req = Request(aid, op)

        req_item = RequestItem(req=req, res_queue=res_queue)
        self.req_queue.put(req_item)
        res = res_queue.get()

        if res is None:
            raise ValueError("Server.Request failed")
        assert isinstance(res, Response)
        res_dict = {
            "status": res.status,
            "balance": res.balance,
            "message": res.message,
        }
        return res_dict

    def dump(self) -> None:
        """
        This method is a RPC handler provided by the server.
        Prints the server ID.
        """
        print(f"server {self.id}")
