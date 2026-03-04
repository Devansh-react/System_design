class NoSingleton:
    """
    Not a singleton: every call creates a new object.

    Problem:
    - Nothing stops the caller from creating many instances.
    - If you want exactly one shared object (e.g. config, logger),
      this fails the singleton requirement completely.
    """

    def __init__(self) -> None:
        print("NoSingleton: constructor called (new object created)")  # demo only


def demo_no_singleton() -> None:
    s1 = NoSingleton()
    s2 = NoSingleton()
    print("NoSingleton: s1 is s2 ->", s1 is s2)  # False


if __name__ == "__main__":
    demo_no_singleton()

