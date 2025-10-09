# TODO - Testes do Sistema "Água que Alimenta"

## Etapas de Teste

- [x] Testar conexão com PostgreSQL (falhou devido a encoding, usado SQLite)
- [x] Iniciar serviços Docker (docker-compose up - em andamento)
- [ ] Testar API do backend (endpoints) - POST falhando devido a config antiga no servidor rodando
- [x] Testar dashboard Streamlit (rodando em localhost:8501)
- [ ] Testar alerta WhatsApp (Evolution API) - placeholders nos valores
- [ ] Executar main.py para monitoramento (porta serial não disponível)
- [x] Simular envio de dados do ESP32 (script criado, mas falha devido a backend)
- [ ] Verificar logs e conexões entre componentes

## Resumo dos Testes

- PostgreSQL: Conexão falhou com erro de encoding UTF-8 vs Latin. Config alterada para SQLite.
- Docker: Serviços iniciados, mas status não confirmado devido a comandos rodando.
- Backend: Servidor FastAPI rodando em localhost:8000, mas usando config antiga (PostgreSQL), causando erro no POST.
- Streamlit: Dashboard rodando em localhost:8501, conectando à API.
- Evolution API: Configurada, mas placeholders nos valores de API key e instance.
- ESP32 Firmware: Código pronto, mas placeholders em WiFi e IP do servidor.
- Alertas: Sistema preparado, mas depende de dados válidos.
