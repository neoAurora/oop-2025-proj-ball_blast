import pygame

def play_audio(filename, loop=False):
    """
    Play an audio file using pygame.mixer.
    :param filename: Path to the audio file
    :param loop: Whether to loop the audio (True/False)
    """
    pygame.mixer.init()
    try:
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play(-1 if loop else 0)
    except pygame.error as e:
        print(f"Error loading audio: {e}")
def stop_audio():
    pygame.mixer.music.stop()
/////////////
