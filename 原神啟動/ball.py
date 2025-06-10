# ball.py
import pygame
import math

class Ball:
    def __init__(self, x, y, radius, hp):
        self.x = x
        self.y = y
        self.radius = radius
        self.hp = hp
        self.dy = 2
        self.font = pygame.font.SysFont("Arial", 24)  # 建立自己的字型物件

    def move(self):
        self.y += self.dy

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

