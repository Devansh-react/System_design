class SimpleSingleton:
    """
    Lazily creates the instance when first requested.

    Pattern:
    - Class attribute `_instance` starts as None.
    - `get_instance()` creates one if it does not exist.

    Problem:
    - **Not thread‑safe**: two threads can see `_instance is None`
      at the same time and each create a separate object.

    Extra notes:
    - `get_instance` is a **class method**. It receives `cls`, can
      access class variables, and is called on the class itself.
    """

    _instance = None

    def __init__(self) -> None:
        print("SimpleSingleton: constructor called")  # demo only

    @classmethod
    def get_instance(cls) -> "SimpleSingleton":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance


def demo_simple_singleton() -> None:
    s1 = SimpleSingleton.get_instance()
    s2 = SimpleSingleton.get_instance()
    print("SimpleSingleton: s1 is s2 ->", s1 is s2)  # True in single‑threaded code


if __name__ == "__main__":
    demo_simple_singleton()

