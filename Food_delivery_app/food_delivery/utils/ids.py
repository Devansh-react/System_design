from __future__ import annotations

import itertools
from dataclasses import dataclass


@dataclass(frozen=True)
class IdGenerator:
    prefix: str
    _counter: itertools.count

    @classmethod
    def create(cls, prefix: str, start: int = 1) -> "IdGenerator":
        return cls(prefix=prefix, _counter=itertools.count(start))

    def next(self) -> str:
        return f"{self.prefix}{next(self._counter)}"

