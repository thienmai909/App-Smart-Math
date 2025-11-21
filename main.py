import pygame
import sys
from src.config import *
from src.core.game_manager import GameManager

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()

    game_manager = GameManager()

    running = True
    while running:
        # 1. Xử lý Input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                game_manager.handle_input(event)
        
        # 2. Cập nhật logic
        game_manager.update()

        # 3. Vẽ
        screen.fill(COLOR_BG)
        game_manager.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
        