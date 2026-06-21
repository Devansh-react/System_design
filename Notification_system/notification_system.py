"""
Event-Driven Fan-out Notification System (Interview Demo)

Real-world mapping (AWS):
  App Server  ->  SNS (pub/sub)  ->  SQS queues  ->  Workers  ->  Email / Push / In-app

What we SKIP on purpose (mention in interview, don't code):
  Load Balancer, Auto-scaling, EC2, Kafka — infra concerns, not core notification logic.

Core ideas this code shows:
  1. API returns fast — publish event and move on (async via background workers).
  2. Fan-out — one event can go to multiple notification channels.
  3. Decoupling — app server does not know HOW email/push is sent.
  4. Queues absorb spikes and allow retries if a provider is down.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from queue import Empty, Queue
from threading import Event, Thread
import time
import uuid


# ---------------------------------------------------------------------------
# 1. Domain models
# ---------------------------------------------------------------------------

class EventType(Enum):
    USER_LOGIN = "user_login"
    USER_SIGNUP = "user_signup"
    USER_POST = "user_post"
    FRIEND_REQUEST = "friend_request"


class ChannelType(Enum):
    EMAIL = "email"
    IN_APP = "in_app"
    PUSH = "push"


@dataclass
class UserEvent:
    """What the app server receives from a user action."""

    event_type: EventType
    user_id: str
    data: dict = field(default_factory=dict)


@dataclass
class NotificationTask:
    """One unit of work sitting inside an SQS-like queue."""

    task_id: str
    channel: ChannelType
    user_id: str
    title: str
    body: str
    retry_count: int = 0


# Which channels should fire for each event? (SNS subscription rules)
EVENT_TO_CHANNELS: dict[EventType, list[ChannelType]] = {
    EventType.USER_LOGIN: [ChannelType.EMAIL],
    EventType.USER_SIGNUP: [ChannelType.EMAIL],
    EventType.USER_POST: [ChannelType.PUSH],
    EventType.FRIEND_REQUEST: [ChannelType.IN_APP, ChannelType.PUSH],
}


def build_notification(user_event: UserEvent, channel: ChannelType) -> NotificationTask:
    """Turn a raw user event into a channel-specific notification."""

    templates: dict[tuple[EventType, ChannelType], tuple[str, str]] = {
        (EventType.USER_LOGIN, ChannelType.EMAIL): (
            "Login alert",
            f"New login for user {user_event.user_id}",
        ),
        (EventType.USER_SIGNUP, ChannelType.EMAIL): (
            "Welcome!",
            f"Thanks for signing up, {user_event.user_id}",
        ),
        (EventType.USER_POST, ChannelType.PUSH): (
            "New post",
            f"{user_event.user_id} shared: {user_event.data.get('post_text', '...')}",
        ),
        (EventType.FRIEND_REQUEST, ChannelType.IN_APP): (
            "Friend request",
            f"{user_event.data.get('from_user', 'Someone')} sent you a request",
        ),
        (EventType.FRIEND_REQUEST, ChannelType.PUSH): (
            "Friend request",
            f"{user_event.data.get('from_user', 'Someone')} wants to connect",
        ),
    }

    title, body = templates[(user_event.event_type, channel)]
    return NotificationTask(
        task_id=str(uuid.uuid4())[:8],
        channel=channel,
        user_id=user_event.user_id,
        title=title,
        body=body,
    )


# ---------------------------------------------------------------------------
# 2. SQS — message queue with optional Dead Letter Queue (DLQ)
# ---------------------------------------------------------------------------

class MessageQueue:
    """
    Simulates AWS SQS.

    Interview talking points:
      - Buffers messages when workers are slow or down.
      - DLQ holds messages that failed too many times (for manual inspection).
    """

    def __init__(self, name: str, dead_letter_queue: MessageQueue | None = None) -> None:
        self.name = name
        self._queue: Queue[NotificationTask] = Queue()
        self._dlq = dead_letter_queue
        self.max_retries = 3

    def enqueue(self, task: NotificationTask) -> None:
        self._queue.put(task)
        print(f"  [SQS:{self.name}] enqueued task {task.task_id} -> {task.channel.value}")

    def dequeue(self, timeout: float = 0.5) -> NotificationTask | None:
        try:
            return self._queue.get(timeout=timeout)
        except Empty:
            return None

    def requeue_or_send_to_dlq(self, task: NotificationTask) -> None:
        task.retry_count += 1
        if task.retry_count >= self.max_retries and self._dlq is not None:
            self._dlq.enqueue(task)
            print(f"  [SQS:{self.name}] moved task {task.task_id} to DLQ after {task.retry_count} failures")
        else:
            self.enqueue(task)
            print(f"  [SQS:{self.name}] retry #{task.retry_count} for task {task.task_id}")


# ---------------------------------------------------------------------------
# 3. SNS — event dispatcher (pub/sub fan-out)
# ---------------------------------------------------------------------------

class EventDispatcher:
    """
    Simulates AWS SNS.

    App server publishes ONE event here.
    SNS fans out copies to every subscribed queue (email / push / in-app).
    """

    def __init__(self) -> None:
        self._queues: dict[ChannelType, MessageQueue] = {}

    def register_queue(self, channel: ChannelType, queue: MessageQueue) -> None:
        self._queues[channel] = queue

    def publish(self, user_event: UserEvent) -> None:
        channels = EVENT_TO_CHANNELS.get(user_event.event_type, [])
        print(f"\n[SNS] event={user_event.event_type.value} -> channels={[c.value for c in channels]}")

        for channel in channels:
            queue = self._queues.get(channel)
            if queue is None:
                continue
            task = build_notification(user_event, channel)
            queue.enqueue(task)


# ---------------------------------------------------------------------------
# 4. Delivery services (third-party providers — mocked with print)
# ---------------------------------------------------------------------------

class EmailService:
    def send(self, task: NotificationTask) -> bool:
        print(f"    [Email] To {task.user_id}: {task.title} — {task.body}")
        return True


class PushService:
    def send(self, task: NotificationTask) -> bool:
        print(f"    [Push] To {task.user_id}: {task.title} — {task.body}")
        return True


class InAppService:
    def send(self, task: NotificationTask) -> bool:
        print(f"    [In-App] To {task.user_id}: {task.title} — {task.body}")
        return True


# ---------------------------------------------------------------------------
# 5. Worker — polls one queue and calls the right delivery service
# ---------------------------------------------------------------------------

class NotificationWorker:
    """
    Simulates EC2 worker instances.

    In production: many workers per queue, auto-scaled based on queue depth.
    Here: one background thread per queue is enough to show the idea.
    """

    def __init__(self, queue: MessageQueue, channel: ChannelType) -> None:
        self.queue = queue
        self.channel = channel
        self._stop = Event()
        self._senders = {
            ChannelType.EMAIL: EmailService().send,
            ChannelType.PUSH: PushService().send,
            ChannelType.IN_APP: InAppService().send,
        }

    def start(self) -> Thread:
        thread = Thread(target=self._run, daemon=True, name=f"worker-{self.channel.value}")
        thread.start()
        return thread

    def stop(self) -> None:
        self._stop.set()

    def _run(self) -> None:
        sender = self._senders[self.channel]
        while not self._stop.is_set():
            task = self.queue.dequeue(timeout=0.3)
            if task is None:
                continue

            print(f"  [Worker:{self.channel.value}] processing task {task.task_id}")
            success = sender(task)
            if not success:
                self.queue.requeue_or_send_to_dlq(task)


# ---------------------------------------------------------------------------
# 6. App server — entry point (what user hits via HTTP in real life)
# ---------------------------------------------------------------------------

class AppServer:
    """
    Handles user requests.

    Important: we do NOT send notifications here.
    We only publish to SNS and return 200 OK immediately.
    """

    def __init__(self, dispatcher: EventDispatcher) -> None:
        self.dispatcher = dispatcher

    def handle(self, user_event: UserEvent) -> dict:
        print(f"\n[AppServer] received {user_event.event_type.value} for {user_event.user_id}")
        self.dispatcher.publish(user_event)
        return {"status": "ok", "message": "Request accepted. Notifications queued."}


# ---------------------------------------------------------------------------
# Demo — wire everything together
# ---------------------------------------------------------------------------

def build_system() -> tuple[AppServer, list[NotificationWorker], MessageQueue]:
    email_dlq = MessageQueue("email-dlq")
    email_queue = MessageQueue("email", dead_letter_queue=email_dlq)
    in_app_queue = MessageQueue("in-app")
    push_queue = MessageQueue("push")

    dispatcher = EventDispatcher()
    dispatcher.register_queue(ChannelType.EMAIL, email_queue)
    dispatcher.register_queue(ChannelType.IN_APP, in_app_queue)
    dispatcher.register_queue(ChannelType.PUSH, push_queue)

    workers = [
        NotificationWorker(email_queue, ChannelType.EMAIL),
        NotificationWorker(in_app_queue, ChannelType.IN_APP),
        NotificationWorker(push_queue, ChannelType.PUSH),
    ]
    for worker in workers:
        worker.start()

    return AppServer(dispatcher), workers, email_dlq


def main() -> None:
    app, workers, email_dlq = build_system()

    print("=" * 60)
    print("NOTIFICATION SYSTEM DEMO")
    print("=" * 60)

    # Simulate user actions — API responds instantly, workers run in background
    app.handle(UserEvent(EventType.USER_SIGNUP, "alice@mail.com"))
    app.handle(UserEvent(EventType.USER_LOGIN, "alice@mail.com"))
    app.handle(UserEvent(EventType.USER_POST, "bob", {"post_text": "Hello world!"}))
    app.handle(
        UserEvent(EventType.FRIEND_REQUEST, "charlie", {"from_user": "diana"}),
    )

    # Give background workers time to drain queues
    time.sleep(2)

    for worker in workers:
        worker.stop()

    print("\n" + "=" * 60)
    print("INTERVIEW CHEAT SHEET")
    print("=" * 60)
    print("""
Flow:
  User -> App Server -> SNS -> [Email SQS | In-App SQS | Push SQS] -> Workers -> Providers

Why queues?
  - Decouple producers from consumers
  - Handle traffic spikes
  - Retry on failure (DLQ for poison messages)

Why fan-out (SNS)?
  - One login event should trigger email only
  - One friend request should trigger in-app AND push
  - App server stays simple — it just publishes the event type

Scale later with:
  - Multiple worker instances per queue
  - Idempotency keys (avoid duplicate notifications)
  - User preference store (opt-out of push/email)
  - Rate limiting per provider
""")


if __name__ == "__main__":
    main()
