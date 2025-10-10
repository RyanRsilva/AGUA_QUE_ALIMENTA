# TODO - Testes do Sistema "Água que Alimenta"

## Etapas de Teste

- [x] Iniciar serviços Docker (docker-compose up)
- [ ] Testar API do backend (endpoints)
- [x] Testar dashboard Streamlit (rodando em localhost:8501)
- [ ] Testar alerta WhatsApp (CallMeBot) - placeholders nos valores
- [ ] Executar main.py para monitoramento (porta serial não disponível)
- [x] Simular envio de dados do ESP32 (script criado)
- [ ] Verificar logs e conexões entre componentes

## Resumo dos Testes

- Banco de Dados: Configuração atualizada para usar **SQLite**.
- Docker: Serviços de monitoramento (ELK, Prometheus) prontos para serem testados.
- Backend: Servidor FastAPI rodando em localhost:8000 com configuração para SQLite.
- Streamlit: Dashboard rodando em localhost:8501, conectando à API.
- Alertas: Sistema de alertas com CallMeBot preparado, mas depende de API key e número de telefone válidos no arquivo `.env`.
- ESP32 Firmware: Código pronto, mas placeholders em WiFi e IP do servidor.
