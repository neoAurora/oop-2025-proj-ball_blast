# game.py - Fixed version with level manager support and multiplayer
import pygame
import random
from cannon import Cannon
from bullet import Bullet
from ball import Ball
from gacha import GachaSystem
from ball import RewardBall
from status import StatusPanel

class Game:
    def __init__(self, screen, multiplayer=False, network_manager=None, player_id=0, level_manager=None, coins=100):
        self.screen = screen
        self.width, self.height = screen.get_size()
        self.multiplayer = multiplayer
        self.network_manager = network_manager
        self.player_id = player_id
        self.level_manager = level_manager  # Add level manager
        self.gacha_system = GachaSystem(self)
        self.previous_level = 0      # 用來偵測關卡變動

        self.bullets_per_second = 10  
        self.bullet_rows = 1
        self.row_spacing = 21  # 每排子彈之間的水平間距（單位：像素）
        self.damage_per_bullet = 1
        self.crit_rate = 5
        self.crit_damage = 150

        self.status_panel = StatusPanel(self)
        self.coins = coins
        self.coin_font = pygame.font.SysFont("Arial", 20)  # 金幣顯示字體

        


        # Load level configuration
        if self.level_manager:
            self.level_config = self.level_manager.get_level_config()
        else:
            # Default configuration for backward compatibility
            self.level_config = {
                'spawn_interval': 300,
                'ball_hp_min': 20,
                'ball_hp_max': 30,
                'ball_speed_min': 1.0,
                'ball_speed_max': 2.5,
                'reward_ball_chance': 0.2
            }
        
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
            # 為了保持代碼一致性，在單人模式下也使用 my_cannon
            self.cannon = self.my_cannon
        
        self.font = pygame.font.SysFont("Arial", 24)
        
        # 遊戲狀態
        self.reset_game_state()

    def reset_game_state(self):
        """重置遊戲運行狀態"""
        if self.multiplayer:
            self.my_bullets = []
            self.other_bullets = []
        else:
            self.bullets = []
        
        self.balls = []
        self.score = 0
        self.other_score = 0
        self.running = True
        self.clock = pygame.time.Clock()
        
        # 射擊計時器 - 合併兩種射擊系統
        if self.multiplayer:
            # 多人模式使用波次射擊系統
            self.wave_timer = 0
            self.bullet_cooldown = 0
            self.bullet_in_wave = 0
            self.wave_interval = 15    # 1秒一波
            self.bullet_delay = 3      # 0.05秒一發
            self.bullets_per_wave = 5  # 每波5發
        else:
            # 單人模式使用連續射擊系統
            self.last_shot_time = 0   # 記錄上次射擊時間
            self.shot_delay = 1000 // self.bullets_per_second     # 射擊間隔(毫秒)
        
        self.spawn_timer = 0

    def spawn_ball(self):
        """Generate new balls with level-based difficulty"""
        # Use level configuration for ball generation
        if random.random() < self.level_config['reward_ball_chance']:
            ball = RewardBall(
                x=random.randint(50, self.width-50),
                y=0
            )
            ball.dx = random.uniform(-4, 4)
            ball.dy = random.uniform(
                self.level_config['ball_speed_min'], 
                self.level_config['ball_speed_max']
            )
        else:
            ball = Ball(
                x=random.randint(50, self.width-50),
                y=0,
                radius=random.randint(40, 70),
                hp=random.randint(
                    self.level_config['ball_hp_min'], 
                    self.level_config['ball_hp_max']
                ),
                max_splits=3
            )
            ball.dx = random.uniform(-4, 4)
            ball.dy = random.uniform(
                self.level_config['ball_speed_min'], 
                self.level_config['ball_speed_max']
            )
        
        self.balls.append(ball)

    def handle_events(self):
        """處理輸入事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    from main import show_pause_screen
                    result = show_pause_screen(self)
                    if not result:
                        self.running = False

    def handle_input(self):
        """處理玩家輸入"""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.my_cannon.move("LEFT", self.width)
        if keys[pygame.K_RIGHT]:
            self.my_cannon.move("RIGHT", self.width)

    def update_bullets(self):
        """更新子彈狀態 - 支持兩種射擊模式"""
        if self.multiplayer:
            # 多人模式：波次射擊系統
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
            
            # 移動對方的子彈
            for bullet in self.other_bullets[:]:
                bullet.move()
                if bullet.y < 0:
                    self.other_bullets.remove(bullet)
        else:
            # 單人模式：連續射擊系統
            current_time = pygame.time.get_ticks()
            
            # 檢查是否達到射擊間隔
            if current_time - self.last_shot_time > self.shot_delay:
                self.last_shot_time = current_time
                # 發射新子彈
                for i in range(self.bullet_rows):
                    # 從中心開始左右分布
                    offset = (i - self.bullet_rows // 2) * self.row_spacing
                    bullet_x = self.my_cannon.x + offset
                    bullet_y = self.my_cannon.y
                    self.bullets.append(Bullet(bullet_x, bullet_y))
            
            # 移動子彈並移除超出屏幕的
            for bullet in self.bullets[:]:
                bullet.move()
                if bullet.y < 0:
                    self.bullets.remove(bullet)

    def update_balls(self):
        """Update ball status with level-based spawn rate"""
        # 只有玩家0或單人模式才生成球
        if not self.multiplayer or self.player_id == 0:
            self.spawn_timer += 1
            # Use level configuration for spawn interval
            if self.spawn_timer > self.level_config['spawn_interval']:
                self.spawn_timer = 0
                self.spawn_ball()

        # 移動球體
        for ball in self.balls:
            ball.move(self.width, self.height)

        # --------------------------------------------------------------
    def _animate_card_draw(self, img_path: str, total_ms: int = 1000, hold_ms: int = 3000):
        """
        非阻塞版抽卡動畫：
        1. 0.5 秒翻牌 → 漸放大
        2. 停留 hold_ms 毫秒
        3. 自動返回主畫面
        """
        try:
            card = pygame.image.load(img_path).convert()
        except Exception as e:
            print("載入卡圖失敗：", e)
            return

        sw, sh = self.screen.get_size()
        iw, ih = card.get_size()
        scale_fit = min(sw / iw, sh / ih)

        half = total_ms // 2
        start_ticks = pygame.time.get_ticks()

        clock = pygame.time.Clock()
        running_anim = True

        while running_anim:
            now = pygame.time.get_ticks()
            elapsed = now - start_ticks

            #  處理事件，防止當機
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            if elapsed >= total_ms + hold_ms:
                break

            # ---- 更新動畫狀態 ----
            self.screen.fill((0, 0, 0))

            if elapsed < half:
                t = elapsed / half
                scale = 0.1 + 0.9 * t  # 從小放大
            else:
                scale = scale_fit  # 停留放大後的大小

            surf = pygame.transform.smoothscale(card, (int(iw * scale), int(ih * scale)))
            rect = surf.get_rect(center=(sw // 2, sh // 2))
            self.screen.blit(surf, rect)

            pygame.display.update()
            clock.tick(60)  # 每秒最多 60 幀



    def handle_collisions(self):
        """處理碰撞檢測 - 支持獎勵球和普通球"""
        if self.multiplayer:
            # 多人模式：處理我的子彈與球的碰撞
            for ball in self.balls[:]:
                for bullet in self.my_bullets[:]:
                    if ball.is_hit(bullet):
                        self.my_bullets.remove(bullet)
                        
                        damage = self.calculate_damage()

                        if isinstance(ball, RewardBall):
                            # 獎勵球被擊中會變大
                            if ball.radius >= ball.max_radius:
                                self.balls.remove(ball)
                                self.bullets_per_wave += 1  # 增加每波子彈數量
                                self.score += 50  # 額外分數獎勵
                        else:
                            # 普通球的處理邏輯
                            ball.hp -= damage
                            if ball.hp <= 0:
                                self.balls.remove(ball)
                                if ball.radius > 10 and ball.splits_remaining > 0:
                                    self.balls.extend(ball.split())
                                self.score += 10
                        break
            
            # 處理對方子彈與球的碰撞
            for ball in self.balls[:]:
                for bullet in self.other_bullets[:]:
                    if ball.is_hit(bullet):
                        self.other_bullets.remove(bullet)
                        
                        damage = self.calculate_damage()

                        if isinstance(ball, RewardBall):
                            # 獎勵球被擊中會變大
                            if ball.radius >= ball.max_radius:
                                self.balls.remove(ball)
                                self.other_score += 50  # 額外分數獎勵
                        else:
                            # 普通球的處理邏輯
                            ball.hp -= damage
                            if ball.hp <= 0:
                                self.balls.remove(ball)
                                if ball.radius > 10 and ball.splits_remaining > 0:
                                    self.balls.extend(ball.split())
                                self.other_score += 10
                        break
        else:
            # 單人模式：處理碰撞
            for ball in self.balls[:]:
                for bullet in self.bullets[:]:
                    if ball.is_hit(bullet):
                        self.bullets.remove(bullet)

                        damage = self.calculate_damage()

                        if isinstance(ball, RewardBall):
                            # 獎勵球沒有HP概念，只有被擊中會變大
                            if ball.radius >= ball.max_radius:
                                # 當獎勵球達到最大尺寸時消失，並增加子彈速度
                                self.balls.remove(ball)
                                self.bullets_per_second += 3  # 增加射擊速度
                                if self.shot_delay > 20:  # 防止射擊間隔過短
                                    self.shot_delay -= 5  # 減少射擊間隔
                                self.score += 50  # 額外分數獎勵
                        else:
                            # 普通球的處理邏輯
                            ball.hp -= damage
                            if ball.hp <= 0:
                                self.balls.remove(ball)
                                if ball.radius > 10 and ball.splits_remaining > 0:
                                    self.balls.extend(ball.split())
                                self.score += 10
                        break

    def calculate_damage(self):
        """計算傷害，包含暴擊判定"""
        base_damage = self.damage_per_bullet
        
        # 暴擊判定
        if random.randint(1, 100) <= self.crit_rate:
            return int(base_damage * (self.crit_damage / 100))
        return base_damage
 

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
        
        # FIX: 更新球體狀態（客戶端從主機同步）
        if 'balls' in game_state and self.player_id == 1:
            # 重建球體列表
            self.balls = []
            for ball_data in game_state['balls']:
                if ball_data['type'] == 'reward':
                    ball = RewardBall(ball_data['x'], ball_data['y'])
                    ball.radius = ball_data['radius']
                    # 重新生成縮放後的圖片
                    ball.current_image = ball._get_scaled_image(ball.radius)
                    ball.mask = pygame.mask.from_surface(ball.current_image)
                else:
                    ball = Ball(
                        ball_data['x'], 
                        ball_data['y'], 
                        ball_data['radius'], 
                        ball_data['hp'],
                        ball_data['max_splits']
                    )
                    ball.splits_remaining = ball_data['splits_remaining']
                    # 重新生成對應尺寸的圖片
                    ball.current_image = pygame.transform.scale(
                        ball.current_image,
                        (ball.radius*2, ball.radius*2)
                    )
                    ball.mask = pygame.mask.from_surface(ball.current_image)
                
                # 同步物理參數
                ball.dx = ball_data['dx']
                ball.dy = ball_data['dy']
                self.balls.append(ball)
        
        # 更新對方分數
        if 'other_score' in game_state:
            self.other_score = game_state['other_score']

    def get_player_state(self):
        """獲取當前玩家狀態（用於網路傳輸）"""
        if self.multiplayer:
            bullet_data = [{'x': bullet.x, 'y': bullet.y} for bullet in self.my_bullets]
        else:
            bullet_data = [{'x': bullet.x, 'y': bullet.y} for bullet in self.bullets]
        
        state = {
            'cannon_x': self.my_cannon.x,
            'bullets': bullet_data,
            'score': self.score
        }
        
        # FIX: 如果是主機（玩家0），同步完整的球體狀態
        if self.multiplayer and self.player_id == 0:
            balls_data = []
            for ball in self.balls:
                ball_info = {
                    'x': ball.x,
                    'y': ball.y,
                    'radius': ball.radius,
                    'dx': ball.dx,
                    'dy': ball.dy,
                    'type': 'reward' if isinstance(ball, RewardBall) else 'normal'
                }
                
                if isinstance(ball, RewardBall):
                    # 獎勵球的特殊屬性
                    pass  # 獎勵球只需要基本屬性
                else:
                    # 普通球的額外屬性
                    ball_info.update({
                        'hp': ball.hp,
                        'max_splits': ball.max_splits,
                        'splits_remaining': ball.splits_remaining
                    })
                
                balls_data.append(ball_info)
            
            state['balls'] = balls_data
        
        return state

    def render(self):
        """Render game screen with level information"""
        self.screen.blit(self.background, (0, 0))
        coin_text = self.coin_font.render(f"coins: {self.coins}", True, (255, 215, 0))
        self.screen.blit(coin_text, (self.width - coin_text.get_width() - 20, 10))

        # Draw bullets
        if self.multiplayer:
            for bullet in self.my_bullets: 
                bullet.draw(self.screen)
            for bullet in self.other_bullets:
                bullet.draw(self.screen)
        else:
            for bullet in self.bullets: 
                bullet.draw(self.screen)
        
        # Draw balls
        for ball in self.balls: 
            ball.draw(self.screen)
        
        # Draw cannons
        self.my_cannon.draw(self.screen)
        if self.multiplayer and self.other_cannon:
            self.other_cannon.draw(self.screen)
        
        # Draw score and game info
        if self.multiplayer:
            my_score_text = self.font.render(f"Your Score: {self.score}", True, (0, 0, 0))
            other_score_text = self.font.render(f"Other Score: {self.other_score}", True, (0, 0, 0))
            self.screen.blit(my_score_text, (10, 10))
            self.screen.blit(other_score_text, (10, 40))
            
            bullet_info = self.font.render(f"Bullets per wave: {self.bullets_per_wave}", True, (0, 0, 0))
            self.screen.blit(bullet_info, (10, 70))
        else:
            score_text = self.font.render(f"Score: {self.score}", True, (0, 0, 0))
            self.screen.blit(score_text, (10, 10))
            
            # Show level information
            if self.level_manager:
                level_text = self.font.render(f"Level: {self.level_manager.current_level} - {self.level_manager.get_level_config()['name']}", True, (0, 0, 0))
                self.screen.blit(level_text, (10, 40))
                
                # Show next unlock info
                next_unlock = self.level_manager.get_next_unlock_info()
                if next_unlock:
                    unlock_text = self.font.render(f"Next: {next_unlock['name']} at {next_unlock['required_score']} pts", True, (0, 0, 0))
                    self.screen.blit(unlock_text, (10, 70))
            else:
                speed_info = self.font.render(f"Fire rate: {self.bullets_per_second}/sec", True, (0, 0, 0))
                self.screen.blit(speed_info, (10, 40))

        self.status_panel.draw(self.screen)
        pygame.display.update()

        # ──── 原本若只有簡單 if/else，可整段換成下面 ────
    def apply_card_effect(self, card_name: str):
        """根據 effect dict 套用到屬性"""
        if card_name == "TOYZ(R)":
            self.my_cannon.speed += 3

        if card_name == "一步都沒有退(R)":
            self.damage_per_bullet += 1
            self.bullets_per_second -= 5
            self.bullets_per_second = max(self.bullets_per_second, 5)

        if card_name == "咻碰阿罵(R)":
            self.crit_damage += 25

        if card_name == "張家檸檬綠茶(R)":
            self.coins *= 0.25

        if card_name == "杰哥的麵包(R)":
            self.crit_rate += 15
            self.crit_rate = min(self.crit_rate, 100)

        if card_name == "114514(SR)":
            self.damage_per_bullet += 3

        if card_name == "MVP(SR)":
            self.bullets_per_second += 10
            self.coins -= 500

        if card_name == "圓神啟動(SR)":
            self.crit_rate += 50
            self.crit_rate = min(self.crit_rate, 100)
            self.crit_damage += 75

        if card_name == "最強(SSR)":
            self.bullet_rows += 1
            self.bullet_rows = min(self.bullet_rows, 3)
        
        if card_name == "oop之神(UR)":
            self.crit_rate = 100
            self.crit_damage += 150
            self.damage_per_bullet += 5
            self.bullets_per_second += 20
            self.bullet_rows = 3

    def _show_card_fullscreen(self, img_path: str, duration_ms: int = 3000):
        try:
            card = pygame.image.load(img_path).convert()
        except Exception as e:
            print("載入卡圖失敗：", e)
            return

        sw, sh = self.screen.get_size()
        iw, ih = card.get_size()
        scale = min(sw / iw, sh / ih)
        new_size = (int(iw * scale), int(ih * scale))
        card = pygame.transform.smoothscale(card, new_size)

        rect = card.get_rect(center=(sw // 2, sh // 2))
        start_time = pygame.time.get_ticks()

        running = True
        while running:
            # 處理事件，防止視窗無回應
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            self.screen.fill((0, 0, 0))
            self.screen.blit(card, rect)
            pygame.display.flip()

            if pygame.time.get_ticks() - start_time > duration_ms:
                running = False

            pygame.time.delay(16)  # ~60FPS


    def run(self):
        self.running = True
        while self.running:
            self.handle_events()
            self.handle_input()
            self.update_bullets()
            self.update_balls()
            self.handle_collisions()
            self.check_game_over()

            if self.multiplayer and self.network_manager and self.network_manager.is_connected:
                # 發送與接收網路資料
                self.network_manager.send_player_state(self.get_player_state())
                game_state = self.network_manager.get_game_state()
                if game_state:
                    self.update_from_network(game_state)

            self.render()
            self.clock.tick(60)  # 每秒 60 幀
