"""
This module contains the definition of the VectorClock class.
"""

from redblue_demo.common.common import COLOR


class VectorClock:
    """
    A class representing a vector clock.

    Attributes:
        b (list): A list of integers representing the clock values for each server.
        r (int): An integer representing the red clock value.
    """

    b: list
    r: int

    def __init__(self, num_server: int) -> None:
        """
        Initializes the vector clock with the given number of servers.

        Args:
            num_server (int): The number of servers.

        Returns:
            None
        """
        self.b = [0] * num_server
        self.r = 0

    def ready(self, now: "VectorClock") -> bool:
        """
        Checks if the current clock is ready to process the given clock.

        Args:
            now (VectorClock): The clock to compare with.

        Returns:
            bool: True if the current clock is ready, False otherwise.
        """
        for i, bi in enumerate(now.b):
            if self.b[i] > bi:
                return False
        if self.r > now.r:
            return False
        return True

    def copy(self) -> "VectorClock":
        """
        Creates a copy of the vector clock.

        Returns:
            VectorClock: A copy of the vector clock.
        """
        b = [self.b[i] for i in range(len(self.b))]
        vector_clock = VectorClock(len(self.b))
        vector_clock.b = b
        vector_clock.r = self.r
        return vector_clock

    def red(self) -> int:
        """
        Returns the red clock value.

        Returns:
            int: The red clock value.
        """
        return self.r

    def tick(self, server_id: int, color: COLOR) -> "VectorClock":
        """
        Updates the clock values based on the server ID and color.

        Args:
            server_id (int): The ID of the server.
            color (COLOR): The color of the clock tick.

        Returns:
            VectorClock: The previous state of the vector clock.
        """
        old = self.copy()
        self.b[server_id] = self.b[server_id] + 1
        if color == COLOR.RED:
            self.r = self.r + 1
        return old

    def print(self, server_id: int) -> None:
        """
        Prints the clock values for the given server ID.

        Args:
            server_id (int): The ID of the server.

        Returns:
            None
        """
        print(f"#{server_id} [", end="")
        for _, bi in enumerate(self.b):
            print(f" {bi}", end="")
        print(f" ; {self.r} ]")
