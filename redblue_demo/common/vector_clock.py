from redblue_demo.common.common import COLOR


class VectorClock:
    def __init__(self, num_server: int) -> None:
        raise NotImplementedError("TODO: Implement this functionality")

    def ready(self, now: "VectorClock") -> bool:
        raise NotImplementedError("TODO: Implement this functionality")

    def red(self) -> int:
        raise NotImplementedError("TODO: Implement this functionality")

    def tick(self, server_id: int, color: COLOR) -> "VectorClock":
        raise NotImplementedError("TODO: Implement this functionality")

    def print(self, server_id: int) -> None:
        raise NotImplementedError("TODO: Implement this functionality")
