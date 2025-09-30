import pytest
from unittest.mock import patch
from whatsapp.alerta_whatsapp import enviar_alerta_whatsapp


@patch('whatsapp.alerta_whatsapp.requests.get')
def test_enviar_alerta_sucesso(mock_get):
    """Testa envio de alerta com sucesso."""
    mock_get.return_value.status_code = 200
    result = enviar_alerta_whatsapp("5511999999999", "Teste")
    assert result is True


@patch('whatsapp.alerta_whatsapp.requests.get')
def test_enviar_alerta_falha(mock_get):
    """Testa envio de alerta com falha."""
    mock_get.return_value.status_code = 400
    result = enviar_alerta_whatsapp("5511999999999", "Teste")
    assert result is False


def test_enviar_alerta_sem_numero():
    """Testa envio sem número."""
    result = enviar_alerta_whatsapp("", "Teste")
    assert result is False


def test_enviar_alerta_sem_mensagem():
    """Testa envio sem mensagem."""
    result = enviar_alerta_whatsapp("5511999999999", "")
    assert result is False
