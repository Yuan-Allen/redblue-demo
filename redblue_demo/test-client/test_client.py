from redblue_demo.client.client import Client
import sys
import time

if __name__== "__main__":
    clients = []
    for i in range(len(sys.argv)-1):
        clients.append(Client(sys.argv[i + 1]))
    
    res = clients[0].request({"cmd": "DEPOSIT", "aid": 20, "amount": 1000})
    print(res)
    res = clients[1].request({"cmd": "DEPOSIT", "aid": 20, "amount": 1100})
    print(res)
    time.sleep(10)
    res = clients[1].request({"cmd": "DEPOSIT", "aid": 20, "amount": 1})
    # res = clients[0].request({"cmd": "INTEREST", "aid": 20})
    # print(res)
    # time.sleep(1)
    # res = clients[1].request({"cmd": "WITHDRAW", "aid": 20, "amount": 2500})
    # print(res)