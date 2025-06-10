# cannon.py
import pygame

class Cannon:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 5
        self.width = 50
        self.height = 40

        self.original_image = pygame.image.load("cannon.png").convert_alpha()
        
        # 調整圖片大小
        self.width = 200  # 設定想要的寬度
        self.height = 200  # 設定想要的高度
        self.image = pygame.transform.scale(self.original_image, (self.width, self.height))
        
        # 計算旋轉中心點
        self.rect = self.image.get_rect(center=(x, y))

    def move(self, direction, screen_width):
        if direction == "LEFT" and self.x - self.speed > 0:
            self.x -= self.speed
        if direction == "RIGHT" and self.x + self.speed < screen_width:
            self.x += self.speed
        self.rect.centerx = self.x

    def draw(self, win):
        win.blit(self.image, self.rect)

