# main.py - Fixed version with proper imports and level system
import pygame
import sys
import threading
import os
import time
from game import Game
from leaderboard import Leaderboard
from network_manager import NetworkManager
from level_manager import LevelManager
from moviepy.editor import VideoFileClip


# Initialize pygame
pygame.init()

# Screen settings
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Ball Blast - OOP Project")

def load_image(name, scale=None):
    """Load and optionally scale images"""
    try:
        image = pygame.image.load(name)
        if scale:
            image = pygame.transform.scale(image, scale)
        return image
    except pygame.error as e:
        print(f"Cannot load image: {name}")
        print(e)
        surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        surf.fill((100, 200, 100))
        font = pygame.font.SysFont("Arial", 36)
        text = font.render("Image Load Failed", True, (0, 0, 0))
        surf.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, 
                         SCREEN_HEIGHT//2 - text.get_height()//2))
        return surf

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

def show_main_menu(game_instance=None):
    """Modified main menu to include level selection"""
    first_page = load_image("firstpage.png", (SCREEN_WIDTH, SCREEN_HEIGHT))
    font_title = pygame.font.SysFont("Arial", 48)
    font_option = pygame.font.SysFont("Arial", 32)
    
    clock = pygame.time.Clock()
    blink_timer = 0
    show_text = True
    
    while True:
        screen.blit(first_page, (0, 0))
    
        # Modified options to include level selection
        single_text = font_option.render("1 - Single Player", True, (255, 255, 255))
        levels_text = font_option.render("2 - Select Level", True, (255, 255, 255))
        multi_text = font_option.render("3 - Multiplayer", True, (255, 255, 255))
        leaderboard_text = font_option.render("4 - View Leaderboard", True, (255, 255, 255))
        gacha_text = font_option.render("5 - gacha", True, (255, 255, 255))
        quit_text = font_option.render("ESC - Quit", True, (255, 255, 255))

        # Background frames
        buttons = [
            ("1 - Single Player", "single"),
            ("2 - Select Level", "levels"),
            ("3 - Multiplayer", "multiplayer"),
            ("4 - Gacha", "gacha"),
            ("5 - View Leaderboard", "leaderboard"),
            ("ESC - Quit", "quit"),
        ]

        button_rects = []
        button_font = pygame.font.SysFont("Arial", 32)

        y_start = 400
        button_w, button_h = 360, 50

        mouse_pos = pygame.mouse.get_pos()

        for i, (label, action) in enumerate(buttons):
            x = SCREEN_WIDTH // 2 - button_w // 2
            y = y_start + i * 60

            rect = pygame.Rect(x, y, button_w, button_h)

            # 懸停特效
            is_hovered = rect.collidepoint(mouse_pos)
            color = (70, 120, 200) if is_hovered else (40, 40, 60)

            pygame.draw.rect(screen, color, rect, border_radius=12)

            # 陰影效果（內框）
            pygame.draw.rect(screen, (100, 100, 150), rect, width=2, border_radius=12)

            text_surface = button_font.render(label, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=rect.center)
            screen.blit(text_surface, text_rect)
             # ✅ 把 rect 和對應動作一起存起來
            button_rects.append((rect, action))
        
        # Blinking prompt
        blink_timer += 1
        if blink_timer >= 30:
            show_text = not show_text
            blink_timer = 0
        
        if show_text:
            prompt = font_option.render("Choose your option", True, (255, 255, 0))
            prompt_rect = prompt.get_rect(center=(SCREEN_WIDTH//2, 310))
            pygame.draw.rect(screen, (0, 0, 0), 
                           (prompt_rect.x-10, prompt_rect.y-10, 
                            prompt_rect.width+20, prompt_rect.height+20))
            screen.blit(prompt, prompt_rect)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return "single"
                elif event.key == pygame.K_2:
                    return "levels"
                elif event.key == pygame.K_3:
                    return "multiplayer"
                elif event.key == pygame.K_4:
                    return "gacha"
                elif event.key == pygame.K_5:  
                    return "leaderboard"
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()      
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for rect, action in button_rects:
                    if rect.collidepoint(event.pos):
                        return action
        
        clock.tick(60)

# main.py 新增函式
def show_gacha_menu(game):
    """顯示抽卡選單"""
    font_title = pygame.font.SysFont("Arial", 36)
    font_option = pygame.font.SysFont("Arial", 24)
    font_small = pygame.font.SysFont("Arial", 18)
    
    clock = pygame.time.Clock()
    result_card = None
    result_timer = 0
    
    while True:
        screen.fill((20, 20, 40))
        
        # 顯示金幣數量
        coin_text = font_option.render(f"coins: {game.coins}", True, (255, 215, 0))
        screen.blit(coin_text, (20, 20))
        
        # 標題
        title = font_title.render("banner", True, (255, 255, 255))
        title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 100))
        screen.blit(title, title_rect)
        
        # 抽卡按鈕
        draw_button = pygame.Rect(SCREEN_WIDTH//2 - 100, 200, 200, 50)
        pygame.draw.rect(screen, (70, 70, 120), draw_button)
        
        if game.gacha_system.can_draw():
            draw_text = font_option.render("pull (100coins)", True, (255, 255, 255))

        if not game.gacha_system.can_draw():
            ad_button = pygame.Rect(SCREEN_WIDTH//2 - 100, 300, 200, 50)
            pygame.draw.rect(screen, (70, 120, 70), ad_button)
            ad_text = font_option.render("watch ad (free)", True, (255, 255, 255))
            ad_text_rect = ad_text.get_rect(center=ad_button.center)
            screen.blit(ad_text, ad_text_rect)
        
        draw_text_rect = draw_text.get_rect(center=draw_button.center)
        screen.blit(draw_text, draw_text_rect)
        

        # 返回按鈕
        back_button = pygame.Rect(SCREEN_WIDTH//2 - 100, 400, 200, 50)
        pygame.draw.rect(screen, (120, 70, 70), back_button)
        back_text = font_option.render("return", True, (255, 255, 255))
        back_text_rect = back_text.get_rect(center=back_button.center)
        screen.blit(back_text, back_text_rect)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if draw_button.collidepoint(mouse_pos) and game.gacha_system.can_draw():
                    result_card = game.gacha_system.draw_card()
                    if result_card:
                        name, img_path, effect, rarity = result_card
                        game._animate_card_draw(img_path)  # ✅ 在這裡只播一次動畫
                elif not game.gacha_system.can_draw() and ad_button.collidepoint(mouse_pos):
                    play_ad_and_draw(game)
                elif back_button.collidepoint(mouse_pos):
                    return game
        
        clock.tick(60)

def show_connection_screen():
    """Show connection screen"""
    font_title = pygame.font.SysFont("Arial", 36)
    font_text = pygame.font.SysFont("Arial", 24)
    
    # Create network manager
    network_manager = NetworkManager()
    
    # Try to connect
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
        
        # Check for cancel events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return None
        
        # Try to connect
        if network_manager.connect_to_server():
            connecting = False
            break
        
        connection_attempts += 1
        pygame.time.wait(1000)  # Wait 1 second before retry
    
    if connecting:
        # Connection failed
        screen.fill((0, 0, 0))
        failed_text = font_title.render("Connection Failed!", True, (255, 0, 0))
        failed_rect = failed_text.get_rect(center=(SCREEN_WIDTH//2, 300))
        screen.blit(failed_text, failed_rect)
        
        retry_text = font_text.render("Press any key to return to menu", True, (255, 255, 255))
        retry_rect = retry_text.get_rect(center=(SCREEN_WIDTH//2, 350))
        screen.blit(retry_text, retry_rect)
        
        pygame.display.flip()
        
        # Wait for key press
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    waiting = False
        
        return None
    
    # Connection successful, wait for other player
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
        
        # Check events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                network_manager.disconnect()
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                network_manager.disconnect()
                return None
        
        # Check if game ready signal received
        game_state = network_manager.get_game_state()
        if game_state and game_state.get('game_ready'):
            waiting_for_player = False
        
        pygame.time.wait(100)
    
    return network_manager

def show_pause_screen(game):
    """Show pause screen with status panel support"""
    clock = pygame.time.Clock()
    
    pause_background = screen.copy()  # ✅ 抓當下畫面當背景

    while True:
        # 繪製暫停畫面
        screen.blit(pause_background, (0, 0))  # ✅ 顯示遊戲背景
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        screen.blit(overlay, (0, 0))
        
        font_large = pygame.font.SysFont("Arial", 48)
        font_medium = pygame.font.SysFont("Arial", 36)
        
        paused = font_large.render("PAUSED", True, (255, 255, 255))
        resume = font_medium.render("Press ESC to Resume", True, (255, 255, 255))
        status_text = font_medium.render("Press S for Status", True, (255, 255, 255))
        quit_text = font_medium.render("Press Q to Quit", True, (255, 255, 255))
        
        screen.blit(paused, (SCREEN_WIDTH//2 - paused.get_width()//2, 300))
        screen.blit(resume, (SCREEN_WIDTH//2 - resume.get_width()//2, 400))
        screen.blit(status_text, (SCREEN_WIDTH//2 - status_text.get_width()//2, 450))
        screen.blit(quit_text, (SCREEN_WIDTH//2 - quit_text.get_width()//2, 500))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return True  # 繼續遊戲
                elif event.key == pygame.K_s:
                    game.status_panel.toggle_visibility()
                    pause_background = screen.copy()
                    while game.status_panel.visible:
                        screen.blit(pause_background, (0, 0))  # 靜態畫面
                        game.status_panel.draw(screen)
                        pygame.display.flip()
                        for ev in pygame.event.get():
                            if ev.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()
                            if ev.type == pygame.KEYDOWN and ev.key == pygame.K_s:
                                game.status_panel.toggle_visibility()
                elif event.key == pygame.K_q:
                    return False  # 退出遊戲
        
        clock.tick(60)

def show_game_over_screen(score, other_score=None, is_multiplayer=False):
    """Show game over screen"""
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
    
    # Draw text
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
                    return True  # Restart
                elif event.key == pygame.K_q:
                    return False  # Quit
        
        pygame.time.Clock().tick(60)

def run_single_player(leaderboard, level_manager=None, selected_level=None, game=None):
    """單人模式主流程：使用現有 Game 實例，否則建立新的。"""
    global game_instance

    # 玩家名稱輸入
    player_name = leaderboard.get_player_name(screen)
    if player_name is None:
        return game_instance

    # 如果有傳入舊的 game（例如從抽卡過來），就沿用它
    if game is not None:
        game_instance = game
    elif game_instance is None:
        # 否則第一次進入，創建新的 Game 實例
        game_instance = Game(screen, multiplayer=False, level_manager=level_manager)

    # 設定關卡
    if level_manager and selected_level:
        level_manager.set_current_level(selected_level)

    game = game_instance  # 確保使用的是正確的 Game
    game.reset_game_state()
    game.run()

    # 遊戲結束給金幣獎勵
    reward = game.score // 10
    game.coins += reward
    print(f"Game Over! Final Score: {game.score}\n獲得{reward}金幣！")

    return game


def run_multiplayer(network_manager):
    """Run multiplayer game"""    
    game = Game(screen, multiplayer=True, network_manager=network_manager, player_id=network_manager.player_id)
    global game_instance  # 讓主循環可以訪問
    game_instance = game

    game_active = True
    while game_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                network_manager.disconnect()
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                if not show_pause_screen(game):
                    game_active = False
                    break
        
        if not game_active:
            break
        
        # Check network connection status
        if not network_manager.is_connected:
            print("Connection lost!")
            game_active = False
            break
        
        game.run()
        
        if not game.running:
            if show_game_over_screen(game.score, game.other_score, is_multiplayer=True):
                break  # Restart game
            else:
                network_manager.disconnect()
                return
        
        pygame.display.flip()
        pygame.time.Clock().tick(60)
    
    network_manager.disconnect()
    return game 

def show_leaderboard_only(leaderboard):
    """Show leaderboard only (no game)"""
    leaderboard.show_leaderboard(screen, score=None, player_name=None, view_only=True)

def play_video(filename, screen):
    """播放影片並帶有聲音，不改變原來的視窗大小"""
    if not os.path.exists(filename):
        print(f"Video file not found: {filename}")
        return

    clip = VideoFileClip(filename)
    sw, sh = screen.get_size()
    frame_delay = 1 / 28

    def play_audio():
        clip.audio.preview()

    audio_thread = threading.Thread(target=play_audio)
    audio_thread.start()

    for frame in clip.iter_frames(fps=24, dtype='uint8'):
        start_time = time.time()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        # 影片幀轉 surface 並縮放到遊戲畫面大小
        surf = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
        surf = pygame.transform.scale(surf, (sw, sh))
        screen.blit(surf, (0, 0))
        pygame.display.update()

        # 控制播放速度
        elapsed = time.time() - start_time
        time.sleep(max(0, frame_delay - elapsed))
        

def play_ad_and_draw(game):
    """播放廣告影片，影片結束後免費抽一次卡"""
    screen = game.screen
    play_video("lemon.mp4", screen)  # 播放影片（請確保檔案存在）

    card = game.gacha_system.draw_card_for_free()
    if card:
        name, img_path, effect, rarity = card
        game._animate_card_draw(img_path)
    
def main():
    global game_instance  # ✅ 讓其他函式能使用它
    game_instance = None  # ✅ 避免第一次使用時出現未定義錯
    """Modified main function with level system"""
    leaderboard = Leaderboard(SCREEN_WIDTH, SCREEN_HEIGHT)
    level_manager = LevelManager()  # Create level manager
    
    while True:
        # 修改這裡，傳遞 game_instance 參數
        choice = show_main_menu(game_instance)
        
        if choice == "single":
            # Run single player with level 1
            game_instance = run_single_player(leaderboard, level_manager, selected_level=1, game=game_instance)
        elif choice == "levels":  # New option
            # Show level selection
            selected_level = show_level_selection(screen, level_manager)
            if selected_level:
                game_instance = run_single_player(leaderboard, level_manager, selected_level)
        elif choice == "multiplayer":
            network_manager = show_connection_screen()
            if network_manager:
                game_instance = run_multiplayer(network_manager)
        elif choice == "gacha":  # 新增抽卡選項
            if game_instance is None:
                game_instance = Game(screen, multiplayer=False, level_manager=level_manager)
            game_instance = show_gacha_menu(game_instance)
        elif choice == "leaderboard":
            show_leaderboard_only(leaderboard)
        

if __name__ == "__main__":
    main()
