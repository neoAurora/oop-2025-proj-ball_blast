import pygame
from bullet import Bullet
from cannon import Cannon  # 如需類型提示，可確保 cannon.py 存在並定義 Cannon 類別

class MiniCannon:
    """
    縮小複製砲台
    - 跟隨主砲移動
    - 射速為主砲 50%（100 ms/發）
    - 壽命 15 秒
    - 被球撞到或時間結束即消失
    """
    FIRE_DELAY = 100       # 毫秒（主砲一半速度）
    LIFE_TIME  = 15_000    # 15 秒
    SIZE       = (90, 90)  # 小砲台尺寸

    def __init__(self, main_cannon: 'Cannon'):
        self.main_cannon = main_cannon
        self.offset_y = 40  # 顯示在主砲下方一點
        self.offset_x = 60
        # 初始位置（根據主砲）
        self.x = self.main_cannon.x + self.offset_x
        self.y = self.main_cannon.y + self.offset_y

        # 圖像處理
        self.image = pygame.transform.scale(
            pygame.image.load("cannon.png").convert_alpha(),
            MiniCannon.SIZE
        )
        self.rect = self.image.get_rect(center=(int(self.x), int(self.y)))
        self.mask = pygame.mask.from_surface(self.image)

        # 計時與子彈管理
        self.spawn_time = pygame.time.get_ticks()
        self.last_shot_time = self.spawn_time
        self.bullets: list[Bullet] = []

    def update(self) -> bool:
        """
        更新位置、發射、壽命等邏輯。
        回傳 True 表示仍存活；False 表示時間到應該被移除。
        """
        now = pygame.time.get_ticks()

        # 1. 跟隨主砲位置
        self.x = self.main_cannon.x + self.offset_x
        self.y = self.main_cannon.y + self.offset_y
        self.rect.center = (int(self.x), int(self.y))

        # 2. 發射子彈
        if now - self.last_shot_time >= MiniCannon.FIRE_DELAY:
            self.last_shot_time = now
            self.bullets.append(Bullet(self.x, self.y))

        # 3. 更新子彈
        for bullet in self.bullets[:]:
            bullet.move()
            if bullet.y < 0:
                self.bullets.remove(bullet)

        # 4. 判定是否過期
        return now - self.spawn_time < MiniCannon.LIFE_TIME

    def draw(self, surface: pygame.Surface):
        """繪製 mini cannon 與其子彈"""
        surface.blit(self.image, self.rect)
        for bullet in self.bullets:
            bullet.draw(surface)
