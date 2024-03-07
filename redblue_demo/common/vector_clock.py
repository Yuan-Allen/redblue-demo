from redblue_demo.common.common import COLOR
import copy


class VectorClock:
    B: list
    R: int

    def __init__(self, num_server: int) -> None:
        self.B = [_ for _ in range(num_server)]
        self.R = 0

    def ready(self, now: "VectorClock") -> bool:
        for i in range(len(now.B)):
            if self.B[i] > now.B[i]:
                return False
        if self.R > now.R:
            return False
        return True

    def copy(self):
        b = [self.B[i] for i in range(len(self.B))]
        vectorClock = VectorClock(len(self.B))
        vectorClock.B = b
        vectorClock.R = self.R
        return vectorClock

    def red(self) -> int:
        return self.R

    def tick(self, server_id: int, color: COLOR) -> "VectorClock":
        old = self.copy()
        self.B[server_id] = self.B[server_id] + 1
        if color == COLOR.RED:
            self.R = self.R + 1
        return old

    def print(self, server_id: int) -> None:
        print(f"#{server_id} [")
        for i in range(len(self.B)):
            print(f" {self.B[i]}")
        print(f" ; {self.R} ]\n")
