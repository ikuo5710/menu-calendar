"""ドラッグ＆ドロップマネージャ"""

from __future__ import annotations

import pygame

from src.asset_manager import AssetManager
from src.model.board import Board
from src.ui.grid import grid_hit_test, cell_rect, CELL_SIZE
from src.ui.palette import Palette
from src.constants import (
    MENU_EMOJI,
    MENU_NAMES,
    MENU_COLORS,
    MENU_BG_COLORS,
)


class DragDrop:
    """パレット→セル、セル→セルのドラッグ＆ドロップを管理。"""

    def __init__(self, assets: AssetManager, board: Board, palette: Palette) -> None:
        self.assets = assets
        self.board = board
        self.palette = palette

        self._dragging = False
        self._drag_menu_id: int | None = None
        self._drag_source: tuple[int, int] | None = None  # セル起点の場合 (row, col)
        self._drag_pos: tuple[int, int] = (0, 0)

        self._font_emoji = None
        try:
            self._font_emoji = pygame.font.SysFont("segoeUIemoji", 28)
        except Exception:
            self._font_emoji = pygame.font.SysFont(None, 28)
        self._font_name = assets.get_font(12)

    @property
    def is_dragging(self) -> bool:
        return self._dragging

    def handle_event(self, event: pygame.event.Event) -> str | None:
        """イベント処理。戻り値: 'placed', 'moved', 'removed', None。"""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self._on_mouse_down(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            return self._on_right_click(event.pos)
        elif event.type == pygame.MOUSEMOTION:
            if self._dragging:
                self._drag_pos = event.pos
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self._dragging:
                return self._on_drop(event.pos)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_DELETE:
            return self._on_delete_key()
        return None

    def _on_mouse_down(self, pos: tuple[int, int]) -> None:
        # パレットからドラッグ開始
        menu_id = self.palette.hit_test(pos)
        if menu_id is not None:
            self._start_drag(menu_id, None, pos)
            return None

        # セルからドラッグ開始
        cell = grid_hit_test(pos)
        if cell is not None:
            r, c = cell
            menu_id = self.board.get(r, c)
            if menu_id is not None:
                self._start_drag(menu_id, (r, c), pos)
        return None

    def _on_right_click(self, pos: tuple[int, int]) -> str | None:
        cell = grid_hit_test(pos)
        if cell is not None:
            r, c = cell
            if self.board.get(r, c) is not None:
                self.board.remove(r, c)
                return "removed"
        return None

    def _on_delete_key(self) -> str | None:
        pos = pygame.mouse.get_pos()
        cell = grid_hit_test(pos)
        if cell is not None:
            r, c = cell
            if self.board.get(r, c) is not None:
                self.board.remove(r, c)
                return "removed"
        return None

    def _start_drag(self, menu_id: int, source: tuple[int, int] | None, pos: tuple[int, int]) -> None:
        self._dragging = True
        self._drag_menu_id = menu_id
        self._drag_source = source
        self._drag_pos = pos
        if source is not None:
            self.board.remove(source[0], source[1])

    def _on_drop(self, pos: tuple[int, int]) -> str | None:
        if not self._dragging or self._drag_menu_id is None:
            self._cancel_drag()
            return None

        cell = grid_hit_test(pos)
        result = None

        if cell is not None:
            r, c = cell
            self.board.place(r, c, self._drag_menu_id)
            result = "moved" if self._drag_source else "placed"
        elif self._drag_source is not None:
            # グリッド外にドロップ → 除去（元のセルは既に空）
            result = "removed"

        self._cancel_drag()
        return result

    def _cancel_drag(self) -> None:
        self._dragging = False
        self._drag_menu_id = None
        self._drag_source = None

    def draw_dragging(self, surface: pygame.Surface) -> None:
        """ドラッグ中のメニューアイテムを描画。"""
        if not self._dragging or self._drag_menu_id is None:
            return

        mid = self._drag_menu_id
        mx, my = self._drag_pos
        size = 80

        bg = MENU_BG_COLORS.get(mid, (240, 240, 240))
        rect = pygame.Rect(mx - size // 2, my - size // 2, size, size)
        # 半透明効果（影付き）
        shadow = pygame.Surface((size + 4, size + 4), pygame.SRCALPHA)
        shadow.fill((0, 0, 0, 40))
        surface.blit(shadow, (rect.x - 2, rect.y + 2))

        pygame.draw.rect(surface, bg, rect, border_radius=10)
        pygame.draw.rect(surface, MENU_COLORS.get(mid, (100, 100, 100)), rect, width=2, border_radius=10)

        emoji = MENU_EMOJI.get(mid, "?")
        emoji_surf = self._font_emoji.render(emoji, True, (10, 10, 10))
        emoji_rect = emoji_surf.get_rect(centerx=rect.centerx, centery=rect.centery - 6)
        surface.blit(emoji_surf, emoji_rect)

        name = MENU_NAMES.get(mid, "?")
        name_surf = self._font_name.render(name, True, MENU_COLORS.get(mid, (10, 10, 10)))
        name_rect = name_surf.get_rect(centerx=rect.centerx, top=emoji_rect.bottom + 2)
        surface.blit(name_surf, name_rect)
