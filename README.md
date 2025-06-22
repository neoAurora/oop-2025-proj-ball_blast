
## 🎮 Ball Blast - Python OOP 射擊遊戲專題

> 這是一款以 Python + Pygame 製作的射擊遊戲，支援單人模式、多人生存模式與抽卡強化系統，展現良好的物件導向程式設計（OOP）架構。

----

## 🧠 專題簡介

本專題以遊戲開發為主軸，結合物件導向程式設計（OOP）與基礎網路通訊，實作一款從 UI 操作、遊戲邏輯到抽卡強化的完整遊戲框架。

### 核心特點：

- 🎯 **單人/雙人遊玩模式**
- 💥 **子彈擊破分裂球體的射擊機制**
- 🌟 **Gacha 抽卡強化系統**
- 📊 **排行榜紀錄與命名**
- 📦 **模組化 OOP 設計：9+ 類別與繼承、多型應用**
- 🌐 **基礎網路對戰（TCP Server / Client）**

----

## 🧩 系統需求

- Python 3.10+
- pygame
- socket
- threading
- json
- 作業系統支援：Windows / macOS / Linux

----

## 🚀 安裝與執行方式

### 1. 下載專案
```bash
git clone https://github.com/your-username/ball-blast-oop-game.git
cd ball-blast-oop-game
```

### 2. 安裝依賴套件
建議使用虛擬環境：
```bash
python -m venv venv
source venv/bin/activate  # mac/Linux
venv\Scripts\activate     # Windows

pip install -r requirements.txt
```

> 若無 `requirements.txt`，可手動安裝：
```bash
pip install pygame
```

### 3. 執行遊戲
```bash
python main.py
```

### 4. 啟動多人模式（選擇 Multiplayer 時）

請先開啟伺服器：
```bash
python server.py
```

----

## 🎮 遊戲操作說明

| 功能        | 鍵盤操作     |
|-------------|--------------|
| 移動        | 左 / 右鍵    |
| 暫停        | ESC          |
| 狀態面板    | S（暫停時）  |
| 抽卡選單    | 主畫面選擇 Gacha |
| 排行榜      | 主畫面選擇 Leaderboard |
| 確認選單    | Enter        |
| 返回 / 退出 | ESC / Q      |

----

## 🧱 專案結構說明

```
ball-blast-oop-game/
│
├── main.py                # 遊戲主程式與主選單控制
├── game.py                # Game 類：遊戲邏輯總控
├── gacha.py               # GachaSystem 類：抽卡邏輯
├── cannon.py              # Cannon 類：玩家砲台
├── bullet.py              # Bullet 類：子彈
├── ball.py                # Ball / RewardBall 類：敵人球體
├── leaderboard.py         # Leaderboard 類：排行榜管理
├── level_manager.py       # LevelManager 類：關卡管理
├── status.py              # StatusPanel 類：顯示強化狀態
├── network_manager.py     # NetworkManager 類：用戶端網路通訊
├── server.py              # GameServer 類：伺服器
├── background.png         # 遊戲背景圖
├── image/                 # 卡牌圖片資料夾
├── leaderboard.json       # 儲存排行榜資料
└── README.md              # 本說明文件
```

----

## 🧠 程式設計特點（OOP 分析）

| 類別          | 責任                          |
|---------------|-------------------------------|
| `Game`        | 控制整體流程、整合所有物件     |
| `Cannon`      | 玩家移動與繪圖                 |
| `Bullet`      | 子彈飛行與碰撞                 |
| `Ball`        | 敵人球體、擊中判定、分裂       |
| `RewardBall`  | 特殊球體、命中後增強效果       |
| `GachaSystem` | 抽卡並套用對應效果             |
| `Leaderboard` | 排行榜儲存與顯示               |
| `StatusPanel` | 顯示當前屬性（暴擊、射速等）   |
| `LevelManager`| 關卡解鎖與設定                 |
| `NetworkManager` | 處理 TCP 客戶端連線        |
| `GameServer`  | 接收並同步多位玩家狀態         |

> ✅ 使用 OOP 原則：封裝、繼承、多型、模組化清晰分工

----

## 📈 未來擴充方向

- ✅ 新增更多關卡與卡牌
- ✅ 更完整的抽卡動畫與卡片說明
- ⏳ 伺服器多人同步畫面優化
- ⏳ UI 音效與特效
- ⏳ 支援儲存遊戲進度 / 記錄成就

----



