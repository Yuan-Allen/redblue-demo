"""
This module contains a test client script for the redblue_demo application.

The script creates multiple instances of the `Client` class and performs various operations 
such as deposit, interest calculation, withdrawal, 
and checking account balance on different servers.
"""

import sys
import time
from redblue_demo.client.client import Client


if __name__ == "__main__":
    clients = []
    for i in range(len(sys.argv) - 1):
        clients.append(Client(sys.argv[i + 1]))

    res = clients[0].request({"cmd": "DEPOSIT", "aid": 20, "amount": 1000})
    print(f"DEPOSIT server 0 (+ 1000): {res}")
    res = clients[1].request({"cmd": "DEPOSIT", "aid": 20, "amount": 1100})
    print(f"DEPOSIT server 1 (+ 1100): {res}")
    res = clients[0].request({"cmd": "INTEREST", "aid": 20})
    print(f"DEPOSIT server 0 (rate 0.04): {res}")
    res = clients[1].request({"cmd": "WITHDRAW", "aid": 20, "amount": 2500})
    print(f"WITHDRAW server 1 (- 2500): {res}")
    time.sleep(5)
    print("-----------------")
    res = clients[0].request({"cmd": "CHECK", "aid": 20})
    print(f"CHECK server 0: {res}")
    res = clients[1].request({"cmd": "CHECK", "aid": 20})
    print(f"CHECK server 1: {res}")
    res = clients[0].request({"cmd": "CHECK", "aid": 20})
    print(f"CHECK server 2: {res}")
