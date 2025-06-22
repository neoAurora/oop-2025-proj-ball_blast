# server.py
import socket
import threading
import pickle
import time

class GameServer:
    def __init__(self, host='localhost', port=5555):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        # 遊戲狀態  
        self.players = {}  # {player_id: connection}
        self.player_states = {}  # {player_id: player_state}
        self.max_players = 2
        self.game_started = False
        
    def start_server(self):
        """啟動伺服器"""
        try:
            self.socket.bind((self.host, self.port))
            self.socket.listen(self.max_players)
            print(f"伺服器啟動在 {self.host}:{self.port}")
            print("等待玩家連接...")
            
            while len(self.players) < self.max_players:
                conn, addr = self.socket.accept()
                player_id = len(self.players)
                
                print(f"玩家 {player_id} 從 {addr} 連接")
                
                # 發送初始數據給玩家
                initial_data = {
                    'player_id': player_id,
                    'game_ready': len(self.players) == self.max_players - 1
                }
                conn.send(pickle.dumps(initial_data))
                
                # 儲存玩家連接
                self.players[player_id] = conn
                self.player_states[player_id] = {}
                
                # 為每個玩家創建處理線程
                client_thread = threading.Thread(
                    target=self.handle_client, 
                    args=(conn, player_id)
                )
                client_thread.daemon = True
                client_thread.start()
            
            # 當兩個玩家都連接後，發送遊戲開始信號
            self.game_started = True
            game_ready_signal = {'game_ready': True}
            for player_id, conn in self.players.items():
                try:
                    conn.send(pickle.dumps(game_ready_signal))
                except:
                    pass
            
            print("遊戲開始！")
            
            # 保持伺服器運行
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("伺服器關閉")
                self.shutdown()
                
        except Exception as e:
            print(f"伺服器錯誤: {e}")
            self.shutdown()
    
    def handle_client(self, conn, player_id):
        """處理單個客戶端連接"""
        print(f"開始處理玩家 {player_id}")
        
        try:
            while True:
                # 接收玩家狀態
                data = conn.recv(4096)
                if not data:
                    break
                
                player_state = pickle.loads(data)
                self.player_states[player_id] = player_state
                
                # 準備發送給該玩家的遊戲狀態
                other_player_id = 1 - player_id
                game_state = {}
                
                if other_player_id in self.player_states:
                    other_state = self.player_states[other_player_id]
                    
                    # 發送對方的狀態
                    game_state['other_cannon_x'] = other_state.get('cannon_x', 300)
                    game_state['other_bullets'] = other_state.get('bullets', [])
                    game_state['other_score'] = other_state.get('score', 0)
                    
                    # 如果對方是主機（玩家0），同步球體狀態
                    if other_player_id == 0 and 'balls' in other_state:
                        game_state['balls'] = other_state['balls']
                
                # 發送遊戲狀態給玩家
                conn.send(pickle.dumps(game_state))
                
        except Exception as e:
            print(f"處理玩家 {player_id} 時發生錯誤: {e}")
        finally:
            self.disconnect_player(player_id)
    
    def disconnect_player(self, player_id):
        """斷開玩家連接"""
        if player_id in self.players:
            print(f"玩家 {player_id} 斷開連接")
            try:
                self.players[player_id].close()
            except:
                pass
            del self.players[player_id]
            
        if player_id in self.player_states:
            del self.player_states[player_id]
    
    def shutdown(self):
        """關閉伺服器"""
        print("正在關閉伺服器...")
        
        # 關閉所有玩家連接
        for player_id in list(self.players.keys()):
            self.disconnect_player(player_id)
        
        # 關閉伺服器socket
        try:
            self.socket.close()
        except:
            pass

def main():
    server = GameServer()
    try:
        server.start_server()
    except KeyboardInterrupt:
        print("\n伺服器被用戶中斷")
        server.shutdown()

if __name__ == "__main__":
    main()
