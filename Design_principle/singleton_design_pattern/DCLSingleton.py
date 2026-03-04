import threading


class DCLSingleton:
    """
    Double‑checked locking (DCL) version.

    Pattern:
    - First check without lock (fast path).
    - If `_instance is None`, acquire lock and check again, then create.

    Improvement over LockedSingleton:
    - After initialization, most calls do not take the lock,
      so it is faster under read‑heavy, write‑once workloads.

    Problems / caveats:
    - In some languages, DCL is tricky or unsafe because of memory
      reordering (C++/Java before proper fences/volatile semantics).
    - In CPython, the GIL plus this style is generally safe, but
      still more complex than needed; prefer simpler patterns unless
      you *really* need the micro‑optimization.
    """

    _instance = None
    _lock = threading.Lock()

    def __init__(self) -> None:
        print("DCLSingleton: constructor called")  # demo only

    @classmethod
    def get_instance(cls) -> "DCLSingleton":
        if cls._instance is None:  # first check (no lock)
            # Multiple threads can arrive here, but only one will
            # create the instance after acquiring the lock.
            with cls._lock:
                if cls._instance is None:  # second check (with lock)
                    cls._instance = cls()
        return cls._instance


def demo_dcl_singleton() -> None:
    s1 = DCLSingleton.get_instance()
    s2 = DCLSingleton.get_instance()
    print("DCLSingleton: s1 is s2 ->", s1 is s2)


if __name__ == "__main__":
    demo_dcl_singleton()

