[wokwi]
version = 1;
firmware = 'Documentos/PROGRAMAÇÃO/Água que alimenta/AGUA_QUE_ALIMENTA';
elf = 'path-to-your-firmware.elf';


// #include <Arduino.h>

// Pino GPIO do ESP32 conectado à saída analógica do módulo de pH
const int PH_SENSOR_PIN = 34; // Usando GPIO 34 como exemplo para entrada ADC

// Valores de calibração do sensor de pH
// Estes valores são obtidos durante a calibração do seu sensor.
// Substitua-os pelos seus próprios valores.
// Exemplo:
// Tensão (mV) para pH 7.0 (neutro)
const float NEUTRAL_VOLTAGE_MV = 1500; // Tensão em mV quando o pH é 7.0 (aprox. 1.5V)
// Tensão (mV) para pH 4.0 (ácido)
const float ACID_VOLTAGE_MV = 2068; // Tensão em mV quando o pH é 4.0 (aprox. 2.068V)
// Tensão (mV) para pH 10.0 (básico)
const float BASIC_VOLTAGE_MV = 932; // Tensão em mV quando o pH é 10.0 (aprox. 0.932V)

// Coeficiente de sensibilidade (Slope) e Offset
// Estes serão calculados a partir dos valores de calibração.
float slope = 0;
float offset = 0;

// Constantes para conversão ADC
const float ADC_RESOLUTION = 4095.0; // Resolução ADC do ESP32 (12 bits)
const float ESP32_ANALOG_REF_VOLTAGE = 3300.0; // Tensão de referência ADC do ESP32 em mV (3.3V)

// Variáveis para média das leituras
const int NUM_READINGS = 10; // Número de leituras para média
int phReadings[NUM_READINGS];
int readIndex = 0;
long totalPhValue = 0;
float averagePhValue = 0;

void setup() {
  Serial.begin(115200); // Inicializa a comunicação serial para debug

  // Configura a resolução do ADC (opcional, 12 bits é o padrão)
  // analogReadResolution(12);

  // Calibrar o sensor (você fará isso uma vez e depois usará os valores calculados)
  // Neste exemplo, vamos calcular slope e offset usando dois pontos de calibração.
  // Recomenda-se calibrar com pH 7.0 e pH 4.0 (ou 10.0) para uma boa linearidade.

  // Calculando o slope (coeficiente angular) e offset (intercepto) da reta de calibração
  // A equação da reta é pH = slope * Voltage + offset
  // Usando dois pontos: (Voltage_PH7, 7.0) e (Voltage_PH4, 4.0)
  // slope = (pH2 - pH1) / (Voltage2 - Voltage1)
  // offset = pH1 - slope * Voltage1

  // Usando pH 7.0 e pH 4.0 para calibração
    slope = (7.0 - 4.0) / (NEUTRAL_VOLTAGE_MV - ACID_VOLTAGE_MV);
    offset = 7.0 - (slope * NEUTRAL_VOLTAGE_MV);

    Serial.println("pHmetro inicializado.");
    Serial.print("Slope calculado: ");
    Serial.println(slope, 6);
    Serial.print("Offset calculado: ");
    Serial.println(offset, 6);
    Serial.println("----------------------------------");
}

void loop() {
  // Leitura analógica do sensor de pH
    int rawADCValue = analogRead(PH_SENSOR_PIN);

  // Converte o valor ADC para milivolts
  float voltageMV = (rawADCValue / ADC_RESOLUTION) * ESP32_ANALOG_REF_VOLTAGE;

  // Calcula o pH usando a equação da calibração
  float pHValue = slope * voltageMV + offset;

  // Implementa um filtro de média móvel para estabilizar a leitura
    totalPhValue = totalPhValue - phReadings[readIndex];
    phReadings[readIndex] = pHValue * 100; // Multiplica por 100 para manter precisão como int
    totalPhValue = totalPhValue + phReadings[readIndex];
    readIndex = (readIndex + 1) % NUM_READINGS;
    averagePhValue = (float)totalPhValue / NUM_READINGS / 100.0;

    // Exibe os valores no Serial Monitor
    Serial.print("Leitura ADC: ");
    Serial.print(rawADCValue);
    Serial.print("\tTensão (mV): ");
    Serial.print(voltageMV, 2);
    Serial.print("\tpH Calculado: ");
    Serial.print(pHValue, 2); // Exibe com 2 casas decimais
    Serial.print("\tpH Médio: ");
    Serial.println(averagePhValue, 2); // Exibe com 2 casas decimais

  delay(500); // Pequeno atraso para não sobrecarregar a porta serial
}

