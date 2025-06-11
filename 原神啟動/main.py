# main.py
import pygame
import sys
from game import Game

# 初始化pygame
pygame.init()

# 設置屏幕
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Ball Blast - OOP Project")

def load_image(name, scale=None):
    """加載並可選縮放圖片"""
    try:
        image = pygame.image.load(name)
        if scale:
            image = pygame.transform.scale(image, scale)
        return image
    except pygame.error as e:
        print(f"無法加載圖片: {name}")
        print(e)
        surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        surf.fill((100, 200, 100))
        font = pygame.font.SysFont("Arial", 36)
        text = font.render("圖片加載失敗", True, (0, 0, 0))
        surf.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, 
                         SCREEN_HEIGHT//2 - text.get_height()//2))
        return surf

def show_first_page():
    """顯示首頁圖片，等待用戶按ENTER"""
    first_page = load_image("firstpage.png", (SCREEN_WIDTH, SCREEN_HEIGHT))
    font = pygame.font.SysFont("Arial", 24)
    
    clock = pygame.time.Clock()
    show_prompt = True
    prompt_timer = 0
    
    while True:
        screen.blit(first_page, (0, 0))
        
        prompt_timer += 1
        if prompt_timer >= 30:
            show_prompt = not show_prompt
            prompt_timer = 0
        
        if show_prompt:
            prompt = font.render("Press ENTER to Start", True, (255, 255, 255))
            prompt_rect = prompt.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT - 50))
            pygame.draw.rect(screen, (0, 0, 0), 
                           (prompt_rect.x-10, prompt_rect.y-10, 
                            prompt_rect.width+20, prompt_rect.height+20))
            screen.blit(prompt, prompt_rect)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        
        clock.tick(60)

def show_pause_screen():
    """顯示暫停畫面"""
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 128))
    screen.blit(overlay, (0, 0))
    
    font_large = pygame.font.SysFont("Arial", 48)
    font_medium = pygame.font.SysFont("Arial", 36)
    
    paused = font_large.render("PAUSED", True, (255, 255, 255))
    resume = font_medium.render("Press ESC to Resume", True, (255, 255, 255))
    quit_text = font_medium.render("Press Q to Quit", True, (255, 255, 255))
    
    screen.blit(paused, (SCREEN_WIDTH//2 - paused.get_width()//2, 300))
    screen.blit(resume, (SCREEN_WIDTH//2 - resume.get_width()//2, 400))
    screen.blit(quit_text, (SCREEN_WIDTH//2 - quit_text.get_width()//2, 450))
    
    pygame.display.flip()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return True  # 繼續遊戲
                elif event.key == pygame.K_q:
                    return False  # 退出遊戲
        
        pygame.time.Clock().tick(60)

def show_game_over_screen(score):
    """顯示遊戲結束畫面"""
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 128))
    screen.blit(overlay, (0, 0))
    
    font_large = pygame.font.SysFont("Arial", 48)
    font_medium = pygame.font.SysFont("Arial", 36)
    
    game_over = font_large.render("GAME OVER", True, (255, 0, 0))
    score_text = font_medium.render(f"Final Score: {score}", True, (255, 255, 255))
    restart = font_medium.render("Press ENTER to Restart", True, (255, 255, 255))
    quit_text = font_medium.render("Press Q to Quit", True, (255, 255, 255))
    
    screen.blit(game_over, (SCREEN_WIDTH//2 - game_over.get_width()//2, 250))
    screen.blit(score_text, (SCREEN_WIDTH//2 - score_text.get_width()//2, 320))
    screen.blit(restart, (SCREEN_WIDTH//2 - restart.get_width()//2, 400))
    screen.blit(quit_text, (SCREEN_WIDTH//2 - quit_text.get_width()//2, 450))
    
    pygame.display.flip()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return True  # 重新開始
                elif event.key == pygame.K_q:
                    return False  # 退出
        
        pygame.time.Clock().tick(60)

def main():
    """主遊戲循環"""
    while True:
        show_first_page()
        
        # 遊戲實例化
        game = Game(screen)
        
        # 遊戲主循環
        game_active = True
        while game_active:
            # 處理事件
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    if not show_pause_screen():
                        game_active = False
                        break
            
            if not game_active:
                break
            
            # 運行遊戲幀
            game.run()
            
            # 檢查遊戲結束
            if not game.running:
                print("Game Over! Final Score:", game.score)
                if show_game_over_screen(game.score):
                    break  # 重新開始遊戲
                else:
                    pygame.quit()
                    sys.exit()
            
            pygame.display.flip()
            pygame.time.Clock().tick(60)

if __name__ == "__main__":
    main()