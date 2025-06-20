# src/gateio_framework/helpers.py

import time
from datetime import datetime, timezone, timedelta
from decimal import Decimal

class TradingWebSocketGateHelper:
    @classmethod
    def get_time(cls):
        now_string = (datetime.now(timezone(timedelta(hours=+8)))).strftime("%Y/%m/%d %H:%M:%S")
        return now_string

    @classmethod
    def get_ts(cls):
        return int(time.time())

    @classmethod
    def get_ts_ms(cls):
        return int(time.time() * 1000)

    @classmethod
    def get_signature(cls, secret, channel, request_param_bytes, ts):
        key = f"api\n{channel}\n{request_param_bytes.decode()}\n{ts}"
        return hmac.new(secret.encode(), key.encode(), hashlib.sha512).hexdigest()

    @classmethod
    def build_login_request(cls, api_key, api_secret):
        ts = TradingWebSocketGateHelper.get_ts()
        req_id = f"{TradingWebSocketGateHelper.get_ts_ms()}-1"
        request_param = b""

        sign = TradingWebSocketGateHelper.get_signature(
            api_secret, "spot.login", request_param, ts
        )

        payload = {
            "api_key": api_key,
            "signature": sign,
            "timestamp": str(ts),
            "req_id": req_id,
        }

        return {"time": ts, "channel": "spot.login", "event": "api", "payload": payload}

    @classmethod
    def build_spot_order_request(cls, text, currency_pair, side, amount, price):
        ts = TradingWebSocketGateHelper.get_ts()
        req_id = f"{TradingWebSocketGateHelper.get_ts_ms()}-2"
        order_param = {
            "text": f"t-{text}",
            "currency_pair": currency_pair,
            "type": "limit",
            "account": "spot",
            "side": side,
            "iceberg": "0",
            "amount": amount,
            "price": price,
            "time_in_force": "gtc",
            "auto_borrow": False,
        }

        payload = {"req_id": req_id, "req_param": order_param}

        return {
            "time": ts,
            "channel": "spot.order_place",
            "event": "api",
            "payload": payload,
        }

    @classmethod
    def cancel_spot_order(cls, currency_pair, side=""):
        time = TradingWebSocketGateHelper.get_ts()
        cancel_param = {
            "side": side,
            "currency_pair": currency_pair,
        }
        if side == "":
            cancel_param = {
                "currency_pair": currency_pair,
            }

        channel = "spot.order_cancel_cp"

        return {
            "time": time,
            "channel": channel,
            "event": "api",
            "payload": {
                "req_id": f"{TradingWebSocketGateHelper.get_ts_ms()}-2",
                "req_param": cancel_param,
            },
        }

class SpotOrderResponseJsonResult:
    def __init__(self, response_json):
        self._resp_result = response_json["result"][0]
        self._finish_as = self._resp_result["finish_as"]
        self._text = self._resp_result["text"]
        self._currency_pair = self._resp_result["currency_pair"]
        self._side = self._resp_result["side"]
        self._amount = self._resp_result["amount"]
        self._price = Decimal(self._resp_result["price"])
        self._finish_as = self._resp_result["finish_as"]

    def get_msg(self):
        ret = f"\r\n{self._currency_pair} {self._finish_as} | {self._side} : {self._price} * {self._amount}"
        return ret

    @property
    def text(self):
        return self._text

    @property
    def currency_pair(self):
        return self._currency_pair

    @property
    def side(self):
        return self._side

    @property
    def amount(self):
        return self._amount

    @property
    def price(self):
        return self._price

    @property
    def finish_as(self):
        return self._finish_as