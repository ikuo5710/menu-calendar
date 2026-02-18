"""Board クラスの単体テスト"""

import pytest
from src.model.board import Board
from src.constants import GRID_ROWS, GRID_COLS, MENU_KARAAGE, MENU_CHIRASHI


class TestBoard:
    def test_initial_state(self):
        board = Board()
        for r in range(GRID_ROWS):
            for c in range(GRID_COLS):
                assert board.get(r, c) is None
        assert board.empty_count() == 25
        assert not board.is_full()

    def test_place_and_get(self):
        board = Board()
        board.place(0, 0, MENU_KARAAGE)
        assert board.get(0, 0) == MENU_KARAAGE
        assert board.empty_count() == 24

    def test_place_overwrite(self):
        board = Board()
        board.place(0, 0, MENU_KARAAGE)
        board.place(0, 0, MENU_CHIRASHI)
        assert board.get(0, 0) == MENU_CHIRASHI

    def test_remove(self):
        board = Board()
        board.place(1, 2, MENU_KARAAGE)
        board.remove(1, 2)
        assert board.get(1, 2) is None

    def test_move(self):
        board = Board()
        board.place(0, 0, MENU_KARAAGE)
        board.move(0, 0, 2, 3)
        assert board.get(0, 0) is None
        assert board.get(2, 3) == MENU_KARAAGE

    def test_move_empty_source(self):
        board = Board()
        board.move(0, 0, 1, 1)
        assert board.get(0, 0) is None
        assert board.get(1, 1) is None

    def test_reset(self):
        board = Board()
        for r in range(GRID_ROWS):
            for c in range(GRID_COLS):
                board.place(r, c, MENU_KARAAGE)
        assert board.is_full()
        board.reset()
        assert board.empty_count() == 25

    def test_copy_independence(self):
        board = Board()
        board.place(0, 0, MENU_KARAAGE)
        copied = board.copy()
        copied.place(0, 0, MENU_CHIRASHI)
        assert board.get(0, 0) == MENU_KARAAGE
        assert copied.get(0, 0) == MENU_CHIRASHI

    def test_grid_returns_copy(self):
        board = Board()
        board.place(0, 0, MENU_KARAAGE)
        grid = board.grid
        grid[0][0] = None
        assert board.get(0, 0) == MENU_KARAAGE

    def test_out_of_bounds(self):
        board = Board()
        with pytest.raises(IndexError):
            board.place(-1, 0, MENU_KARAAGE)
        with pytest.raises(IndexError):
            board.place(5, 0, MENU_KARAAGE)
        with pytest.raises(IndexError):
            board.remove(0, 5)
