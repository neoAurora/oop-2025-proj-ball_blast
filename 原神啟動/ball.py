# ball.py
import pygame
import math
import random
import os

class Ball:
    _ball_images = None
    
    def __init__(self, x, y, radius, hp):
        self.x = x
        self.y = y
        self.radius = radius
        self.hp = hp
        self.dx = random.uniform(-3, 3)
        self.dy = random.uniform(1, 3)
        self.elasticity = 0.7
        self.gravity = 0.2
        self.has_bounced = False
        
        # 圖片載入
        self._load_images()
        self.current_image = random.choice(self._ball_images)
        self.current_image = pygame.transform.scale(
            self.current_image, 
            (radius*2, radius*2)
        )
        self.mask = pygame.mask.from_surface(self.current_image)
        self.font = pygame.font.SysFont("Arial", 24)

    @classmethod
    def _load_images(cls):
        if cls._ball_images is None:
            cls._ball_images = []
            for i in range(15):
                try:
                    img = pygame.image.load(f"ball{i}.png").convert_alpha()
                    cls._ball_images.append(img)
                except:
                    surf = pygame.Surface((100,100), pygame.SRCALPHA)
                    pygame.draw.circle(surf, (random.randint(50,255),0,0), (50,50), 50)
                    cls._ball_images.append(surf)

    def move(self, screen_width, screen_height):
        self.dy += self.gravity
        self.x += self.dx
        self.y += self.dy
        
        if self.y + self.radius >= screen_height - 100:
            self.y = screen_height - 100 - self.radius
            if not self.has_bounced:
                self.dy = -self.dy * self.elasticity
                self.has_bounced = True
            else:
                self.dy = -abs(self.dy)
            self.dx *= 0.9
        
        if self.x - self.radius <= 0:
            self.x = self.radius
            self.dx = -self.dx * self.elasticity
        elif self.x + self.radius >= screen_width:
            self.x = screen_width - self.radius
            self.dx = -self.dx * self.elasticity

    def draw(self, win):
        img_rect = self.current_image.get_rect(center=(int(self.x), int(self.y)))
        win.blit(self.current_image, img_rect)
        text = self.font.render(str(self.hp), True, (255, 255, 255))
        win.blit(text, (self.x - text.get_width()//2, self.y - text.get_height()//2))

    def is_hit(self, bullet):
        distance = math.hypot(self.x - bullet.x, self.y - bullet.y)
        if distance > self.radius + bullet.radius:
            return False
        bullet_mask = pygame.mask.Mask((bullet.radius*2, bullet.radius*2), True)
        offset = (int(bullet.x - self.x + self.radius), 
                 int(bullet.y - self.y + self.radius))
        return self.mask.overlap(bullet_mask, offset)

    def split(self):
        """修正後的分裂方法：確保返回新球體列表"""
        if self.radius <= 15:  # 增加hp檢查
            return []  # 無法分裂時返回空列表

        new_radius = self.radius // 2
        new_hp = max(1, self.hp // 2)  # 確保HP至少為1

        # 確保新球體有最小尺寸和HP
        new_radius = max(10, new_radius)  # 最小半徑10
        new_hp = max(1, new_hp)          # 最小HP為1
        
        left_ball = self._create_split_ball(self.x - new_radius, new_radius, new_hp)
        right_ball = self._create_split_ball(self.x + new_radius, new_radius, new_hp)
        
        return [ball for ball in [left_ball, right_ball] if ball is not None]  # 過濾None

    def _create_split_ball(self, x, radius, hp):
        """安全創建球體"""
        try:
            new_ball = Ball(x, self.y, radius, hp)
            new_ball.current_image = pygame.transform.scale(
                self.current_image, (radius*2, radius*2))
            new_ball.mask = pygame.mask.from_surface(new_ball.current_image)
            new_ball.dx = random.uniform(-2, 2)
            new_ball.dy = random.uniform(-3, -1)  # 向上彈跳
            new_ball.has_bounced = False
            return new_ball
        except Exception as e:
            print(f"Error creating split ball: {e}")
            return None