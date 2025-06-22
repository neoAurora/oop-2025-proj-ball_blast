import pygame
from moviepy.editor import VideoFileClip
import threading
import time
import os

# === Initialize Pygame ==
pygame.init()
screen = pygame.display.set_mode((640, 360))  # default window size
pygame.display.set_caption("Video Player with Button")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 48)

# === Button Setup ==
button_color = (70, 130, 180)
hover_color = (100, 160, 210)
text_color = (255, 255, 255)
button_rect = pygame.Rect(220, 150, 200, 60)
button_text = font.render("Play Video", True, text_color)

# === Function: Play video with audio ==
def play_video(filename):
    if not os.path.exists(filename):
        print(f"Video file not found: {filename}")
        return

    clip = VideoFileClip(filename)
    pygame.display.set_mode(clip.size)

    def play_audio():
        clip.audio.preview()

    audio_thread = threading.Thread(target=play_audio)
    audio_thread.start()

    for frame in clip.iter_frames(fps=24, dtype='uint8'):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
        screen.blit(surface, (0, 0))
        pygame.display.update()
        clock.tick(24)

    # Reset window to default after video
    pygame.display.set_mode((640, 360))

# === Main Loop ===
playing = False
running = True

while running:
    screen.fill((30, 30, 30))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos) and not playing:
                playing = True
                play_video("test_vid.mp4")  # ← Call the function with video name
                playing = False  # Allow replay

    # Draw button when not playing
    if not playing:
        mouse_pos = pygame.mouse.get_pos()
        color = hover_color if button_rect.collidepoint(mouse_pos) else button_color
        pygame.draw.rect(screen, color, button_rect)
        screen.blit(button_text, (button_rect.x + 25, button_rect.y + 10))

    pygame.display.update()
    clock.tick(60)

pygame.quit()

