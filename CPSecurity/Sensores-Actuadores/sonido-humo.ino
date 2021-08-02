#include <WiFiClient.h>
#include <ESP8266WiFi.h>
#include "FirebaseESP8266.h"

//pines
int MIC = 9;        // D0 de modulo a pin 2
int VALOR;        // variable para almacenar valor de D0
int humo = 0;        //Analogo 0
#define FIREBASE_HOST "proyecto-ciber-default-rtdb.firebaseio.com"
#define FIREBASE_AUTH "Zt96LuHznsfJqNxnlwJ4r22KkIGbHjU3Wiv3ASxC" 

//Credenciales
const char* ssid = "NETLIFE-PANELA";
const char* password = "$0uthP4rk";

FirebaseData firebaseData;

void setup(){
  pinMode(MIC, INPUT);      // pin 2 como entrada
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  Serial.print("Conectando");

  while(WiFi.status()!=WL_CONNECTED){
    delay(500);
    Serial.print(".");
    }  
  Serial.println("WiFi conectado");
  Firebase.begin(FIREBASE_HOST, FIREBASE_AUTH);
  Firebase.reconnectWiFi(true);
}


void loop(){
  //Sonido
  VALOR = digitalRead(MIC);   // obtiene valor de D0
  if (VALOR == HIGH){     // si D0 tiene un valor alto
    Firebase.setInt(firebaseData,"/Proyecto/Sonido",1);
    }else{
    Firebase.setInt(firebaseData,"/Proyecto/Sonido",0);
  } 
  //Humo
  int H=analogRead(humo);
  Serial.println(H);
  Firebase.setInt(firebaseData,"/Proyecto/Humo",H);
  delay(500);  
  }
