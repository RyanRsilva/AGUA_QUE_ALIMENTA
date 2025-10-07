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
   - Copie `.env` e edite os valores:
     ```env
     MINHA_APIKEY=SUA_CHAVE_APIKEY_AQUI
     CLIENT_nascente_teste_01=558194330307
     API_USERNAME=admin
     API_PASSWORD=senha123
     ```

## Uso

### Executar o Sistema Completo
```bash
cd banco_geral
python run_all.py
```

Ou diretamente:
```bash
python src/main/main.py
```

Isso iniciará:
- Leitura serial (ou simulação)
- Serviço de alertas
- Servidor API (porta 8000)

### Executar Componentes Individualmente

**Servidor API**:
```bash
python src/backend_server.py
```

**Dashboard**:
```bash
streamlit run src/main/dashboard.py
```

**Leitura Serial**:
```bash
python src/sensores/leitor_serial.py
```

**Monitoramento de Alertas**:
```bash
python src/sensores/monitoramento_ph.py
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

### WhatsApp API
1. Acesse [CallMeBot](https://www.callmebot.com/)
2. Obtenha sua API key
3. Configure no `.env`

### Clientes
Adicione mapeamentos de dispositivos para números no `.env`:
```env
CLIENT_device_id=55xxxxxxxxx
```

## Desenvolvimento

## Estrutura do Projeto
```
agua_que_alimenta/
├── src/                        # Código fonte principal
│   ├── alertas/                # Serviços e lógica de alertas
│   │   ├── __init__.py
│   ├── banco/                  # Banco de dados, arquivos CSV, gráficos
│   │   ├── __init__.py
│   │   ├── dados_ph.db         # Banco SQLite
│   │   ├── historico_ph.csv    # Arquivo CSV histórico
│   │   ├── graficos_excel.py
│   │   └── graficos_SQl.py
│   ├── config/                 # Configurações e variáveis de ambiente
│   │   ├── __init__.py
│   │   └── config.py
│   ├── main/                   # Código principal da aplicação
│   │   ├── __init__.py
│   │   ├── main.py             # Entry point principal (threading)
│   │   ├── main_fase1.py       # Versão alternativa
│   │   └── dashboard.py        # Dashboard Streamlit
│   ├── sensores/               # Leitura e monitoramento dos sensores
│   │   ├── __init__.py
│   │   ├── leitor_serial.py    # Leitura serial/simulada
│   │   └── monitoramento_ph.py # Monitoramento de pH e alertas
│   ├── utils/                  # Utilitários e helpers
│   │   ├── __init__.py
│   │   ├── LEITURAS/
│   │   └── test/
│   ├── whatsapp/               # Integração com WhatsApp
│   │   ├── __init__.py
│   │   └── alerta_whatsapp.py
│   └── backend_server.py       # Servidor FastAPI
├── tests/                      # Testes unitários e de integração
├── banco/                      # Dados persistentes
├── banco_geral/                # Configurações Docker
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── requirements.txt
│   ├── run_all.py
│   ├── start_all.sh
│   ├── README.md
│   └── TODO.md
├── .env                        # Variáveis de ambiente
├── .gitignore
├── LICENSE
└── AGUA_QUE_ALIMENTA.code-workspace
```

### Logs
Logs são salvos em `app.log` com nível INFO.

## Docker

Para executar com Docker Compose (recomendado, inclui Evolution API para WhatsApp):
```bash
cd banco_geral
docker-compose up --build
```

Ou manualmente:
```bash
cd banco_geral
docker build -t agua-monitor .
docker run -p 8000:8000 -p 8501:8501 agua-monitor
```

## Segurança

- Autenticação básica HTTP nos endpoints de leitura.
- Validação de entrada para prevenir injeções.
- Chaves de API armazenadas em variáveis de ambiente.

## Melhorias Futuras

- Suporte a múltiplos tipos de sensores.
- Interface web mais avançada.
- Notificações push/email.
- Migração para PostgreSQL.
- Deploy em nuvem.

## Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para detalhes.

## Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request
