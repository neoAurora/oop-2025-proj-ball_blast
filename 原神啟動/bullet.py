# bullet.py
import pygame

class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 5
        self.speed = 10

    def move(self):
        self.y -= self.speed

    def draw(self, win):
        pygame.draw.circle(win, (255, 0, 0), (self.x, self.y), self.radius)

