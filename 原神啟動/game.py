# game.py
import pygame
import random
from cannon import Cannon
from bullet import Bullet
from ball import Ball
from ball import RewardBall

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.width, self.height = screen.get_size()

        
        # 初始化遊戲資源
        self.background = pygame.transform.scale(
            pygame.image.load("background.png").convert(),
            (self.width, self.height)
        )
        self.cannon = Cannon(self.width//2, self.height-130)
        self.font = pygame.font.SysFont("Arial", 24)
        
        # 遊戲狀態
        self.reset_game_state()

    def reset_game_state(self):
        """重置遊戲運行狀態"""
        self.bullets = []
        self.balls = []
        self.score = 0
        self.running = True
        self.clock = pygame.time.Clock()

        self.spawn_timer = 0
        
        # 射擊計時器
        self.last_shot_time = 0  # 記錄上次射擊時間
        self.shot_delay = 50     # 射擊間隔(毫秒)，1000/20=50ms per bullet
        
        # 遊戲參數
        self.bullets_per_second = 20  # 每秒20發子彈


    def spawn_ball(self):
        """生成新球體，有小機率生成獎勵球"""
        if random.random() < 0.2:  # 10%機率生成獎勵球
            ball = RewardBall(
                x=random.randint(50, self.width-50),
                y=0
            )
            ball.dx = random.uniform(-4, 4)
            ball.dy = random.uniform(1, 2.5)
        else:
            ball = Ball(
                x=random.randint(50, self.width-50),
                y=0,
                radius=random.randint(40, 70),
                hp=random.randint(20, 30),
                max_splits=3
            )
            ball.dx = random.uniform(-4, 4)
            ball.dy = random.uniform(1, 2.5)
        self.balls.append(ball)

    def handle_events(self):
        """處理輸入事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
    def handle_input(self):
        """處理玩家輸入"""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.cannon.move("LEFT", self.width)
        if keys[pygame.K_RIGHT]:
            self.cannon.move("RIGHT", self.width)

    def update_bullets(self):
        """更新子彈狀態 - 連續射擊版本"""
        # 獲取當前時間(毫秒)
        current_time = pygame.time.get_ticks()
        
        # 檢查是否達到射擊間隔
        if current_time - self.last_shot_time > self.shot_delay:
            self.last_shot_time = current_time
            # 發射新子彈
            self.bullets.append(Bullet(self.cannon.x, self.cannon.y))
        
        # 移動子彈並移除超出屏幕的
        for bullet in self.bullets[:]:
            bullet.move()
            if bullet.y < 0:
                self.bullets.remove(bullet)

    def update_balls(self):
        """更新球體狀態"""
        # 生成新球
        self.spawn_timer += 1
        if self.spawn_timer > 300:
            self.spawn_timer = 0
            self.spawn_ball()

        # 移動球體
        for ball in self.balls:
            ball.move(self.width, self.height)

    def handle_collisions(self):
        """處理碰撞檢測"""
        for ball in self.balls[:]:
            for bullet in self.bullets[:]:
                if ball.is_hit(bullet):
                    ball.hp -= 1
                    self.bullets.remove(bullet)

                    if isinstance(ball, RewardBall):
                        # 獎勵球沒有HP概念，只有被擊中會變大
                        if ball.radius >= ball.max_radius:
                            # 當獎勵球達到最大尺寸時消失，並增加子彈速度
                            self.balls.remove(ball)
                            self.bullets_per_wave += 1  # 增加每波子彈數量
                            self.score += 50  # 額外分數獎勵
                    else:
                        # 普通球的處理邏輯
                        ball.hp -= 1
                        if ball.hp <= 0:
                            self.balls.remove(ball)
                            if ball.radius > 10 and ball.splits_remaining > 0:
                                self.balls.extend(ball.split())
                                self.score += 10
                    break

    def check_game_over(self):
        """檢查遊戲結束條件：若任何 Ball 的 mask 和 Cannon 的 mask 重疊，就結束遊戲。"""
        for ball in self.balls:
            # 1. 計算球在畫面上的 Rect（中心對齊）
            ball_rect = ball.current_image.get_rect(center=(int(ball.x), int(ball.y)))

            # 2. 算出 ball_rect 和 cannon.rect 的左上角差距 (offset)
            offset_x = ball_rect.left - self.cannon.rect.left
            offset_y = ball_rect.top - self.cannon.rect.top

            # 3. 用 mask.overlap() 做精準碰撞檢測
            if self.cannon.mask.overlap(ball.mask, (offset_x, offset_y)):
                self.running = False
                return

    def render(self):
        """渲染遊戲畫面"""
        self.screen.blit(self.background, (0, 0))
        
        # 繪製所有遊戲物件
        for bullet in self.bullets: bullet.draw(self.screen)
        for ball in self.balls: ball.draw(self.screen)
        self.cannon.draw(self.screen)
        
        # 繪製分數
        score_text = self.font.render(f"Score: {self.score}", True, (0, 0, 0))
        self.screen.blit(score_text, (10, 10))

        pygame.display.update()

    def run(self):
        """執行一幀遊戲邏輯"""
        if not self.running:
            return
        self.handle_events()
        self.handle_input()
        self.update_bullets()
        self.update_balls()
        self.handle_collisions()
        self.check_game_over()
        self.render()