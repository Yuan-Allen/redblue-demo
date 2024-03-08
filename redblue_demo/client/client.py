"""
This module contains the Client class for interacting with the rpc server.
"""

import time
from xmlrpc.client import ServerProxy
import threading
from redblue_demo.common.shadow_op import ShadowOp
from redblue_demo.common.common import SERVER_DELAY


class Client:
    """
    Wrapper for xmlrpc client.
    """

    rpcClient: ServerProxy

    def __init__(self, addr: str) -> None:
        """
        Initializes a new instance of the Client class.

        Args:
        addr (str): The address of the server.

        Returns:
        None
        """
        self.rpc_client = ServerProxy(addr)
        self.addr = addr

    def pass_token(self, max_r: int) -> None:
        """
        Passes a token to the server asynchronously.

        Args:
        max_r (int): The red token.

        Returns:
        None
        """

        def task():
            time.sleep(SERVER_DELAY)
            try:
                self.rpc_client.pass_token(max_r)
            except ValueError as e:
                print(f"client.PassToken() : {e}")

        threading.Thread(target=task).start()

    def add_shadow_op_async(self, op: ShadowOp) -> None:
        """
        Adds a shadow operation to the server asynchronously.

        Args:
        op (ShadowOp): The shadow operation to add.

        Returns:
        None
        """

        def task():
            time.sleep(SERVER_DELAY)
            rpc_client = ServerProxy(self.addr)
            try:
                rpc_client.add_shadow_op(op)
            except ValueError as e:
                print(f"client.AddShadowOp() : {e}")

        threading.Thread(target=task).start()

    def request(self, req: dict) -> dict:
        """
        Sends a request to the server and returns the response.

        Args:
        req (dict): The request to send.

        Returns:
        dict: The response from the server.
        """
        return self.rpc_client.request(req)

    def dump(self) -> None:
        """
        Dumps the current state of the server.

        Returns:
        None
        """
        self.rpc_client.dump()
