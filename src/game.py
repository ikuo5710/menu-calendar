"""画面状態管理と遷移ロジック"""

from enum import Enum, auto


class GameState(Enum):
    START = auto()
    PLAYING = auto()
    RESULT = auto()


class GameManager:
    """ゲーム全体の状態を管理する。"""

    def __init__(self) -> None:
        self.state = GameState.START

    def go_to_start(self) -> None:
        self.state = GameState.START

    def go_to_playing(self) -> None:
        self.state = GameState.PLAYING

    def go_to_result(self) -> None:
        self.state = GameState.RESULT
