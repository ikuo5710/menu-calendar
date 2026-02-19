"""採点ロジック

score = min(100, max(0, 100 - penalty + bonus))
"""

from __future__ import annotations

from dataclasses import dataclass, field

from src.model.board import Board
from src.model.rules import ViolationResult, check_all
from src.constants import (
    PENALTY_EMPTY,
    PENALTY_BLOCK_DUPLICATE,
    PENALTY_CHIRASHI_EXCESS,
    PENALTY_FRIED_EXCESS,
    PENALTY_CURRY_CONSECUTIVE,
    BONUS_EARLY_120,
    BONUS_EARLY_60,
)


@dataclass
class PenaltyDetail:
    """減点内訳1件。"""
    label: str
    count: int
    per_point: int

    @property
    def total(self) -> int:
        return self.count * self.per_point


@dataclass
class ScoreResult:
    """採点結果。"""
    score: int
    penalties: list[PenaltyDetail] = field(default_factory=list)
    bonus: int = 0
    bonus_label: str = ""
    comment: str = ""
    violations: ViolationResult | None = None

    @property
    def total_penalty(self) -> int:
        return sum(p.total for p in self.penalties)


def calculate_score(
    board: Board,
    remaining_seconds: int,
    completed_by_button: bool,
) -> ScoreResult:
    """盤面を採点し、結果を返す。"""
    violations = check_all(board)
    penalties: list[PenaltyDetail] = []

    # A) 未配置マス
    empty = board.empty_count()
    if empty > 0:
        penalties.append(PenaltyDetail(
            label="未配置マス",
            count=empty,
            per_point=PENALTY_EMPTY,
        ))

    # B) ブロック内重複
    dup_count = violations.count_by_kind("duplicate")
    if dup_count > 0:
        penalties.append(PenaltyDetail(
            label="ブロック内重複",
            count=dup_count,
            per_point=PENALTY_BLOCK_DUPLICATE,
        ))

    # ちらし寿司超過
    chi_count = violations.count_by_kind("chirashi")
    if chi_count > 0:
        penalties.append(PenaltyDetail(
            label="ちらし寿司 同日超過",
            count=chi_count,
            per_point=PENALTY_CHIRASHI_EXCESS,
        ))

    # 揚げ物超過
    fri_count = violations.count_by_kind("fried")
    if fri_count > 0:
        penalties.append(PenaltyDetail(
            label="揚げ物 同日超過",
            count=fri_count,
            per_point=PENALTY_FRIED_EXCESS,
        ))

    # カレー連続
    cur_count = violations.count_by_kind("curry")
    if cur_count > 0:
        penalties.append(PenaltyDetail(
            label="カレー2種 連続",
            count=cur_count,
            per_point=PENALTY_CURRY_CONSECUTIVE,
        ))

    # C) 早解きボーナス
    bonus = 0
    bonus_label = ""
    if completed_by_button:
        if remaining_seconds >= 120:
            bonus = BONUS_EARLY_120
            bonus_label = f"早解きボーナス（残り{remaining_seconds}秒）"
        elif remaining_seconds >= 60:
            bonus = BONUS_EARLY_60
            bonus_label = f"早解きボーナス（残り{remaining_seconds}秒）"

    total_penalty = sum(p.total for p in penalties)
    score = min(100, max(0, 100 - total_penalty + bonus))

    comment = _generate_comment(score, empty, violations)

    return ScoreResult(
        score=score,
        penalties=penalties,
        bonus=bonus,
        bonus_label=bonus_label,
        comment=comment,
        violations=violations,
    )


def _generate_comment(score: int, empty: int, violations: ViolationResult) -> str:
    """点数帯別の講評コメント。"""
    if score == 100:
        return "パーフェクト！すべての制約を満たした完璧な献立表です！"
    elif score >= 90:
        return "すばらしい！ほぼ完璧な献立表です！"
    elif score >= 70:
        return "よくがんばりました！あと少しで完璧です！"
    elif score >= 50:
        return "まずまずの出来です。制約をもう少し意識してみよう！"
    elif score >= 30:
        return "もう少しがんばろう！ルールをよく確認してね。"
    else:
        if empty > 15:
            return "まずは全部のマスを埋めることから始めよう！"
        return "むずかしかったかな？ルールを確認してもう一度チャレンジ！"
