"""ゲーム実行画面"""

from __future__ import annotations

import pygame

from src.asset_manager import AssetManager
from src.model.board import Board
from src.model.rules import check_all
from src.model.solver import generate_solution
from src.ui.grid import Grid, cell_rect, GRID_X, DAY_LABEL_W, CELL_SIZE, CELL_GAP, GRID_Y, HEADER_H
from src.ui.palette import Palette
from src.ui.timer import Timer
from src.ui.drag_drop import DragDrop
from src.ui.button import Button
from src.ui.toggle_switch import ToggleSwitch
from src.constants import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    GRID_ROWS,
    GRID_COLS,
    COLOR_BG,
    COLOR_WHITE,
    COLOR_HEADER_BG,
    COLOR_ACCENT_ORANGE,
    COLOR_COUNTER_TEXT,
    COLOR_TEXT_SUB,
    COLOR_HIGHLIGHT_RED,
    COLOR_HIGHLIGHT_BLUE,
    COLOR_HIGHLIGHT_ORANGE,
    COLOR_HIGHLIGHT_PURPLE,
    COLOR_BTN_BACK_BG,
    COLOR_BTN_BACK_TEXT,
    COLOR_BTN_RESET_BG,
    COLOR_BTN_RESET_TEXT,
    COLOR_BTN_DONE_BG,
    COLOR_BTN_DONE_TEXT,
    RULES,
)

# 違反種別→枠色のマッピング
_VIOLATION_COLORS = {
    "duplicate": COLOR_HIGHLIGHT_RED,
    "chirashi": COLOR_HIGHLIGHT_BLUE,
    "fried": COLOR_HIGHLIGHT_ORANGE,
    "curry": COLOR_HIGHLIGHT_PURPLE,
}

# 警告点滅の持続時間(フレーム数)
_FLASH_DURATION = 20


class PlayScreen:
    """ゲーム実行画面の統合。"""

    def __init__(self, assets: AssetManager) -> None:
        self.assets = assets
        self.board = Board()
        self.grid = Grid(assets)
        self.palette = Palette(assets)
        self.timer = Timer(assets)
        self.drag_drop = DragDrop(assets, self.board, self.palette)

        self._font_logo = assets.get_font(20)
        self._font_counter = assets.get_font(16)
        self._font_btn = assets.get_font(18)
        self._font_rule_title = assets.get_font(11)
        self._font_rule_desc = assets.get_font(10)
        self._font_rule_num = assets.get_font(10)
        self._font_emoji = None
        try:
            self._font_emoji = pygame.font.SysFont("segoeUIemoji", 20)
        except Exception:
            self._font_emoji = pygame.font.SysFont(None, 20)

        # フッターボタン
        btn_y = SCREEN_HEIGHT - 55
        btn_h = 42
        cx = SCREEN_WIDTH // 2
        self.btn_back = Button(
            rect=pygame.Rect(cx - 200, btn_y, 110, btn_h),
            text="もどる",
            font=self._font_btn,
            color=COLOR_BTN_BACK_BG,
            hover_color=(210, 212, 216),
            text_color=COLOR_BTN_BACK_TEXT,
            border_radius=8,
        )
        self.btn_reset = Button(
            rect=pygame.Rect(cx - 70, btn_y, 120, btn_h),
            text="リセット",
            font=self._font_btn,
            color=COLOR_BTN_RESET_BG,
            hover_color=(240, 185, 0),
            text_color=COLOR_BTN_RESET_TEXT,
            border_radius=8,
        )
        self.btn_done = Button(
            rect=pygame.Rect(cx + 70, btn_y, 130, btn_h),
            text="完了！",
            font=self._font_btn,
            color=COLOR_BTN_DONE_BG,
            hover_color=(220, 60, 0),
            text_color=COLOR_BTN_DONE_TEXT,
            border_radius=8,
        )

        # トグルスイッチ
        toggle_font = assets.get_font(14)
        self._bgm_toggle = ToggleSwitch(
            SCREEN_WIDTH - 220, 14, "BGM", toggle_font, initial=assets.bgm_enabled
        )
        self._sfx_toggle = ToggleSwitch(
            SCREEN_WIDTH - 110, 14, "SFX", toggle_font, initial=assets.sfx_enabled
        )

        self._locked = False
        self._flash_cells: dict[tuple[int, int], tuple[tuple[int, int, int], int]] = {}
        self._prev_violation_cells: set[tuple[int, int]] = set()
        self._answer: Board | None = None  # 模範解答キャッシュ

    def start(self) -> None:
        """ゲーム開始時にリセットし、模範解答を生成。"""
        self.board.reset()
        self.timer.start()
        self._locked = False
        self._flash_cells.clear()
        self._prev_violation_cells.clear()
        self._answer = generate_solution()

    @property
    def answer(self) -> Board | None:
        """模範解答（結果画面で使用）。"""
        return self._answer

    def handle_event(self, event: pygame.event.Event) -> str | None:
        """イベント処理。戻り値: 'done', 'back', 'timeout', None。"""
        bgm_state = self._bgm_toggle.handle_event(event)
        if bgm_state is not None:
            self.assets.set_bgm_enabled(bgm_state)
        sfx_state = self._sfx_toggle.handle_event(event)
        if sfx_state is not None:
            self.assets.set_sfx_enabled(sfx_state)

        if self._locked:
            return None

        # ボタン
        if self.btn_done.handle_event(event):
            self.assets.play_sound("button_click")
            self._locked = True
            return "done"
        if self.btn_back.handle_event(event):
            self.assets.play_sound("button_click")
            return "back"
        if self.btn_reset.handle_event(event):
            self.assets.play_sound("button_click")
            self.board.reset()
            return None

        # D&D
        result = self.drag_drop.handle_event(event)
        if result in ("placed", "moved", "removed"):
            if result != "removed":
                self.assets.play_sound("drop")
            self._check_realtime_warnings()

        return None

    def _check_realtime_warnings(self) -> None:
        """配置直後に違反をチェックし、新規違反セルを点滅させる。"""
        violations = check_all(self.board)
        current_cells: set[tuple[int, int]] = set()
        for v in violations.violations:
            color = _VIOLATION_COLORS.get(v.kind, COLOR_HIGHLIGHT_RED)
            for cell in v.cells:
                current_cells.add(cell)
                if cell not in self._prev_violation_cells:
                    self._flash_cells[cell] = (color, _FLASH_DURATION)

        if current_cells - self._prev_violation_cells:
            self.assets.play_sound("warning")

        self._prev_violation_cells = current_cells

    def update(self, dt_ms: int) -> str | None:
        """毎フレーム更新。タイムアウト時 'timeout' を返す。"""
        # 点滅カウンタ更新
        expired = []
        for cell, (color, frames) in self._flash_cells.items():
            self._flash_cells[cell] = (color, frames - 1)
            if frames - 1 <= 0:
                expired.append(cell)
        for cell in expired:
            del self._flash_cells[cell]

        if self._locked:
            return None
        if self.timer.update(dt_ms):
            self._locked = True
            return "timeout"
        return None

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(COLOR_BG)

        # ヘッダ
        self._draw_header(surface)

        # パレット
        self.palette.draw(surface)

        # グリッド
        self.grid.draw(surface, self.board)

        # 違反セル点滅ハイライト
        self._draw_flash_highlights(surface)

        # ルールパネル（グリッド右横）
        self._draw_rules_panel(surface)

        # フッター
        self._draw_footer(surface)

        # ドラッグ中のアイテム（最前面）
        self.drag_drop.draw_dragging(surface)

    def _draw_header(self, surface: pygame.Surface) -> None:
        header_rect = pygame.Rect(0, 0, SCREEN_WIDTH, 50)
        pygame.draw.rect(surface, COLOR_HEADER_BG, header_rect)
        pygame.draw.line(surface, (230, 230, 230), (0, 50), (SCREEN_WIDTH, 50))

        # ロゴ
        logo = self._font_logo.render("献立表パズル", True, COLOR_ACCENT_ORANGE)
        emoji = self._font_emoji.render("\U0001f371", True, (10, 10, 10))
        surface.blit(emoji, (15, 12))
        surface.blit(logo, (15 + emoji.get_width() + 6, 14))

        # タイマー
        self.timer.draw(surface, SCREEN_WIDTH // 2, 25)

        # 配置カウンター
        placed = GRID_ROWS * GRID_COLS - self.board.empty_count()
        total = GRID_ROWS * GRID_COLS
        counter_text = f"配置: {placed}/{total}"
        counter = self._font_counter.render(counter_text, True, COLOR_COUNTER_TEXT)
        surface.blit(counter, (SCREEN_WIDTH - counter.get_width() - 20, 32))

        # トグルスイッチ
        self._bgm_toggle.draw(surface)
        self._sfx_toggle.draw(surface)

    def _draw_flash_highlights(self, surface: pygame.Surface) -> None:
        """違反セルの点滅ハイライトを描画。"""
        for (r, c), (color, frames) in self._flash_cells.items():
            if frames % 4 < 2:  # 点滅効果
                continue
            rect = cell_rect(r, c)
            pygame.draw.rect(surface, color, rect, width=3, border_radius=8)

    def _draw_rules_panel(self, surface: pygame.Surface) -> None:
        """グリッド右横にルール（4つの約束）を描画。"""
        # グリッド右端の位置
        grid_right = GRID_X + DAY_LABEL_W + GRID_COLS * (CELL_SIZE + CELL_GAP)
        panel_x = grid_right + 12
        panel_y = GRID_Y + HEADER_H
        panel_w = SCREEN_WIDTH - panel_x - 12

        # 見出し
        heading = self._font_rule_title.render(
            "4つの約束", True, COLOR_ACCENT_ORANGE
        )
        surface.blit(heading, (panel_x + 4, panel_y))
        card_y = panel_y + heading.get_height() + 6

        # 利用可能な高さからカード高さを計算
        footer_top = SCREEN_HEIGHT - 65
        avail_h = footer_top - card_y - 8
        card_gap = 8
        card_h = (avail_h - card_gap * (len(RULES) - 1)) // len(RULES)

        for rule in RULES:
            self._draw_rule_card(surface, rule, panel_x, card_y, panel_w, card_h)
            card_y += card_h + card_gap

    def _draw_rule_card(
        self, surface: pygame.Surface, rule: dict,
        x: int, y: int, w: int, h: int
    ) -> None:
        """ルールカード1枚を描画。"""
        rect = pygame.Rect(x, y, w, h)
        pygame.draw.rect(surface, rule["bg"], rect, border_radius=8)

        pad = 8
        # 番号バッジ
        badge_size = 20
        badge_rect = pygame.Rect(x + pad, y + pad, badge_size, badge_size)
        pygame.draw.rect(surface, rule["color"], badge_rect, border_radius=10)
        num_surf = self._font_rule_num.render(str(rule["number"]), True, COLOR_WHITE)
        surface.blit(num_surf, num_surf.get_rect(center=badge_rect.center))

        # タイトル
        title_x = x + pad + badge_size + 6
        title_surf = self._font_rule_title.render(rule["title"], True, rule["color"])
        surface.blit(title_surf, (title_x, y + pad + 1))

        # 説明
        desc_surf = self._font_rule_desc.render(rule["desc"], True, COLOR_TEXT_SUB)
        surface.blit(desc_surf, (title_x, y + pad + title_surf.get_height() + 3))

    def _draw_footer(self, surface: pygame.Surface) -> None:
        footer_rect = pygame.Rect(0, SCREEN_HEIGHT - 65, SCREEN_WIDTH, 65)
        pygame.draw.rect(surface, COLOR_HEADER_BG, footer_rect)
        pygame.draw.line(surface, (230, 230, 230), (0, SCREEN_HEIGHT - 65), (SCREEN_WIDTH, SCREEN_HEIGHT - 65))

        self.btn_back.draw(surface)
        self.btn_reset.draw(surface)
        self.btn_done.draw(surface)
