# whatsapp/alerta_whatsapp.py 

import requests
import urllib.parse

# --- CONFIGURAÇÕES GLOBAIS ---

MINHA_APIKEY = "2180486"


def enviar_alerta_whatsapp(numero_destino, mensagem):
    """
    Envia uma MENSAGEM específica para um NÚMERO DE TELEFONE específico.
    """
    if not MINHA_APIKEY or MINHA_APIKEY == "SUA_CHAVE_APIKEY_AQUI":
        print(
            "[ALERTA WHATSAPP] Erro: APIKEY não configurada no arquivo alerta_whatsapp.py")
        return False

    if not numero_destino or not mensagem:
        print("[ALERTA WHATSAPP] Erro: Número de destino ou mensagem não fornecidos.")
        return False

    mensagem_formatada = urllib.parse.quote(mensagem)
    url = f"https://api.callmebot.com/whatsapp.php?phone={numero_destino}&text={mensagem_formatada}&apikey={MINHA_APIKEY}"

    print(
        f"[ALERTA WHATSAPP] Enviando notificação para o número {numero_destino}...")

    try:
        response = requests.get(url)
        if response.status_code == 200:
            print("[ALERTA WHATSAPP] Notificação enviada com sucesso!")
            return True
        else:
            print(
                f"[ALERTA WHATSAPP] Erro ao enviar. Código: {response.status_code}, Resposta: {response.text}")
            return False
    except Exception as e:
        print(f"[ALERTA WHATSAPP] Falha de conexão: {e}")
        return False


# --- Bloco de Teste ---
if __name__ == '__main__':
    print("--- Testando o módulo de alerta do WhatsApp ---")
    numero_teste = "55SEUNUMEROAQUI"
    mensagem_teste = "Olá! Este é um teste do sistema de alertas dinâmico. Kronnos."
    enviar_alerta_whatsapp(numero_teste, mensagem_teste)
