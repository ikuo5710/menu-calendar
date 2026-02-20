"""メニューパレット（左サイドバー）"""

from __future__ import annotations

import pygame

from src.asset_manager import AssetManager
from src.constants import (
    MENU_KARAAGE,
    MENU_EBI_FRY,
    MENU_CURRY_UDON,
    MENU_CURRY_RICE,
    MENU_CHIRASHI,
    MENU_NAMES,
    MENU_EMOJI,
    MENU_ICON_KEYS,
    MENU_COLORS,
    MENU_BG_COLORS,
    FRIED_FOODS,
    COLOR_WHITE,
    COLOR_ACCENT_ORANGE,
    COLOR_ACCENT_SUB,
    COLOR_TEXT_SUB,
)

# レイアウト
PALETTE_X = 15
PALETTE_Y = 65
PALETTE_W = 200
ITEM_H = 52
ITEM_GAP = 8

MENU_ORDER = [MENU_KARAAGE, MENU_EBI_FRY, MENU_CURRY_UDON, MENU_CURRY_RICE, MENU_CHIRASHI]


class Palette:
    """メニュー5種のパレット。ドラッグ開始元。"""

    def __init__(self, assets: AssetManager) -> None:
        self.assets = assets
        self._font_heading = assets.get_font(18)
        self._font_name = assets.get_font(16)
        self._font_badge = assets.get_font(12)
        self._font_hint = assets.get_font(12)
        self._font_emoji = None
        try:
            self._font_emoji = pygame.font.SysFont("segoeUIemoji", 22)
        except Exception:
            self._font_emoji = pygame.font.SysFont(None, 22)

        self._item_rects: list[tuple[int, pygame.Rect]] = []
        self._build_rects()

    def _build_rects(self) -> None:
        self._item_rects = []
        y = PALETTE_Y + 36
        for mid in MENU_ORDER:
            rect = pygame.Rect(PALETTE_X + 12, y, PALETTE_W - 24, ITEM_H)
            self._item_rects.append((mid, rect))
            y += ITEM_H + ITEM_GAP

    def hit_test(self, pos: tuple[int, int]) -> int | None:
        """マウス座標がパレット項目上ならメニューIDを返す。"""
        for mid, rect in self._item_rects:
            if rect.collidepoint(pos):
                return mid
        return None

    def get_item_rect(self, menu_id: int) -> pygame.Rect | None:
        for mid, rect in self._item_rects:
            if mid == menu_id:
                return rect
        return None

    def draw(self, surface: pygame.Surface) -> None:
        # パレット背景
        bg_rect = pygame.Rect(PALETTE_X, PALETTE_Y, PALETTE_W, 420)
        pygame.draw.rect(surface, COLOR_WHITE, bg_rect, border_radius=12)
        pygame.draw.rect(surface, (230, 230, 230), bg_rect, width=1, border_radius=12)

        # 見出し
        heading = self._font_heading.render("メニュー", True, COLOR_ACCENT_ORANGE)
        surface.blit(heading, (PALETTE_X + 14, PALETTE_Y + 10))

        # メニュー項目
        for mid, rect in self._item_rects:
            self._draw_item(surface, mid, rect)

        # ヒント
        hint = self._font_hint.render("ドラッグしてグリッドに配置！", True, COLOR_TEXT_SUB)
        hint_rect = hint.get_rect(centerx=PALETTE_X + PALETTE_W // 2,
                                  top=self._item_rects[-1][1].bottom + 12)
        surface.blit(hint, hint_rect)

    def _draw_item(self, surface: pygame.Surface, menu_id: int, rect: pygame.Rect) -> None:
        bg = MENU_BG_COLORS[menu_id]
        pygame.draw.rect(surface, bg, rect, border_radius=8)

        emoji = MENU_EMOJI[menu_id]
        name = MENU_NAMES[menu_id]
        text_color = MENU_COLORS[menu_id]

        icon_key = MENU_ICON_KEYS.get(menu_id)
        icon_size = (32, 32)
        icon = self.assets.get_icon(icon_key, icon_size) if icon_key else None

        name_surf = self._font_name.render(name, True, text_color)

        if icon is not None:
            icon_y = rect.centery - icon.get_height() // 2
            surface.blit(icon, (rect.x + 10, icon_y))
            icon_w = icon.get_width()
        else:
            emoji_surf = self._font_emoji.render(emoji, True, (10, 10, 10))
            emoji_y = rect.centery - emoji_surf.get_height() // 2
            surface.blit(emoji_surf, (rect.x + 10, emoji_y))
            icon_w = emoji_surf.get_width()

        name_y = rect.centery - name_surf.get_height() // 2
        surface.blit(name_surf, (rect.x + 10 + icon_w + 6, name_y))

        if menu_id in FRIED_FOODS:
            badge_surf = self._font_badge.render("揚げ物", True, COLOR_WHITE)
            bw = badge_surf.get_width() + 8
            bh = 18
            bx = rect.right - bw - 8
            by = rect.centery - bh // 2
            badge_rect = pygame.Rect(bx, by, bw, bh)
            pygame.draw.rect(surface, COLOR_ACCENT_SUB, badge_rect, border_radius=4)
            surface.blit(badge_surf, (bx + 4, by + (bh - badge_surf.get_height()) // 2))
