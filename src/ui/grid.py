"""5×5 グリッド描画"""

from __future__ import annotations

import pygame

from src.asset_manager import AssetManager
from src.model.board import Board
from src.constants import (
    GRID_ROWS,
    GRID_COLS,
    DAY_LABELS,
    BLOCK_LABELS,
    MENU_NAMES,
    MENU_EMOJI,
    MENU_ICON_KEYS,
    MENU_COLORS,
    MENU_BG_COLORS,
    COLOR_WHITE,
    COLOR_BLOCK_LABEL,
    COLOR_DAY_LABEL_BG,
    COLOR_DAY_LABEL_TEXT,
    COLOR_CELL_EMPTY,
    COLOR_CELL_PLUS,
)

# レイアウト定数
GRID_X = 280          # グリッド領域左端
GRID_Y = 55           # グリッド領域上端
DAY_LABEL_W = 55      # 曜日ラベル幅
HEADER_H = 22         # ブロックヘッダ高さ
CELL_SIZE = 110       # セル一辺
CELL_GAP = 4          # セル間隔


def cell_rect(row: int, col: int) -> pygame.Rect:
    """セル (row, col) の矩形を返す。"""
    x = GRID_X + DAY_LABEL_W + col * (CELL_SIZE + CELL_GAP)
    y = GRID_Y + HEADER_H + row * (CELL_SIZE + CELL_GAP)
    return pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)


def grid_hit_test(pos: tuple[int, int]) -> tuple[int, int] | None:
    """マウス座標からセル (row, col) を返す。該当なし None。"""
    for r in range(GRID_ROWS):
        for c in range(GRID_COLS):
            if cell_rect(r, c).collidepoint(pos):
                return (r, c)
    return None


class Grid:
    """5×5 グリッドの描画。"""

    def __init__(self, assets: AssetManager) -> None:
        self.assets = assets
        self._font_header = assets.get_font(14)
        self._font_day = assets.get_font(14)
        self._font_cell_plus = assets.get_font(24)
        self._font_emoji = None
        self._font_menu_name = assets.get_font(13)
        try:
            self._font_emoji = pygame.font.SysFont("segoeUIemoji", 32)
        except Exception:
            self._font_emoji = pygame.font.SysFont(None, 32)

    def draw(self, surface: pygame.Surface, board: Board) -> None:
        self._draw_block_headers(surface)
        self._draw_day_labels(surface)
        self._draw_cells(surface, board)

    def _draw_block_headers(self, surface: pygame.Surface) -> None:
        for c in range(GRID_COLS):
            r = cell_rect(0, c)
            label = self._font_header.render(BLOCK_LABELS[c], True, COLOR_BLOCK_LABEL)
            label_rect = label.get_rect(centerx=r.centerx, bottom=GRID_Y + HEADER_H - 2)
            surface.blit(label, label_rect)

    def _draw_day_labels(self, surface: pygame.Surface) -> None:
        for r in range(GRID_ROWS):
            cr = cell_rect(r, 0)
            label_rect = pygame.Rect(GRID_X, cr.y, DAY_LABEL_W, CELL_SIZE)
            pygame.draw.rect(surface, COLOR_DAY_LABEL_BG, label_rect, border_radius=6)
            label = self._font_day.render(DAY_LABELS[r], True, COLOR_DAY_LABEL_TEXT)
            lr = label.get_rect(center=label_rect.center)
            surface.blit(label, lr)

    def _draw_cells(self, surface: pygame.Surface, board: Board) -> None:
        for r in range(GRID_ROWS):
            for c in range(GRID_COLS):
                rect = cell_rect(r, c)
                menu_id = board.get(r, c)
                if menu_id is None:
                    self._draw_empty_cell(surface, rect)
                else:
                    self._draw_filled_cell(surface, rect, menu_id)

    def _draw_empty_cell(self, surface: pygame.Surface, rect: pygame.Rect) -> None:
        pygame.draw.rect(surface, COLOR_CELL_EMPTY, rect, border_radius=8)
        plus = self._font_cell_plus.render("＋", True, COLOR_CELL_PLUS)
        pr = plus.get_rect(center=rect.center)
        surface.blit(plus, pr)

    def _draw_filled_cell(self, surface: pygame.Surface, rect: pygame.Rect, menu_id: int) -> None:
        bg = MENU_BG_COLORS.get(menu_id, COLOR_CELL_EMPTY)
        pygame.draw.rect(surface, bg, rect, border_radius=8)

        icon_key = MENU_ICON_KEYS.get(menu_id)
        icon_size = (56, 56)
        icon = self.assets.get_icon(icon_key, icon_size) if icon_key else None

        if icon is not None:
            icon_rect = icon.get_rect(centerx=rect.centerx, centery=rect.centery - 10)
            surface.blit(icon, icon_rect)
        else:
            emoji_text = MENU_EMOJI.get(menu_id, "?")
            emoji_surf = self._font_emoji.render(emoji_text, True, (10, 10, 10))
            icon_rect = emoji_surf.get_rect(centerx=rect.centerx, centery=rect.centery - 10)
            surface.blit(emoji_surf, icon_rect)

        name = MENU_NAMES.get(menu_id, "?")
        text_color = MENU_COLORS.get(menu_id, (10, 10, 10))
        name_surf = self._font_menu_name.render(name, True, text_color)
        name_rect = name_surf.get_rect(centerx=rect.centerx, top=icon_rect.bottom + 4)
        surface.blit(name_surf, name_rect)
