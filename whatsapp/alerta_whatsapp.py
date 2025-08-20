# whatsapp/alerta_whatsapp.py

import requests
import urllib.parse

# --- CONFIGURAÇÕES ---
MEU_TELEFONE = "558194330307" 
MINHA_APIKEY = "2180486"


def enviar_alerta_whatsapp(ph_valor):

    mensagem = f"⚠️ *Alerta de pH!* ⚠️\n\nO valor atual é *{ph_valor}*, que está fora da faixa ideal (6.5 a 8.0)."
    mensagem_formatada = urllib.parse.quote(mensagem)

    url = f"https://api.callmebot.com/whatsapp.php?phone={MEU_TELEFONE}&text={mensagem_formatada}&apikey={MINHA_APIKEY}"

    print(
        f"\n[ALERTA] pH fora da faixa ({ph_valor}). Enviando notificação para o WhatsApp...")

    try:
        response = requests.get(url, timeout=10)  # Adicionado timeout de 10s
        if response.status_code == 200:
            print("[ALERTA] Notificação enviada com sucesso!")
        else:
            print(
                f"[ALERTA] Erro ao enviar notificação. Código: {response.status_code}, Resposta: {response.text}")
    except Exception as e:
        print(f"[ALERTA] Falha na conexão ao enviar notificação: {e}")


# Adicione estas linhas no final do arquivo whatsapp/alerta_whatsapp.py

if __name__ == '__main__':
    enviar_alerta_whatsapp("9.5")  # Envia um teste com pH 9.5
