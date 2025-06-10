import pygame
import math
import random

class Ball:
    def __init__(self, x, y, radius, hp):
        self.x = x
        self.y = y
        self.radius = radius
        self.hp = hp
        self.dx = random.uniform(-3, 3)
        self.dy = random.uniform(1, 2)
        self.elasticity = 0.7
        self.font = pygame.font.SysFont("Arial", 24)

    def move(self, screen_width, screen_height):
        self.dy += 0.1  # 固定重力值
        self.x += self.dx
        self.y += self.dy
        
        # 邊界碰撞檢測
        if self.y + self.radius >= screen_height-100:
            self.y = screen_height-100 - self.radius
            self.dy = -self.dy   
        if self.x - self.radius <= 0 or self.x + self.radius >= screen_width:
            self.dx = -self.dx * self.elasticity

    def draw(self, win):
        pygame.draw.circle(win, (0, 0, 0), (int(self.x), int(self.y)), self.radius)
        text = self.font.render(str(self.hp), True, (255, 255, 255))
        win.blit(text, (self.x - text.get_width()//2, self.y - text.get_height()//2))

    def is_hit(self, bullet):
        return math.hypot(self.x - bullet.x, self.y - bullet.y) < self.radius

    def split(self):
        if self.radius <= 15: return []
        new_radius = self.radius // 2
        return [
            Ball(self.x - new_radius, self.y, new_radius, self.hp//2),
            Ball(self.x + new_radius, self.y, new_radius, self.hp//2)
        ]