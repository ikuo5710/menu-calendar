"""結果確認画面"""

from __future__ import annotations

import pygame

from src.asset_manager import AssetManager
from src.model.board import Board
from src.model.scoring import ScoreResult
from src.ui.button import Button
from src.ui.toggle_switch import ToggleSwitch
from src.constants import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
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
    COLOR_HEADER_BG,
    COLOR_BLOCK_LABEL,
    COLOR_DAY_LABEL_BG,
    COLOR_DAY_LABEL_TEXT,
    COLOR_CELL_EMPTY,
    COLOR_CELL_PLUS,
    COLOR_RESULT_TITLE,
    COLOR_RESULT_COMMENT,
    COLOR_RESULT_PLAYER_HEADING,
    COLOR_RESULT_ANSWER_HEADING,
    COLOR_RESULT_BONUS_BG,
    COLOR_RESULT_BONUS_TEXT,
    COLOR_RESULT_TROPHY,
    COLOR_SCORE_GRADIENT_START,
    COLOR_SCORE_GRADIENT_END,
    COLOR_HIGHLIGHT_RED,
    COLOR_HIGHLIGHT_BLUE,
    COLOR_HIGHLIGHT_ORANGE,
    COLOR_HIGHLIGHT_PURPLE,
)

# 違反種別→枠色
_VIOLATION_COLORS = {
    "duplicate": COLOR_HIGHLIGHT_RED,
    "chirashi": COLOR_HIGHLIGHT_BLUE,
    "fried": COLOR_HIGHLIGHT_ORANGE,
    "curry": COLOR_HIGHLIGHT_PURPLE,
}

# ミニグリッドレイアウト定数
_MINI_CELL = 72
_MINI_GAP = 3
_MINI_DAY_W = 45
_MINI_HEADER_H = 18


class ResultScreen:
    """結果確認画面。"""

    def __init__(self, assets: AssetManager) -> None:
        self.assets = assets
        self._font_title = assets.get_font(26)
        self._font_score = assets.get_font(36)
        self._font_score_unit = assets.get_font(12)
        self._font_comment = assets.get_font(16)
        self._font_bonus = assets.get_font(12)
        self._font_heading = assets.get_font(15)
        self._font_block = assets.get_font(9)
        self._font_day = assets.get_font(9)
        self._font_menu = assets.get_font(9)
        self._font_btn = assets.get_font(16)
        self._font_penalty = assets.get_font(11)
        self._font_emoji = None
        try:
            self._font_emoji = pygame.font.SysFont("segoeUIemoji", 18)
        except Exception:
            self._font_emoji = pygame.font.SysFont(None, 18)

        # トグルスイッチ
        toggle_font = assets.get_font(14)
        self._bgm_toggle = ToggleSwitch(
            SCREEN_WIDTH - 220, 8, "BGM", toggle_font, initial=assets.bgm_enabled
        )
        self._sfx_toggle = ToggleSwitch(
            SCREEN_WIDTH - 110, 8, "SFX", toggle_font, initial=assets.sfx_enabled
        )

        # フッターボタン
        btn_w, btn_h = 220, 44
        self.btn_return = Button(
            rect=pygame.Rect(
                (SCREEN_WIDTH - btn_w) // 2,
                SCREEN_HEIGHT - 60,
                btn_w,
                btn_h,
            ),
            text="スタートにもどる",
            font=self._font_btn,
            color=(255, 137, 4),
            hover_color=(230, 110, 0),
            text_color=COLOR_WHITE,
            border_radius=22,
        )

        self._player_board: Board | None = None
        self._answer_board: Board | None = None
        self._score_result: ScoreResult | None = None

    def set_result(
        self,
        player_board: Board,
        answer_board: Board | None,
        score_result: ScoreResult,
    ) -> None:
        """結果データを設定する。"""
        self._player_board = player_board
        self._answer_board = answer_board
        self._score_result = score_result

    def handle_event(self, event: pygame.event.Event) -> str | None:
        """イベント処理。'back' を返すとスタート画面へ。"""
        bgm_state = self._bgm_toggle.handle_event(event)
        if bgm_state is not None:
            self.assets.set_bgm_enabled(bgm_state)
        sfx_state = self._sfx_toggle.handle_event(event)
        if sfx_state is not None:
            self.assets.set_sfx_enabled(sfx_state)

        if self.btn_return.handle_event(event):
            self.assets.play_sound("button_click")
            return "back"
        return None

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(COLOR_WHITE)

        if self._score_result is None:
            return

        # トグルスイッチ（最前面に描画するため先にヘッダ）
        # ヘッダ（スコア領域）
        self._draw_header(surface)

        # トグルスイッチ（他画面での変更を反映）
        self._bgm_toggle.enabled = self.assets.bgm_enabled
        self._sfx_toggle.enabled = self.assets.sfx_enabled
        self._bgm_toggle.draw(surface)
        self._sfx_toggle.draw(surface)

        # ボディ（2パネル）
        self._draw_body(surface)

        # フッター
        self._draw_footer(surface)

    # ---- ヘッダ: スコア表示 ----

    def _header_height(self) -> int:
        """ヘッダの必要高さを計算する。"""
        sr = self._score_result
        # タイトル(8) + タイトル高さ(~30) + スコア円(直径80) + コメント(~20) + 余白
        h = 8 + 30 + 80 + 6 + 20 + 16
        if sr and sr.bonus > 0:
            h += 30  # ボーナスバッジ分 + 下マージン
        return h

    def _draw_header(self, surface: pygame.Surface) -> None:
        sr = self._score_result
        header_h = self._header_height()
        header_rect = pygame.Rect(0, 0, SCREEN_WIDTH, header_h)
        pygame.draw.rect(surface, COLOR_HEADER_BG, header_rect)
        pygame.draw.line(
            surface, (230, 230, 230), (0, header_h), (SCREEN_WIDTH, header_h)
        )

        cx = SCREEN_WIDTH // 2

        # タイトル "けっか発表！"
        title = self._font_title.render("けっか発表！", True, COLOR_RESULT_TITLE)
        title_rect = title.get_rect(centerx=cx, top=8)
        # トロフィーアイコン（テキストで代用）
        trophy = self._font_title.render("★", True, COLOR_RESULT_TROPHY)
        surface.blit(trophy, (title_rect.left - trophy.get_width() - 8, title_rect.top))
        surface.blit(title, title_rect)
        surface.blit(
            trophy, (title_rect.right + 8, title_rect.top)
        )

        # スコア円
        circle_r = 40
        circle_cx = cx
        circle_cy = title_rect.bottom + 6 + circle_r
        self._draw_score_circle(surface, circle_cx, circle_cy, circle_r, sr.score)

        # コメント
        comment = self._font_comment.render(sr.comment, True, COLOR_RESULT_COMMENT)
        comment_rect = comment.get_rect(centerx=cx, top=circle_cy + circle_r + 6)
        surface.blit(comment, comment_rect)

        # ボーナスバッジ
        if sr.bonus > 0:
            badge_text = f"早解きボーナス: +{sr.bonus}点"
            badge_surf = self._font_bonus.render(badge_text, True, COLOR_RESULT_BONUS_TEXT)
            bw = badge_surf.get_width() + 20
            bh = 22
            badge_rect = pygame.Rect(cx - bw // 2, comment_rect.bottom + 4, bw, bh)
            pygame.draw.rect(surface, COLOR_RESULT_BONUS_BG, badge_rect, border_radius=11)
            surface.blit(
                badge_surf,
                badge_surf.get_rect(center=badge_rect.center),
            )

    def _draw_score_circle(
        self, surface: pygame.Surface, cx: int, cy: int, r: int, score: int
    ) -> None:
        """グラデーション風スコア円を描画。"""
        # 単色で代用（pygame にはネイティブグラデーションなし）
        # 上から下に色を遷移させる簡易グラデーション
        for dy in range(-r, r + 1):
            t = (dy + r) / (2 * r) if r > 0 else 0
            color = tuple(
                int(COLOR_SCORE_GRADIENT_START[i] * (1 - t) + COLOR_SCORE_GRADIENT_END[i] * t)
                for i in range(3)
            )
            # 円の水平方向のスパン
            import math

            dx = int(math.sqrt(max(0, r * r - dy * dy)))
            if dx > 0:
                pygame.draw.line(surface, color, (cx - dx, cy + dy), (cx + dx, cy + dy))

        # スコア数字
        score_text = self._font_score.render(str(score), True, COLOR_WHITE)
        score_rect = score_text.get_rect(centerx=cx, centery=cy - 4)
        surface.blit(score_text, score_rect)

        # "てん"
        unit = self._font_score_unit.render("てん", True, (255, 255, 255, 200))
        unit_rect = unit.get_rect(centerx=cx, top=score_rect.bottom - 2)
        surface.blit(unit, unit_rect)

    # ---- ボディ: 2パネル ----

    def _draw_body(self, surface: pygame.Surface) -> None:
        body_top = self._header_height() + 5
        body_h = SCREEN_HEIGHT - body_top - 70
        panel_gap = 16
        panel_pad = 16
        panel_w = (SCREEN_WIDTH - panel_gap * 3) // 2

        # 左パネル: プレイヤーの献立表
        left_x = panel_pad
        self._draw_panel(
            surface,
            pygame.Rect(left_x, body_top, panel_w, body_h),
            "あなたの献立表",
            COLOR_RESULT_PLAYER_HEADING,
            self._player_board,
            show_violations=True,
        )

        # 右パネル: 模範解答
        right_x = left_x + panel_w + panel_gap
        self._draw_panel(
            surface,
            pygame.Rect(right_x, body_top, panel_w, body_h),
            "模範解答（コンピュータの回答）",
            COLOR_RESULT_ANSWER_HEADING,
            self._answer_board,
            show_violations=False,
        )

    def _draw_panel(
        self,
        surface: pygame.Surface,
        panel_rect: pygame.Rect,
        heading: str,
        heading_color: tuple[int, int, int],
        board: Board | None,
        show_violations: bool,
    ) -> None:
        # パネル背景
        pygame.draw.rect(surface, COLOR_WHITE, panel_rect, border_radius=12)
        pygame.draw.rect(surface, (230, 230, 230), panel_rect, width=1, border_radius=12)

        pad = 12
        inner_x = panel_rect.x + pad
        inner_y = panel_rect.y + pad

        # 見出し（中央揃え）
        heading_surf = self._font_heading.render(heading, True, heading_color)
        heading_rect = heading_surf.get_rect(centerx=panel_rect.centerx, top=inner_y)
        surface.blit(heading_surf, heading_rect)
        grid_top = inner_y + heading_surf.get_height() + 8

        if board is None:
            na = self._font_comment.render("データなし", True, (150, 150, 150))
            surface.blit(na, na.get_rect(center=panel_rect.center))
            return

        # ミニグリッド描画
        grid_y = grid_top
        avail_w = panel_rect.width - pad * 2
        avail_h = panel_rect.height - pad - (grid_top - panel_rect.y)

        # セルサイズを利用可能な領域に合わせて計算
        cell_w = (avail_w - _MINI_DAY_W - _MINI_GAP * (GRID_COLS - 1)) // GRID_COLS
        cell_h = (avail_h - _MINI_HEADER_H - _MINI_GAP * (GRID_ROWS - 1)) // GRID_ROWS
        cell = min(cell_w, cell_h, _MINI_CELL)

        # グリッド全体幅を計算し、パネル内で中央揃え
        grid_total_w = _MINI_DAY_W + GRID_COLS * cell + (GRID_COLS - 1) * _MINI_GAP
        grid_x = panel_rect.x + (panel_rect.width - grid_total_w) // 2

        self._draw_mini_grid(surface, grid_x, grid_y, cell, board, show_violations)

        # 違反一覧（左パネルのグリッド下部）
        if show_violations and self._score_result:
            penalty_y = grid_y + _MINI_HEADER_H + GRID_ROWS * (cell + _MINI_GAP) + 4
            self._draw_penalty_summary(surface, grid_x, penalty_y, avail_w)

    def _draw_mini_grid(
        self,
        surface: pygame.Surface,
        gx: int,
        gy: int,
        cell: int,
        board: Board,
        show_violations: bool,
    ) -> None:
        """ミニサイズの5×5グリッドを描画する。"""
        # ブロックヘッダ
        for c in range(GRID_COLS):
            cx = gx + _MINI_DAY_W + c * (cell + _MINI_GAP) + cell // 2
            label = self._font_block.render(BLOCK_LABELS[c], True, COLOR_BLOCK_LABEL)
            lr = label.get_rect(centerx=cx, top=gy)
            surface.blit(label, lr)

        cells_top = gy + _MINI_HEADER_H

        # 違反セル集合
        violation_cells: dict[tuple[int, int], tuple[int, int, int]] = {}
        if show_violations and self._score_result and self._score_result.violations:
            for v in self._score_result.violations.violations:
                color = _VIOLATION_COLORS.get(v.kind, COLOR_HIGHLIGHT_RED)
                for cell_pos in v.cells:
                    violation_cells[cell_pos] = color

        for r in range(GRID_ROWS):
            ry = cells_top + r * (cell + _MINI_GAP)

            # 曜日ラベル
            day_rect = pygame.Rect(gx, ry, _MINI_DAY_W - 4, cell)
            pygame.draw.rect(surface, COLOR_DAY_LABEL_BG, day_rect, border_radius=3)
            day_label = self._font_day.render(DAY_LABELS[r], True, COLOR_DAY_LABEL_TEXT)
            surface.blit(day_label, day_label.get_rect(center=day_rect.center))

            for c in range(GRID_COLS):
                rx = gx + _MINI_DAY_W + c * (cell + _MINI_GAP)
                rect = pygame.Rect(rx, ry, cell, cell)
                menu_id = board.get(r, c)

                if menu_id is None:
                    # 空セル
                    pygame.draw.rect(surface, COLOR_CELL_EMPTY, rect, border_radius=6)
                    q = self._font_menu.render("？", True, COLOR_CELL_PLUS)
                    surface.blit(q, q.get_rect(center=rect.center))
                else:
                    bg = MENU_BG_COLORS.get(menu_id, COLOR_CELL_EMPTY)
                    pygame.draw.rect(surface, bg, rect, border_radius=6)

                    # アイコン画像（欠損時は絵文字フォールバック）
                    icon_key = MENU_ICON_KEYS.get(menu_id)
                    icon_sz = max(cell // 2, 24)
                    icon = self.assets.get_icon(icon_key, (icon_sz, icon_sz)) if icon_key else None

                    if icon is not None:
                        img_rect = icon.get_rect(
                            centerx=rect.centerx, centery=rect.centery - 6
                        )
                        surface.blit(icon, img_rect)
                    else:
                        emoji_text = MENU_EMOJI.get(menu_id, "?")
                        emoji_surf = self._font_emoji.render(emoji_text, True, (10, 10, 10))
                        img_rect = emoji_surf.get_rect(
                            centerx=rect.centerx, centery=rect.centery - 6
                        )
                        surface.blit(emoji_surf, img_rect)

                    # メニュー名
                    name = MENU_NAMES.get(menu_id, "?")
                    text_color = MENU_COLORS.get(menu_id, (10, 10, 10))
                    name_surf = self._font_menu.render(name, True, text_color)
                    name_rect = name_surf.get_rect(
                        centerx=rect.centerx, top=img_rect.bottom + 1
                    )
                    surface.blit(name_surf, name_rect)

                # 違反ハイライト枠
                if show_violations and (r, c) in violation_cells:
                    v_color = violation_cells[(r, c)]
                    pygame.draw.rect(surface, v_color, rect, width=3, border_radius=6)

    def _draw_penalty_summary(
        self, surface: pygame.Surface, x: int, y: int, w: int
    ) -> None:
        """減点内訳をコンパクトに表示。"""
        sr = self._score_result
        if not sr or not sr.penalties:
            return

        cur_y = y
        for p in sr.penalties:
            # 違反種別の色マーカー
            kind_color = COLOR_HIGHLIGHT_RED
            if "ちらし" in p.label:
                kind_color = COLOR_HIGHLIGHT_BLUE
            elif "揚げ物" in p.label:
                kind_color = COLOR_HIGHLIGHT_ORANGE
            elif "カレー" in p.label:
                kind_color = COLOR_HIGHLIGHT_PURPLE

            marker_rect = pygame.Rect(x, cur_y + 3, 8, 8)
            pygame.draw.rect(surface, kind_color, marker_rect, border_radius=2)

            text = f"{p.label}: {p.count}件 (-{p.total}点)"
            text_surf = self._font_penalty.render(text, True, COLOR_RESULT_COMMENT)
            surface.blit(text_surf, (x + 14, cur_y))
            cur_y += text_surf.get_height() + 3

    # ---- フッター ----

    def _draw_footer(self, surface: pygame.Surface) -> None:
        footer_h = 65
        footer_rect = pygame.Rect(0, SCREEN_HEIGHT - footer_h, SCREEN_WIDTH, footer_h)
        pygame.draw.rect(surface, COLOR_HEADER_BG, footer_rect)
        pygame.draw.line(
            surface,
            (230, 230, 230),
            (0, SCREEN_HEIGHT - footer_h),
            (SCREEN_WIDTH, SCREEN_HEIGHT - footer_h),
        )
        self.btn_return.draw(surface)
