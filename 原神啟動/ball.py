# ball.py
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
        self.dy = random.uniform(1, 3)
        self.gravity = 0.1
        self.font = pygame.font.SysFont("Arial", 24)  # 建立自己的字型物件

    def move(self, screen_height):
        self.dy += self.gravity

        self.x += self.dx
        self.y += self.dy

        if self.y + self.radius >= screen_height - 100:
            self.y = screen_height - self.radius - 100  # 防止卡進地面
            self.dy = -10

    def draw(self, win):
        if self.hp > 0:  # 只有HP大于0才绘制
            pygame.draw.circle(win, (0, 0, 0), (int(self.x), int(self.y)), self.radius)
            text = self.font.render(str(self.hp), True, (255, 255, 255))
            win.blit(text, (self.x - text.get_width() // 2, self.y - text.get_height() // 2))

    def is_hit(self, bullet):
        return math.hypot(self.x - bullet.x, self.y - bullet.y) < self.radius

    def split(self):
        if self.radius <= 15:
            return []
        new_radius = self.radius // 2
        new_hp = self.hp // 2
        return [
            Ball(self.x - new_radius, self.y, new_radius, new_hp),
            Ball(self.x + new_radius, self.y, new_radius, new_hp),
        ]

