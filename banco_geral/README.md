# Sistema de Monitoramento da Qualidade da Água

Este projeto implementa um sistema IoT para monitoramento da qualidade da água, focado em medições de pH, com alertas via WhatsApp e visualização em tempo real através de um dashboard web.

## Funcionalidades

- **Coleta de Dados**: Recebe dados de sensores pH via API REST ou leitura serial simulada.
- **Armazenamento**: Dados salvos em SQLite e CSV para persistência.
- **Alertas**: Notificações automáticas via WhatsApp quando o pH sai da faixa ideal (6.5-8.0).
- **Dashboard**: Interface web em tempo real com gráficos e estatísticas.
- **API REST**: Endpoints para consultar dados históricos e resumos.

## Arquitetura

- **Backend**: FastAPI com autenticação básica.
- **Banco de Dados**: SQLite com SQLAlchemy.
- **Frontend**: Streamlit para dashboard.
- **Alertas**: Integração com CallMeBot API para WhatsApp.
- **Configuração**: Variáveis de ambiente com python-dotenv.

## Instalação

1. **Clone o repositório**:
   ```bash
   git clone <url-do-repositorio>
   cd agua_que_alimenta
   ```

2. **Crie um ambiente virtual**:
   ```bash
   python -m venv .venv
   .\.venv\Scripts\activate  # Windows
   ```

3. **Instale as dependências**:
   ```bash
   pip install -r banco_geral/requirements.txt
   ```

4. **Configure as variáveis de ambiente**:
   - Crie um arquivo `.env` na raiz do projeto e adicione os seguintes valores:
     ```env
     MINHA_APIKEY=SUA_CHAVE_APIKEY_AQUI
     CLIENT_nascente_teste_01=558194330307
     API_USERNAME=admin
     API_PASSWORD=senha123
     ```

## Uso

Para executar o projeto, você precisará iniciar os componentes em terminais separados.

**1. Servidor API**:
```bash
python -m uvicorn src.backend_server:app --reload
```

**2. Dashboard**:
```bash
streamlit run src/main/dashboard.py
```

**3. Monitoramento e Leitura Serial**:
```bash
python src/main/main.py
```

### API Endpoints

- `POST /data`: Receber dados do sensor
- `GET /dados/ultimo`: Última leitura (autenticado)
- `GET /dados/historico/{limit}`: Histórico (autenticado)
- `GET /dados/resumo`: Estatísticas (autenticado)

### Testes

```bash
pytest tests/
```

## Configuração

### WhatsApp API (CallMeBot)
1. Acesse [CallMeBot](https://www.callmebot.com/)
2. Obtenha sua API key após ativar o bot.
3. Adicione a chave no arquivo `.env` como `MINHA_APIKEY`.

### Clientes
Adicione mapeamentos de `device_id` para números de telefone no `.env`:
```env
CLIENT_nomedispositivo=55DDDNUMERO
```

## Docker

Para executar com Docker Compose (inclui serviços de monitoramento como ELK e Prometheus):
```bash
cd banco_geral
docker-compose up --build
```

## Melhorias Futuras

- Suporte a múltiplos tipos de sensores.
- Interface web mais avançada (ex: React, Vue.js).
- Notificações via outros canais (push, email).
- Deploy em nuvem (AWS, GCP, Azure).

## Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para detalhes.
