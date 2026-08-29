"""SimPy Store wrapper representing inter-station buffers."""

import simpy
from typing import Any, List


class SimBuffer:
    def __init__(self, env: simpy.Environment, buffer_id: str, capacity: int, upstream_id: str, downstream_id: str):
        self.env = env
        self.buffer_id = buffer_id
        self.capacity = capacity
        self.upstream_id = upstream_id
        self.downstream_id = downstream_id
        self.store = simpy.Store(env, capacity=capacity)

    @property
    def occupancy(self) -> int:
        return len(self.store.items)

    @property
    def is_full(self) -> bool:
        return self.occupancy >= self.capacity

    def put(self, item: Any):
        return self.store.put(item)

    def get(self):
        return self.store.get()
