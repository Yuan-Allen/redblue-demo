from redblue_demo.common.common import COLOR
import copy


class VectorClock:
    def __init__(self, num_server: int) -> None:
        self.B = [0] * num_server
        self.R = 0

    def ready(self, now: "VectorClock") -> bool:
        for i in range(len(self.B)):
            if self.B[i] > now.B[i]:
                return False
        if self.R > now.R:
            return False
        return True

    def red(self) -> int:
        return self.R

    def tick(self, server_id: int, color: COLOR) -> "VectorClock":
        old = copy.copy(self)
        self.B[server_id] = self.B[server_id] + 1
        if color == COLOR.RED:
            self.R = self.R + 1
        return old

    def print(self, server_id: int) -> None:
        print("#", end='')
        print(server_id, end='')
        print("[", end='')
        for i in range(len(self.B)):
            print(self.B[i], end=' ')
        print('|', end='')
        print(self.R, end='')
        print(']')
