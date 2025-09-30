# TODO - Melhorias no Sistema de Monitoramento de Água

## 1. Configuração e Dependências
- [x] Criar requirements.txt com todas as bibliotecas
- [x] Criar .env para variáveis de ambiente
- [x] Criar config.py para configurações centralizadas
- [x] Atualizar .gitignore para ignorar .env

## 2. Refatoração e Consistência
- [x] Renomear main_fase1.py para main.py
- [x] Consolidar monitoramento_ph.py e alert_service.py em alertas/alert_service.py
- [x] Padronizar nomes de variáveis e arquivos

## 3. Segurança
- [x] Mover chaves de API para .env
- [x] Adicionar autenticação básica na API FastAPI
- [x] Validar entradas para prevenir injeção SQL

## 4. Logging e Manutenibilidade
- [x] Adicionar logging estruturado em todos os módulos
- [x] Adicionar type hints
- [x] Separar lógica em classes/services

## 5. Testes e Qualidade
- [x] Instalar pytest e criar testes unitários
- [ ] Adicionar linting com flake8/black

## 6. Escalabilidade e Performance
- [ ] Melhorar concurrency com asyncio
- [ ] Otimizar queries SQL

## 7. Funcionalidades Adicionais
- [ ] Suporte dinâmico a múltiplos dispositivos
- [ ] Melhorar dashboard com filtros

## 8. Documentação e Deploy
- [x] Atualizar README.md
- [x] Criar Dockerfile

## Testes Finais
- [ ] Testar sistema completo após mudanças
