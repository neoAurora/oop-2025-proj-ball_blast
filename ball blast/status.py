# status.py
import pygame

class StatusPanel:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.SysFont("Arial", 23)
        self.title_font = pygame.font.SysFont("Arial", 36)
        self.visible = False
        
    def toggle_visibility(self):
        """切換面板的可見性"""
        self.visible = not self.visible
        
    def draw(self, screen):
        
        """繪製狀態面板"""
        if not self.visible:
            return
            
        # 創建半透明背景
        overlay = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # 半透明黑色
        screen.blit(overlay, (0, 0))
        
        # 面板背景
        panel_width = 400
        panel_height = 400
        panel_x = (screen.get_width() - panel_width) // 2
        panel_y = (screen.get_height() - panel_height) // 2
        
        pygame.draw.rect(screen, (50, 50, 80), (panel_x, panel_y, panel_width, panel_height))
        pygame.draw.rect(screen, (100, 100, 150), (panel_x, panel_y, panel_width, panel_height), 2)
        
        # 標題
        title = self.title_font.render("STATUS PANEL", True, (255, 255, 255))
        screen.blit(title, (panel_x + (panel_width - title.get_width()) // 2, panel_y + 20))
        
        # 狀態資訊
        y_offset = panel_y + 70
        line_height = 40

        # 狀態項目
        status_items = [
            ("CRIT Rate", f"{self.game.crit_rate}%"),
            ("CRIT Damage", f"{self.game.crit_damage}%"),
            ("Fire Rate", f"{self.game.bullets_per_second}/sec"),
            ("Bullet Damage", f"{self.game.damage_per_bullet}"),
            ("Bullet Rows", f"{self.game.bullet_rows}")
        ]
        
        for label, value in status_items:
            # 標籤
            label_text = self.font.render(label + ":", True, (200, 200, 255))
            screen.blit(label_text, (panel_x + 40, y_offset))
            
            # 數值
            value_text = self.font.render(value, True, (255, 255, 255))
            screen.blit(value_text, (panel_x + panel_width - 40 - value_text.get_width(), y_offset))
            
            y_offset += line_height
        
        # 提示文字
        hint = self.font.render("Press S to close", True, (200, 200, 200))
        screen.blit(hint, (panel_x + (panel_width - hint.get_width()) // 2, panel_y + panel_height - 40))
