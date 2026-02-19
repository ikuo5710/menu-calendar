"""ボタンUI部品"""

from __future__ import annotations

import pygame


class Button:
    """矩形＋テキストのボタン。ホバー・クリック判定付き。"""

    def __init__(
        self,
        rect: pygame.Rect,
        text: str,
        font: pygame.font.Font,
        color: tuple[int, int, int] = (245, 73, 0),
        hover_color: tuple[int, int, int] = (220, 60, 0),
        text_color: tuple[int, int, int] = (255, 255, 255),
        border_radius: int = 12,
    ) -> None:
        self.rect = rect
        self.text = text
        self.font = font
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.border_radius = border_radius
        self._hovered = False

    def handle_event(self, event: pygame.event.Event) -> bool:
        """イベント処理。クリックされたら True を返す。"""
        if event.type == pygame.MOUSEMOTION:
            self._hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False

    def draw(self, surface: pygame.Surface) -> None:
        color = self.hover_color if self._hovered else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=self.border_radius)
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
