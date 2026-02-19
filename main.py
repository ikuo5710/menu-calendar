"""献立表カレンダー作成ゲーム - エントリポイント"""

import sys
import pygame
from src.constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, TITLE
from src.game import GameManager, GameState
from src.asset_manager import AssetManager
from src.ui.start_screen import StartScreen
from src.ui.play_screen import PlayScreen


def main():
    pygame.init()
    try:
        pygame.mixer.init()
    except pygame.error:
        pass

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()

    assets = AssetManager()
    game = GameManager()
    start_screen = StartScreen(assets)
    play_screen = PlayScreen(assets)

    running = True
    while running:
        dt_ms = clock.get_time()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                continue

            if game.state == GameState.START:
                if start_screen.handle_event(event):
                    play_screen.start()
                    game.go_to_playing()
            elif game.state == GameState.PLAYING:
                result = play_screen.handle_event(event)
                if result == "done" or result == "timeout":
                    game.go_to_result()
                elif result == "back":
                    game.go_to_start()
            elif game.state == GameState.RESULT:
                # Phase 6 で実装
                pass

        # --- 更新 ---
        if game.state == GameState.PLAYING:
            result = play_screen.update(dt_ms)
            if result == "timeout":
                game.go_to_result()

        # --- 描画 ---
        if game.state == GameState.START:
            start_screen.draw(screen)
        elif game.state == GameState.PLAYING:
            play_screen.draw(screen)
        elif game.state == GameState.RESULT:
            # Phase 6 で実装（仮: 背景色のみ）
            screen.fill((255, 240, 245))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
