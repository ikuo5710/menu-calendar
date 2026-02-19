"""制約違反検出

4種類の制約をチェックし、違反セル座標リストを返す。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from collections import Counter

from src.model.board import Board
from src.constants import (
    GRID_ROWS,
    GRID_COLS,
    MENU_CHIRASHI,
    FRIED_FOODS,
    MENU_CURRY_UDON,
    MENU_CURRY_RICE,
    CHIRASHI_PER_ROW_MAX,
    FRIED_PER_ROW_MAX,
)


@dataclass
class Violation:
    """違反1件。"""
    kind: str            # "duplicate", "chirashi", "fried", "curry"
    cells: list[tuple[int, int]]  # 違反セル座標 (row, col)
    count: int = 1       # 違反件数


@dataclass
class ViolationResult:
    """全違反の集約。"""
    violations: list[Violation] = field(default_factory=list)

    @property
    def total_count(self) -> int:
        return sum(v.count for v in self.violations)

    def by_kind(self, kind: str) -> list[Violation]:
        return [v for v in self.violations if v.kind == kind]

    def count_by_kind(self, kind: str) -> int:
        return sum(v.count for v in self.violations if v.kind == kind)

    def all_violation_cells(self) -> set[tuple[int, int]]:
        cells: set[tuple[int, int]] = set()
        for v in self.violations:
            cells.update(v.cells)
        return cells


def check_all(board: Board) -> ViolationResult:
    """盤面の全制約をチェックし、違反結果を返す。"""
    result = ViolationResult()
    result.violations.extend(check_block_duplicates(board))
    result.violations.extend(check_chirashi_limit(board))
    result.violations.extend(check_fried_limit(board))
    result.violations.extend(check_curry_consecutive(board))
    return result


def check_block_duplicates(board: Board) -> list[Violation]:
    """制約1: ブロック内重複（列ごと）。

    ある列でメニューが k 回出現 → 違反 k-1 件。
    """
    violations: list[Violation] = []
    for c in range(GRID_COLS):
        counter: dict[int, list[int]] = {}
        for r in range(GRID_ROWS):
            mid = board.get(r, c)
            if mid is not None:
                counter.setdefault(mid, []).append(r)
        for mid, rows in counter.items():
            if len(rows) > 1:
                cells = [(r, c) for r in rows]
                violations.append(Violation(
                    kind="duplicate",
                    cells=cells,
                    count=len(rows) - 1,
                ))
    return violations


def check_chirashi_limit(board: Board) -> list[Violation]:
    """制約2: ちらし寿司は同じ日に1ブロックまで（行ごと）。

    ある行でちらし寿司が k 個 → 超過 max(0, k-1) 件。
    """
    violations: list[Violation] = []
    for r in range(GRID_ROWS):
        cols = [c for c in range(GRID_COLS) if board.get(r, c) == MENU_CHIRASHI]
        excess = len(cols) - CHIRASHI_PER_ROW_MAX
        if excess > 0:
            cells = [(r, c) for c in cols]
            violations.append(Violation(
                kind="chirashi",
                cells=cells,
                count=excess,
            ))
    return violations


def check_fried_limit(board: Board) -> list[Violation]:
    """制約3: 揚げ物カテゴリ上限（行ごと）。

    ある行で揚げ物の合計が f 個 → 超過 max(0, f-3) 件。
    超過分: 左から順に3つ許容、4つ目以降を超過扱い。
    """
    violations: list[Violation] = []
    for r in range(GRID_ROWS):
        fried_cols = [c for c in range(GRID_COLS) if board.get(r, c) in FRIED_FOODS]
        excess = len(fried_cols) - FRIED_PER_ROW_MAX
        if excess > 0:
            # 左から3つ許容、4つ目以降が超過
            excess_cells = [(r, c) for c in fried_cols[FRIED_PER_ROW_MAX:]]
            violations.append(Violation(
                kind="fried",
                cells=excess_cells,
                count=excess,
            ))
    return violations


def check_curry_consecutive(board: Board) -> list[Violation]:
    """制約4: カレー2種の連続禁止（列ごと隣接ペア）。

    同じブロック（列）で連続する2日に
    (カレーうどん→カレーライス) or (カレーライス→カレーうどん) を禁止。
    """
    curry_pair = {MENU_CURRY_UDON, MENU_CURRY_RICE}
    violations: list[Violation] = []
    for c in range(GRID_COLS):
        for r in range(GRID_ROWS - 1):
            m1 = board.get(r, c)
            m2 = board.get(r + 1, c)
            if m1 is not None and m2 is not None:
                if {m1, m2} == curry_pair:
                    violations.append(Violation(
                        kind="curry",
                        cells=[(r, c), (r + 1, c)],
                        count=1,
                    ))
    return violations
