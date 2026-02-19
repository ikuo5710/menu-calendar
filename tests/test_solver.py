"""solver.py の単体テスト"""

import pytest
from src.model.board import Board
from src.model.solver import generate_solution, _fallback_board, _solve_with_cpsat
from src.model.rules import check_all
from src.constants import (
    GRID_ROWS,
    GRID_COLS,
    MENU_COUNT,
    FRIED_FOODS,
    MENU_CHIRASHI,
    MENU_CURRY_UDON,
    MENU_CURRY_RICE,
    CHIRASHI_PER_ROW_MAX,
    FRIED_PER_ROW_MAX,
)


def _validate_board(board: Board) -> None:
    """生成された解が全制約を満たしていることを検証。"""
    # 全マス埋まっている
    assert board.is_full(), "Board is not full"

    # 各マスの値が有効範囲
    for r in range(GRID_ROWS):
        for c in range(GRID_COLS):
            v = board.get(r, c)
            assert v is not None
            assert 0 <= v < MENU_COUNT, f"Invalid menu_id {v} at ({r},{c})"

    # rules.py の全チェックで違反なし
    result = check_all(board)
    assert result.total_count == 0, (
        f"Violations found: {[(v.kind, v.cells) for v in result.violations]}"
    )


class TestFallbackSolution:
    def test_fallback_is_valid(self):
        board = _fallback_board()
        _validate_board(board)

    def test_fallback_all_different_per_col(self):
        board = _fallback_board()
        for c in range(GRID_COLS):
            col_vals = {board.get(r, c) for r in range(GRID_ROWS)}
            assert len(col_vals) == GRID_ROWS

    def test_fallback_chirashi_limit(self):
        board = _fallback_board()
        for r in range(GRID_ROWS):
            chirashi_count = sum(
                1 for c in range(GRID_COLS)
                if board.get(r, c) == MENU_CHIRASHI
            )
            assert chirashi_count <= CHIRASHI_PER_ROW_MAX

    def test_fallback_fried_limit(self):
        board = _fallback_board()
        for r in range(GRID_ROWS):
            fried_count = sum(
                1 for c in range(GRID_COLS)
                if board.get(r, c) in FRIED_FOODS
            )
            assert fried_count <= FRIED_PER_ROW_MAX

    def test_fallback_no_curry_consecutive(self):
        board = _fallback_board()
        curry_pair = {MENU_CURRY_UDON, MENU_CURRY_RICE}
        for c in range(GRID_COLS):
            for r in range(GRID_ROWS - 1):
                m1 = board.get(r, c)
                m2 = board.get(r + 1, c)
                if m1 in curry_pair and m2 in curry_pair:
                    assert m1 == m2, (
                        f"Curry consecutive at col={c}, rows={r},{r+1}"
                    )


class TestCPSATSolver:
    def test_cpsat_generates_valid_solution(self):
        board = _solve_with_cpsat(timeout_seconds=10.0)
        if board is None:
            pytest.skip("ortools not available")
        _validate_board(board)

    def test_cpsat_all_different_per_col(self):
        board = _solve_with_cpsat(timeout_seconds=10.0)
        if board is None:
            pytest.skip("ortools not available")
        for c in range(GRID_COLS):
            col_vals = {board.get(r, c) for r in range(GRID_ROWS)}
            assert len(col_vals) == GRID_ROWS


class TestGenerateSolution:
    def test_returns_valid_board(self):
        board = generate_solution(timeout_seconds=10.0)
        _validate_board(board)

    def test_board_is_full(self):
        board = generate_solution(timeout_seconds=10.0)
        assert board.is_full()

    def test_no_violations(self):
        board = generate_solution(timeout_seconds=10.0)
        result = check_all(board)
        assert result.total_count == 0
