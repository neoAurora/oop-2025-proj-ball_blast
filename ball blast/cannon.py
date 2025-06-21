# cannon.py
import pygame

class Cannon:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 8
        self.image = pygame.transform.scale(
            pygame.image.load("cannon.png").convert_alpha(),(200, 200))
        self.rect = self.image.get_rect(center=(x, y))

        self.mask = pygame.mask.from_surface(self.image)   #建立mask，進行碰撞判定

    def move(self, direction, screen_width):
        if direction == "LEFT" and self.x - self.speed > 0:
            self.x -= self.speed
        elif direction == "RIGHT" and self.x + self.speed < screen_width:
            self.x += self.speed
        self.rect.center = (self.x, self.y)

    def draw(self, win):
        win.blit(self.image, self.rect)