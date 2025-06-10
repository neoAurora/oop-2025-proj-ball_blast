import pygame
from game import Game

pygame.init()

if __name__ == "__main__":
    screen = pygame.display.set_mode((600, 800))
    pygame.display.set_caption("Ball Blast - OOP Project")
    
    def show_main_menu():
        font = pygame.font.SysFont("Arial", 36)
        while True:
            screen.fill((255, 255, 255))
            screen.blit(font.render("Ball Blast", True, (0,0,0)), (300-100, 300))
            screen.blit(font.render("Press ENTER to Start", True, (0,0,0)), (300-150, 400))
            pygame.display.update()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    Game(screen).run()
                    return

    show_main_menu()