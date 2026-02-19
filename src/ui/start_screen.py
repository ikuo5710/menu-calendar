"""スタート画面"""

from __future__ import annotations

import pygame

from src.asset_manager import AssetManager
from src.ui.button import Button
from src.constants import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    COLOR_BG,
    COLOR_ACCENT_ORANGE,
    COLOR_ACCENT_SUB,
    COLOR_TEXT_SUB,
    COLOR_WHITE,
    COLOR_HIGHLIGHT_RED,
    COLOR_HIGHLIGHT_BLUE,
    COLOR_HIGHLIGHT_ORANGE,
    COLOR_HIGHLIGHT_PURPLE,
    COLOR_RULE_BG,
    COLOR_BUTTON_START,
    COLOR_BUTTON_START_HOVER,
    COLOR_BUTTON_TEXT,
    MENU_NAMES,
    MENU_EMOJI,
    MENU_COLORS,
    MENU_BG_COLORS,
    MENU_KARAAGE,
    MENU_EBI_FRY,
    MENU_CURRY_UDON,
    MENU_CURRY_RICE,
    MENU_CHIRASHI,
    FRIED_FOODS,
    FONT_SIZE_TITLE,
    FONT_SIZE_LARGE,
    FONT_SIZE_MEDIUM,
    FONT_SIZE_SMALL,
)

# ルール定義
RULES = [
    {
        "number": 1,
        "color": COLOR_HIGHLIGHT_RED,
        "bg": COLOR_RULE_BG[1],
        "title": "同じブロック（列）に同じメニューは1回だけ！",
        "desc": "各ブロック内で同じ献立が重複しないようにしよう",
    },
    {
        "number": 2,
        "color": COLOR_HIGHLIGHT_BLUE,
        "bg": COLOR_RULE_BG[2],
        "title": "ちらし寿司は1日1ブロックまで！",
        "desc": "同じ日（行）でちらし寿司は最大1つ",
    },
    {
        "number": 3,
        "color": COLOR_HIGHLIGHT_ORANGE,
        "bg": COLOR_RULE_BG[3],
        "title": "揚げ物は1日3ブロックまで！",
        "desc": "同じ日でからあげ・エビフライの合計は最大3つ",
    },
    {
        "number": 4,
        "color": COLOR_HIGHLIGHT_PURPLE,
        "bg": COLOR_RULE_BG[4],
        "title": "カレー2種の連続禁止！",
        "desc": "同じブロックで連続する日にカレーうどん↔カレーライスはNG",
    },
]


class StartScreen:
    """スタート画面の描画とイベント処理。"""

    def __init__(self, assets: AssetManager) -> None:
        self.assets = assets
        self._start_clicked = False

        # フォント
        self._font_title = assets.get_font(40)
        self._font_large = assets.get_font(28)
        self._font_medium = assets.get_font(20)
        self._font_small = assets.get_font(16)
        self._font_emoji = self._load_emoji_font(36)
        self._font_emoji_small = self._load_emoji_font(20)

        # スタートボタン
        btn_w, btn_h = 280, 56
        btn_x = (SCREEN_WIDTH - btn_w) // 2
        btn_y = SCREEN_HEIGHT - 75
        self.start_button = Button(
            rect=pygame.Rect(btn_x, btn_y, btn_w, btn_h),
            text="ゲームスタート！",
            font=self._font_large,
            color=COLOR_BUTTON_START,
            hover_color=COLOR_BUTTON_START_HOVER,
            text_color=COLOR_BUTTON_TEXT,
            border_radius=16,
        )

    @staticmethod
    def _load_emoji_font(size: int) -> pygame.font.Font:
        """絵文字表示用フォントを読み込む。"""
        try:
            return pygame.font.SysFont("segoeUIemoji", size)
        except Exception:
            return pygame.font.SysFont(None, size)

    def handle_event(self, event: pygame.event.Event) -> bool:
        """イベント処理。スタートボタンが押されたら True を返す。"""
        if self.start_button.handle_event(event):
            self.assets.play_sound("button_click")
            return True
        return False

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(COLOR_BG)

        cx = SCREEN_WIDTH // 2
        y = 12

        # --- タイトルエリア ---
        y = self._draw_title(surface, cx, y)

        # --- メニュー紹介エリア ---
        y = self._draw_menu_section(surface, cx, y + 10)

        # --- ルールエリア ---
        y = self._draw_rules_section(surface, cx, y + 10)

        # --- フッター情報 ---
        self._draw_footer_info(surface, cx)

        # --- スタートボタン ---
        self.start_button.draw(surface)

    def _draw_title(self, surface: pygame.Surface, cx: int, y: int) -> int:
        title_text = "献立表パズル"
        title_surf = self._font_title.render(title_text, True, COLOR_ACCENT_ORANGE)
        emoji_surf = self._font_emoji.render("\U0001f371", True, (10, 10, 10))

        gap = 10
        total_w = emoji_surf.get_width() + gap + title_surf.get_width() + gap + emoji_surf.get_width()
        start_x = cx - total_w // 2
        title_y = y + (emoji_surf.get_height() - title_surf.get_height()) // 2

        surface.blit(emoji_surf, (start_x, y))
        surface.blit(title_surf, (start_x + emoji_surf.get_width() + gap, title_y))
        surface.blit(emoji_surf, (start_x + total_w - emoji_surf.get_width(), y))

        y += max(title_surf.get_height(), emoji_surf.get_height()) + 4

        sub_text = "制限時間内に、ルールを守って献立表を完成させよう！"
        sub_surf = self._font_medium.render(sub_text, True, COLOR_ACCENT_SUB)
        sub_rect = sub_surf.get_rect(centerx=cx, top=y)
        surface.blit(sub_surf, sub_rect)

        return sub_rect.bottom

    def _draw_menu_section(self, surface: pygame.Surface, cx: int, y: int) -> int:
        section_w = 576
        section_x = cx - section_w // 2

        section_rect = pygame.Rect(section_x, y, section_w, 140)
        pygame.draw.rect(surface, COLOR_WHITE, section_rect, border_radius=12)
        pygame.draw.rect(surface, (230, 230, 230), section_rect, width=1, border_radius=12)

        heading = self._font_medium.render("使えるメニュー（5種類）", True, COLOR_ACCENT_ORANGE)
        heading_rect = heading.get_rect(centerx=cx, top=y + 10)
        surface.blit(heading, heading_rect)

        menus_row1 = [MENU_KARAAGE, MENU_EBI_FRY]
        menus_row2 = [MENU_CURRY_UDON, MENU_CURRY_RICE, MENU_CHIRASHI]

        card_y = y + 40
        self._draw_menu_row(surface, menus_row1, cx, card_y)
        card_y += 50
        self._draw_menu_row(surface, menus_row2, cx, card_y)

        return section_rect.bottom

    def _draw_menu_row(self, surface: pygame.Surface, menu_ids: list[int], cx: int, y: int) -> None:
        card_w = 160
        card_h = 42
        gap = 10
        total_w = len(menu_ids) * card_w + (len(menu_ids) - 1) * gap
        start_x = cx - total_w // 2

        for i, mid in enumerate(menu_ids):
            x = start_x + i * (card_w + gap)
            bg_color = MENU_BG_COLORS[mid]
            text_color = MENU_COLORS[mid]
            rect = pygame.Rect(x, y, card_w, card_h)
            pygame.draw.rect(surface, bg_color, rect, border_radius=8)

            emoji = MENU_EMOJI[mid]
            name = MENU_NAMES[mid]
            emoji_surf = self._font_emoji_small.render(emoji, True, (10, 10, 10))
            name_surf = self._font_small.render(name, True, text_color)

            content_w = emoji_surf.get_width() + 4 + name_surf.get_width()
            badge_surf = None
            if mid in FRIED_FOODS:
                badge_surf = self._font_small.render("揚げ物", True, COLOR_WHITE)
                content_w += 4 + badge_surf.get_width() + 10

            content_x = x + (card_w - content_w) // 2
            emoji_y = y + (card_h - emoji_surf.get_height()) // 2
            name_y = y + (card_h - name_surf.get_height()) // 2

            surface.blit(emoji_surf, (content_x, emoji_y))
            surface.blit(name_surf, (content_x + emoji_surf.get_width() + 4, name_y))

            if badge_surf:
                badge_x = content_x + emoji_surf.get_width() + 4 + name_surf.get_width() + 4
                badge_rect = pygame.Rect(
                    badge_x, y + (card_h - 20) // 2, badge_surf.get_width() + 10, 20
                )
                pygame.draw.rect(surface, COLOR_ACCENT_SUB, badge_rect, border_radius=4)
                surface.blit(badge_surf, (badge_x + 5, y + (card_h - badge_surf.get_height()) // 2))

    def _draw_rules_section(self, surface: pygame.Surface, cx: int, y: int) -> int:
        section_w = 576
        section_x = cx - section_w // 2
        card_h = 56
        card_gap = 6
        section_h = 38 + len(RULES) * card_h + (len(RULES) - 1) * card_gap + 12

        section_rect = pygame.Rect(section_x, y, section_w, section_h)
        pygame.draw.rect(surface, COLOR_WHITE, section_rect, border_radius=12)
        pygame.draw.rect(surface, (230, 230, 230), section_rect, width=1, border_radius=12)

        heading = self._font_medium.render("ルール（4つの約束）", True, (230, 0, 118))
        heading_rect = heading.get_rect(centerx=cx, top=y + 10)
        surface.blit(heading, heading_rect)

        card_y = y + 38
        for rule in RULES:
            self._draw_rule_card(surface, rule, section_x + 14, card_y, section_w - 28, card_h)
            card_y += card_h + card_gap

        return section_rect.bottom

    def _draw_rule_card(
        self, surface: pygame.Surface, rule: dict, x: int, y: int, w: int, h: int
    ) -> None:
        rect = pygame.Rect(x, y, w, h)
        pygame.draw.rect(surface, rule["bg"], rect, border_radius=8)

        badge_size = 24
        badge_rect = pygame.Rect(x + 10, y + (h - badge_size) // 2, badge_size, badge_size)
        pygame.draw.rect(surface, rule["color"], badge_rect, border_radius=12)
        num_surf = self._font_small.render(str(rule["number"]), True, COLOR_WHITE)
        num_rect = num_surf.get_rect(center=badge_rect.center)
        surface.blit(num_surf, num_rect)

        title_surf = self._font_small.render(rule["title"], True, rule["color"])
        surface.blit(title_surf, (x + 44, y + 8))

        desc_font = self.assets.get_font(14)
        desc_surf = desc_font.render(rule["desc"], True, COLOR_TEXT_SUB)
        surface.blit(desc_surf, (x + 44, y + 30))

    def _draw_footer_info(self, surface: pygame.Surface, cx: int) -> None:
        y = self.start_button.rect.top - 28
        info_text = "制限時間 3:00  |  早く完成すると ボーナス点"
        info_surf = self._font_small.render(info_text, True, COLOR_TEXT_SUB)
        info_rect = info_surf.get_rect(centerx=cx, top=y)
        surface.blit(info_surf, info_rect)
