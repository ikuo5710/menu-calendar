"""アセット管理: config.json 読込、欠損時プレースホルダ"""

from __future__ import annotations
import json
import os

import pygame


class AssetManager:
    """画像・音声・フォントの読み込みと管理。

    アセットが欠損してもゲームは継続する。
    """

    def __init__(self, base_path: str = "", config_path: str = "assets/config.json") -> None:
        self._base_path = base_path
        self._config: dict = {}
        self._images: dict[str, pygame.Surface | None] = {}
        self._sounds: dict[str, pygame.mixer.Sound | None] = {}
        self._font_cache: dict[tuple[str | None, int], pygame.font.Font] = {}
        self._bgm_enabled: bool = True
        self._sfx_enabled: bool = True
        self._current_bgm: str | None = None
        self._load_config(self._resolve(config_path))

    def _resolve(self, relative_path: str) -> str:
        """ベースパスからの相対パスを絶対パスに解決する。"""
        if not relative_path:
            return ""
        if self._base_path:
            return os.path.join(self._base_path, relative_path)
        return relative_path

    def _load_config(self, path: str) -> None:
        try:
            with open(path, encoding="utf-8") as f:
                self._config = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self._config = {}

    # --- 画像 ---

    def load_image(self, key: str) -> pygame.Surface | None:
        if key in self._images:
            return self._images[key]
        path = self._resolve(self._config.get("icons", {}).get(key, ""))
        surf = None
        if path and os.path.isfile(path):
            try:
                surf = pygame.image.load(path).convert_alpha()
            except pygame.error:
                surf = None
        self._images[key] = surf
        return surf

    def get_icon(self, key: str, size: tuple[int, int]) -> pygame.Surface | None:
        """アイコン画像を指定サイズにスケーリングして返す。キャッシュ付き。"""
        cache_key = (key, size)
        if cache_key in self._images:
            return self._images[cache_key]
        raw = self.load_image(key)
        if raw is None:
            self._images[cache_key] = None
            return None
        scaled = pygame.transform.smoothscale(raw, size)
        self._images[cache_key] = scaled
        return scaled

    # --- 音声 ---

    def load_sound(self, key: str) -> pygame.mixer.Sound | None:
        if key in self._sounds:
            return self._sounds[key]
        path = self._resolve(self._config.get("sounds", {}).get(key, ""))
        sound = None
        if path and os.path.isfile(path):
            try:
                sound = pygame.mixer.Sound(path)
            except pygame.error:
                sound = None
        self._sounds[key] = sound
        return sound

    def play_sound(self, key: str) -> None:
        if not self._sfx_enabled:
            return
        sound = self.load_sound(key)
        if sound:
            sound.play()

    # --- BGM ---

    def play_bgm(self, key: str) -> None:
        """BGMをループ再生する。同じ曲なら再読み込みしない。"""
        if key == self._current_bgm:
            return
        self._current_bgm = key
        path = self._resolve(self._config.get("bgm", {}).get(key, ""))
        if not path or not os.path.isfile(path):
            return
        try:
            pygame.mixer.music.load(path)
            if self._bgm_enabled:
                pygame.mixer.music.play(-1)
            else:
                pygame.mixer.music.play(-1)
                pygame.mixer.music.pause()
        except pygame.error:
            pass

    def stop_bgm(self) -> None:
        self._current_bgm = None
        try:
            pygame.mixer.music.stop()
        except pygame.error:
            pass

    def set_bgm_enabled(self, enabled: bool) -> None:
        self._bgm_enabled = enabled
        try:
            if enabled:
                pygame.mixer.music.unpause()
            else:
                pygame.mixer.music.pause()
        except pygame.error:
            pass

    def set_sfx_enabled(self, enabled: bool) -> None:
        self._sfx_enabled = enabled

    @property
    def bgm_enabled(self) -> bool:
        return self._bgm_enabled

    @property
    def sfx_enabled(self) -> bool:
        return self._sfx_enabled

    # --- フォント ---

    def get_font(self, size: int) -> pygame.font.Font:
        font_path = self._resolve(self._config.get("fonts", {}).get("main", ""))
        cache_key = (font_path, size)
        if cache_key in self._font_cache:
            return self._font_cache[cache_key]
        font = None
        if font_path and os.path.isfile(font_path):
            try:
                font = pygame.font.Font(font_path, size)
            except pygame.error:
                font = None
        if font is None:
            font = pygame.font.SysFont("meiryoui", size)
        self._font_cache[cache_key] = font
        return font
