# game.py
import pygame
import random
from cannon import Cannon
from bullet import Bullet
from ball import Ball

print("game started")

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.width, self.height = screen.get_size()
        self.cannon = Cannon(self.width // 2, self.height - 50)
        self.bullets = []
        self.balls = []
        self.spawn_timer = 0
        self.running = True
        self.score = 0
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 24)

        self.max_bullets = 5      # 最大子弹数量
        self.bullet_cooldown = 10 # 子弹发射冷却时间（帧数）
        self.cooldown_timer = 0   # 冷却计时器

    def spawn_ball(self):
        x = random.randint(50, self.width - 50)
        radius = random.randint(20, 30)
        hp = radius 
        self.balls.append(Ball(x, 0, radius, hp))

    def handle_bullets(self):
        for bullet in self.bullets[:]:
            bullet.move()
            if bullet.y < 0:
                self.bullets.remove(bullet)

    def handle_collisions(self):
        for ball in self.balls[:]:
            for bullet in self.bullets[:]:
                if ball.is_hit(bullet):
                    ball.hp -= 1
                    self.bullets.remove(bullet)
                    if ball.hp <= 0:
                        self.balls.remove(ball)
                        new_balls = ball.split()
                        for new_ball in new_balls:
                            if new_ball.hp > 0:  # 确保新分裂的球HP大于0
                                self.balls.append(new_ball)
                        self.score += 10
                    break

    def check_game_over(self):
        for ball in self.balls:
            if ball.hp > 0 and abs(ball.x - self.cannon.x) < ball.radius and abs(ball.y - self.cannon.y) < ball.radius:
                self.running = False

    def draw(self):
        self.screen.fill((255, 255, 255))
        self.cannon.draw(self.screen)
        for bullet in self.bullets:
            bullet.draw(self.screen)
        for ball in self.balls:
            if ball.hp > 0:  # 只绘制HP大于0的球
                ball.draw(self.screen)
        score_text = self.font.render(f"Score: {self.score}", True, (0, 0, 0))
        self.screen.blit(score_text, (10, 10))
        pygame.display.update()

    def run(self):
        while self.running:
            self.clock.tick(60)
        
            # 处理事件
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # 炮台移动
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.cannon.move("LEFT", self.width)
            if keys[pygame.K_RIGHT]:
                self.cannon.move("RIGHT", self.width)

            # 子弹发射逻辑（按住空格键可以连发）
            if keys[pygame.K_SPACE]:
                if len(self.bullets) < self.max_bullets and self.cooldown_timer <= 0:
                    self.bullets.append(Bullet(self.cannon.x, self.cannon.y))
                    self.cooldown_timer = self.bullet_cooldown  # 重置冷却时间
            self.cooldown_timer -= 1  # 冷却计时器递减

            # 生成新球
            self.spawn_timer += 1
            if self.spawn_timer > 60:
                self.spawn_ball()
                self.spawn_timer = 0

            # 更新球和子弹
            for ball in self.balls[:]:
                ball.move()
            self.handle_bullets()
            self.handle_collisions()
            self.check_game_over()
            self.draw()

        print("Game Over! Score:", self.score)
        pygame.quit()
