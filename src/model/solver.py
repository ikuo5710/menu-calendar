"""CP-SAT ソルバーによる模範解答生成

OR-Tools の CP-SAT ソルバーで全制約を満たす解を生成する。
失敗時はハードコード済みのフォールバック解を返す。
"""

from __future__ import annotations

import logging
import random
from typing import Optional

from src.model.board import Board
from src.constants import (
    GRID_ROWS,
    GRID_COLS,
    MENU_COUNT,
    MENU_KARAAGE,
    MENU_EBI_FRY,
    MENU_CURRY_UDON,
    MENU_CURRY_RICE,
    MENU_CHIRASHI,
    FRIED_FOODS,
    CHIRASHI_PER_ROW_MAX,
    FRIED_PER_ROW_MAX,
)

logger = logging.getLogger(__name__)

# フォールバック固定解（全制約を満たす配置）
_FALLBACK_SOLUTION: list[list[int]] = [
    [0, 1, 2, 3, 4],
    [2, 3, 4, 0, 1],
    [4, 0, 1, 2, 3],
    [1, 2, 3, 4, 0],
    [3, 4, 0, 1, 2],
]


def generate_solution(timeout_seconds: float = 5.0) -> Board:
    """全制約を満たす模範解答を生成する。

    CP-SAT で解を探索し、失敗時はフォールバック解を返す。

    Args:
        timeout_seconds: ソルバーのタイムアウト（秒）。

    Returns:
        全制約を満たす Board。
    """
    board = _solve_with_cpsat(timeout_seconds)
    if board is not None:
        return board

    logger.warning("CP-SAT solver failed, using fallback solution")
    return _fallback_board()


def _solve_with_cpsat(timeout_seconds: float) -> Optional[Board]:
    """CP-SAT ソルバーで解を生成する。失敗時は None。"""
    try:
        from ortools.sat.python import cp_model
    except ImportError:
        logger.warning("ortools not installed, skipping CP-SAT solver")
        return None

    model = cp_model.CpModel()

    # 変数: x[r][c] ∈ {0..4}
    x = [
        [model.new_int_var(0, MENU_COUNT - 1, f"x_{r}_{c}") for c in range(GRID_COLS)]
        for r in range(GRID_ROWS)
    ]

    # 制約1: 列ごと AllDifferent
    for c in range(GRID_COLS):
        model.add_all_different([x[r][c] for r in range(GRID_ROWS)])

    # 制約2: 行ごと ちらし寿司 ≤ 1
    for r in range(GRID_ROWS):
        chirashi_bools = []
        for c in range(GRID_COLS):
            b = model.new_bool_var(f"chirashi_{r}_{c}")
            model.add(x[r][c] == MENU_CHIRASHI).only_enforce_if(b)
            model.add(x[r][c] != MENU_CHIRASHI).only_enforce_if(b.negated())
            chirashi_bools.append(b)
        model.add(sum(chirashi_bools) <= CHIRASHI_PER_ROW_MAX)

    # 制約3: 行ごと 揚げ物 ≤ 3
    fried_list = sorted(FRIED_FOODS)  # [0, 1]
    for r in range(GRID_ROWS):
        fried_bools = []
        for c in range(GRID_COLS):
            b = model.new_bool_var(f"fried_{r}_{c}")
            # b == 1 ⟺ x[r][c] ∈ FRIED_FOODS
            model.add_linear_expression_in_domain(
                x[r][c],
                cp_model.Domain.from_values(fried_list),
            ).only_enforce_if(b)
            model.add_linear_expression_in_domain(
                x[r][c],
                cp_model.Domain.from_values(fried_list).complement(),
            ).only_enforce_if(b.negated())
            fried_bools.append(b)
        model.add(sum(fried_bools) <= FRIED_PER_ROW_MAX)

    # 制約4: 列ごと隣接カレー連続禁止
    # カレーうどん→カレーライス or カレーライス→カレーうどん を禁止
    curry_pair = {MENU_CURRY_UDON, MENU_CURRY_RICE}
    for c in range(GRID_COLS):
        for r in range(GRID_ROWS - 1):
            # 2セルが異なるカレー種の組合せを禁止
            for m1 in curry_pair:
                m2 = (curry_pair - {m1}).pop()
                b1 = model.new_bool_var(f"curry_a_{r}_{c}_{m1}")
                b2 = model.new_bool_var(f"curry_b_{r}_{c}_{m2}")
                model.add(x[r][c] == m1).only_enforce_if(b1)
                model.add(x[r][c] != m1).only_enforce_if(b1.negated())
                model.add(x[r + 1][c] == m2).only_enforce_if(b2)
                model.add(x[r + 1][c] != m2).only_enforce_if(b2.negated())
                # b1 AND b2 を禁止
                model.add_bool_or([b1.negated(), b2.negated()])

    # ランダム目的関数で解を多様化
    coeffs = [random.randint(-10, 10) for _ in range(GRID_ROWS * GRID_COLS)]
    obj = sum(
        coeffs[r * GRID_COLS + c] * x[r][c]
        for r in range(GRID_ROWS)
        for c in range(GRID_COLS)
    )
    model.maximize(obj)

    # ソルバー実行
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = timeout_seconds

    status = solver.solve(model)

    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        board = Board()
        for r in range(GRID_ROWS):
            for c in range(GRID_COLS):
                board.place(r, c, solver.value(x[r][c]))
        return board

    logger.warning("CP-SAT solver status: %s", status)
    return None


def _fallback_board() -> Board:
    """ハードコード済みのフォールバック固定解を返す。"""
    board = Board()
    for r in range(GRID_ROWS):
        for c in range(GRID_COLS):
            board.place(r, c, _FALLBACK_SOLUTION[r][c])
    return board
