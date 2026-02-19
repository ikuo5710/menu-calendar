"""カウントダウンタイマー"""

from __future__ import annotations

import pygame

from src.asset_manager import AssetManager
from src.constants import TIMER_SECONDS, COLOR_TIMER_TEXT


class Timer:
    """180秒カウントダウンタイマー。"""

    def __init__(self, assets: AssetManager) -> None:
        self.assets = assets
        self._font = assets.get_font(28)
        self._remaining: float = TIMER_SECONDS
        self._running = False
        self._expired = False

    @property
    def remaining(self) -> float:
        return max(0.0, self._remaining)

    @property
    def remaining_int(self) -> int:
        return int(self.remaining)

    @property
    def expired(self) -> bool:
        return self._expired

    def start(self) -> None:
        self._remaining = TIMER_SECONDS
        self._running = True
        self._expired = False

    def stop(self) -> None:
        self._running = False

    def reset(self) -> None:
        """タイマーはリセットしない（仕様: 盤面のみリセット）。"""
        pass

    def update(self, dt_ms: int) -> bool:
        """経過時間(ms)で更新。期限切れなら True を返す。"""
        if not self._running or self._expired:
            return self._expired
        self._remaining -= dt_ms / 1000.0
        if self._remaining <= 0:
            self._remaining = 0
            self._running = False
            self._expired = True
            return True
        return False

    def format_time(self) -> str:
        secs = self.remaining_int
        m, s = divmod(secs, 60)
        return f"{m}:{s:02d}"

    def draw(self, surface: pygame.Surface, cx: int, y: int) -> None:
        time_str = self.format_time()
        color = (220, 38, 38) if self.remaining_int <= 30 else COLOR_TIMER_TEXT
        text = self._font.render(time_str, True, color)
        rect = text.get_rect(centerx=cx, centery=y)
        surface.blit(text, rect)
