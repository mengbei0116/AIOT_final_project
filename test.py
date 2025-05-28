import requests

# ======= 自訂你要測試的 URL =======
url = "http://127.0.0.1:5000/capture"  # 可改為你的 Flask 伺服器網址
# ===================================

try:
    response = requests.get(url, timeout=10)
    print("📡 已發送 GET 請求到:", url)
    print("🔁 HTTP 狀態碼:", response.status_code)
    print("📨 回傳內容:")
    print(response.text)
except Exception as e:
    print("❌ 請求失敗:", e)
