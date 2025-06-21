# ball.py
import pygame
import math
import random
import os

class Ball:
    # 類別變數：預載所有球體圖片（避免重複載入）
    _ball_images = None
    
    def __init__(self, x, y, radius, hp, max_splits = 4):
        self.x = x
        self.y = y
        self.radius = radius
        self.hp = hp
        self.original_hp = hp
        self.max_splits = max_splits     #最大分裂次數
        self.splits_remaining = max_splits
        
        # 初始化物理參數
        self.dx = random.uniform(-3, 3)  # 水平速度
        self.dy = random.uniform(1, 3)   # 垂直速度
        self.gravity = 0.1               # 重力加速度
        self.elasticity = 0.96           #橫向彈性係數
        
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
        for i in range(15):  # ball0.png ~ ball14.png
            # 嘗試載入圖片（支援相對路徑）
            img_path = os.path.join("image", f"ball{i}.png")
            img = pygame.image.load(img_path).convert_alpha()
            cls._ball_images.append(img)

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
            self.dx = -self.dx * self.elasticity
        elif self.x + self.radius >= screen_width:
            self.x = screen_width - self.radius
            self.dx = -self.dx * self.elasticity

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
        # 1. 先用簡易的矩形包圍盒（AABB）做一次快篩 (optional)
        ball_rect = self.current_image.get_rect(center=(int(self.x), int(self.y)))
        bullet_rect = bullet.image.get_rect(center=(int(bullet.x), int(bullet.y)))
        
        if not ball_rect.colliderect(bullet_rect):
            # 如果它們的包圍盒都沒碰到，就不用繼續做 pixel-level
            return False

        # 2. 計算兩個遮罩的 offset
        offset_x = bullet_rect.left - ball_rect.left
        offset_y = bullet_rect.top  - ball_rect.top
        offset = (offset_x, offset_y)

        # 3. 呼叫 mask.overlap() 來檢查是否有真正的像素重疊
        #    如果有重疊就回傳 (non-None)；否則回傳 None
        return self.mask.overlap(bullet.mask, offset) is not None

    def split(self):
        """分裂球體（保持相同圖片）"""
        if self.radius <= 2 or self.splits_remaining <= 0:
            return []
        
        self.splits_remaining -= 1  
        new_radius = self.radius // 1.4
        new_hp = max(1, self.original_hp // 2)
        
        left_ball = self._create_split_ball(self.x - new_radius, new_radius, new_hp)
        right_ball = self._create_split_ball(self.x + new_radius, new_radius, new_hp)
        return [ball for ball in [left_ball, right_ball] if ball is not None]
    
    def _create_split_ball(self, x, radius, hp):
        """創建分裂後的子球體"""
        new_ball = Ball(x, self.y, radius, hp)
        new_ball.max_splits = self.max_splits
        new_ball.splits_remaining = self.splits_remaining
        
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


class RewardBall(Ball):
    """獎勵球，繼承自Ball類別"""
    _original_reward_image = None  # 儲存原始高解析度圖片
    
    def __init__(self, x, y):
        # 載入高解析度獎勵球圖片（只執行一次）
        if RewardBall._original_reward_image is None:
            img_path = os.path.join("image", "ball15.png")
            RewardBall._original_reward_image = pygame.image.load(img_path).convert_alpha()
        
        # 計算縮放比例（假設原始圖片是標準尺寸的5倍）
        # 例如：標準球直徑100px，你的圖片就是500px
        self.scale_factor = 5  
        self.base_radius = 40  # 初始邏輯半徑
        
        # 初始化父類別
        super().__init__(x, y, radius=self.base_radius, hp=5, max_splits=0)
        
        # 設定初始圖片（從大圖縮小）
        self.current_image = self._get_scaled_image(self.radius)
        self.mask = pygame.mask.from_surface(self.current_image)
        
        # 獎勵球特有屬性
        self.growth_factor = 2  # 每次被擊中半徑增長係數
        self.min_radius = 40
        self.max_radius = 100

    def _get_scaled_image(self, target_radius):
        """從高解析度原圖生成目標尺寸的圖片"""
        # 計算在高解析度圖中的對應尺寸
        src_radius = int(target_radius * self.scale_factor)
        src_size = src_radius * 2
        
        # 從原圖裁剪中心區域（避免邊緣變形）
        original_size = RewardBall._original_reward_image.get_size()
        center_x = original_size[0] // 2
        center_y = original_size[1] // 2
        crop_rect = pygame.Rect(
            center_x - src_radius,
            center_y - src_radius,
            src_size,
            src_size
        )
        
        # 確保裁剪區域不超出原圖範圍
        crop_rect = crop_rect.clip(pygame.Rect((0, 0), original_size))
        cropped = RewardBall._original_reward_image.subsurface(crop_rect)
        
        # 縮放到目標尺寸
        return pygame.transform.smoothscale(
            cropped,
            (target_radius * 2, target_radius * 2)
        )

    def draw(self, win):
        """覆寫draw方法，顯示?而不是HP"""
        img_rect = self.current_image.get_rect(center=(int(self.x), int(self.y)))
        win.blit(self.current_image, img_rect)
        
        # 繪製?文字（居中）
        text = self.font.render("?", True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.x, self.y))
        win.blit(text, text_rect)

    def is_hit(self, bullet):
        hit = super().is_hit(bullet)
        if hit:
            # 被擊中時增加半徑
            new_radius = min(int(self.radius + self.growth_factor), self.max_radius)
            
            if new_radius != self.radius:
                self.radius = new_radius
                # 從高解析度原圖生成新尺寸圖片
                self.current_image = self._get_scaled_image(self.radius)
                self.mask = pygame.mask.from_surface(self.current_image)
        return hit

    def split(self):
        """覆寫split方法，獎勵球不會分裂"""
        return []