# TODO List for Project Fixes

## 1. Fix main.cpp
- [x] Change "valor" to "value" in JSON payload to match backend expectation.
- [x] Add comments indicating placeholders that need real values (WiFi SSID/password, server IP).

## 2. Fix Backend Compatibility
- [x] Correct CSV columns order in backend_server.py for proper data saving.

## 3. Update Configuration
- [x] Change POSTGRES_DB in config.py to match docker-compose ("agua_qualidade").
- [x] Update POSTGRES_USER, PASSWORD, PORT to match docker-compose.

## 4. Create Environment File
- [x] .env file exists in root, update manually with real values.

## 5. PostgreSQL Setup
- [ ] Ensure PostgreSQL connection is ready with real credentials.

## 6. WhatsApp API Configuration
- [ ] Fill Evolution API placeholders with real values.

## 7. Docker Configuration
- [x] Verify Docker setup is complete and provide instructions for running on another computer.

## 8. Testing
- [ ] Test PostgreSQL connection.
- [ ] Test backend endpoints.
- [ ] Calibrate pH sensor in main.cpp.
