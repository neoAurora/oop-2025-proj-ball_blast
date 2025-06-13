# main.py
import pygame
import sys
from game import Game
from leaderboard import Leaderboard
from network_manager import NetworkManager

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

def show_main_menu():
    """顯示主選單"""
    first_page = load_image("firstpage.png", (SCREEN_WIDTH, SCREEN_HEIGHT))
    font_title = pygame.font.SysFont("Arial", 48)
    font_option = pygame.font.SysFont("Arial", 32)
    
    clock = pygame.time.Clock()
    blink_timer = 0
    show_text = True
    
    while True:
        screen.blit(first_page, (0, 0))
        
        # 標題
        title = font_title.render("Ball Blast", True, (255, 255, 255))
        title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 150))
        pygame.draw.rect(screen, (0, 0, 0), 
                        (title_rect.x-10, title_rect.y-10, 
                         title_rect.width+20, title_rect.height+20))
        screen.blit(title, title_rect)
        
        # 選項
        single_text = font_option.render("1 - Single Player", True, (255, 255, 255))
        multi_text = font_option.render("2 - Multiplayer", True, (255, 255, 255))
        leaderboard_text = font_option.render("3 - View Leaderboard", True, (255, 255, 255))
        quit_text = font_option.render("ESC - Quit", True, (255, 255, 255))
        
        # 背景框
        options = [single_text, multi_text, leaderboard_text, quit_text]
        y_positions = [380, 420, 460, 500]
        
        for i, (text, y_pos) in enumerate(zip(options, y_positions)):
            text_rect = text.get_rect(center=(SCREEN_WIDTH//2, y_pos))
            pygame.draw.rect(screen, (0, 0, 0), 
                           (text_rect.x-10, text_rect.y-10, 
                            text_rect.width+20, text_rect.height+20))
            screen.blit(text, text_rect)
        
        # 閃爍提示
        blink_timer += 1
        if blink_timer >= 30:
            show_text = not show_text
            blink_timer = 0
        
        if show_text:
            prompt = font_option.render("Choose your option", True, (255, 255, 0))
            prompt_rect = prompt.get_rect(center=(SCREEN_WIDTH//2, 330))
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
                if event.key == pygame.K_1:
                    return "single"
                elif event.key == pygame.K_2:
                    return "multiplayer"
                elif event.key == pygame.K_3:
                    return "leaderboard"
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        
        clock.tick(60)

def show_connection_screen():
    """顯示連線畫面"""
    font_title = pygame.font.SysFont("Arial", 36)
    font_text = pygame.font.SysFont("Arial", 24)
    
    # 創建網路管理器
    network_manager = NetworkManager()
    
    # 嘗試連接
    connecting = True
    connection_attempts = 0
    max_attempts = 5
    
    while connecting and connection_attempts < max_attempts:
        screen.fill((0, 0, 0))
        
        title = font_title.render("Connecting to Server...", True, (255, 255, 255))
        title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 300))
        screen.blit(title, title_rect)
        
        attempt_text = font_text.render(f"Attempt {connection_attempts + 1} of {max_attempts}", True, (255, 255, 255))
        attempt_rect = attempt_text.get_rect(center=(SCREEN_WIDTH//2, 350))
        screen.blit(attempt_text, attempt_rect)
        
        cancel_text = font_text.render("Press ESC to cancel", True, (255, 255, 255))
        cancel_rect = cancel_text.get_rect(center=(SCREEN_WIDTH//2, 400))
        screen.blit(cancel_text, cancel_rect)
        
        pygame.display.flip()
        
        # 檢查取消事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return None
        
        # 嘗試連接
        if network_manager.connect_to_server():
            connecting = False
            break
        
        connection_attempts += 1
        pygame.time.wait(1000)  # 等待1秒後重試
    
    if connecting:
        # 連接失敗
        screen.fill((0, 0, 0))
        failed_text = font_title.render("Connection Failed!", True, (255, 0, 0))
        failed_rect = failed_text.get_rect(center=(SCREEN_WIDTH//2, 300))
        screen.blit(failed_text, failed_rect)
        
        retry_text = font_text.render("Press any key to return to menu", True, (255, 255, 255))
        retry_rect = retry_text.get_rect(center=(SCREEN_WIDTH//2, 350))
        screen.blit(retry_text, retry_rect)
        
        pygame.display.flip()
        
        # 等待按鍵
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    waiting = False
        
        return None
    
    # 連接成功，等待其他玩家
    waiting_for_player = True
    while waiting_for_player:
        screen.fill((0, 0, 0))
        
        success_text = font_title.render("Connected Successfully!", True, (0, 255, 0))
        success_rect = success_text.get_rect(center=(SCREEN_WIDTH//2, 280))
        screen.blit(success_text, success_rect)
        
        player_text = font_text.render(f"You are Player {network_manager.player_id + 1}", True, (255, 255, 255))
        player_rect = player_text.get_rect(center=(SCREEN_WIDTH//2, 320))
        screen.blit(player_text, player_rect)
        
        waiting_text = font_text.render("Waiting for other player...", True, (255, 255, 255))
        waiting_rect = waiting_text.get_rect(center=(SCREEN_WIDTH//2, 360))
        screen.blit(waiting_text, waiting_rect)
        
        cancel_text = font_text.render("Press ESC to cancel", True, (255, 255, 255))
        cancel_rect = cancel_text.get_rect(center=(SCREEN_WIDTH//2, 400))
        screen.blit(cancel_text, cancel_rect)
        
        pygame.display.flip()
        
        # 檢查事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                network_manager.disconnect()
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                network_manager.disconnect()
                return None
        
        # 檢查是否收到遊戲開始信號
        game_state = network_manager.get_game_state()
        if game_state and game_state.get('game_ready'):
            waiting_for_player = False
        
        pygame.time.wait(100)
    
    return network_manager

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

def show_game_over_screen(score, other_score=None, is_multiplayer=False):
    """顯示遊戲結束畫面"""
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 128))
    screen.blit(overlay, (0, 0))
    
    font_large = pygame.font.SysFont("Arial", 48)
    font_medium = pygame.font.SysFont("Arial", 36)
    
    game_over = font_large.render("GAME OVER", True, (255, 0, 0))
    
    if is_multiplayer and other_score is not None:
        your_score_text = font_medium.render(f"Your Score: {score}", True, (255, 255, 255))
        other_score_text = font_medium.render(f"Other Score: {other_score}", True, (255, 255, 255))
        
        if score > other_score:
            result_text = font_medium.render("YOU WIN!", True, (0, 255, 0))
        elif score < other_score:
            result_text = font_medium.render("YOU LOSE!", True, (255, 0, 0))
        else:
            result_text = font_medium.render("TIE!", True, (255, 255, 0))
    else:
        your_score_text = font_medium.render(f"Final Score: {score}", True, (255, 255, 255))
        other_score_text = None
        result_text = None
    
    restart = font_medium.render("Press ENTER to Restart", True, (255, 255, 255))
    quit_text = font_medium.render("Press Q to Quit", True, (255, 255, 255))
    
    # 繪製文字
    screen.blit(game_over, (SCREEN_WIDTH//2 - game_over.get_width()//2, 200))
    
    y_pos = 270
    if result_text:
        screen.blit(result_text, (SCREEN_WIDTH//2 - result_text.get_width()//2, y_pos))
        y_pos += 50
    
    screen.blit(your_score_text, (SCREEN_WIDTH//2 - your_score_text.get_width()//2, y_pos))
    y_pos += 40
    
    if other_score_text:
        screen.blit(other_score_text, (SCREEN_WIDTH//2 - other_score_text.get_width()//2, y_pos))
        y_pos += 60
    else:
        y_pos += 40
    
    screen.blit(restart, (SCREEN_WIDTH//2 - restart.get_width()//2, y_pos))
    screen.blit(quit_text, (SCREEN_WIDTH//2 - quit_text.get_width()//2, y_pos + 40))
    
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

def run_single_player(leaderboard):
    """運行單人遊戲 - 包含排行榜功能"""
    # 獲取玩家名稱
    player_name = leaderboard.get_player_name(screen)
    if player_name is None:  # 玩家關閉了窗口
        return
    
    # 遊戲實例化
    game = Game(screen, multiplayer=False)
    
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
            # 顯示排行榜並獲取是否重新開始
            restart = leaderboard.show_leaderboard(screen, game.score, player_name)
            if restart:
                break  # 重新開始遊戲
            else:
                return
        
        pygame.display.flip()
        pygame.time.Clock().tick(60)

def run_multiplayer(network_manager):
    """運行多人遊戲"""
    game = Game(screen, multiplayer=True, network_manager=network_manager, player_id=network_manager.player_id)
    
    game_active = True
    while game_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                network_manager.disconnect()
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                if not show_pause_screen():
                    game_active = False
                    break
        
        if not game_active:
            break
        
        # 檢查網路連接狀態
        if not network_manager.is_connected:
            print("Connection lost!")
            game_active = False
            break
        
        game.run()
        
        if not game.running:
            if show_game_over_screen(game.score, game.other_score, is_multiplayer=True):
                break  # 重新開始遊戲
            else:
                network_manager.disconnect()
                return
        
        pygame.display.flip()
        pygame.time.Clock().tick(60)
    
    network_manager.disconnect()

def show_leaderboard_only(leaderboard):
    """只顯示排行榜（不遊戲）"""
    leaderboard.show_leaderboard(screen, score=None, player_name=None, view_only=True)

def main():
    """主遊戲循環"""
    leaderboard = Leaderboard(SCREEN_WIDTH, SCREEN_HEIGHT)  # 創建排行榜實例
    
    while True:
        # 顯示主選單
        choice = show_main_menu()
        
        if choice == "single":
            run_single_player(leaderboard)
        elif choice == "multiplayer":
            network_manager = show_connection_screen()
            if network_manager:
                run_multiplayer(network_manager)
        elif choice == "leaderboard":
            show_leaderboard_only(leaderboard)

if __name__ == "__main__":
    main()
