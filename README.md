# Python Framework for Gate.io WebSocket API v4

[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

一個簡潔、易用的 Python 框架，用於與 [Gate.io](https://www.gate.io/) 的 WebSocket API v4 進行互動。此框架封裝了連線管理、心跳維持、以及私有頻道的簽名認證，讓您可以專注於交易策略的開發。

## 目錄

- [✨ 功能特性](#-功能特性)
- [🔧 安裝與設定](#-安裝與設定)
  - [1. 安裝依賴套件](#1-安裝依賴套件)
  - [2. 取得並設定 API 金鑰](#2-取得並設定-api-金鑰)
- [🚀 快速開始](#-快速開始)
- [📘 API 類別概覽](#-api-類別概覽)
  - [`TradingWebSocketGate`](#tradingwebsocketgate)
  - [`TradingWebSocketGateHelper`](#tradingwebsocketgatehelper)
  - [`SpotOrderResponseJsonResult`](#spotorderresponsejsonresult)
- [🤝 貢獻](#-貢獻)
- [⚠️ 免責聲明](#️-免責聲明)
- [📜 授權條款](#-授權條款)

## ✨ 功能特性

*   **自動連線管理**: 基於 `websocket-client`，穩定可靠。
*   **自動心跳維持**: 自動發送 Ping 訊息，確保 WebSocket 連線不中斷。
*   **內建簽名認證**: 自動處理私有頻道所需的 HMAC-SHA512 簽名。
*   **簡潔的訂閱介面**: 提供 `subscribe()` 和 `unsubscribe()` 方法，輕鬆管理頻道。
*   **請求產生輔助**: 包含 `Helper` 類別，用於快速建構登入、下單、撤單等請求。
*   **物件導向設計**: 程式碼結構清晰，易於擴充與維護。

## 🔧 安裝與設定

### 1. 安裝依賴套件

本框架主要依賴 `websocket-client`。

```bash
pip install websocket-client
```

### 2. 取得並設定 API 金鑰

您需要從 Gate.io 官網取得 API Key 和 Secret Key 才能使用私有頻道（如帳戶查詢、下單等）。

1.  登入 [Gate.io](https://www.gate.io/)，前往「API 管理」頁面建立一組新的 API Key。
2.  請務必給予該 API Key 適當的權限（例如：現貨交易、讀取餘額）。

#### ⚠️ 安全設定指南

**絕對不要將您的 API Key 或 Secret Key 硬編碼（hardcode）在程式碼中！** 最佳實踐是使用環境變數來管理您的金鑰。

**在 Linux / macOS 中設定：**
```bash
export GATEIO_API_KEY="YOUR_API_KEY"
export GATEIO_API_SECRET="YOUR_API_SECRET"
```

**在 Windows (Command Prompt) 中設定：**
```bash
set GATEIO_API_KEY="YOUR_API_KEY"
set GATEIO_API_SECRET="YOUR_API_SECRET"
```

**在 Windows (PowerShell) 中設定：**
```powershell
$env:GATEIO_API_KEY="YOUR_API_KEY"
$env:GATEIO_API_SECRET="YOUR_API_SECRET"
```

## 🚀 快速開始

### 執行範例程式

1.  **安裝依賴套件**:
    ```bash
    pip install python-dotenv
    ```

2.  **設定您的 API 金鑰**:
    -   將專案根目錄下的 `.env.example` 檔案複製一份，並重新命名為 `.env`。
    -   打開 `.env` 檔案，將 `YOUR_API_KEY_HERE` 和 `YOUR_API_SECRET_HERE` 替換成您自己的真實金鑰。
    -   **安全性提醒**: ` .env` 檔案已經被 ` .gitignore` 忽略，請確保不會將此檔案上傳到任何公開的 Git 倉庫。

3.  **執行範例**:
    ```bash
    python examples/simple_usage.py
    ```

    您將會看到程式啟動、連線成功，並開始接收訂單更新的訊息。按下 `Ctrl+C` 可以優雅地關閉程式。


## 📘 API 類別概覽

### `TradingWebSocketGate`
這是框架的核心類別，繼承自 `websocket.WebSocketApp`。
-   **`__init__(self, url, api_key, api_secret, **kwargs)`**: 初始化客戶端，傳入 URL 和 API 金鑰。
-   **`subscribe(self, channel, payload=None, auth_required=True)`**: 訂閱指定頻道。
-   **`unsubscribe(self, channel, payload=None, auth_required=True)`**: 取消訂閱指定頻道。

### `TradingWebSocketGateHelper`
一個靜態輔助類別，用於建構符合 Gate.io API 格式的請求 payload。
-   **`build_login_request(api_key, api_secret)`**: 產生用於 WebSocket 登入的請求。(*注意：本框架已將認證整合進 `subscribe`，通常不需手動呼叫*)。
-   **`build_spot_order_request(...)`**: 建立現貨下單請求。
-   **`cancel_spot_order(...)`**: 建立現貨撤單請求。

### `SpotOrderResponseJsonResult`
一個便利的類別，用於解析和存取已完成訂單的回應 JSON。
-   可以輕鬆地取得 `currency_pair`, `side`, `price`, `amount` 等資訊。

## 🤝 貢獻

歡迎提交 Pull Request 或回報 Issue 來改進這個專案。

## ⚠️ 免責聲明

本軟體按「原樣」提供，不附帶任何明示或暗示的保證。作者不對因使用本軟體而導致的任何財務損失或其他損害承擔責任。

所有交易決策均由您自行負責。在進行真實交易前，請務必在測試環境中充分測試您的策略。**請謹慎保管您的 API 金鑰**。

## 📜 授權條款

本專案採用 [MIT License](https://opensource.org/licenses/MIT) 授權。
