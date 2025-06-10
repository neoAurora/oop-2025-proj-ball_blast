# bullet.py
import pygame
import os

class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 10

        img_path = os.path.join("bullet.jpg")  
        self.image = pygame.image.load(img_path).convert()
        self.image.set_colorkey((255, 255, 255))   #去除白色背景
        self.image = pygame.transform.scale(self.image, (20, 20))
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        self.y -= self.speed
        self.rect.center = (self.x, self.y)

    def draw(self, win):
        win.blit(self.image, self.rect)

