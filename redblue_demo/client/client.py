import threading
import time
from redblue_demo.common.shadow_op import ShadowOp
from redblue_demo.common.common import SERVER_DELAY
from xmlrpc.client import ServerProxy


class Client:
    """
    Wrapper for xmlrpc client.

    Attributes:
    rpcClient (SimpleXMLRPCClinet): The request object.
    """

    rpcClient: ServerProxy

    def __init__(self, addr: str) -> None:
        self.rpc_client = ServerProxy(addr)

    def pass_token(self, max_r: int) -> None:
        def task():
            time.sleep(SERVER_DELAY)
            try:
                self.rpc_client.pass_token(max_r)
            except ValueError as e:
                print(f"client.PassToken() : {e}")

        threading.Thread(target=task).start()

    def add_shadow_op_async(self, op: ShadowOp) -> None:
        def task():
            time.sleep(SERVER_DELAY)
            try:
                self.rpc_client.add_shadow_op(op)
            except ValueError as e:
                print(f"client.AddShadowOp() : {e}")

        threading.Thread(target=task).start()

    def request(self, req: dict) -> dict:
        return self.rpc_client.request(req)

    def dump(self) -> None:
        self.rpc_client.dump()
