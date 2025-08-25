# AIOT_final_project
AI-based Trash Sorting Machine  
實際演示影片:https://www.youtube.com/watch?v=sAg9dxRGvAo  

### 專案介紹
#### 動機
資源回收與垃圾分類是近年來非常熱門的議題，然而許多人缺乏相關知識或懶惰無法有效進行分類，因此我們基於ESP32S3設計一機器可以自動判別投放的垃圾並自動分類到正確的垃圾桶內。

#### 模型訓練
1.資料集採用Kaggle現成資料集、關鍵字爬蟲、自行拍攝三種不同的來源，以涵蓋多種情況豐富資料集  
2.針對每張圖片皆進行微幅旋轉的前處理以應對不同擺放角度的實際垃圾  
3.模型使用resnet進行訓練  
4.以常見廚房垃圾[紙杯、紙餐盒、鐵鋁罐、寶特瓶]做proof of concept

#### 裝置介紹
裝置具有一可傾斜的平台，上方裝有攝影機拍攝照片，透過回傳至電腦判斷後根據垃圾種類旋轉擋板到正確位置並清倒垃圾，同時在網頁上記錄垃圾量以便清潔人員掌握垃圾量  
![image](https://github.com/mengbei0116/AIOT_final_project/blob/main/%E5%9E%83%E5%9C%BE%E5%88%86%E9%A1%9E%E6%A9%9F.png)

### 檔案功能介紹
* ```clean_dataset``` 是各類別訓練資料
* ```model``` 資料夾內有三個 pth 檔案，分別對應 CNN, resnet 18, resnet 50
* ```templates``` 資料夾存放網頁的 html 檔，用於```flask``` 渲染
* ```imagedownload.py``` 用於下載資料集
* ```main.ino``` 用來操控 ESP32 控制各垃圾桶上元件以及與電腦後端進行溝通
* ```server.py``` 用於接收回傳資料，進行種類的判別以及用來架設 ```flask``` 後端

### 操作方法
#### 後端
將server.py執行即可啟動伺服器與網頁    
※須設定該程式內與esp32程式內的網路名稱與密碼
#### 機械結構
將垃圾放至平台即可
#### 網頁
1.網頁上方有不同垃圾的容量門檻值，可設定多少垃圾後觸發告警提醒倒垃圾時機，旁邊的清空按鈕可以重置該垃圾數量  
2.下方可看到垃圾量的折線圖與圓餅圖方便掌握各垃圾數量  
3.在網頁最底端會顯示是否有垃圾大於門檻值  
![image](https://github.com/AIOT_final_project/picture/blob/main/%E7%B6%B2%E9%A0%811.png)
![image](https://github.com/AIOT_final_project/picture/blob/main/%E7%B6%B2%E9%A0%812.png)
