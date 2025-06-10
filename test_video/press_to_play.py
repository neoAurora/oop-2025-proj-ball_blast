import pygame
from moviepy.editor import VideoFileClip
import threading
import time

# === Load video ===
clip = VideoFileClip("lemon.mp4")

# === Pygame Setup ===
pygame.init()
screen = pygame.display.set_mode(clip.size)
pygame.display.set_caption("Video Player with Button")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 48)

# === Button ===
button_color = (70, 130, 180)
hover_color = (100, 160, 210)
text_color = (255, 255, 255)
button_rect = pygame.Rect(clip.w//2 - 100, clip.h//2 - 30, 200, 60)
button_text = font.render("Play Video", True, text_color)

# === Function to play audio in a thread ===
def play_audio():
    clip.audio.preview()

# === Function to play video ===
def play_video():
    audio_thread = threading.Thread(target=play_audio)
    audio_thread.start()
    start_time = time.time()
    for frame in clip.iter_frames(fps=24, dtype='uint8'):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
        screen.blit(surface, (0, 0))
        pygame.display.update()
        clock.tick(24)

# === Main Loop ===
playing = False
running = True

while running:
    screen.fill((30, 30, 30))  # Background

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos) and not playing:
                playing = True
                play_video()

    # Draw button if not playing
    if not playing:
        mouse_pos = pygame.mouse.get_pos()
        color = hover_color if button_rect.collidepoint(mouse_pos) else button_color
        pygame.draw.rect(screen, color, button_rect)
        screen.blit(button_text, (button_rect.x + 25, button_rect.y + 10))

    pygame.display.update()
    clock.tick(60)

pygame.quit()

