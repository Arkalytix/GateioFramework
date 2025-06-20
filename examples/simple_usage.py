import os
import json
import logging
import time
from dotenv import load_dotenv

# 從您的框架套件中匯入主要類別
# 假設您的套件結構是 src/gateio_framework/
from gateio_framework import TradingWebSocketGate, SpotOrderResponseJsonResult

# --- 1. 設定日誌 ---
# 使用 logging 取代 print，可以得到帶有時間戳和級別的輸出，更專業
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- 2. 載入並驗證設定 ---
# 從 .env 檔案載入環境變數
load_dotenv()

API_KEY = os.getenv("GATEIO_API_KEY")
API_SECRET = os.getenv("GATEIO_API_SECRET")
WS_URL = "wss://api.gateio.ws/ws/v4/"

# 檢查金鑰是否存在，如果不存在則提供清晰的錯誤提示並退出
if not API_KEY or not API_SECRET or API_KEY == "YOUR_API_KEY_HERE":
    logging.error("錯誤：請先將 .env.example 複製為 .env，並填入您的 API 金鑰。")
    exit(1)

# --- 3. 定義 WebSocket 事件處理函式 ---

def on_open(ws: TradingWebSocketGate):
    """當 WebSocket 連線成功建立時會被呼叫"""
    logging.info("✅ WebSocket 連線已成功建立。")
    
    # 【重要】優化後的認證流程：
    # 您不需要手動發送登入請求。框架會在您訂閱第一個私有頻道時，
    # 自動處理簽名和認證。
    
    # 範例：訂閱私有「現貨訂單更新」頻道
    channel = "spot.orders"
    # 您可以指定要監聽的交易對，如果為空陣列 `[]` 則代表監聽所有
    payload = ["BTC_USDT", "ETH_USDT"]
    
    logging.info(f"正在訂閱私有頻道 '{channel}'，交易對: {payload}...")
    ws.subscribe(channel, payload, auth_required=True)

def on_message(ws, message: str):
    """當收到來自伺服器的訊息時會被呼叫"""
    data = json.loads(message)
    
    # 排除心跳回應，讓日誌更乾淨
    if data.get('channel') == 'spot.ping':
        return

    logging.info(f"📩 收到訊息: {json.dumps(data, indent=2)}")

    # 處理訂單頻道的訊息
    if data.get("channel") == "spot.orders":
        event = data.get("event")
        
        if event == "subscribe":
            logging.info(f"🎉 成功訂閱頻道: {data['channel']}")
        
        elif event == "update":
            logging.info("📈 收到訂單狀態更新！")
            # Gate.io 的 result 欄位是一個列表
            for order_info in data['result']:
                # 在這裡您可以加上您的交易邏輯
                # 例如：判斷訂單是否完全成交
                if order_info.get('finish_as') == 'filled':
                    logging.info(f"訂單 {order_info.get('id')} 已完全成交！")
                
                # 您也可以使用 SpotOrderResponseJsonResult 來解析
                # 注意：該類別是為「下單請求的回應」設計的，欄位可能略有不同
                # 但如果結構相符，可以這樣使用
                # parsed_order = SpotOrderResponseJsonResult({'result': [order_info]})
                # logging.info(f"解析後的訂單訊息: {parsed_order.get_msg()}")

def on_error(ws, error: Exception):
    """當發生錯誤時會被呼叫"""
    logging.error(f"❌ 發生錯誤: {error}")

def on_close(ws, close_status_code, close_msg):
    """當連線關閉時會被呼叫"""
    logging.warning(f"🔌 WebSocket 連線已關閉。 Code: {close_status_code}, Msg: {close_msg}")

# --- 4. 啟動 WebSocket 客戶端 ---

def main():
    """主執行函式"""
    logging.info("🚀 正在啟動 Gate.io WebSocket 客戶端...")
    
    ws_app = TradingWebSocketGate(
        WS_URL,
        API_KEY,
        API_SECRET,
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
    )
    
    try:
        # run_forever() 會在一個新執行緒中執行，並阻塞主執行緒直到連線關閉
        # 框架內的 ping_interval 已被自動處理，不需在此傳遞
        ws_app.run_forever()
    except KeyboardInterrupt:
        logging.info("手動中斷程式，正在關閉連線...")
        ws_app.close()

if __name__ == "__main__":
    main()