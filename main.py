"""献立表カレンダー作成ゲーム - エントリポイント"""

import sys
import pygame
from src.constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, TITLE
from src.game import GameManager, GameState
from src.asset_manager import AssetManager
from src.ui.start_screen import StartScreen
from src.ui.play_screen import PlayScreen
from src.ui.result_screen import ResultScreen
from src.model.scoring import calculate_score


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
    result_screen = ResultScreen(assets)

    # 起動時にBGM再生開始
    assets.play_bgm("opening")

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
                    assets.play_bgm("playing")
            elif game.state == GameState.PLAYING:
                result = play_screen.handle_event(event)
                if result in ("done", "timeout"):
                    completed = result == "done"
                    score_result = calculate_score(
                        play_screen.board,
                        remaining_seconds=play_screen.timer.remaining_int,
                        completed_by_button=completed,
                    )
                    result_screen.set_result(
                        player_board=play_screen.board.copy(),
                        answer_board=play_screen.answer,
                        score_result=score_result,
                    )
                    game.go_to_result()
                    assets.play_bgm("ending")
                elif result == "back":
                    game.go_to_start()
                    assets.play_bgm("opening")
            elif game.state == GameState.RESULT:
                result = result_screen.handle_event(event)
                if result == "back":
                    game.go_to_start()
                    assets.play_bgm("opening")

        # --- 更新 ---
        if game.state == GameState.PLAYING:
            result = play_screen.update(dt_ms)
            if result == "timeout":
                score_result = calculate_score(
                    play_screen.board,
                    remaining_seconds=0,
                    completed_by_button=False,
                )
                result_screen.set_result(
                    player_board=play_screen.board.copy(),
                    answer_board=play_screen.answer,
                    score_result=score_result,
                )
                game.go_to_result()
                assets.play_bgm("ending")

        # --- 描画 ---
        if game.state == GameState.START:
            start_screen.draw(screen)
        elif game.state == GameState.PLAYING:
            play_screen.draw(screen)
        elif game.state == GameState.RESULT:
            result_screen.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
