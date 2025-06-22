# network_manager.py          
import socket
import pickle
import threading
import queue

class NetworkManager:
    def __init__(self):
        self.socket = None
        self.is_connected = False
        self.player_id = None
        self.game_state_queue = queue.Queue()
        self.receive_thread = None
        
    def connect_to_server(self, host='localhost', port=5555):
        """連接到伺服器"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((host, port))
            
            # 接收玩家ID和初始遊戲狀態
            initial_data = pickle.loads(self.socket.recv(4096))
            self.player_id = initial_data['player_id']
            self.is_connected = True
            
            # 開始接收線程
            self.receive_thread = threading.Thread(target=self._receive_loop)
            self.receive_thread.daemon = True
            self.receive_thread.start()
            
            return True
        except Exception as e:
            print(f"連接失敗: {e}")
            return False
    
    def _receive_loop(self):
        """接收遊戲狀態的循環"""
        while self.is_connected:
            try:
                data = self.socket.recv(4096)
                if not data:
                    break
                game_state = pickle.loads(data)
                self.game_state_queue.put(game_state)
            except Exception as e:
                print(f"接收數據錯誤: {e}")
                break
        self.is_connected = False
    
    def send_player_state(self, player_state):
        """發送玩家狀態"""
        if self.is_connected:
            try:
                self.socket.send(pickle.dumps(player_state))
            except Exception as e:
                print(f"發送數據錯誤: {e}")
                self.is_connected = False
    
    def get_game_state(self):
        """獲取最新的遊戲狀態"""
        try:
            return self.game_state_queue.get_nowait()
        except queue.Empty:
            return None
    
    def disconnect(self):
        """斷開連接"""
        self.is_connected = False
        if self.socket:
            self.socket.close()
        if self.receive_thread:
            self.receive_thread.join(timeout=1)
