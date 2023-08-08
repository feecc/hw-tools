from enum import Enum


class State(str, Enum):
    open = "open"
    close = "close"


class TestBarrier:
    def __init__(self) -> None:
        self.state: State = State.close

    def change_state(self):
        self.state = State.open if self.state == State.close else State.close
        return self.state

    def check_state(self):
        return self.state


testbarrier = TestBarrier()
