import socket
import threading
import pickle

# Constants
HOST = 'localhost'
PORT = 5555

# Store player positions
players = {
    0: (50, 50),
    1: (250, 250)
}

# Handle each client connection
def handle_client(conn, player_id):
    conn.send(pickle.dumps(players[player_id]))
    while True:
        try:
            data = pickle.loads(conn.recv(1024))
            players[player_id] = data

            # Send other player's data
            other_player_id = 1 - player_id
            reply = players[other_player_id]
            conn.send(pickle.dumps(reply))
        except:
            break

    print(f"Player {player_id} disconnected")
    conn.close()

# Start the server
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(2)
    print("Server started. Waiting for connections...")

    current_player = 0
    while current_player < 2:
        conn, addr = server.accept()
        print(f"Connected to: {addr}")
        threading.Thread(target=handle_client, args=(conn, current_player)).start()
        current_player += 1

start_server()

