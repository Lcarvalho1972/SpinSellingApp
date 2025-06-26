
import requests

def enviar_telegram(mensagem):
    token = '7607631100:AAFefforJQtpqXsIVrgGR7HPaR9gMwawJcI'
    chat_id = '886309597'
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    dados = {'chat_id': chat_id, 'text': mensagem}
    try:
        resposta = requests.post(url, data=dados)
        if resposta.status_code == 200:
            print('✅ Mensagem enviada para o Telegram!')
        else:
            print(f'❌ Erro ao enviar mensagem: {resposta.text}')
    except Exception as e:
        print(f'❌ Erro: {e}')
