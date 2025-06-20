# main.py - Fixed version with proper imports and level system
import pygame
import sys
from game import Game
from leaderboard import Leaderboard
from network_manager import NetworkManager
from level_manager import LevelManager

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

def show_main_menu():
    """Modified main menu to include level selection"""
    first_page = load_image("firstpage.png", (SCREEN_WIDTH, SCREEN_HEIGHT))
    font_title = pygame.font.SysFont("Arial", 48)
    font_option = pygame.font.SysFont("Arial", 32)
    
    clock = pygame.time.Clock()
    blink_timer = 0
    show_text = True
    
    while True:
        screen.blit(first_page, (0, 0))
        
        # Title
        title = font_title.render("Ball Blast", True, (255, 255, 255))
        title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 150))
        pygame.draw.rect(screen, (0, 0, 0), 
                        (title_rect.x-10, title_rect.y-10, 
                         title_rect.width+20, title_rect.height+20))
        screen.blit(title, title_rect)
        
        # Modified options to include level selection
        single_text = font_option.render("1 - Single Player", True, (255, 255, 255))
        levels_text = font_option.render("2 - Select Level", True, (255, 255, 255))
        multi_text = font_option.render("3 - Multiplayer", True, (255, 255, 255))
        leaderboard_text = font_option.render("4 - View Leaderboard", True, (255, 255, 255))
        quit_text = font_option.render("ESC - Quit", True, (255, 255, 255))
        
        # Background frames
        options = [single_text, levels_text, multi_text, leaderboard_text, quit_text]
        y_positions = [360, 400, 440, 480, 520]
        
        for i, (text, y_pos) in enumerate(zip(options, y_positions)):
            text_rect = text.get_rect(center=(SCREEN_WIDTH//2, y_pos))
            pygame.draw.rect(screen, (0, 0, 0), 
                           (text_rect.x-10, text_rect.y-10, 
                            text_rect.width+20, text_rect.height+20))
            screen.blit(text, text_rect)
        
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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return "single"
                elif event.key == pygame.K_2:
                    return "levels"
                elif event.key == pygame.K_3:
                    return "multiplayer"
                elif event.key == pygame.K_4:
                    return "leaderboard"
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        
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

def show_pause_screen():
    """Show pause screen"""
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
                    return True  # Continue game
                elif event.key == pygame.K_q:
                    return False  # Quit game
        
        pygame.time.Clock().tick(60)

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

def run_single_player(leaderboard, level_manager=None, selected_level=None):
    """Modified single player with level support"""
    # Get player name
    player_name = leaderboard.get_player_name(screen)
    if player_name is None:
        return
    
    # Set level if specified
    if level_manager and selected_level:
        level_manager.set_current_level(selected_level)
    
    # Create game instance with level manager
    game = Game(screen, multiplayer=False, level_manager=level_manager)
    
    # Game main loop
    game_active = True
    while game_active:
        # Handle events
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
        
        # Run game frame
        game.run()
        
        # Check game over
        if not game.running:
            print("Game Over! Final Score:", game.score)
            
            # Update level progress
            if level_manager:
                level_manager.update_progress(game.score)
            
            # Show leaderboard and get restart choice
            restart = leaderboard.show_leaderboard(screen, game.score, player_name)
            if restart:
                break  # Restart game
            else:
                return
        
        pygame.display.flip()
        pygame.time.Clock().tick(60)

def run_multiplayer(network_manager):
    """Run multiplayer game"""
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

def show_leaderboard_only(leaderboard):
    """Show leaderboard only (no game)"""
    leaderboard.show_leaderboard(screen, score=None, player_name=None, view_only=True)

def main():
    """Modified main function with level system"""
    leaderboard = Leaderboard(SCREEN_WIDTH, SCREEN_HEIGHT)
    level_manager = LevelManager()  # Create level manager
    
    while True:
        # Show main menu
        choice = show_main_menu()
        
        if choice == "single":
            # Run single player with level 1
            run_single_player(leaderboard, level_manager, selected_level=1)
        elif choice == "levels":  # New option
            # Show level selection
            selected_level = show_level_selection(screen, level_manager)
            if selected_level:
                run_single_player(leaderboard, level_manager, selected_level)
        elif choice == "multiplayer":
            network_manager = show_connection_screen()
            if network_manager:
                run_multiplayer(network_manager)
        elif choice == "leaderboard":
            show_leaderboard_only(leaderboard)

if __name__ == "__main__":
    main()
