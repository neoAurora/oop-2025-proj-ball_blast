# level_manager.py - New file to manage game levels
import pygame
import json
import os

class LevelManager:
    def __init__(self):
        self.levels = {
            1: {
                'name': 'Beginner',
                'unlock_score': 0,
                'spawn_interval': 300,  # frames between ball spawns
                'ball_hp_min': 20,
                'ball_hp_max': 30,
                'ball_speed_min': 1.0,
                'ball_speed_max': 2.5,
                'reward_ball_chance': 0.2,
                'description': 'Welcome to Ball Blast!'
            },
            2: {
                'name': 'Rookie',
                'unlock_score': 500,
                'spawn_interval': 250,
                'ball_hp_min': 25,
                'ball_hp_max': 35,
                'ball_speed_min': 1.2,
                'ball_speed_max': 2.8,
                'reward_ball_chance': 0.18,
                'description': 'Things are heating up!'
            },
            3: {
                'name': 'Veteran',
                'unlock_score': 1500,
                'spawn_interval': 200,
                'ball_hp_min': 30,
                'ball_hp_max': 45,
                'ball_speed_min': 1.5,
                'ball_speed_max': 3.2,
                'reward_ball_chance': 0.15,
                'description': 'Prepare for battle!'
            },
            4: {
                'name': 'Expert',
                'unlock_score': 3000,
                'spawn_interval': 150,
                'ball_hp_min': 40,
                'ball_hp_max': 55,
                'ball_speed_min': 1.8,
                'ball_speed_max': 3.5,
                'reward_ball_chance': 0.12,
                'description': 'Only the skilled survive!'
            },
            5: {
                'name': 'Master',
                'unlock_score': 5000,
                'spawn_interval': 120,
                'ball_hp_min': 50,
                'ball_hp_max': 70,
                'ball_speed_min': 2.0,
                'ball_speed_max': 4.0,
                'reward_ball_chance': 0.1,
                'description': 'Ultimate challenge awaits!'
            }
        }
        
        self.current_level = 1
        self.player_progress = self.load_progress()
        
    def load_progress(self):
        """Load player progress from file"""
        try:
            if os.path.exists('player_progress.json'):
                with open('player_progress.json', 'r') as f:
                    return json.load(f)
            return {'highest_score': 0, 'unlocked_levels': [1]}
        except:
            return {'highest_score': 0, 'unlocked_levels': [1]}
    
    def save_progress(self):
        """Save player progress to file"""
        try:
            with open('player_progress.json', 'w') as f:
                json.dump(self.player_progress, f)
        except:
            pass
    
    def update_progress(self, score):
        """Update player progress and unlock new levels"""
        if score > self.player_progress['highest_score']:
            self.player_progress['highest_score'] = score
            
            # Check for new level unlocks
            for level_num, level_data in self.levels.items():
                if (score >= level_data['unlock_score'] and 
                    level_num not in self.player_progress['unlocked_levels']):
                    self.player_progress['unlocked_levels'].append(level_num)
            
            self.save_progress()
    
    def get_unlocked_levels(self):
        """Get list of unlocked levels"""
        return sorted(self.player_progress['unlocked_levels'])
    
    def is_level_unlocked(self, level_num):
        """Check if a level is unlocked"""
        return level_num in self.player_progress['unlocked_levels']
    
    def get_level_config(self, level_num=None):
        """Get configuration for a specific level"""
        if level_num is None:
            level_num = self.current_level
        return self.levels.get(level_num, self.levels[1])
    
    def set_current_level(self, level_num):
        """Set the current level"""
        if self.is_level_unlocked(level_num):
            self.current_level = level_num
            return True
        return False
    
    def get_next_unlock_info(self):
        """Get info about the next level to unlock"""
        unlocked = self.get_unlocked_levels()
        if len(unlocked) >= len(self.levels):
            return None
        
        next_level = max(unlocked) + 1
        if next_level in self.levels:
            return {
                'level': next_level,
                'name': self.levels[next_level]['name'],
                'required_score': self.levels[next_level]['unlock_score']
            }
        return None

# Modified game.py sections
class Game:
    def __init__(self, screen, multiplayer=False, network_manager=None, player_id=0, level_manager=None):
        self.screen = screen
        self.width, self.height = screen.get_size()
        self.multiplayer = multiplayer
        self.network_manager = network_manager
        self.player_id = player_id
        self.level_manager = level_manager  # Add level manager
        
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
        
        # Initialize game resources
        self.background = pygame.transform.scale(
            pygame.image.load("background.png").convert(),
            (self.width, self.height)
        )
        
        # Initialize cannons based on game mode
        if multiplayer:
            if player_id == 0:
                self.my_cannon = Cannon(self.width//4, self.height-130)
                self.other_cannon = Cannon(3*self.width//4, self.height-130)
            else:
                self.my_cannon = Cannon(3*self.width//4, self.height-130)
                self.other_cannon = Cannon(self.width//4, self.height-130)
        else:
            self.my_cannon = Cannon(self.width//2, self.height-130)
            self.other_cannon = None
            self.cannon = self.my_cannon
        
        self.font = pygame.font.SysFont("Arial", 24)
        self.reset_game_state()

    def spawn_ball(self):
        """Generate new balls with level-based difficulty"""
        from ball import Ball, RewardBall
        import random
        
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

    def update_balls(self):
        """Update ball status with level-based spawn rate"""
        # Only generate balls for player 0 or single player mode
        if not self.multiplayer or self.player_id == 0:
            self.spawn_timer += 1
            # Use level configuration for spawn interval
            if self.spawn_timer > self.level_config['spawn_interval']:
                self.spawn_timer = 0
                self.spawn_ball()

        # Move balls
        for ball in self.balls:
            ball.move(self.width, self.height)

    def render(self):
        """Render game screen with level information"""
        self.screen.blit(self.background, (0, 0))
        
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

        pygame.display.update()

def show_level_selection(screen, level_manager):
    """Show level selection screen"""
    font_title = pygame.font.SysFont("Arial", 48)
    font_option = pygame.font.SysFont("Arial", 24)
    font_small = pygame.font.SysFont("Arial", 18)
    
    unlocked_levels = level_manager.get_unlocked_levels()
    selected_level = 0
    
    clock = pygame.time.Clock()
    
    while True:
        screen.fill((20, 20, 40))
        
        # Title
        title = font_title.render("Select Level", True, (255, 255, 255))
        title_rect = title.get_rect(center=(screen.get_width()//2, 100))
        screen.blit(title, title_rect)
        
        # Level options
        y_start = 200
        for i, level_num in enumerate(range(1, 6)):  # Show all 5 levels
            is_unlocked = level_num in unlocked_levels
            is_selected = i == selected_level
            
            level_data = level_manager.levels[level_num]
            
            # Background for selected level
            if is_selected:
                pygame.draw.rect(screen, (100, 100, 150), 
                               (50, y_start + i * 80 - 5, screen.get_width() - 100, 70))
            
            # Level name and status
            if is_unlocked:
                color = (255, 255, 255) if is_selected else (200, 200, 200)
                level_text = font_option.render(f"Level {level_num}: {level_data['name']}", True, color)
                desc_text = font_small.render(level_data['description'], True, color)
            else:
                color = (100, 100, 100)
                level_text = font_option.render(f"Level {level_num}: LOCKED", True, color)
                desc_text = font_small.render(f"Unlock at {level_data['unlock_score']} points", True, color)
            
            screen.blit(level_text, (70, y_start + i * 80))
            screen.blit(desc_text, (70, y_start + i * 80 + 30))
        
        # Instructions
        instructions = [
            "Use UP/DOWN arrows to select",
            "Press ENTER to confirm",
            "Press ESC to go back"
        ]
        
        for i, instruction in enumerate(instructions):
            text = font_small.render(instruction, True, (255, 255, 255))
            screen.blit(text, (70, 600 + i * 25))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_level = (selected_level - 1) % 5
                elif event.key == pygame.K_DOWN:
                    selected_level = (selected_level + 1) % 5
                elif event.key == pygame.K_RETURN:
                    chosen_level = selected_level + 1
                    if level_manager.is_level_unlocked(chosen_level):
                        level_manager.set_current_level(chosen_level)
                        return chosen_level
                elif event.key == pygame.K_ESCAPE:
                    return None
        
        clock.tick(60)
