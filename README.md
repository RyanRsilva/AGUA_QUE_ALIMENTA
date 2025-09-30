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
   pip install -r requirements.txt
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
python main/main.py
```

Isso iniciará:
- Leitura serial (ou simulação)
- Serviço de alertas
- Servidor API (porta 8000)

### Executar Componentes Individualmente

**Servidor API**:
```bash
python backend_server.py
```

**Dashboard**:
```bash
streamlit run main/dashboard.py
```

**Alertas**:
```bash
python -m alertas.alert_service
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

### Estrutura do Projeto
```
.
├── main/
│   ├── main.py              # Ponto de entrada principal
│   └── dashboard.py         # Dashboard Streamlit
├── sensores/
│   ├── leitor_serial.py     # Leitura de dados serial
│   └── monitoramento_ph.py  # (obsoleto, usar alertas/)
├── alertas/
│   └── alert_service.py     # Serviço de alertas
├── whatsapp/
│   └── alerta_whatsapp.py   # Envio de mensagens WhatsApp
├── banco/                   # Dados e gráficos
├── config.py                # Configurações centralizadas
├── backend_server.py       # API FastAPI
├── tests/                   # Testes unitários
└── requirements.txt         # Dependências
```

### Logs
Logs são salvos em `app.log` com nível INFO.

## Docker

Para executar com Docker:
```bash
docker build -t agua-monitor .
docker run -p 8000:8000 agua-monitor
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
