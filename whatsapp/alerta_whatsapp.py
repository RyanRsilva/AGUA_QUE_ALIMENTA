""# whatsapp/alerta_whatsapp.py

import requests
import urllib.parse

# --- CONFIGURAÇÕES ---
# Coloque aqui o seu número de telefone com o código do país (55 para o Brasil)
MEU_TELEFONE = "55819xxxxxxxx"  # Ex: 5581999998888
# Coloque aqui a APIKEY que você recebeu do bot
MINHA_APIKEY = "1234567" # Substitua pela sua chave

# --- FUNÇÃO DE ENVIO ---
def enviar_alerta_whatsapp(ph_valor):
    """
    Envia uma mensagem de alerta para o seu WhatsApp usando a API da CallMeBot.
    """
    # Monta a mensagem. O urllib.parse.quote garante que espaços e caracteres especiais funcionem.
    mensagem = f"⚠️ *Alerta de pH!* ⚠️\n\nO valor atual é *{ph_valor}*, que está fora da faixa ideal."
    mensagem_formatada = urllib.parse.quote(mensagem)

    # Monta a URL da API
    url = f"https://api.callmebot.com/whatsapp.php?phone={MEU_TELEFONE}&text={mensagem_formatada}&apikey={MINHA_APIKEY}"

    print(f"\n[ALERTA] pH fora da faixa ({ph_valor}). Enviando notificação para o WhatsApp...")

    try:
        # Faz a requisição HTTP GET
        response = requests.get(url)
        if response.status_code == 200:
            print("[ALERTA] Notificação enviada com sucesso!")
        else:
            print(f"[ALERTA] Erro ao enviar notificação. Código: {response.status_code}")
    except Exception as e:
        print(f"[ALERTA] Falha na conexão ao enviar notificação: {e}")

# Se quisermos testar este script diretamente, podemos fazer isso:
if __name__ == '__main__':
    print("Enviando mensagem de teste...")
    enviar_alerta_whatsapp(5.2) # Envia um alerta com um valor de exemplo
    ""

    # Em whatsapp/alerta_whatsapp.py

def enviar_alerta_whatsapp(ph_valor):
    """
    (VERSÃO DE TESTE) Apenas imprime um alerta no console.
    """
    print("\n" + "="*50)
    print(f"      ⚠️  ALERTA DE PH DETECTADO! VALOR: {ph_valor} ⚠️")
    print("="*50 + "\n")