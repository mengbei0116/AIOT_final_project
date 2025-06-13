## 檔案功能介紹
* ```clean_dataset``` 是各類別訓練資料
* ```model``` 資料夾內有三個 pth 檔案，分別對應 CNN, resnet 18, resnet 50
* ```templates``` 資料夾存放網頁的 html 檔，用於```flask``` 渲染
* ```imagedownload.py``` 用於下載資料集
* ```main.ino``` 用來操控 ESP32 控制各垃圾桶上元件以及與電腦後端進行溝通
* ```server.py``` 用於接收回傳資料，進行種類的判別以及用來架設 ```flask``` 後端