# leaderboard.py
import pygame
import json
import os
from pygame.locals import *

class Leaderboard:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.leaderboard_file = "leaderboard.json"
        self.leaderboard = []
        self.current_player = ""
        self.font = pygame.font.SysFont("Arial", 24)
        self.title_font = pygame.font.SysFont("Arial", 36)
        self.input_active = True
        self.input_text = ""
        
        # 載入現有排行榜
        self.load_leaderboard()

    def load_leaderboard(self):
        """載入排行榜數據"""
        if os.path.exists(self.leaderboard_file):
            try:
                with open(self.leaderboard_file, 'r') as f:
                    self.leaderboard = json.load(f)
            except:
                self.leaderboard = []
        else:
            self.leaderboard = []

    def save_leaderboard(self):
        """保存排行榜數據"""
        with open(self.leaderboard_file, 'w') as f:
            json.dump(self.leaderboard, f)

    def add_score(self, name, score):
        """添加分數到排行榜"""
        # 檢查是否已有相同名稱的記錄
        player_exists = False
        for entry in self.leaderboard:
            if entry["name"].lower() == name.lower():
                player_exists = True
                # 更新最高分
                if score > entry["score"]:
                    entry["score"] = score
                break
        
        if not player_exists:
            self.leaderboard.append({"name": name, "score": score})
        
        # 按分數排序
        self.leaderboard.sort(key=lambda x: x["score"], reverse=True)
        self.save_leaderboard()

    def get_player_name(self, screen):
        """獲取玩家名稱輸入"""
        input_rect = pygame.Rect(
            self.screen_width//2 - 150, 
            self.screen_height//2, 
            300, 40
        )
        color_active = pygame.Color('lightskyblue3')
        color_passive = pygame.Color('gray15')
        color = color_active if self.input_active else color_passive
        
        clock = pygame.time.Clock()
        
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    return None
                
                if event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        if self.input_text.strip():
                            self.current_player = self.input_text
                            return self.input_text
                    elif event.key == K_BACKSPACE:
                        self.input_text = self.input_text[:-1]
                    else:
                        self.input_text += event.unicode
            
            # 繪製輸入界面
            screen.fill((0, 0, 0))
            
            # 標題
            title = self.title_font.render("Enter Your Name", True, (255, 255, 255))
            screen.blit(title, (self.screen_width//2 - title.get_width()//2, self.screen_height//2 - 100))
            
            # 輸入框
            pygame.draw.rect(screen, color, input_rect, 2)
            text_surface = self.font.render(self.input_text, True, (255, 255, 255))
            screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))
            
            # 提示文字
            prompt = self.font.render("Press ENTER to Continue", True, (200, 200, 200))
            screen.blit(prompt, (self.screen_width//2 - prompt.get_width()//2, self.screen_height//2 + 60))
            
            pygame.display.flip()
            clock.tick(60)

    def show_leaderboard(self, screen, current_score=None):
        """顯示排行榜"""
        clock = pygame.time.Clock()
        
        # 如果有當前分數，添加到排行榜
        if current_score is not None and self.current_player:
            self.add_score(self.current_player, current_score)
        
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    return False
                if event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        return True  # 重新開始遊戲
                    elif event.key == K_ESCAPE:
                        return False  # 退出遊戲
            
            # 繪製排行榜界面
            screen.fill((0, 0, 0))
            
            # 標題
            title = self.title_font.render("Leaderboard", True, (255, 255, 255))
            screen.blit(title, (self.screen_width//2 - title.get_width()//2, 50))
            
            # 當前玩家分數
            if current_score is not None:
                score_text = self.font.render(
                    f"Your Score: {current_score}", 
                    True, (255, 255, 0)
                )
                screen.blit(score_text, (self.screen_width//2 - score_text.get_width()//2, 120))
            
            # 排行榜內容
            for i, entry in enumerate(self.leaderboard[:10]):  # 只顯示前10名
                entry_text = self.font.render(
                    f"{i+1}. {entry['name']}: {entry['score']}", 
                    True, (255, 255, 255)
                )
                screen.blit(
                    entry_text, 
                    (self.screen_width//2 - entry_text.get_width()//2, 180 + i * 40)
                )
            
            # 提示文字
            prompt = self.font.render("Press ENTER to Restart, ESC to Quit", True, (200, 200, 200))
            screen.blit(prompt, (self.screen_width//2 - prompt.get_width()//2, self.screen_height - 100))
            
            pygame.display.flip()
            clock.tick(60)