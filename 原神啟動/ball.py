# ball.py
import pygame
import math
import random
import os

class Ball:
    # 類別變數：預載所有球體圖片（避免重複載入）
    _ball_images = None
    
    def __init__(self, x, y, radius, hp):
        self.x = x
        self.y = y
        self.radius = radius
        self.hp = hp
        
        # 初始化物理參數
        self.dx = random.uniform(-3, 3)  # 水平速度
        self.dy = random.uniform(1, 3)   # 垂直速度
        self.gravity = 0.1               # 重力加速度
        
        # 載入圖片資源
        self._load_images()
        
        # 隨機選擇圖片並縮放
        self.current_image = random.choice(self._ball_images)
        self.current_image = pygame.transform.scale(
            self.current_image,
            (radius*2, radius*2)  # 根據半徑調整大小
        )
        
        # 文字渲染
        self.font = pygame.font.SysFont("Arial", 24)
        
        # 碰撞遮罩（用於精確碰撞檢測）
        self.mask = pygame.mask.from_surface(self.current_image)

    @classmethod
    def _load_images(cls):
        """類別方法：預載所有球體圖片（只執行一次）"""
        if cls._ball_images is not None:
            return
            
        cls._ball_images = []
        for i in range(14):  # ball0.png ~ ball14.png
            try:
                # 嘗試載入圖片（支援相對路徑）
                img_path = os.path.join("image", f"ball{i}.png")
                img = pygame.image.load(img_path).convert_alpha()
                cls._ball_images.append(img)
            except Exception as e:
                print(f"Warning: Failed to load {img_path}, using fallback. Error: {e}")
                # 圖片缺失時建立彩色替代圓形
                surf = pygame.Surface((100, 100), pygame.SRCALPHA)
                color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
                pygame.draw.circle(surf, color, (50, 50), 50)
                cls._ball_images.append(surf)

    def move(self, screen_width, screen_height):
        """更新球體位置（含邊界反彈）"""
        # 應用重力
        self.dy += self.gravity
        
        # 更新位置
        self.x += self.dx
        self.y += self.dy
        
        # 底部反彈
        if self.y + self.radius >= screen_height - 100:  # -100 留出地面空間
            self.y = screen_height - 100 - self.radius
            self.dy = -10
            
        # 側邊反彈
        if self.x - self.radius <= 0:
            self.x = self.radius
            self.dx = -self.dx 
        elif self.x + self.radius >= screen_width:
            self.x = screen_width - self.radius
            self.dx = -self.dx 

    def draw(self, win):
        """繪製球體（使用圖片替代圓形）"""
        # 計算繪製位置（中心對齊）
        img_rect = self.current_image.get_rect(center=(int(self.x), int(self.y)))
        win.blit(self.current_image, img_rect)
        
        # 繪製HP文字（居中）
        text = self.font.render(str(self.hp), True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.x, self.y))
        win.blit(text, text_rect)

    def is_hit(self, bullet):
        """檢測與子彈的碰撞（使用遮罩精確檢測）"""
        # 計算兩者距離（快速初步檢測）
        distance = math.hypot(self.x - bullet.x, self.y - bullet.y)
        if distance > self.radius + bullet.radius:
            return False
            
        # 精確像素級碰撞檢測
        bullet_mask = pygame.mask.Mask((bullet.radius*2, bullet.radius*2), True)
        offset = (int(bullet.x - self.x + self.radius), 
                 int(bullet.y - self.y + self.radius))
        return self.mask.overlap(bullet_mask, offset)

    def split(self):
        """分裂球體（保持相同圖片）"""
        if self.radius <= 15:
            return []
            
        new_radius = self.radius // 2
        new_hp = self.hp // 2
        
        # 新球體繼承相同圖片（但重新縮放）
        return [
            self._create_split_ball(self.x - new_radius, new_radius, new_hp),
            self._create_split_ball(self.x + new_radius, new_radius, new_hp)
        ]
    
    def _create_split_ball(self, x, radius, hp):
        """創建分裂後的子球體"""
        new_ball = Ball(x, self.y, radius, hp)
        
        # 複製當前圖片（避免重新隨機選擇）
        new_ball.current_image = pygame.transform.scale(
            self.current_image,
            (radius*2, radius*2)
        )
        new_ball.mask = pygame.mask.from_surface(new_ball.current_image)
        
        # 調整物理參數
        new_ball.dx = random.uniform(-2, 2)
        new_ball.dy = random.uniform(-3, -1)  # 向上彈跳
        
        return new_ball