# src/gateio_framework/client.py

import hashlib
import hmac
import json
import time
import threading
from websocket import WebSocketApp

PING_INTERVAL = 30
event = threading.Event()

class TradingWebSocketGate(WebSocketApp):
    """
    Gate.io WebSocket API v4 Client.
    Manages connection, authentication, and subscriptions.
    """
    def __init__(self, url, api_key, api_secret, **kwargs):
        super(TradingWebSocketGate, self).__init__(url, **kwargs)
        self._api_key = api_key
        self._api_secret = api_secret
        # 啟動心跳執行緒
        threading.Thread(target=self._send_ping, daemon=True).start()

    def _send_ping(self):
        while not event.wait(PING_INTERVAL):
            if self.sock and self.sock.connected:
                try:
                    self.sock.ping()
                    # Gate.io v4 也需要應用層的心跳
                    self._request("spot.ping", auth_required=False)
                except Exception as ex:
                    print(f"send_ping routine terminated: {ex}")
                    break
            else:
                break # 如果連線關閉，則停止心跳

    def _request(self, channel, event=None, payload=None, auth_required=True):
        current_time = int(time.time())
        data = {
            "time": current_time,
            "channel": channel,
            "event": event,
            "payload": payload,
        }
        if auth_required:
            message = f"channel={channel}&event={event}&time={current_time}"
            data["auth"] = {
                "method": "api_key",
                "KEY": self._api_key,
                "SIGN": self._get_sign(message),
            }
        data_str = json.dumps(data)
        self.send(data_str)

    def _get_sign(self, message):
        h = hmac.new(
            self._api_secret.encode("utf8"), message.encode("utf8"), hashlib.sha512
        )
        return h.hexdigest()

    def subscribe(self, channel, payload=None, auth_required=True):
        """Subscribe to a channel."""
        self._request(channel, "subscribe", payload, auth_required)

    def unsubscribe(self, channel, payload=None, auth_required=True):
        """Unsubscribe from a channel."""
        self._request(channel, "unsubscribe", payload, auth_required)