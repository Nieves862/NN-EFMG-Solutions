// C++
// --- ESTACIÓN METEOROLÓGICA  (HARDWARE REAL) ---
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include "DHT.h"
// Configuración del sensor DHT11
#define DHTPIN 2     
#define DHTTYPE DHT11 
// Instancias de periféricos
LiquidCrystal_I2C lcd(0x27, 16, 2);
DHT dht(DHTPIN, DHTTYPE);
// Asignación de pines
const int pinGas = A0;         // Entrada analógica del sensor MQ
const int pinLedCalor = 13;
const int pinLedFrio = 12;
const int pinBuzzer = 11;
void setup() {
  Serial.begin(9600);  
  dht.begin();  
  lcd.init();
  lcd.backlight();  
  // Configuración de salidas
  pinMode(pinLedCalor, OUTPUT);
  pinMode(pinLedFrio, OUTPUT);
  pinMode(pinBuzzer, OUTPUT);  
  // Mensaje de inicio
  lcd.setCursor(0, 0);
  lcd.print("PRoA RIO III");
  lcd.setCursor(0, 1);
  lcd.print("Iniciando...");
  delay(2000);
  lcd.clear();
}
void loop() {
  // Lectura del sensor ambiental DHT11
  float humedad = dht.readHumidity();
  float temperatura = dht.readTemperature();
  // Lectura analógica del sensor de gas MQ
  int nivelGas = analogRead(pinGas);
  // Control de fallos del DHT11 por si se desconecta un cable Dupont
  if (isnan(humedad) || isnan(temperatura)) {
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("ERROR DHT11");
    lcd.setCursor(0, 1);
    lcd.print("Revisar Pin D2");
    Serial.println("ERROR,ERROR,ERROR"); 
    delay(2000);
    return;
  }
  // --- CADENA SERIAL PARA Python y  MySQL ---
  // Formato: Humedad,Temperatura, NivelGas
  Serial.print((int)humedad);
  Serial.print(",");
  Serial.print((int)temperatura);
  Serial.print(",");
  Serial.println(nivelGas);
  // --- MUESTRA EN PANTALLA LCD ---
  lcd.clear();
  
  // Fila 1: Variables de Clima (Temp y Humedad)
  lcd.setCursor(0, 0);
  lcd.print("T:");
  lcd.print((int)temperatura);
  lcd.print("C | H:");
  lcd.print((int)humedad);
  lcd.print("%");
  // Fila 2: Diagnóstico Prioritario (Gases > Temperatura)
  lcd.setCursor(0, 1);  
  // ALERTA 1: Calidad de Aire / Presencia de Gases (Máxima Prioridad)
  if (nivelGas > 300) { 
    lcd.print("GAS: !ALERTA!");
    digitalWrite(pinLedCalor, HIGH);
    digitalWrite(pinLedFrio, LOW);
    tone(pinBuzzer, 1200); // Tono agudo de emergencia
  } 
  // ALERTA 2: Temperatura Elevada
  else if (temperatura >= 35) {
    lcd.print("ALERTA: CALOR!");
    digitalWrite(pinLedCalor, HIGH);
    digitalWrite(pinLedFrio, LOW);
    tone(pinBuzzer, 800);
  } 
  // ALERTA 3: Temperatura Baja
  else if (temperatura <= 15) {
    lcd.print("ALERTA: FRIO");
    digitalWrite(pinLedCalor, LOW);
    digitalWrite(pinLedFrio, HIGH);
    noTone(pinBuzzer);
  }
  // ESTADO ÓPTIMO
  else {
    lcd.print("AIRE: Normal");
    digitalWrite(pinLedCalor, LOW);
    digitalWrite(pinLedFrio, LOW);
    noTone(pinBuzzer);
  }
  delay(2000); // Muestreo cada 2 segundos acorde al tiempo de respuesta del DHT11
}

