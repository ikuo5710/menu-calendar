"""アセット管理: config.json 読込、欠損時プレースホルダ"""

from __future__ import annotations
import json
import os

import pygame


class AssetManager:
    """画像・音声・フォントの読み込みと管理。

    アセットが欠損してもゲームは継続する。
    """

    def __init__(self, config_path: str = "assets/config.json") -> None:
        self._config: dict = {}
        self._images: dict[str, pygame.Surface | None] = {}
        self._sounds: dict[str, pygame.mixer.Sound | None] = {}
        self._font_cache: dict[tuple[str | None, int], pygame.font.Font] = {}
        self._load_config(config_path)

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
        path = self._config.get("icons", {}).get(key, "")
        surf = None
        if path and os.path.isfile(path):
            try:
                surf = pygame.image.load(path).convert_alpha()
            except pygame.error:
                surf = None
        self._images[key] = surf
        return surf

    # --- 音声 ---

    def load_sound(self, key: str) -> pygame.mixer.Sound | None:
        if key in self._sounds:
            return self._sounds[key]
        path = self._config.get("sounds", {}).get(key, "")
        sound = None
        if path and os.path.isfile(path):
            try:
                sound = pygame.mixer.Sound(path)
            except pygame.error:
                sound = None
        self._sounds[key] = sound
        return sound

    def play_sound(self, key: str) -> None:
        sound = self.load_sound(key)
        if sound:
            sound.play()

    # --- フォント ---

    def get_font(self, size: int) -> pygame.font.Font:
        font_path = self._config.get("fonts", {}).get("main", "")
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
