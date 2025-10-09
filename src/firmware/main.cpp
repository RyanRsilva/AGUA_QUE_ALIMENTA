#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

// Configurações Wi-Fi - PREENCHER COM DADOS REAIS
const char* ssid = "SEU_SSID";  // Substitua pelo nome da sua rede Wi-Fi
const char* password = "SUA_SENHA";  // Substitua pela senha da sua rede Wi-Fi

// Configurações do servidor - PREENCHER COM IP REAL DO SERVIDOR
const char* serverUrl = "http://192.168.1.100:8000/data";  // IP do servidor Python (substitua pelo IP real)
const char* deviceId = "esp32_ph_01";

// Pino do sensor pH
const int phPin = 34;  // Pino analógico

// Limites pH
const float phMin = 0.0;
const float phMax = 14.0;

// Intervalo de leitura (segundos)
const int interval = 300;  // 5 minutos

void setup() {
  Serial.begin(115200);
  pinMode(phPin, INPUT);

  // Conectar ao Wi-Fi
  WiFi.begin(ssid, password);
  Serial.print("Conectando ao Wi-Fi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }
  Serial.println("\nConectado ao Wi-Fi");
  Serial.print("IP: ");
  Serial.println(WiFi.localIP());
}

void loop() {
  if (WiFi.status() == WL_CONNECTED) {
    // Ler sensor pH
    int rawValue = analogRead(phPin);
    float voltage = (rawValue / 4095.0) * 3.3;  // ESP32 12-bit ADC, 3.3V
    float phValue = map(voltage, 0, 3.3, phMin, phMax);  // Mapeamento simples (ajustar calibração)

    Serial.print("Valor pH: ");
    Serial.println(phValue);

    // Criar JSON
    StaticJsonDocument<200> doc;
    doc["sensor"] = "ph";
    doc["value"] = phValue;
    doc["device_id"] = deviceId;

    String jsonString;
    serializeJson(doc, jsonString);

    // Enviar via HTTP POST
    HTTPClient http;
    http.begin(serverUrl);
    http.addHeader("Content-Type", "application/json");

    int httpResponseCode = http.POST(jsonString);

    if (httpResponseCode > 0) {
      Serial.print("Resposta do servidor: ");
      Serial.println(httpResponseCode);
      String response = http.getString();
      Serial.println(response);
    } else {
      Serial.print("Erro no POST: ");
      Serial.println(httpResponseCode);
    }

    http.end();
  } else {
    Serial.println("Wi-Fi desconectado");
  }

  delay(interval * 1000);  // Aguardar próximo intervalo
}
