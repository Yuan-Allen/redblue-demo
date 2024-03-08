"""
This module contains a test client script for the redblue_demo application.

The script creates multiple instances of the `Client` class and performs various operations 
such as deposit, interest calculation, withdrawal, 
and checking account balance on different servers.
"""

import sys
import time
from typing import List
from redblue_demo.client.client import Client


def case1(rpc_clients: List[Client]):
    """
    Executes a series of operations on the specified RPC clients for account 20.
    server 0: deposit 1000
    server 1: deposit 1100
    server 0: interest
    server 1: withdraw 2500

    Args:
        rpc_clients (List[Client]): A list of RPC clients.

    Returns:
        None
    """
    print("------------test case 1-------------")
    res = rpc_clients[0].request({"cmd": "DEPOSIT", "aid": 20, "amount": 1000})
    print(f"[account 20] DEPOSIT server 0 (+ 1000): {res}")
    res = rpc_clients[1].request({"cmd": "DEPOSIT", "aid": 20, "amount": 1100})
    print(f"[account 20] DEPOSIT server 1 (+ 1100): {res}")
    res = rpc_clients[0].request({"cmd": "INTEREST", "aid": 20})
    print(f"[account 20] DEPOSIT server 0 (rate 0.04): {res}")
    res = rpc_clients[1].request({"cmd": "WITHDRAW", "aid": 20, "amount": 2500})
    print(f"[account 20] WITHDRAW server 1 (- 2500): {res}")
    time.sleep(5)
    print("-----------------")
    res = rpc_clients[0].request({"cmd": "CHECK", "aid": 20})
    print(f"[account 20] CHECK server 0: {res}")
    res = rpc_clients[1].request({"cmd": "CHECK", "aid": 20})
    print(f"[account 20] CHECK server 1: {res}")
    res = rpc_clients[2].request({"cmd": "CHECK", "aid": 20})
    print(f"[account 20] CHECK server 2: {res}")


def case2(rpc_clients: List[Client]):
    """
    Executes a test case for withdrawing funds from account 21 using multiple RPC clients.
    server 0: withdraw 800
    server 1: withdraw 800

    Args:
        rpc_clients (List[Client]): A list of RPC clients.

    Returns:
        None
    """
    print("------------test case 2-------------")
    res = rpc_clients[0].request({"cmd": "WITHDRAW", "aid": 21, "amount": 800})
    print(f"[account 21] WITHDRAW server 0 (- 800): {res}")
    res = rpc_clients[1].request({"cmd": "WITHDRAW", "aid": 21, "amount": 800})
    print(f"[account 21] WITHDRAW server 1 (- 800): {res}")
    time.sleep(5)
    print("-----------------")
    res = rpc_clients[0].request({"cmd": "CHECK", "aid": 21})
    print(f"[account 21] CHECK server 0: {res}")
    res = rpc_clients[1].request({"cmd": "CHECK", "aid": 21})
    print(f"[account 21] CHECK server 1: {res}")
    res = rpc_clients[2].request({"cmd": "CHECK", "aid": 21})
    print(f"[account 21] CHECK server 2: {res}")


if __name__ == "__main__":
    clients = []
    for i in range(len(sys.argv) - 1):
        clients.append(Client(sys.argv[i + 1]))

    case1(clients)
    case2(clients)
