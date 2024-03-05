"""
This module contains the entry point for running the server.

It defines the `main` function which parses the command line arguments, 
creates a `Server` instance, and runs the server.
"""

import sys
from redblue_demo.server.server import Server, ServerConfig


def usage():
    """
    Prints the usage information and exits the program.
    """
    print("Usage: python server.py index addr1 addr2 ...")
    sys.exit("Wrong command line argument")


def main():
    """
    Parses the command line arguments, creates a Server instance, and runs the server.
    """
    args = sys.argv[1:]
    if len(args) < 2:
        usage()
    try:
        index = int(args[0], 16)
    except ValueError:
        usage()
    addr = args[1:]
    server = Server.from_config(ServerConfig(index, addr))
    server.run()


if __name__ == "__main__":
    main()
