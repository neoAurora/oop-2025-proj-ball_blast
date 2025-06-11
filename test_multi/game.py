# game.py
import pygame
import random
from cannon import Cannon
from bullet import Bullet
from ball import Ball

class Game:
    def __init__(self, screen, multiplayer=False, network_manager=None, player_id=0):
        self.screen = screen
        self.width, self.height = screen.get_size()
        self.multiplayer = multiplayer
        self.network_manager = network_manager
        self.player_id = player_id
        
        # 初始化遊戲資源
        self.background = pygame.transform.scale(
            pygame.image.load("background.png").convert(),
            (self.width, self.height)
        )
        
        # 根據遊戲模式初始化大砲
        if multiplayer:
            # 多人模式：兩個玩家分別在左右兩側
            if player_id == 0:
                self.my_cannon = Cannon(self.width//4, self.height-130)
                self.other_cannon = Cannon(3*self.width//4, self.height-130)
            else:
                self.my_cannon = Cannon(3*self.width//4, self.height-130)
                self.other_cannon = Cannon(self.width//4, self.height-130)
        else:
            # 單人模式：只有一個大砲在中央
            self.my_cannon = Cannon(self.width//2, self.height-130)
            self.other_cannon = None
        
        self.font = pygame.font.SysFont("Arial", 24)
        
        # 遊戲狀態
        self.reset_game_state()

    def reset_game_state(self):
        """重置遊戲運行狀態"""
        self.my_bullets = []
        self.other_bullets = []
        self.balls = []
        self.score = 0
        self.other_score = 0
        self.running = True
        self.clock = pygame.time.Clock()
        
        # 射擊計時器
        self.wave_timer = 0
        self.bullet_cooldown = 0
        self.bullet_in_wave = 0
        self.spawn_timer = 0
        
        # 遊戲參數
        self.wave_interval = 15    # 1秒一波
        self.bullet_delay = 3      # 0.05秒一發
        self.bullets_per_wave = 5  # 每波5發

    def spawn_ball(self):
        """生成新球體"""
        ball = Ball(
            x=random.randint(50, self.width-50),
            y=0,
            radius=random.randint(40, 70),
            hp=random.randint(20, 30),
            max_splits = 3   #初始球最多分裂3次
        )
        ball.dx = random.uniform(-4, 4)  # 水平速度
        ball.dy = random.uniform(1, 2.5) # 垂直速度
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
            self.my_cannon.move("LEFT", self.width)
        if keys[pygame.K_RIGHT]:
            self.my_cannon.move("RIGHT", self.width)

    def update_bullets(self):
        """更新子彈狀態"""
        # 自動射擊邏輯
        self.wave_timer += 1
        if self.wave_timer >= self.wave_interval:
            self.wave_timer = 0
            self.bullet_in_wave = 0
        
        if self.bullet_in_wave < self.bullets_per_wave:
            self.bullet_cooldown += 1
            if self.bullet_cooldown >= self.bullet_delay:
                self.bullet_cooldown = 0
                self.my_bullets.append(Bullet(self.my_cannon.x, self.my_cannon.y))
                self.bullet_in_wave += 1

        # 移動我的子彈並移除超出屏幕的
        for bullet in self.my_bullets[:]:
            bullet.move()
            if bullet.y < 0:
                self.my_bullets.remove(bullet)
        
        # 移動對方的子彈（多人模式）
        if self.multiplayer:
            for bullet in self.other_bullets[:]:
                bullet.move()
                if bullet.y < 0:
                    self.other_bullets.remove(bullet)

    def update_balls(self):
        """更新球體狀態"""
        # 只有玩家0或單人模式才生成球
        if not self.multiplayer or self.player_id == 0:
            self.spawn_timer += 1
            if self.spawn_timer > 300:
                self.spawn_timer = 0
                self.spawn_ball()

        # 移動球體
        for ball in self.balls:
            ball.move(self.width, self.height)

    def handle_collisions(self):
        """處理碰撞檢測"""
        # 處理我的子彈與球的碰撞
        for ball in self.balls[:]:
            for bullet in self.my_bullets[:]:
                if ball.is_hit(bullet):
                    ball.hp -= 1
                    self.my_bullets.remove(bullet)

                    if ball.hp <= 0:
                        self.balls.remove(ball)
                        if ball.radius > 10 and ball.splits_remaining > 0:
                            self.balls.extend(ball.split())
                        self.score += 10
                    break
        
        # 處理對方子彈與球的碰撞（多人模式）
        if self.multiplayer:
            for ball in self.balls[:]:
                for bullet in self.other_bullets[:]:
                    if ball.is_hit(bullet):
                        ball.hp -= 1
                        self.other_bullets.remove(bullet)

                        if ball.hp <= 0:
                            self.balls.remove(ball)
                            if ball.radius > 10 and ball.splits_remaining > 0:
                                self.balls.extend(ball.split())
                            self.other_score += 10
                        break

    def check_game_over(self):
        """檢查遊戲結束條件"""
        # 檢查我的大砲
        for ball in self.balls:
            ball_rect = ball.current_image.get_rect(center=(int(ball.x), int(ball.y)))
            offset_x = ball_rect.left - self.my_cannon.rect.left
            offset_y = ball_rect.top - self.my_cannon.rect.top

            if self.my_cannon.mask.overlap(ball.mask, (offset_x, offset_y)):
                self.running = False
                return
        
        # 檢查對方大砲（多人模式）
        if self.multiplayer and self.other_cannon:
            for ball in self.balls:
                ball_rect = ball.current_image.get_rect(center=(int(ball.x), int(ball.y)))
                offset_x = ball_rect.left - self.other_cannon.rect.left
                offset_y = ball_rect.top - self.other_cannon.rect.top

                if self.other_cannon.mask.overlap(ball.mask, (offset_x, offset_y)):
                    self.running = False
                    return

    def update_from_network(self, game_state):
        """從網路更新遊戲狀態（多人模式）"""
        if not self.multiplayer:
            return
        
        # 更新對方大砲位置
        if 'other_cannon_x' in game_state:
            self.other_cannon.x = game_state['other_cannon_x']
            self.other_cannon.rect.center = (self.other_cannon.x, self.other_cannon.y)
        
        # 更新對方子彈
        if 'other_bullets' in game_state:
            self.other_bullets = []
            for bullet_data in game_state['other_bullets']:
                bullet = Bullet(bullet_data['x'], bullet_data['y'])
                self.other_bullets.append(bullet)
        
        # 更新球體狀態（由主機同步）
        if 'balls' in game_state and self.player_id == 1:
            self.balls = game_state['balls']
        
        # 更新對方分數
        if 'other_score' in game_state:
            self.other_score = game_state['other_score']

    def get_player_state(self):
        """獲取當前玩家狀態（用於網路傳輸）"""
        bullet_data = [{'x': bullet.x, 'y': bullet.y} for bullet in self.my_bullets]
        
        state = {
            'cannon_x': self.my_cannon.x,
            'bullets': bullet_data,
            'score': self.score
        }
        
        # 如果是主機（玩家0），同步球體狀態
        if self.player_id == 0:
            state['balls'] = self.balls
        
        return state

    def render(self):
        """渲染遊戲畫面"""
        self.screen.blit(self.background, (0, 0))
        
        # 繪製所有子彈
        for bullet in self.my_bullets: 
            bullet.draw(self.screen)
        if self.multiplayer:
            for bullet in self.other_bullets:
                bullet.draw(self.screen)
        
        # 繪製球體
        for ball in self.balls: 
            ball.draw(self.screen)
        
        # 繪製大砲
        self.my_cannon.draw(self.screen)
        if self.multiplayer and self.other_cannon:
            self.other_cannon.draw(self.screen)
        
        # 繪製分數
        if self.multiplayer:
            my_score_text = self.font.render(f"Your Score: {self.score}", True, (0, 0, 0))
            other_score_text = self.font.render(f"Other Score: {self.other_score}", True, (0, 0, 0))
            self.screen.blit(my_score_text, (10, 10))
            self.screen.blit(other_score_text, (10, 40))
        else:
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
        
        # 網路同步（多人模式）
        if self.multiplayer and self.network_manager and self.network_manager.is_connected:
            # 發送我的狀態
            self.network_manager.send_player_state(self.get_player_state())
            
            # 接收對方狀態
            game_state = self.network_manager.get_game_state()
            if game_state:
                self.update_from_network(game_state)
        
        self.render()
