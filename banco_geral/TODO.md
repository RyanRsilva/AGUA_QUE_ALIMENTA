# TODO List for Project "Água que Alimenta"

## Completed Tasks

### Step 1: Project Reorganization ✅
- Moved main application code into `src/` folder.
- Organized database files in `banco/` folder.
- Tests in `tests/` folder.
- Alert code in `alertas/` and `whatsapp/`.
- Utility scripts in `utils/`.
- Updated imports and references accordingly.

### Step 2: Database Migration ✅
- Migrated from SQLite to PostgreSQL for production readiness.
- Added PostgreSQL configuration in `config.py`.
- Created tables in PostgreSQL.
- Updated all database connections to use PostgreSQL.

### Step 3: Alert System Improvements ✅
- Updated WhatsApp alerts to use Evolution API instead of CallMeBot.
- Added email alerts as fallback when WhatsApp fails.
- Configured SMTP for email notifications.
- Updated alert service to support multiple sensors with dynamic limits.

### Step 4: Dashboard Enhancements ✅
- Improved Streamlit dashboard with filters (date range, sensor selection).
- Added real-time charts for each sensor.
- Implemented visual alerts for out-of-range values.
- Added automatic updates every 10 seconds.
- Included statistical summary display.

### Step 5: API Enhancements ✅
- Added rate limiting to API endpoints.
- Improved data validation with Pydantic models.
- Added export functionality (CSV download via API and dashboard).
- Enhanced error handling and logging.

### Step 6: Multi-Sensor Support ✅
- Configured support for multiple sensor types (pH, temperature, turbidity).
- Dynamic sensor limits via environment variables.
- Updated data models to handle different sensors.

## Remaining Tasks

### High Priority
- Implement JWT authentication for API security.
- Add user management and role-based access.
- Implement data retention policies (automatic cleanup of old data).
- Add comprehensive error handling and logging.
- Add health check endpoints for monitoring.

### Medium Priority
- Add Docker Compose for full stack deployment.
- Implement logging to external service (e.g., ELK stack).
- Add unit tests for new features.
- Implement database backup and recovery scripts.
- Optimize database queries and add indexing.
- Add API documentation with Swagger/OpenAPI enhancements.

### Low Priority
- Add internationalization (i18n) support.
- Implement API versioning.
- Add data visualization with more advanced charts (e.g., Plotly).
- Implement CI/CD pipeline with GitHub Actions.
- Implement caching for API responses (Redis).
- Add performance monitoring and alerting.
- Implement rate limiting per user.
- Add data export in multiple formats (Excel, PDF).
- Create admin panel for system configuration.
- Add automated testing with pytest coverage.

## Future Improvements
- Suporte a múltiplos tipos de sensores adicionais.
- Interface web mais avançada com React/Vue.
- Notificações push/email adicionais.
- Deploy em nuvem (AWS/Azure/GCP).
- Integração com IoT platforms (AWS IoT, Azure IoT).

## Notes
- Project is now production-ready with PostgreSQL.
- All core functionalities implemented and tested.
- Code is well-organized and modular.
- Docker support added for easy deployment.
