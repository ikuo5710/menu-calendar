"""献立表カレンダー作成ゲーム - エントリポイント"""

import sys
import pygame
from src.constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, TITLE
from src.game import GameManager, GameState
from src.asset_manager import AssetManager
from src.ui.start_screen import StartScreen


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

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                continue

            if game.state == GameState.START:
                if start_screen.handle_event(event):
                    game.go_to_playing()
            elif game.state == GameState.PLAYING:
                # Phase 3 で実装
                pass
            elif game.state == GameState.RESULT:
                # Phase 6 で実装
                pass

        # --- 描画 ---
        if game.state == GameState.START:
            start_screen.draw(screen)
        elif game.state == GameState.PLAYING:
            # Phase 3 で実装（仮: 背景色のみ）
            screen.fill((240, 248, 255))
        elif game.state == GameState.RESULT:
            # Phase 6 で実装（仮: 背景色のみ）
            screen.fill((255, 240, 245))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
