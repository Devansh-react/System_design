import threading


class LockedSingleton:
    """
    Thread‑safe lazy singleton using one lock around the whole check.

    Improvement over SimpleSingleton:
    - Use a class‑level `threading.Lock` and always acquire it before
      checking/creating the instance.

    Problem:
    - Correct but can be **slower** under heavy contention, because
      every `get_instance()` call acquires the lock even after the
      singleton is already created.
    """

    _instance = None
    _lock = threading.Lock()

    def __init__(self) -> None:
        print("LockedSingleton: constructor called")  # demo only

    @classmethod
    def get_instance(cls) -> "LockedSingleton":
        with cls._lock:
            if cls._instance is None:
                cls._instance = cls()
        return cls._instance


def demo_locked_singleton() -> None:
    s1 = LockedSingleton.get_instance()
    s2 = LockedSingleton.get_instance()
    print("LockedSingleton: s1 is s2 ->", s1 is s2)


if __name__ == "__main__":
    demo_locked_singleton()

