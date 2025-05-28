import requests
import datetime
import os
import time

# 設定 ESP32 Camera 快照網址
camera_url = "http://192.168.99.15/capture"  # 改為你的 ESP32 IP

# 設定要儲存的資料夾
save_folder = "captured_images"

# 確保資料夾存在
os.makedirs(save_folder, exist_ok=True)

def capture_and_save():
    try:
        response = requests.get(camera_url, timeout=10)
        if response.status_code == 200:
            # 檔案名稱加時間戳
            filename = datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + ".jpg"
            filepath = os.path.join(save_folder, filename)
            
            # 儲存圖片
            with open(filepath, 'wb') as f:
                f.write(response.content)
            print(f"✅ 圖片已儲存: {filepath}")
        else:
            print(f"❌ HTTP狀態: {response.status_code}")
    except Exception as e:
        print(f"❌ 錯誤: {e}")

# 自動每5秒抓取一次
while True:
    capture_and_save()
    time.sleep(5)
