#include <IRremote.h>
#include <SPI.h>
#include <SD.h>
#include <WiFiNINA.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include <Wire.h>               // I2C 통신 라이브러리 설정
#include <LiquidCrystal_I2C.h>  // I2C LCD 라이브러리 설정
#include "utility/wifi_drv.h"

//================= ir 통신 =================//
const long RECV_PIN = 2; // ir 수신 핀
const long SEND_PIN = 3; // ir 송신 핀
const int PW = 8;
const int user = 9; //기기 선택 publish 버튼
const int VU = 7;
const int VD = 4;
const int CU = 6;
const int CD = 5;

//================= wifi, mqtt =================//
boolean ledStatus = false;
String message; //선택된 기기

//와이파이 연결
const char* ssid = "sssoc";            // wifi 이름
const char* pass = "sssoc12345";       // wifi 비번
int status = WL_IDLE_STATUS;

//mqtt 서버 설정
const char* mqttServer = "192.168.0.10";
const int mqttPort = 1883;            // Port number
//const char* mqttUser = "sssoc";      // User
//const char* mqttPassword = "sssoc"; // Password
//const char* mqttPassword = "sssoc12345"; // Password

//================= sd =================//
#define CS 10
File myFile;
String device0 = "device0.txt";
String device1 = "device1.txt";
String device2 = "device2.txt";

String dev0, dev1, dev2;
uint32_t a0, b0, c0, d0, e0;
uint32_t a1, b1, c1, d1, e1;
uint32_t a2, b2, c2, d2, e2;

String dev_list[3];

//================= sleep =================//
const unsigned long interval = 30000; //interval 지나면 weather화면 진입(30초)
static unsigned long interruptMillis;
static unsigned long sleepMillis;
static unsigned long lcdMillis;

//================= weather =================//
LiquidCrystal_I2C lcd(0x27, 16, 2); // LCD I2C adrress 설정

String APIKEY = "446302348bbbc5716a8191a9f74539b1";
String CityID = "1835848"; // Seoul, KR

WiFiClient nanoclient;
PubSubClient client(nanoclient);     // mqtt client 객체 설정

char servername[]="api.openweathermap.org";
String result; //weather data
 
String weatherDescription ="";
String weatherLocation = "";
String Country;
float Temperature;
float Humidity;
float Pressure;

//===============================================================//
//===========                 SD                     ============//
//===============================================================//

void sd_check()
{ 
  sdLCD(1);
  while (!SD.begin(CS)) {
    Serial.println(F("Initializing SD card..."));
    if (SD.begin(CS))
    {
      Serial.println(F("Card initializing complete."));
    }
    else {
      Serial.println(F("Card Initializing failed, or not present"));
      delay(1000);
    }
  }
}

void sdBegin(){
  sd_check();
  sd_read(device0, dev0, a0, b0, c0, d0, e0);
  sd_read(device1, dev1, a1, b1, c1, d1, e1);
  sd_read(device2, dev2, a2, b2, c2, d2, e2);
  dev_list[0] = dev0;
  dev_list[1] = dev1;
  dev_list[2] = dev2; 

  for (int i = 0; i < sizeof(dev_list) / sizeof(dev_list[0]); i++) {
  Serial.println(dev_list[i]);
  }

  sdLCD(2);
}

void sdLCD(int i)
{
  lcd.init();
  delay(500);
  lcd.clear();
  lcd.backlight();

  if(i==1){
  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print("SD reading");
  delay(500);
  Serial.println("SD reading");
  }

  if(i==2){
  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print("SD complete");
  delay(500);
  Serial.println("SD Complete");
  }
}

void sd_read(const String& filename, String& dev, uint32_t& a, uint32_t& b, uint32_t& c, uint32_t& d, uint32_t& e)
{
  File myFile = SD.open(filename);

  /* 파일 읽어서 시리얼 포트로 출력 */ 
  if (myFile) {
    Serial.println(F("=====File Read Start!========"));
    while(myFile.available()){
        //디바이스 읽기
        dev = myFile.readStringUntil('\n');
        dev.trim(); // 앞 뒤 공백 없앤 스트링 버전 얻음

        // 주파수 읽기
        a = readUInt32FromFile(myFile);
        b = readUInt32FromFile(myFile);
        c = readUInt32FromFile(myFile);
        d = readUInt32FromFile(myFile);
        e = readUInt32FromFile(myFile);

        Serial.println(a);
        Serial.println(b);
        Serial.println(c);
        Serial.println(d);
        Serial.println(e);
    }
    myFile.close();
    Serial.println(F("=====File Read Succeed!======"));
  }
  else {
    Serial.println(F("error opening datalog.txt"));
  }
}

uint32_t readUInt32FromFile(File file) {
  String line = file.readStringUntil('\n');
  line.trim(); // 앞뒤 공백 제거

  // 16진수 문자열을 10진수로 변환
  uint32_t uintValue = strtoul(line.c_str(), NULL, 16);
  
  return uintValue;
}

//===============================================================//
//============                IR                    =============//
//===============================================================//
void irBegin()
{
  IrReceiver.begin(RECV_PIN, ENABLE_LED_FEEDBACK);
  IrSender.begin(SEND_PIN, ENABLE_LED_FEEDBACK, USE_DEFAULT_FEEDBACK_LED_PIN);

}

void irSend(uint32_t a, uint32_t b, uint32_t c, uint32_t d, uint32_t e)
{
  int s_PW = digitalRead(PW);
  int s_VU = digitalRead(VU);
  int s_VD = digitalRead(VD);
  int s_CU = digitalRead(CU);
  int s_CD = digitalRead(CD);

   // TV 전원 역할 스위치 (평상시는 HIGH)
  if (s_PW == HIGH){
    digitalWrite(3, LOW);
  }
  else{
    interruptMillis = millis();
    IrSender.sendNECMSB(a, 32);     
    delay(40);
    check_receive();
  }
  
  // TV 볼륨 업 역할 스위치 (평상시는 HIGH)
  if (s_VU == HIGH) {
    digitalWrite(3, LOW);
  }
  else{
    interruptMillis = millis();
    IrSender.sendNECMSB(b, 32); 
    delay(40);
    check_receive();
  }

  // TV 볼륨 업 역할 스위치 (평상시는 HIGH)
  if (s_VD == HIGH) {
    digitalWrite(3, LOW);
  }
  else{
    interruptMillis = millis();
    IrSender.sendNECMSB(c, 32); 
    delay(40);
    check_receive();
  }
  
  if (s_CU == HIGH) {
    digitalWrite(3, LOW);
  }
  else{
    interruptMillis = millis();
    IrSender.sendNECMSB(d, 32); 
    delay(40);
    check_receive();
  }

  if (s_CD == HIGH) {
    digitalWrite(3, LOW);
  }
  else{
    interruptMillis = millis();
    IrSender.sendNECMSB(e, 32); 
    delay(40);
    check_receive();
  }
}

void check_receive() {
  if(IrReceiver.decode())
  {
      Serial.println();
      Serial.println("Receive");
      Serial.print("LSB: ");
      Serial.println(IrReceiver.decodedIRData.decodedRawData, HEX); //받아지는 LSB raw-data
      unsigned long lsbValue = IrReceiver.decodedIRData.decodedRawData;
      // 이진수로 표현
      String binaryString = String(lsbValue, BIN);

      // 이진수의 길이가 32비트보다 작을 경우, 앞쪽에 0을 추가하여 32비트로 맞춤
      while (binaryString.length() < 32) {
        binaryString = "0" + binaryString;
      }

      // 이진수를 MSB로 반전
      String msbBinaryString;
      for (int i = 31; i >= 0; i--) {
        msbBinaryString += binaryString[i];
      }

      // 16진수로 변환
      unsigned long msbValue = strtoul(msbBinaryString.c_str(), nullptr, 2);
      String msbHexString = String(msbValue, HEX);

      // MSB 결과 출력
      Serial.print("MSB: ");
      Serial.println(msbHexString);

      IrReceiver.printIRResultShort(&Serial);
      IrReceiver.resume();
    }
}

//===============================================================//
//===========                WIFI,MQTT               ============//
//===============================================================//

// 와이파이 연결
void setup_wifi(){  
  while (status != WL_CONNECTED) {
    Serial.print("Attempting to connect to WPA SSID: ");
    Serial.println(ssid); // Connect to WPA/WPA2 network
    status = WiFi.begin(ssid, pass);
    delay(10000); // wait 10 seconds for connection
  }
  Serial.println("You're connected to the wifi network");
}

void mqttBegin()
{
  client.setServer("192.168.0.10", 1883);
  client.setCallback(MQTTcallback);

  while (!client.connected()) {
    Serial.println("Connecting to MQTT...");
    if (client.connect("arduino mqtt")) {
      Serial.println("connected");
    } 
    else {
      Serial.print("failed with state ");
      Serial.println(client.state());  //If you get state 5: mismatch in configuration
      delay(2000);
    }
  }
  client.subscribe("device");
  client.subscribe("registOK");
  Serial.println("subscribe topic: device");
  Serial.println("subscribe topic: registOK");
}

void regBegin()
{
  int i = 0;
  while(digitalRead(PW) == HIGH){
    // lcd 출력으로 수정
    Serial.print("device num: ");
    Serial.print(i);
    //Serial.print(" device name: ");
    //Serial.print(dev_list[i]);
    Serial.println(" 등록하세요.");
    lcdBegin();

    if(digitalRead(PW) == LOW){
    Serial.println("break");
    break;
    }

    String topic = "regist/" + String(i);

    while(digitalRead(user) == HIGH){
      client.loop();
      if (digitalRead(user) == LOW){
        Serial.println("regist 버튼이 눌렸습니다.");
        Serial.println(topic);
        client.publish(topic.c_str(), "regist");
        reg_LCD();

        if(message != "regist/" + String(i))
        {
          client.publish(topic.c_str(), "regist");
        }
        else
        {
          i++;
          delay(500);
          break;
        }
      }
      if(digitalRead(PW) == LOW){
      Serial.println("break");
      break;
      }
    }
  }
}

void mqtt_to_python()
{
  client.loop();
  //버튼을 누른 경우 publish(서버로 보냄)
  if (digitalRead(user) == LOW) {
    interruptMillis = millis();
    Serial.println(" user 버튼이 눌렸습니다.");
    client.publish("user", "user");
    delay(300);
  }
}

// callback 함수
void MQTTcallback(char* topic, byte* payload, unsigned int length) {
  
  message = "";

  Serial.print("Message arrived in topic: ");
  Serial.println(topic);

  Serial.print("Message:");

  for (int i = 0; i < length; i++) {
    message += (char)payload[i];  //Conver *byte to String
  }
  
  Serial.println(message);
  Serial.println("-----------------------");
}

//===============================================================//
//============              LCD                     =============//
//===============================================================//

void lcdBegin()
{
  lcd.init();
  delay(500);
  lcd.clear();
  lcd.backlight();
  lcd.setCursor(0,0);
  lcd.print("Start Regist");
  delay(500);
}


void reg_LCD()
{
  lcdMillis = millis();
  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print("REGISTRATION");
  lcd.setCursor(0,1);
  lcd.print("!COMPLETE!");
  while(lcdMillis+500 > millis()) {
    client.loop();  
  }
}

void control_LCD()
{
  lcdMillis = millis();
  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print("Look Device and");
  lcd.setCursor(0,1);
  lcd.print("Select & Control");
  //delay(1000);
  while(lcdMillis+1000 > millis()) {
    mqtt_to_python();
  }
}

void displayWeather(String location,String description)
{
  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print(location);
  lcd.print(", ");
  lcd.print(Country);
  lcd.setCursor(0,1);
  lcd.print(description);
  client.loop();
}

void displayConditions(float Temperature,float Humidity, float Pressure)
{
  lcd.clear();
  lcd.print("T:"); 
  lcd.print(Temperature,1);
  lcd.print((char)223);
  lcd.print("C ");

  //Printing Humidity
  lcd.print(" H:");
  lcd.print(Humidity,0);
  lcd.print(" %");

  //Printing Pressure
  lcd.setCursor(0,1);
  lcd.print("P: ");
  lcd.print(Pressure,1);
  lcd.print(" hPa");
  client.loop();
}


//===============================================================//
//============              Weather                 =============//
//===============================================================//
void getWeatherData() //client function to send/receive GET request data.
{
  if (nanoclient.connect(servername, 80)) {  //starts client connection, checks for connection
    nanoclient.println("GET /data/2.5/weather?id="+CityID+"&units=metric&APPID="+APIKEY);
    nanoclient.println("Host: api.openweathermap.org");
    nanoclient.println("User-Agent: ArduinoWiFi/1.1");
    nanoclient.println("Connection: close");
    nanoclient.println();
  } 
  else {
    Serial.println("connection failed"); //error message if no client connect
    Serial.println();
  }

  while(nanoclient.connected() && !nanoclient.available()) delay(1); //waits for data
  while (nanoclient.connected() || nanoclient.available()) { //connected or data available
    char c = nanoclient.read(); //gets byte from ethernet buffer
      result = result+c;
    }

  nanoclient.stop(); //stop client
  result.replace('[', ' ');
  result.replace(']', ' ');
  Serial.println(result);

  char jsonArray [result.length()+1];
  result.toCharArray(jsonArray,sizeof(jsonArray));
  jsonArray[result.length() + 1] = '\0';

  StaticJsonBuffer<1024> json_buf;
  JsonObject &root = json_buf.parseObject(jsonArray);
  if (!root.success())
  {
    Serial.println("parseObject() failed");
  }

  String location = root["name"];
  String country = root["sys"]["country"];
  float temperature = root["main"]["temp"];
  float humidity = root["main"]["humidity"];
  String weather = root["weather"]["main"];
  String description = root["weather"]["description"];
  float pressure = root["main"]["pressure"];

  weatherDescription = description;
  weatherLocation = location;
  Country = country;
  Temperature = temperature;
  Humidity = humidity;
  Pressure = pressure;
}

void lcdWeather()
{
  displayWeather(weatherLocation,weatherDescription);
  while (sleepMillis+3000 > millis()) {
    client.loop();
    if (digitalRead(user)==LOW || digitalRead(PW)==LOW ||
    digitalRead(VU)==LOW ||digitalRead(VD)==LOW ||
    digitalRead(CU)==LOW || digitalRead(CD) == LOW) {
      interruptMillis = millis();
      Serial.println("lcdWeather안에서 interrupt 인식");
      sleepMillis = -3000;
      control_LCD();
    }
  }

  displayConditions(Temperature,Humidity,Pressure);
  while (sleepMillis+6000 > millis()) {
    client.loop();
    if (digitalRead(user)==LOW || digitalRead(PW)==LOW ||
    digitalRead(VU)==LOW ||digitalRead(VD)==LOW ||
    digitalRead(CU)==LOW || digitalRead(CD) == LOW) {
      interruptMillis = millis();
      Serial.println("lcdWeather안에서 interrupt 인식");
      sleepMillis = -6000;
      control_LCD();
    }
  }
  client.loop();
}


//===============================================================//
//============              OPERATIION              =============//
//===============================================================//

void check_sleep(){
  //Serial.print("interval : ");
  //Serial.println(millis()-interruptMillis);
  while (millis()-interruptMillis >= interval){
     // 날씨 불러오는 코드 //
     if (millis()-interruptMillis < interval+1000){
      getWeatherData(); // interrupt 들어가기 전에 날씨 한번 불러오기
      // Serial.println("날씨 불러옴");
    }
    sleepMillis = millis();
    lcdWeather(); // lcd 빠져나오면 interruptMillis = millis() 
  }   
}

//===============================================================//
//===========               setup                   =============//
//===============================================================//

void set_pin(){
  pinMode(PW, INPUT_PULLUP);
  pinMode(VU, INPUT_PULLUP);
  pinMode(VD, INPUT_PULLUP);
  pinMode(CU, INPUT_PULLUP);
  pinMode(CD, INPUT_PULLUP);
  pinMode(SEND_PIN, OUTPUT);
  pinMode(user, INPUT_PULLUP);
}

void setup() {

  Serial.begin(9600);
  setup_wifi();
  set_pin();
  sdBegin();
  
  irBegin();
  lcdBegin();
  getWeatherData();

  mqttBegin();
  regBegin();
  interruptMillis = millis();
  delay(1000);

}
        

//===============================================================//
//===========                loop                   =============//
//===============================================================//
void loop() {
  mqtt_to_python();     
  check_sleep();  
  
  switch (message.toInt()){
    case 0:
      control_LCD();
      irSend(a0, b0, c0, d0, e0);
      check_sleep();

      mqtt_to_python();

      if (message != "0"){
        break;
      }
    
    case 1:  
      control_LCD();
      irSend(a1, b1, c1, d1, e1);
      check_sleep();

      mqtt_to_python();
      
      if (message != "1"){
        break;
      }
    
    case 2:  
      control_LCD();
      irSend(a2, b2, c2, d2, e2);
      check_sleep();

      mqtt_to_python();
      
      if (message != "2"){
        break;
      }
    default:
      control_LCD();
      check_sleep();
  }
}
