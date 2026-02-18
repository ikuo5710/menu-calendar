"""ゲーム全体の定数定義"""

# --- 画面 ---
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
TITLE = "献立表カレンダー作成ゲーム"

# --- グリッド ---
GRID_ROWS = 5  # 日数
GRID_COLS = 5  # ブロック数

# --- タイマー ---
TIMER_SECONDS = 180

# --- メニューID ---
MENU_KARAAGE = 0      # からあげ（揚げ物）
MENU_EBI_FRY = 1      # エビフライ（揚げ物）
MENU_CURRY_UDON = 2   # カレーうどん
MENU_CURRY_RICE = 3   # カレーライス
MENU_CHIRASHI = 4     # ちらし寿司

MENU_COUNT = 5

# メニュー名称
MENU_NAMES = {
    MENU_KARAAGE: "からあげ",
    MENU_EBI_FRY: "エビフライ",
    MENU_CURRY_UDON: "カレーうどん",
    MENU_CURRY_RICE: "カレーライス",
    MENU_CHIRASHI: "ちらし寿司",
}

# カテゴリ: 揚げ物
FRIED_FOODS = {MENU_KARAAGE, MENU_EBI_FRY}

# カレー系
CURRY_MENUS = {MENU_CURRY_UDON, MENU_CURRY_RICE}

# --- 制約上限 ---
CHIRASHI_PER_ROW_MAX = 1
FRIED_PER_ROW_MAX = 3

# --- 採点 ---
PENALTY_EMPTY = 3
PENALTY_BLOCK_DUPLICATE = 8
PENALTY_CHIRASHI_EXCESS = 10
PENALTY_FRIED_EXCESS = 6
PENALTY_CURRY_CONSECUTIVE = 10

BONUS_EARLY_120 = 5   # 残り120秒以上
BONUS_EARLY_60 = 3    # 残り60秒以上

# --- 色 ---
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_GRAY = (200, 200, 200)
COLOR_LIGHT_GRAY = (230, 230, 230)
COLOR_BG = (255, 248, 230)        # 温かみのある背景
COLOR_GRID_BG = (255, 255, 255)
COLOR_GRID_LINE = (180, 180, 180)
COLOR_HIGHLIGHT_RED = (255, 80, 80)       # ブロック内重複
COLOR_HIGHLIGHT_BLUE = (80, 120, 255)     # ちらし寿司超過
COLOR_HIGHLIGHT_ORANGE = (255, 165, 0)    # 揚げ物超過
COLOR_HIGHLIGHT_PURPLE = (160, 80, 200)   # カレー連続
COLOR_EMPTY_BG = (220, 220, 220)          # 空欄

# メニューごとの表示色（アイコン未使用時のプレースホルダ）
MENU_COLORS = {
    MENU_KARAAGE: (210, 160, 60),
    MENU_EBI_FRY: (230, 120, 80),
    MENU_CURRY_UDON: (200, 180, 50),
    MENU_CURRY_RICE: (180, 130, 30),
    MENU_CHIRASHI: (240, 100, 120),
}

# --- フォント ---
FONT_SIZE_TITLE = 48
FONT_SIZE_LARGE = 32
FONT_SIZE_MEDIUM = 24
FONT_SIZE_SMALL = 18

# --- 日・ブロックラベル ---
DAY_LABELS = ["月曜日", "火曜日", "水曜日", "木曜日", "金曜日"]
BLOCK_LABELS = ["1ブロック", "2ブロック", "3ブロック", "4ブロック", "5ブロック"]
