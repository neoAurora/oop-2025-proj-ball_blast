import pygame
from bullet import Bullet
import random

class Cannon:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 5
        self.image = pygame.transform.scale(
            pygame.image.load("cannon.png").convert_alpha(), (200, 200))
        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pygame.mask.from_surface(self.image)
    
        # === 抽卡屬性面板 ===
        self.attributes = {
            "damage_bonus": 0,
            "shot_delay": 0,               # 射速變快 = 減少間隔（例如 -100）
            "bullets_per_second": 0,       # > 0 代表啟用雙發
            "cannon_hp": 1
        }

        self.base_delay = 50  # 射速變超快，50ms一發（每秒約 20 發）
        self.current_delay = self.base_delay + self.attributes["shot_delay"]
        self.last_shot_time = 0
        self.hp = self.attributes["cannon_hp"] 
        
    def move(self, direction, screen_width):
        if direction == "LEFT" and self.x - self.speed > 0:
            self.x -= self.speed
        elif direction == "RIGHT" and self.x + self.speed < screen_width:
            self.x += self.speed
        self.rect.center = (self.x, self.y)

    def draw(self, win):
        win.blit(self.image, self.rect)

    def create_bullet(self):
        damage = 2 if random.random() < 0.3 and self.attributes["damage_bonus"] else 1
        double = self.attributes["bullets_per_second"] > 0
        return Bullet(self.x, self.y, damage=damage, double=double)

    def create_bullet_with_offset(self, offset_x):
        damage = 2 if random.random() < 0.3 and self.attributes["damage_bonus"] else 1
        double = self.attributes["bullets_per_second"] > 0
        return Bullet(self.x + offset_x, self.y, damage=damage, double=double)


    def shoot(self, bullet_group, current_time):
        if current_time - self.last_shot_time >= self.current_delay:
            self.last_shot_time = current_time

            if self.attributes["bullets_per_second"] > 0:
                offset = 20
                bullet_group.append(self.create_bullet_with_offset(-offset))
                bullet_group.append(self.create_bullet_with_offset(+offset))
            else:
                bullet_group.append(self.create_bullet())

    def apply_card_effect(self, effect_dict):
        for k, v in effect_dict.items():
            if k in self.attributes:
                self.attributes[k] += v
                print(f"[Cannon 強化] {k} +{v} → 現在是 {self.attributes[k]}")

                # 射速卡會直接更新 current_delay
                if k == "shot_delay":
                    self.current_delay = max(50, self.base_delay + self.attributes["shot_delay"])
            else:
                print(f"[警告] 未知屬性：{k}")
