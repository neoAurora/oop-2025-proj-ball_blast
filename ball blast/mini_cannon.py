import pygame
from bullet import Bullet

class MiniCannon:
    """
    縮小複製砲台
    - 壽命 10 秒
    - 射速為主砲 50%（100 ms/發）
    - 被球撞到或時間結束即消失
    """
    FIRE_DELAY = 100      # 毫秒（主砲一半速度）
    LIFE_TIME  = 10_000   # 10 秒
    SIZE       = (100, 100)

    def __init__(self, x: int, y: int):
        self.x, self.y = x, y

        # 直接縮小原 cannon 圖
        self.image = pygame.transform.scale(
            pygame.image.load("cannon.png").convert_alpha(),
            MiniCannon.SIZE
        )
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.mask = pygame.mask.from_surface(self.image)

        self.spawn_time = pygame.time.get_ticks()
        self.last_shot_time = self.spawn_time
        self.bullets: list[Bullet] = []

    # ---------- 主要邏輯 ----------
    def update(self) -> bool:
        """
        更新射擊與壽命。
        仍存活回傳 True，超時回傳 False（呼叫者據此移除）。
        """
        now = pygame.time.get_ticks()

        # 發射子彈
        if now - self.last_shot_time >= MiniCannon.FIRE_DELAY:
            self.last_shot_time = now
            self.bullets.append(Bullet(self.x, self.y))

        # 更新子彈
        for bullet in self.bullets[:]:
            bullet.move()
            if bullet.y < 0:
                self.bullets.remove(bullet)

        # 壽命判定
        return now - self.spawn_time < MiniCannon.LIFE_TIME

    # ---------- 繪製 ----------
    def draw(self, surface: pygame.Surface):
        surface.blit(self.image, self.rect)
        for bullet in self.bullets:
            bullet.draw(surface)

