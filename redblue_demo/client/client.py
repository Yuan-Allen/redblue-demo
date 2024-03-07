from redblue_demo.common.shadow_op import ShadowOp
from redblue_demo.common.common import COLOR, REQ, Request, Response, SERVER_DELAY
from xmlrpc.client import ServerProxy
import asyncio

class Client:
    """
    Wrapper for xmlrpc client.
    
    Attributes:
    rpcClient (SimpleXMLRPCClinet): The request object.
    """
    
    rpcClient: ServerProxy
    
    def __init__(self, addr: str) -> None:
        self.rpcClient = ServerProxy(addr)

    async def do_pass_token(self, max_r:int):
        await asyncio.sleep(SERVER_DELAY * 1e-3)
        self.rpcClient.pass_token(max_r);

    def pass_token(self, max_r:int) -> None:
        asyncio.create_task(self.do_pass_token(max_r))
        
    async def do_add_shadow_op_async(self, shadow: ShadowOp) -> None:
        await asyncio.sleep(SERVER_DELAY * 1e-3)
        self.rpcClient.add_shadow_op(shadow)

    def add_shadow_op_async(self, shadow: ShadowOp) -> None:
        asyncio.create_task(self.do_add_shadow_op_async(shadow))
        
    def request(self, req: dict) -> dict:
        return self.rpcClient.request(req)
    
    def dump(self) -> None:
        self.rpcClient.dump()