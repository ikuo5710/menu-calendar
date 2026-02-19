"""テキストラベルUI部品"""

from __future__ import annotations

import pygame


class Label:
    """テキストラベル。フォント・色・位置を指定して描画。"""

    def __init__(
        self,
        text: str,
        font: pygame.font.Font,
        color: tuple[int, int, int] = (10, 10, 10),
        pos: tuple[int, int] = (0, 0),
        anchor: str = "topleft",
    ) -> None:
        self.text = text
        self.font = font
        self.color = color
        self.pos = pos
        self.anchor = anchor
        self._surface: pygame.Surface | None = None

    def set_text(self, text: str) -> None:
        if text != self.text:
            self.text = text
            self._surface = None

    def draw(self, surface: pygame.Surface) -> None:
        if self._surface is None:
            self._surface = self.font.render(self.text, True, self.color)
        rect = self._surface.get_rect(**{self.anchor: self.pos})
        surface.blit(self._surface, rect)
