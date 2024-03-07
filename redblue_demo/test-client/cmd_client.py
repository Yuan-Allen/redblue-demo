import sys
from redblue_demo.client.client import Client
from redblue_demo.common.common import COLOR, REQ, Request, Response

if __name__ == "__main__":
    client = Client(sys.argv[1])
    print("Connected!")
    while True:
        line = input()
        if line.strip() == "":
            break

        parts = line.split()
        res_dict = None
        if len(parts) == 3:
            cmd, arg1, arg2 = parts
            arg1 = int(arg1)
            arg2 = float(arg2)
            if cmd == "deposit":
                # 执行存款操作
                res_dict = client.request(
                    {"cmd": "DEPOSIT", "aid": arg1, "amount": arg2}
                )
            elif cmd == "withdraw":
                # 执行取款操作
                res_dict = client.request(
                    {"cmd": "WITHDRAW", "aid": arg1, "amount": arg2}
                )
        elif len(parts) == 2:
            cmd, arg1 = parts
            arg1 = int(arg1)
            res_dict = client.request({"cmd": "INTEREST", "aid": arg1})
        else:
            print("Retry.")
        print(res_dict)
        if res_dict:
            res = Response(res_dict["status"], res_dict["balance"], res_dict["message"])
