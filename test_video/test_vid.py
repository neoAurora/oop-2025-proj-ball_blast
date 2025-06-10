import pygame
from moviepy.editor import VideoFileClip
import threading
import time

# === Load video using MoviePy ===
clip = VideoFileClip("lemon.mp4")

# === Pygame Setup ===
pygame.init()
screen = pygame.display.set_mode(clip.size)
pygame.display.set_caption("Video with Sound")
clock = pygame.time.Clock()

# === Function to play audio in a separate thread ===
def play_audio():
    clip.audio.preview()  # This will play the audio in real-time

# === Start audio playback ===
audio_thread = threading.Thread(target=play_audio)
audio_thread.start()

# === Play video frames ===
start_time = time.time()
for frame in clip.iter_frames(fps=24, dtype='uint8'):
    # Handle quit events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # Display frame
    surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
    screen.blit(surface, (0, 0))
    pygame.display.update()
    clock.tick(24)

# === Cleanup ===
pygame.quit()
