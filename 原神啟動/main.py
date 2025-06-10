# main.py
import pygame
from game import Game

pygame.init()

if __name__ == "__main__":
    screen = pygame.display.set_mode((600, 800))
    pygame.display.set_caption("Ball Blast - OOP Project")
    
    def show_main_menu():
        font = pygame.font.SysFont("Arial", 36)
        clock = pygame.time.Clock()
        while True:
            screen.fill((255, 255, 255))
            title = font.render("Ball Blast", True, (0, 0, 0))
            prompt = font.render("Press ENTER to Start", True, (0, 0, 0))
            screen.blit(title, (300 - title.get_width() // 2, 300))
            screen.blit(prompt, (300 - prompt.get_width() // 2, 400))
            pygame.display.update()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    return
            clock.tick(60)

    show_main_menu()
    Game(screen).run()
