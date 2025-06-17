import pygame

class Bullet:
    def __init__(self, x, y, damage=1, double=False):
        self.x = x
        self.y = y
        self.speed = 10
        self.damage = damage
        self.double = double

       # bullet.py  ── __init__()
        image_file = "dbullet.jpg" if self.double else "bullet.jpg"

        self.image = pygame.image.load(image_file).convert()   # 先用 convert()
        self.image.set_colorkey((255, 255, 255))              # ← 把白色設透明
        self.image = pygame.transform.scale(self.image, (10, 30))
 
        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pygame.mask.from_surface(self.image)  # ✅ 加這行


    def move(self):
        self.y -= self.speed
        self.rect.centery = self.y

    def draw(self, win):
        win.blit(self.image, self.rect)

