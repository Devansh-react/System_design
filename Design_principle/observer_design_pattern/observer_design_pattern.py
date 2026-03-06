from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List


class ISubscriber(ABC):
    @abstractmethod
    def update(self) -> None:
        """Receive update from the channel."""
        raise NotImplementedError


class IChannel(ABC):
    @abstractmethod
    def subscribe(self, subscriber: ISubscriber) -> None:
        raise NotImplementedError

    @abstractmethod
    def unsubscribe(self, subscriber: ISubscriber) -> None:
        raise NotImplementedError

    @abstractmethod
    def notify_subscribers(self) -> None:
        raise NotImplementedError


class Channel(IChannel):
    def __init__(self, name: str) -> None:
        self._name: str = name
        self._subscribers: List[ISubscriber] = []
        self._latest_video: str | None = None

    def subscribe(self, subscriber: ISubscriber) -> None:
        """Add a subscriber (avoid duplicates)."""
        if subscriber not in self._subscribers:
            self._subscribers.append(subscriber)

    def unsubscribe(self, subscriber: ISubscriber) -> None:
        """Remove a subscriber if present."""
        if subscriber in self._subscribers:
            self._subscribers.remove(subscriber)

    def notify_subscribers(self) -> None:
        """Notify all subscribers of the latest video."""
        for sub in self._subscribers:
            sub.update()

    def upload_video(self, title: str) -> None:
        """Upload a new video and notify all subscribers."""
        self._latest_video = title
        print(f"\n[{self._name} uploaded \"{title}\"]")
        self.notify_subscribers()

    def get_video_data(self) -> str:
        if self._latest_video is None:
            return "\nNo videos uploaded yet.\n"
        return f"\nCheckout our new Video : {self._latest_video}\n"


class Subscriber(ISubscriber):
    def __init__(self, name: str, channel: Channel) -> None:
        self._name = name
        self._channel = channel

    def update(self) -> None:
        """Called by Channel; prints notification message."""
        print(f"Hey {self._name},{self._channel.get_video_data()}", end="")


def main() -> None:
    # Create a channel and subscribers
    channel = Channel("system_design")

    subs1 = Subscriber("p1", channel)
    subs2 = Subscriber("p2", channel)

    # Varun and Tarun subscribe to CoderArmy
    channel.subscribe(subs1)
    channel.subscribe(subs2)

    # Upload a video: both Varun and Tarun are notified
    channel.upload_video("Observer Pattern")

    # Varun unsubscribes; Tarun remains subscribed
    channel.unsubscribe(subs1)

    # Upload another video: only Tarun is notified
    channel.upload_video("Decorator Pattern")
    


if __name__ == "__main__":
    main()