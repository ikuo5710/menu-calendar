"""scoring.py の単体テスト"""

import pytest
from src.model.board import Board
from src.model.scoring import calculate_score
from src.constants import (
    MENU_KARAAGE,
    MENU_EBI_FRY,
    MENU_CURRY_UDON,
    MENU_CURRY_RICE,
    MENU_CHIRASHI,
)


class TestScoring:
    def test_empty_board(self):
        board = Board()
        result = calculate_score(board, remaining_seconds=0, completed_by_button=False)
        # 25空欄 × -3 = -75, score = max(0, 100 - 75) = 25
        assert result.score == 25

    def test_perfect_score(self):
        """全マス埋め、制約違反なし → 100点。"""
        board = Board()
        # 各列 AllDifferent, 各行ちらし寿司≤1, 揚げ物≤3, カレー連続なし
        layout = [
            [0, 1, 2, 3, 4],
            [2, 3, 4, 0, 1],
            [4, 0, 1, 2, 3],
            [1, 2, 3, 4, 0],
            [3, 4, 0, 1, 2],
        ]
        for r in range(5):
            for c in range(5):
                board.place(r, c, layout[r][c])
        result = calculate_score(board, remaining_seconds=0, completed_by_button=False)
        assert result.score == 100
        assert result.total_penalty == 0

    def test_early_bonus_120(self):
        """完了ボタン + 残り120秒以上 → +5点。"""
        board = Board()
        layout = [
            [0, 1, 2, 3, 4],
            [2, 3, 4, 0, 1],
            [4, 0, 1, 2, 3],
            [1, 2, 3, 4, 0],
            [3, 4, 0, 1, 2],
        ]
        for r in range(5):
            for c in range(5):
                board.place(r, c, layout[r][c])
        result = calculate_score(board, remaining_seconds=150, completed_by_button=True)
        assert result.score == 100  # capped at 100
        assert result.bonus == 5

    def test_early_bonus_60(self):
        board = Board()
        layout = [
            [0, 1, 2, 3, 4],
            [2, 3, 4, 0, 1],
            [4, 0, 1, 2, 3],
            [1, 2, 3, 4, 0],
            [3, 4, 0, 1, 2],
        ]
        for r in range(5):
            for c in range(5):
                board.place(r, c, layout[r][c])
        result = calculate_score(board, remaining_seconds=90, completed_by_button=True)
        assert result.bonus == 3

    def test_no_bonus_on_timeout(self):
        board = Board()
        layout = [
            [0, 1, 2, 3, 4],
            [2, 3, 4, 0, 1],
            [4, 0, 1, 2, 3],
            [1, 2, 3, 4, 0],
            [3, 4, 0, 1, 2],
        ]
        for r in range(5):
            for c in range(5):
                board.place(r, c, layout[r][c])
        result = calculate_score(board, remaining_seconds=150, completed_by_button=False)
        assert result.bonus == 0

    def test_duplicate_penalty(self):
        """1列に同じメニュー2回 → -8点。"""
        board = Board()
        # 全マス埋めるがcol=0にからあげ2回
        layout = [
            [0, 1, 2, 3, 4],
            [0, 2, 3, 4, 1],  # col=0 が0=からあげ重複
            [2, 3, 4, 0, 1],
            [3, 4, 0, 1, 2],
            [4, 0, 1, 2, 3],
        ]
        for r in range(5):
            for c in range(5):
                board.place(r, c, layout[r][c])
        result = calculate_score(board, remaining_seconds=0, completed_by_button=False)
        dup_penalties = [p for p in result.penalties if p.label == "ブロック内重複"]
        assert len(dup_penalties) > 0

    def test_score_clamped_at_zero(self):
        """大量違反でも0点以下にならない。"""
        board = Board()
        # 全マスからあげ
        for r in range(5):
            for c in range(5):
                board.place(r, c, MENU_KARAAGE)
        result = calculate_score(board, remaining_seconds=0, completed_by_button=False)
        assert result.score >= 0

    def test_comment_exists(self):
        board = Board()
        result = calculate_score(board, remaining_seconds=0, completed_by_button=False)
        assert len(result.comment) > 0
