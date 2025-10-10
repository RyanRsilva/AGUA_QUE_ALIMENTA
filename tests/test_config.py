import pytest
from config.settings import FAIXA_MIN_PH, FAIXA_MAX_PH, API_USERNAME, API_PASSWORD


def test_faixa_ph():
    """Testa se as faixas de pH estão corretas."""
    assert FAIXA_MIN_PH == 6.5
    assert FAIXA_MAX_PH == 8.0


def test_api_credentials():
    """Testa se as credenciais da API estão definidas."""
    assert API_USERNAME == "admin"
    assert API_PASSWORD == "senha123"
