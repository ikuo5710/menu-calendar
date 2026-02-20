"""トグルスイッチUIコンポーネント"""

from __future__ import annotations

import pygame


class ToggleSwitch:
    """ラベル付きトグルスイッチ。"""

    _W = 40
    _H = 22
    _KNOB = 18
    _COLOR_ON = (76, 175, 80)
    _COLOR_OFF = (189, 189, 189)
    _COLOR_KNOB = (255, 255, 255)

    def __init__(
        self,
        x: int,
        y: int,
        label: str,
        font: pygame.font.Font,
        initial: bool = True,
    ) -> None:
        self._enabled = initial
        self._label = label
        self._font = font

        # ラベルをスイッチの左に配置
        label_surf = font.render(label, True, (60, 60, 60))
        self._label_w = label_surf.get_width()
        self._label_x = x
        self._label_y = y + (self._H - label_surf.get_height()) // 2

        self._switch_x = x + self._label_w + 6
        self._switch_y = y
        self._rect = pygame.Rect(self._switch_x, self._switch_y, self._W, self._H)

    @property
    def enabled(self) -> bool:
        return self._enabled

    def handle_event(self, event: pygame.event.Event) -> bool | None:
        """クリックでトグル。状態変化時に新しい状態を返す。変化なしは None。"""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self._rect.collidepoint(event.pos):
                self._enabled = not self._enabled
                return self._enabled
        return None

    def draw(self, surface: pygame.Surface) -> None:
        # ラベル
        label_surf = self._font.render(self._label, True, (60, 60, 60))
        surface.blit(label_surf, (self._label_x, self._label_y))

        # スイッチ背景（角丸）
        bg_color = self._COLOR_ON if self._enabled else self._COLOR_OFF
        pygame.draw.rect(surface, bg_color, self._rect, border_radius=self._H // 2)

        # ノブ
        knob_pad = (self._H - self._KNOB) // 2
        if self._enabled:
            knob_x = self._switch_x + self._W - self._KNOB - knob_pad
        else:
            knob_x = self._switch_x + knob_pad
        knob_y = self._switch_y + knob_pad
        knob_rect = pygame.Rect(knob_x, knob_y, self._KNOB, self._KNOB)
        pygame.draw.rect(surface, self._COLOR_KNOB, knob_rect, border_radius=self._KNOB // 2)
