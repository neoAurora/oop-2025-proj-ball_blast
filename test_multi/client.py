import pygame
import socket
import pickle

# Pygame setup
WIDTH, HEIGHT = 500, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Online Pygame")

# Colors
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Connect to server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 5555))
pos = pickle.loads(client.recv(1024))  # Initial position from server

# Send position, receive other player
def send_pos(position):
    client.send(pickle.dumps(position))
    return pickle.loads(client.recv(1024))

def redraw_window(my_pos, other_pos):
    WIN.fill((0, 0, 0))
    pygame.draw.rect(WIN, BLUE, (*my_pos, 50, 50))
    pygame.draw.rect(WIN, RED, (*other_pos, 50, 50))
    pygame.display.update()

def main():
    global pos
    clock = pygame.time.Clock()
    run = True
    other_pos = (0, 0)

    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        x, y = pos
        if keys[pygame.K_LEFT]: x -= 5
        if keys[pygame.K_RIGHT]: x += 5
        if keys[pygame.K_UP]: y -= 5
        if keys[pygame.K_DOWN]: y += 5
        pos = (x, y)

        other_pos = send_pos(pos)
        redraw_window(pos, other_pos)

    pygame.quit()

main()

