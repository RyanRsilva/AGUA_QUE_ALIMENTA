# Documentação Técnica do Projeto 'Água que Alimenta'

## 1. Introdução

Este documento detalha a arquitetura técnica, componentes e fluxo de dados do projeto "Água que Alimenta". O sistema foi desenvolvido para monitorar a qualidade da água em tempo real, com foco inicial na medição de pH, utilizando uma arquitetura baseada em IoT, com coleta de dados, armazenamento, alertas e visualização.

O objetivo é fornecer uma solução de baixo custo e eficaz para garantir que a qualidade da água para consumo ou agricultura se mantenha dentro de padrões seguros.

## 2. Arquitetura do Sistema

A arquitetura é modular e composta pelos seguintes elementos principais:

- **Backend (API REST)**: Um servidor **FastAPI** atua como o núcleo do sistema, responsável por receber, processar e armazenar os dados provenientes dos sensores.
- **Frontend (Dashboard)**: Uma aplicação **Streamlit** fornece uma interface de usuário web para visualização dos dados em tempo real, incluindo gráficos de tendência, resumos estatísticos e status de alertas.
- **Banco de Dados**: O sistema utiliza **SQLite** para armazenar as leituras dos sensores, garantindo simplicidade e fácil configuração.
- **Coleta de Dados**: A coleta pode ser feita por um dispositivo de hardware real (como um ESP32) que se comunica com a API ou através de um script de simulação para fins de teste.
- **Sistema de Alertas**: Um serviço independente monitora o banco de dados em busca de leituras que excedam os limites pré-configurados e envia notificações via **WhatsApp** usando a API do CallMeBot.

![Arquitetura do Sistema](https://i.imgur.com/example.png) <!-- Placeholder para um diagrama de arquitetura -->

## 3. Componentes Principais

### 3.1. Backend (`src/backend_server.py`)

- **Framework**: FastAPI.
- **Funcionalidades**:
    - **Recepção de Dados**: Expõe um endpoint `POST /data` para receber leituras de sensores no formato JSON (`{ "device_id": "...", "sensor": "...", "value": ... }`).
    - **Armazenamento**: Salva os dados recebidos em uma tabela `leituras` no banco de dados SQLite e, redundantemente, em um arquivo `historico_ph.csv`.
    - **Consulta de Dados**: Oferece endpoints `GET` para acessar os dados:
        - `GET /dados/ultimo`: Retorna a última leitura registrada.
        - `GET /dados/historico/{limit}`: Retorna um número definido de leituras recentes.
        - `GET /dados/resumo`: Fornece estatísticas (média, mínimo, máximo) por sensor.
    - **Segurança**: Implementa autenticação HTTP Basic para os endpoints de consulta e *rate limiting* para prevenir abuso.
- **Execução**: `uvicorn src.backend_server:app --reload`

### 3.2. Dashboard (`src/main/dashboard.py`)

- **Framework**: Streamlit.
- **Funcionalidades**:
    - **Visualização em Tempo Real**: Conecta-se à API do backend para buscar e exibir os dados mais recentes a cada 10 segundos.
    - **Filtros Interativos**: Permite que o usuário filtre os dados por intervalo de datas e por tipo de sensor.
    - **Componentes Visuais**:
        - Tabela com as últimas 20 leituras.
        - Resumo estatístico com valores médios, mínimos e máximos.
        - Gráficos de linha mostrando a tendência histórica de cada sensor.
        - Seção de alertas que exibe avisos quando os valores estão fora da faixa segura.
- **Execução**: `streamlit run src/main/dashboard.py`

### 3.3. Leitor de Dados (`src/sensores/leitor_serial.py`)

- **Funcionalidade**: Responsável por ler os dados de um dispositivo conectado à porta serial (o hardware real).
- **Operação**: Tenta continuamente ler a porta serial. Se dados são recebidos, eles são decodificados e enviados para o endpoint `POST /data` do backend.
- **Simulação**: Caso nenhum dispositivo serial seja encontrado, o script entra em modo de simulação, gerando dados de pH aleatórios dentro de uma faixa para fins de teste.
- **Execução**: É iniciado como uma thread pelo `src/main/main.py`.

### 3.4. Serviço de Alertas (`src/alertas/alert_service.py`)

- **Funcionalidade**: Monitora o banco de dados para identificar medições de pH que estão fora da faixa segura (configurada em `config.py`).
- **Operação**: A cada 60 segundos, o serviço consulta as últimas leituras no banco de dados. Se um valor está fora do normal e nenhum alerta foi enviado recentemente para aquele dispositivo, ele dispara uma notificação.
- **Integração**: Utiliza a função `enviar_alerta_whatsapp` para se conectar à API do CallMeBot e enviar a mensagem de alerta para o número de telefone associado ao `device_id`.
- **Execução**: É iniciado como uma thread pelo `src/main/main.py`.

### 3.5. Simulador de ESP32 (`simulate_esp32.py`)

- **Funcionalidade**: Um script autônomo para simular um dispositivo ESP32 enviando dados para o backend.
- **Utilidade**: Essencial para desenvolvimento e teste do backend e do dashboard sem a necessidade de hardware físico.
- **Operação**: Envia uma leitura de pH simulada para o endpoint `POST /data` a cada 10 segundos.
- **Execução**: `python simulate_esp32.py`

## 4. Banco de Dados

- **Tecnologia**: SQLite.
- **Arquivo**: `src/banco/dados_ph.db`
- **Tabela Principal**: `leituras`

| Coluna      | Tipo      | Descrição                                     |
|-------------|-----------|-----------------------------------------------|
| `id`          | INTEGER   | Chave primária autoincrementada.              |
| `data_hora`   | TIMESTAMP | Data e hora da leitura.                       |
| `device_id`   | TEXT      | Identificador único do dispositivo/sensor.    |
| `sensor`      | TEXT      | Tipo de sensor (ex: "ph").                     |
| `valor`       | REAL      | O valor numérico da medição.                  |

## 5. Fluxo de Dados

1.  **Coleta**: O **ESP32** (ou o **simulador**) envia uma requisição `POST` para a **API FastAPI** com os dados do sensor.
2.  **Processamento e Armazenamento**: O **Backend** recebe os dados, valida-os e os insere na tabela `leituras` do banco de dados **SQLite**.
3.  **Visualização**: O **Dashboard Streamlit** periodicamente faz requisições `GET` à **API** para obter os dados mais recentes e atualizar os gráficos e tabelas.
4.  **Monitoramento e Alerta**: O **Serviço de Alertas**, rodando em paralelo, consulta o **banco de dados SQLite** diretamente. Se detecta uma anomalia, envia um alerta via **WhatsApp**.

## 6. Configuração e Instalação

1.  **Clone o repositório**.
2.  **Crie e ative um ambiente virtual** (`python -m venv .venv`).
3.  **Instale as dependências**: `pip install -r banco_geral/requirements.txt`.
4.  **Configure o `.env`**: Crie um arquivo `.env` na raiz do projeto e defina as variáveis, como as credenciais da API e a chave do CallMeBot.

    ```env
    MINHA_APIKEY=SUA_CHAVE_APIKEY_AQUI
    CLIENT_nascente_teste_01=558194330307
    API_USERNAME=admin
    API_PASSWORD=senha123
    ```

5.  **Execute os componentes** conforme descrito na Seção 3 (em terminais separados).

## 7. Visão de Futuro e Melhorias

Com base na análise do projeto, as seguintes melhorias estão planejadas ou são recomendadas:

- **Interface Web Avançada**: Evoluir o dashboard do Streamlit para um framework frontend mais completo (ex: React, Vue.js) para oferecer mais interatividade e uma UX mais rica.
- **Suporte a Múltiplos Sensores**: Generalizar o código para facilmente adicionar e gerenciar outros tipos de sensores (temperatura, turbidez, etc.) sem modificações profundas na arquitetura.
- **Sistema de Notificação Aprimorado**: Adicionar outros canais de notificação, como e-mail ou notificações push em um aplicativo móvel.
- **Deploy em Nuvem**: Empacotar a aplicação com Docker (os arquivos `Dockerfile` e `docker-compose.yml` já existem como ponto de partida) e fazer o deploy em um provedor de nuvem (AWS, GCP, Azure) para alta disponibilidade.
- **Calibração de Sensores**: Implementar uma rotina ou endpoint no firmware do ESP32 para permitir a calibração remota dos sensores.
- **Testes Abrangentes**: Expandir a cobertura de testes unitários e de integração, especialmente para a conexão com o banco de dados e os endpoints da API.
