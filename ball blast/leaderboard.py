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
        self.title_font = pygame.font.SysFont("Arial", 35)
        self.input_active = True
        self.input_text = ""
        
        # 載入現有排行榜
        self.load_leaderboard()

    def load_leaderboard(self):
        """載入排行榜數據"""
        if os.path.exists(self.leaderboard_file):
            try:
                with open(self.leaderboard_file, 'r', encoding='utf-8') as f:
                    self.leaderboard = json.load(f)
            except:
                self.leaderboard = []
        else:
            self.leaderboard = []

    def save_leaderboard(self):
        """保存排行榜數據"""
        try:
            with open(self.leaderboard_file, 'w', encoding='utf-8') as f:
                json.dump(self.leaderboard, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error saving leaderboard: {e}")

    def add_score(self, name, score):
        """添加分數到排行榜"""
        if not name or score is None:
            return
            
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
        self.input_text = ""
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
                    return None
                
                if event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        if self.input_text.strip():
                            self.current_player = self.input_text.strip()
                            return self.current_player
                    elif event.key == K_BACKSPACE:
                        self.input_text = self.input_text[:-1]
                    elif event.key == K_ESCAPE:
                        return None
                    else:
                        # 限制輸入長度和字符
                        if len(self.input_text) < 20 and event.unicode.isprintable():
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
            
            # 游標
            if pygame.time.get_ticks() % 1000 < 500:  # 閃爍效果
                cursor_x = input_rect.x + 5 + text_surface.get_width()
                pygame.draw.line(screen, (255, 255, 255), 
                               (cursor_x, input_rect.y + 5), 
                               (cursor_x, input_rect.y + input_rect.height - 5), 2)
            
            # 提示文字
            prompt = self.font.render("Press ENTER to Continue, ESC to Cancel", True, (200, 200, 200))
            screen.blit(prompt, (self.screen_width//2 - prompt.get_width()//2, self.screen_height//2 + 60))
            
            pygame.display.flip()
            clock.tick(60)

    def show_leaderboard(self, screen, score=None, player_name=None, view_only=False):
        """顯示排行榜
        
        Args:
            screen: pygame screen object
            score: 當前遊戲分數（可選）
            player_name: 玩家名稱（可選）
            view_only: 是否僅查看模式（不添加分數，不詢問重新開始）
        
        Returns:
            bool: True if restart, False if quit
        """
        clock = pygame.time.Clock()
        
        # 如果有當前分數和玩家名稱，添加到排行榜
        if score is not None and player_name and not view_only:
            self.add_score(player_name, score)
        elif score is not None and self.current_player and not view_only:
            self.add_score(self.current_player, score)
        
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return False
                if event.type == KEYDOWN:
                    if view_only:
                        # 僅查看模式，任意鍵返回
                        return False
                    else:
                        if event.key == K_RETURN:
                            return True  # 重新開始遊戲
                        elif event.key == K_ESCAPE or event.key == K_q:
                            return False  # 退出遊戲
            
            # 繪製排行榜界面
            screen.fill((0, 0, 0))
            
            # 標題
            title = self.title_font.render("Leaderboard", True, (255, 255, 255))
            screen.blit(title, (self.screen_width//2 - title.get_width()//2, 50))
            
            # 當前玩家分數（只在遊戲結束時顯示）
            y_offset = 120
            if score is not None and not view_only:
                current_player_name = player_name or self.current_player
                score_text = self.font.render(
                    f"{current_player_name}'s Score: {score}", 
                    True, (255, 255, 0)
                )
                screen.blit(score_text, (self.screen_width//2 - score_text.get_width()//2, y_offset))
                y_offset += 40
                
                # 分隔線
                pygame.draw.line(screen, (100, 100, 100), 
                               (self.screen_width//4, y_offset + 10), 
                               (3*self.screen_width//4, y_offset + 10), 2)
                y_offset += 30
            
            # 排行榜內容
            if not self.leaderboard:
                no_scores = self.font.render("No scores yet!", True, (200, 200, 200))
                screen.blit(no_scores, (self.screen_width//2 - no_scores.get_width()//2, y_offset))
            else:
                for i, entry in enumerate(self.leaderboard[:10]):  # 只顯示前10名
                    # 高亮當前玩家的記錄
                    text_color = (255, 255, 255)
                    if not view_only and score is not None:
                        current_name = player_name or self.current_player
                        if entry['name'].lower() == current_name.lower():
                            text_color = (255, 255, 0)
                    
                    # 排名圖標
                    rank_color = (255, 215, 0) if i == 0 else (192, 192, 192) if i == 1 else (205, 127, 50) if i == 2 else (255, 255, 255)
                    
                    entry_text = self.font.render(
                        f"{i+1}. {entry['name']}: {entry['score']}", 
                        True, text_color
                    )
                    
                    # 添加排名背景
                    if i < 3:
                        rank_rect = pygame.Rect(self.screen_width//2 - entry_text.get_width()//2 - 10, 
                                              y_offset - 5, 
                                              entry_text.get_width() + 20, 
                                              entry_text.get_height() + 10)
                        pygame.draw.rect(screen, (*rank_color, 30), rank_rect)
                        pygame.draw.rect(screen, rank_color, rank_rect, 1)
                    
                    screen.blit(
                        entry_text, 
                        (self.screen_width//2 - entry_text.get_width()//2, y_offset)
                    )
                    y_offset += 35
            
            # 提示文字
            if view_only:
                prompt = self.font.render("Press any key to return to menu", True, (200, 200, 200))
            else:
                prompt = self.font.render("Press ENTER to Restart, ESC/Q to Quit", True, (200, 200, 200))
            screen.blit(prompt, (self.screen_width//2 - prompt.get_width()//2, self.screen_height - 60))
            
            pygame.display.flip()
            clock.tick(60)
