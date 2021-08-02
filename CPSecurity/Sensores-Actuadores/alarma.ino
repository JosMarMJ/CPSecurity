#include <Arduino.h>
#include <ESP8266WiFi.h>
#include "AudioFileSourcePROGMEM.h"
#include "AudioGeneratorWAV.h"
#include "AudioOutputI2SNoDAC.h"

// VIOLA sample taken from https://ccrma.stanford.edu/~jos/pasp/Sound_Examples.html
#include "viola.h"

#include <FirebaseESP8266.h>
//Provide the token generation process info.
#include "addons/TokenHelper.h"
//Provide the RTDB payload printing info and other helper functions.
#include "addons/RTDBHelper.h"

// Set these to run example.
#define FIREBASE_HOST "proyecto-ciber-default-rtdb.firebaseio.com"
#define FIREBASE_AUTH "Zt96LuHznsfJqNxnlwJ4r22KkIGbHjU3Wiv3ASxC"
#define WIFI_SSID "Ivan"
#define WIFI_PASSWORD "12345678"

FirebaseData fbdo;

FirebaseAuth auth;
FirebaseConfig config;
String alarma;

AudioGeneratorWAV *wav;
AudioFileSourcePROGMEM *file;
AudioOutputI2SNoDAC *out;


const int led = 4;
void setup()
{
  Serial.begin(115200);
  // connect to wifi.
  pinMode(led, OUTPUT);
  delay(1000);
  Serial.printf("WAV start\n");

  audioLogger = &Serial;
  file = new AudioFileSourcePROGMEM( viola, sizeof(viola) );
  out = new AudioOutputI2SNoDAC();
  wav = new AudioGeneratorWAV();

  pinMode(led,OUTPUT);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("Conectando");
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(500);
  }
  Serial.println();
  Serial.print("Conectado: ");
  Serial.println(WiFi.localIP());
  Serial.println();
  Serial.printf("Firebase Client v%s\n\n", FIREBASE_CLIENT_VERSION);
  Firebase.begin(FIREBASE_HOST, FIREBASE_AUTH);

  if (Firebase.ready()){
    Serial.println("ready ok");
  }
  else{
    Serial.println("Conexión Fallida");
  }
  
}

void loop()
{


    
  if (wav->isRunning()) {
    digitalWrite(led,HIGH);
    if (!wav->loop()) wav->stop();
  } else {
    Firebase.getString(fbdo, "Proyecto/Alarma", alarma);
    Serial.println(alarma);
    Serial.printf("WAV done\n");
    file = new AudioFileSourcePROGMEM( viola, sizeof(viola) );
    out = new AudioOutputI2SNoDAC();
    wav = new AudioGeneratorWAV();
    if(alarma == "1"){
      wav->begin(file, out); 
    }
    else{
      digitalWrite(led,LOW);
    }
    delay(50);
  }
}
