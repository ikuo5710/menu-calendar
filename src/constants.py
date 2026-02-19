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

# --- 色（Figmaデザイン準拠） ---
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (10, 10, 10)
COLOR_GRAY = (200, 200, 200)
COLOR_LIGHT_GRAY = (230, 230, 230)
COLOR_BG = (255, 255, 255)
COLOR_GRID_BG = (255, 255, 255)
COLOR_GRID_LINE = (180, 180, 180)
COLOR_TEXT_MAIN = (10, 10, 10)
COLOR_TEXT_SUB = (106, 114, 130)
COLOR_ACCENT_ORANGE = (245, 73, 0)       # タイトル・揚げ物バッジ
COLOR_ACCENT_SUB = (255, 105, 0)         # サブタイトル
COLOR_HIGHLIGHT_RED = (239, 68, 68)      # ルール1: ブロック内重複
COLOR_HIGHLIGHT_BLUE = (59, 130, 246)    # ルール2: ちらし寿司超過
COLOR_HIGHLIGHT_ORANGE = (249, 115, 22)  # ルール3: 揚げ物超過
COLOR_HIGHLIGHT_PURPLE = (139, 92, 246)  # ルール4: カレー連続
COLOR_EMPTY_BG = (220, 220, 220)         # 空欄

# ルールカード背景色（Figma準拠）
COLOR_RULE_BG = {
    1: (254, 242, 242),  # 赤系
    2: (239, 246, 255),  # 青系
    3: (255, 247, 237),  # オレンジ系
    4: (245, 243, 255),  # 紫系
}

# メニューごとの表示色・背景色（Figma準拠）
MENU_COLORS = {
    MENU_KARAAGE: (217, 119, 6),
    MENU_EBI_FRY: (234, 88, 12),
    MENU_CURRY_UDON: (202, 138, 4),
    MENU_CURRY_RICE: (101, 163, 13),
    MENU_CHIRASHI: (219, 39, 119),
}

MENU_BG_COLORS = {
    MENU_KARAAGE: (254, 243, 199),
    MENU_EBI_FRY: (255, 247, 237),
    MENU_CURRY_UDON: (254, 252, 232),
    MENU_CURRY_RICE: (247, 254, 231),
    MENU_CHIRASHI: (253, 242, 248),
}

# メニュー絵文字
MENU_EMOJI = {
    MENU_KARAAGE: "\U0001f357",     # 🍗
    MENU_EBI_FRY: "\U0001f364",     # 🍤
    MENU_CURRY_UDON: "\U0001f35c",  # 🍜
    MENU_CURRY_RICE: "\U0001f35b",  # 🍛
    MENU_CHIRASHI: "\U0001f363",    # 🍣
}

# ボタン色
COLOR_BUTTON_START = (245, 73, 0)
COLOR_BUTTON_START_HOVER = (220, 60, 0)
COLOR_BUTTON_TEXT = (255, 255, 255)

# --- フォント ---
FONT_SIZE_TITLE = 48
FONT_SIZE_LARGE = 32
FONT_SIZE_MEDIUM = 24
FONT_SIZE_SMALL = 18

# --- 日・ブロックラベル ---
DAY_LABELS = ["月曜日", "火曜日", "水曜日", "木曜日", "金曜日"]
BLOCK_LABELS = ["Aブロック", "Bブロック", "Cブロック", "Dブロック", "Eブロック"]

# --- ゲーム実行画面色（Figma準拠） ---
COLOR_HEADER_BG = (255, 255, 255)
COLOR_BLOCK_LABEL = (152, 16, 250)     # ブロックヘッダ紫
COLOR_DAY_LABEL_BG = (239, 246, 255)   # 曜日ラベル背景
COLOR_DAY_LABEL_TEXT = (21, 93, 252)   # 曜日ラベル文字
COLOR_CELL_EMPTY = (249, 250, 251)     # 空セル背景
COLOR_CELL_PLUS = (209, 213, 220)      # 空セル「＋」
COLOR_TIMER_TEXT = (54, 65, 83)        # タイマー文字
COLOR_COUNTER_TEXT = (106, 114, 130)   # カウンター文字

# ボタン色（ゲーム画面）
COLOR_BTN_BACK_BG = (229, 231, 235)
COLOR_BTN_BACK_TEXT = (74, 85, 101)
COLOR_BTN_RESET_BG = (253, 199, 0)
COLOR_BTN_RESET_TEXT = (115, 62, 10)
COLOR_BTN_DONE_BG = (245, 73, 0)
COLOR_BTN_DONE_TEXT = (255, 255, 255)

# --- 結果確認画面色（Figma準拠） ---
COLOR_RESULT_TITLE = (245, 73, 0)          # "けっか発表！"
COLOR_RESULT_COMMENT = (54, 65, 83)        # 講評コメント
COLOR_RESULT_PLAYER_HEADING = (21, 93, 252)   # "あなたの献立表" 青
COLOR_RESULT_ANSWER_HEADING = (0, 166, 62)    # "模範解答" 緑
COLOR_RESULT_BONUS_BG = (240, 253, 244)       # ボーナスバッジ背景
COLOR_RESULT_BONUS_TEXT = (0, 166, 62)        # ボーナスバッジ文字
COLOR_RESULT_TROPHY = (240, 177, 0)           # トロフィーアイコン
COLOR_SCORE_GRADIENT_START = (255, 223, 32)   # スコア円グラデ開始
COLOR_SCORE_GRADIENT_END = (255, 137, 4)      # スコア円グラデ終了
COLOR_BTN_RETURN_START = (255, 137, 4)        # 戻るボタングラデ開始
COLOR_BTN_RETURN_END = (246, 51, 154)         # 戻るボタングラデ終了
