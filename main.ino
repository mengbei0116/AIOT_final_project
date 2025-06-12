#include "HX711.h"
#include <Stepper.h>
#include <WiFi.h>
#include <HTTPClient.h>

//------------------------接線設定------------------------
//感重
const int DT_PIN = 7; 
const int SCK_PIN = 6;

//------------------------全域宣告----------------------------
int counter=0;
int weight=0;
int steps_per_rotation=0;
int input=0;
int class_num=0;
int pos=0;
//感重
const int scale_factor = 412; //感重比例參數，從校正程式中取得
HX711 scale;

//傾倒馬達
const int STEPS_PER_REV = 2048;  // 28BYJ-48 一圈約有 2048 步（內部有減速比）
Stepper stepper1(STEPS_PER_REV, 9, 11, 10, 12); // IN1, IN3, IN2, IN4 的順序

//分類馬達
const float DEGREE_PER_STEP = 360.0 / STEPS_PER_REV;
Stepper stepper2(STEPS_PER_REV, 38, 40, 39, 41);  // IN1, IN3, IN2, IN4

//連網資訊
const char* ssid = "";
const char* password = "";
const char* serverURL = "http://192.168.1.113:5000/capture";;  // 改成你的PC IPk
//-----------------------初始化函數---------------------------
void weight_set()
{
  Serial.println("Initializing the scale");
  scale.begin(DT_PIN, SCK_PIN);
  Serial.println("Before setting up the scale:");
   
  Serial.println(scale.get_units(5), 0);  //未設定比例參數前的數值
  scale.set_scale(scale_factor);       // 設定比例參數
  scale.tare();               // 歸零

  Serial.println("After setting up the scale:"); 
}

void drop_set()
{
  stepper1.setSpeed(10); // 設定轉速（RPM）
  steps_per_rotation = STEPS_PER_REV / 8;  //傾倒角度
  Serial.println("傾倒馬達準備就緒");
}

void classify_set()
{
  stepper2.setSpeed(10);  // 設定轉速（建議不要太快）
  Serial.println("分類馬達準備就緒");
}

void internet_set() {
  WiFi.begin(ssid, password);

  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println(" Connected!");
}

//-----------------------功能函數-----------------------------
void drop_garbage()
{
  Serial.println("傾倒垃圾");
  stepper1.step(steps_per_rotation);  // 正方向為順時針
  delay(2000);
  stepper1.step(-steps_per_rotation); // 負方向為逆時針
}

void classify_board(int code, int way)
{
  int temp=code-pos;
  pos=code;
  if(temp==3)
    temp=-1;
  else if(temp==-3)
    temp=1;
  int angle = 0;
  
  // 依照輸入決定要轉的角度（相對）
  switch (temp) {
    case 1: angle = 90; break;
    case 2: angle = 180; break;
    case -2: angle = 180; break;
    case -1: angle = -90; break;
    case 0: angle = 0; break;
    default:
      Serial.println("錯誤：輸入必須為 1~4");
      return;
  }

  
  
  int steps = (angle / DEGREE_PER_STEP) * way;  // 轉換為步數
  stepper2.step(steps);
}

void capturePhoto() {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(serverURL);
    int httpCode = http.GET();
    if (httpCode > 0) {
      String payload = http.getString();
      Serial.println("Response: " + payload);
      class_num=payload[0]-48;
    } else {
      Serial.print("HTTP Error Code: ");
      Serial.println(httpCode);
    }
    http.end();
  } else {
    Serial.println("WiFi Disconnected");
  }
}

void setup() {
  Serial.begin(115200);
  weight_set();
  drop_set();
  classify_set();
  internet_set();

}

void loop() {
  counter=0;
  //判斷是否有垃圾
  while(counter<5)
  {
    weight=scale.get_units(2);
    Serial.print("weight:"); 
    Serial.print(weight);
    if(weight>=10)
      counter+=1;
    else
      counter=0;
    Serial.print(" counter:");
    Serial.println(counter);
  }
  
  capturePhoto();

  //分類
  classify_board(class_num, 1);
  delay(200);
  
  //倒垃圾
  drop_garbage();
  delay(500);
  scale.tare();

}
