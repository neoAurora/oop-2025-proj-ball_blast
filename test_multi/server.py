
# server.py
import socket
import threading
import pickle
import time

class GameServer:
    def __init__(self, host='0.0.0.0', port=5555):  # ✅ 修改這裡
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        self.players = {}
        self.player_states = {}
        self.max_players = 2
        self.game_started = False
        
    def start_server(self):
        try:
            self.socket.bind((self.host, self.port))
            self.socket.listen(self.max_players)
            print(f"✅ 伺服器啟動在 {self.host}:{self.port}，等待玩家連接...")
            
            while len(self.players) < self.max_players:
                conn, addr = self.socket.accept()
                player_id = len(self.players)
                
                print(f"🎮 玩家 {player_id} 從 {addr} 連接")
                
                initial_data = {
                    'player_id': player_id,
                    'game_ready': len(self.players) == self.max_players - 1
                }
                conn.send(pickle.dumps(initial_data))
                
                self.players[player_id] = conn
                self.player_states[player_id] = {}
                
                thread = threading.Thread(target=self.handle_client, args=(conn, player_id))
                thread.daemon = True
                thread.start()
            
            self.game_started = True
            game_ready_signal = {'game_ready': True}
            for conn in self.players.values():
                try:
                    conn.send(pickle.dumps(game_ready_signal))
                except:
                    pass
            
            print("🎬 遊戲開始！")

            while True:
                time.sleep(1)

        except Exception as e:
            print(f"❌ 伺服器錯誤: {e}")
            self.shutdown()
    
    def handle_client(self, conn, player_id):
        print(f"🔁 開始處理玩家 {player_id}")
        try:
            while True:
                data = conn.recv(4096)
                if not data:
                    break
                
                self.player_states[player_id] = pickle.loads(data)
                other_id = 1 - player_id
                game_state = {}

                if other_id in self.player_states:
                    other = self.player_states[other_id]
                    game_state = {
                        'other_cannon_x': other.get('cannon_x', 300),
                        'other_bullets': other.get('bullets', []),
                        'other_score': other.get('score', 0),
                    }
                    if other_id == 0 and 'balls' in other:
                        game_state['balls'] = other['balls']

                conn.send(pickle.dumps(game_state))
        except Exception as e:
            print(f"❌ 玩家 {player_id} 錯誤: {e}")
        finally:
            self.disconnect_player(player_id)
    
    def disconnect_player(self, player_id):
        if player_id in self.players:
            print(f"🚪 玩家 {player_id} 離線")
            try:
                self.players[player_id].close()
            except:
                pass
            del self.players[player_id]
        
        if player_id in self.player_states:
            del self.player_states[player_id]
    
    def shutdown(self):
        print("🛑 正在關閉伺服器...")
        for player_id in list(self.players.keys()):
            self.disconnect_player(player_id)
        try:
            self.socket.close()
        except:
            pass

def main():
    server = GameServer()
    try:
        server.start_server()
    except KeyboardInterrupt:
        print("\n🛑 使用者中斷伺服器")
        server.shutdown()

if __name__ == "__main__":
    main()
