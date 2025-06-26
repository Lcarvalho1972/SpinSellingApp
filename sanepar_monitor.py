
import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime

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

print("🔵 Acessando o site da Sanepar...")

url = "https://licitacoes.sanepar.com.br/SLI11000.aspx"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}

try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, 'html.parser')
    tables = pd.read_html(str(soup))

    print(f"📑 Número de tabelas encontradas na página: {len(tables)}")

    if len(tables) >= 2:
        tabela1 = tables[1]
        print("🔍 Licitações encontradas:")
        print(tabela1)

        agora = datetime.now().strftime('%Y-%m-%d')
        nome_arquivo_completo = f'licitacoes_sanepar_completo_{agora}.xlsx'
        tabela1.to_excel(nome_arquivo_completo, index=False)
        print(f"✅ Arquivo Excel completo salvo como: {nome_arquivo_completo}")

        coluna_objeto = 'Objeto'
        PALAVRAS_CHAVE = [
            'bomba', 'motobomba', 'conjunto motobomba', 'bomba centrífuga', 'bomba bipartida',
            'bomba de dupla sucção', 'bomba de turbina', 'bomba vertical', 'bomba submersível',
            'bomba submersa', 'bomba autoescorvante', 'bomba de fluxo misto', 'bomba de vácuo'
        ]

        if coluna_objeto in tabela1.columns:
            tabela_filtrada = tabela1[
                tabela1[coluna_objeto].astype(str).str.contains('|'.join(PALAVRAS_CHAVE), case=False, na=False)
            ]

            if not tabela_filtrada.empty:
                nome_arquivo_filtrado = f'licitacoes_sanepar_filtrado_{agora}.xlsx'
                tabela_filtrada.to_excel(nome_arquivo_filtrado, index=False)
                print(f"✅ Arquivo Excel filtrado salvo como: {nome_arquivo_filtrado}")

                enviar_telegram("🔔 Alerta: Foi encontrada uma nova licitação na Sanepar com palavra-chave!")
            else:
                print("⚠️ Nenhuma licitação encontrada com as palavras-chave.")
        else:
            print(f"❌ Coluna '{coluna_objeto}' não encontrada. Verifique as colunas disponíveis:")
            print(list(tabela1.columns))

    else:
        print('⚠️ Não foram encontradas tabelas suficientes na página.')

except Exception as e:
    print(f"❌ Erro durante o processo: {e}")
