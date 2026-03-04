class EagerSingleton:
    """
    Eager initialization: the instance is created once when the module
    is imported, not lazily on first use.

    Improvement over lazy patterns:
    - **Trivially thread‑safe** in Python: module top‑level code runs
      only once per process, so there is no race.

    Problem:
    - Not lazy: the instance is created even if nobody uses it.
      If creation is expensive or may fail, this can be undesirable.
    """

    def __init__(self) -> None:
        print("EagerSingleton: constructor called")  # demo only


# Global, eagerly created instance – the actual singleton
EAGER_SINGLETON: "EagerSingleton" = EagerSingleton()


def get_eager_singleton() -> "EagerSingleton":
    return EAGER_SINGLETON


def demo_eager_singleton() -> None:
    s1 = get_eager_singleton()
    s2 = get_eager_singleton()
    print("EagerSingleton: s1 is s2 ->", s1 is s2)


if __name__ == "__main__":
    demo_eager_singleton()

