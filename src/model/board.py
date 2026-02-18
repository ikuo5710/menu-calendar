"""5×5 盤面クラス"""

from __future__ import annotations
import copy
from src.constants import GRID_ROWS, GRID_COLS


class Board:
    """5日×5ブロックの献立配置盤面。

    セルの値は メニューID (0-4) または None (空欄)。
    """

    def __init__(self) -> None:
        self._grid: list[list[int | None]] = [
            [None] * GRID_COLS for _ in range(GRID_ROWS)
        ]

    # --- 参照 ---

    def get(self, row: int, col: int) -> int | None:
        """指定セルのメニューIDを返す。空なら None。"""
        return self._grid[row][col]

    @property
    def grid(self) -> list[list[int | None]]:
        """盤面の読み取り専用コピー。"""
        return copy.deepcopy(self._grid)

    # --- 操作 ---

    def place(self, row: int, col: int, menu_id: int) -> None:
        """セルにメニューを配置（上書き可）。"""
        self._validate_pos(row, col)
        self._grid[row][col] = menu_id

    def remove(self, row: int, col: int) -> None:
        """セルを空にする。"""
        self._validate_pos(row, col)
        self._grid[row][col] = None

    def move(self, src_row: int, src_col: int, dst_row: int, dst_col: int) -> None:
        """セルからセルへ移動（元は空になる）。"""
        value = self.get(src_row, src_col)
        if value is None:
            return
        self._grid[dst_row][dst_col] = value
        self._grid[src_row][src_col] = None

    def reset(self) -> None:
        """盤面を全て空にする。"""
        self._grid = [[None] * GRID_COLS for _ in range(GRID_ROWS)]

    def copy(self) -> Board:
        """盤面のディープコピーを返す。"""
        new_board = Board()
        new_board._grid = copy.deepcopy(self._grid)
        return new_board

    # --- ユーティリティ ---

    def empty_count(self) -> int:
        """空マスの数を返す。"""
        return sum(1 for r in self._grid for c in r if c is None)

    def is_full(self) -> bool:
        """全マスが埋まっているか。"""
        return self.empty_count() == 0

    def _validate_pos(self, row: int, col: int) -> None:
        if not (0 <= row < GRID_ROWS and 0 <= col < GRID_COLS):
            raise IndexError(f"Position ({row}, {col}) is out of bounds")
