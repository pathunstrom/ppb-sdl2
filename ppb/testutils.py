import time
from typing import Callable

from ppb.engine import GameEngine
from ppb.events import Heartbeat
from ppb.events import Quit
from ppb.systems import System


class Failer(System):

    def __init__(self, *, fail: Callable[[GameEngine], bool], message: str,
                 run_time: float=1, engine, **kwargs):
        super().__init__(**kwargs)
        self.fail = fail
        self.message = message
        self.start = time.monotonic()
        self.run_time = run_time
        self.engine = engine

    def on_heartbeat(self, heartbeat_event: Heartbeat, signal):
        if time.monotonic() - self.start > self.run_time:
            raise AssertionError("Test ran too long.")
        if self.fail(self.engine):
            raise AssertionError(self.message)


class Quitter(System):
    """
    System for running test. Limits the engine to a single loop.
    """

    def __init__(self, loop_count=1, **kwargs):
        super().__init__(**kwargs)
        self.counter = 0
        self.loop_count = loop_count

    def on_heartbeat(self, heartbeat_event: Heartbeat, signal):
        self.counter += 1
        if self.counter >= self.loop_count:
            signal(Quit())
