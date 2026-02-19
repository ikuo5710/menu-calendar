"""rules.py の単体テスト"""

import pytest
from src.model.board import Board
from src.model.rules import (
    check_all,
    check_block_duplicates,
    check_chirashi_limit,
    check_fried_limit,
    check_curry_consecutive,
)
from src.constants import (
    MENU_KARAAGE,
    MENU_EBI_FRY,
    MENU_CURRY_UDON,
    MENU_CURRY_RICE,
    MENU_CHIRASHI,
)


class TestBlockDuplicates:
    def test_no_duplicates(self):
        board = Board()
        for r in range(5):
            board.place(r, 0, r)  # 0,1,2,3,4 全部違う
        assert check_block_duplicates(board) == []

    def test_one_duplicate(self):
        board = Board()
        board.place(0, 0, MENU_KARAAGE)
        board.place(1, 0, MENU_KARAAGE)
        violations = check_block_duplicates(board)
        assert len(violations) == 1
        assert violations[0].count == 1
        assert violations[0].kind == "duplicate"

    def test_triple_duplicate(self):
        board = Board()
        board.place(0, 0, MENU_KARAAGE)
        board.place(1, 0, MENU_KARAAGE)
        board.place(2, 0, MENU_KARAAGE)
        violations = check_block_duplicates(board)
        assert len(violations) == 1
        assert violations[0].count == 2

    def test_different_columns_independent(self):
        board = Board()
        board.place(0, 0, MENU_KARAAGE)
        board.place(1, 0, MENU_KARAAGE)
        board.place(0, 1, MENU_EBI_FRY)
        board.place(1, 1, MENU_EBI_FRY)
        violations = check_block_duplicates(board)
        assert len(violations) == 2


class TestChirashiLimit:
    def test_one_chirashi_per_row(self):
        board = Board()
        board.place(0, 0, MENU_CHIRASHI)
        assert check_chirashi_limit(board) == []

    def test_two_chirashi_same_row(self):
        board = Board()
        board.place(0, 0, MENU_CHIRASHI)
        board.place(0, 1, MENU_CHIRASHI)
        violations = check_chirashi_limit(board)
        assert len(violations) == 1
        assert violations[0].count == 1

    def test_three_chirashi_same_row(self):
        board = Board()
        board.place(0, 0, MENU_CHIRASHI)
        board.place(0, 1, MENU_CHIRASHI)
        board.place(0, 2, MENU_CHIRASHI)
        violations = check_chirashi_limit(board)
        assert len(violations) == 1
        assert violations[0].count == 2


class TestFriedLimit:
    def test_three_fried_ok(self):
        board = Board()
        board.place(0, 0, MENU_KARAAGE)
        board.place(0, 1, MENU_EBI_FRY)
        board.place(0, 2, MENU_KARAAGE)
        assert check_fried_limit(board) == []

    def test_four_fried_exceeds(self):
        board = Board()
        board.place(0, 0, MENU_KARAAGE)
        board.place(0, 1, MENU_EBI_FRY)
        board.place(0, 2, MENU_KARAAGE)
        board.place(0, 3, MENU_EBI_FRY)
        violations = check_fried_limit(board)
        assert len(violations) == 1
        assert violations[0].count == 1
        # 超過分は4つ目 (col=3) のみ
        assert violations[0].cells == [(0, 3)]

    def test_five_fried_exceeds(self):
        board = Board()
        for c in range(5):
            board.place(0, c, MENU_KARAAGE)
        violations = check_fried_limit(board)
        assert len(violations) == 1
        assert violations[0].count == 2
        assert violations[0].cells == [(0, 3), (0, 4)]


class TestCurryConsecutive:
    def test_no_consecutive(self):
        board = Board()
        board.place(0, 0, MENU_CURRY_UDON)
        board.place(2, 0, MENU_CURRY_RICE)
        assert check_curry_consecutive(board) == []

    def test_same_curry_ok(self):
        board = Board()
        board.place(0, 0, MENU_CURRY_UDON)
        board.place(1, 0, MENU_CURRY_UDON)
        assert check_curry_consecutive(board) == []

    def test_udon_then_rice(self):
        board = Board()
        board.place(0, 0, MENU_CURRY_UDON)
        board.place(1, 0, MENU_CURRY_RICE)
        violations = check_curry_consecutive(board)
        assert len(violations) == 1
        assert violations[0].count == 1
        assert set(violations[0].cells) == {(0, 0), (1, 0)}

    def test_rice_then_udon(self):
        board = Board()
        board.place(0, 0, MENU_CURRY_RICE)
        board.place(1, 0, MENU_CURRY_UDON)
        violations = check_curry_consecutive(board)
        assert len(violations) == 1


class TestCheckAll:
    def test_empty_board(self):
        board = Board()
        result = check_all(board)
        assert result.total_count == 0

    def test_valid_board(self):
        board = Board()
        # 各列で全メニュー1回ずつ（AllDifferent）
        perm = [0, 1, 2, 3, 4]
        for c in range(5):
            for r in range(5):
                board.place(r, c, perm[(r + c) % 5])
        result = check_all(board)
        # 完全に正しい配置かはチェック次第だが、重複なしは確実
        assert result.count_by_kind("duplicate") == 0
