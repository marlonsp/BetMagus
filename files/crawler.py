import requests
from bs4 import BeautifulSoup

url = "https://lolesports.com/vod/110471059652887260/1/ckoxgB42rhE"

# Realizar a solicitação HTTP
response = requests.get(url)

# Verificar se a solicitação foi bem-sucedida (código de status 200)
if response.status_code == 200:
    # Parsear o conteúdo HTML com BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # salvar o conteúdo HTML em um arquivo txt
    with open('lolesports.txt', 'w') as file:
        file.write(soup.prettify())
    # # Imprimir o HTML
    # print(soup.prettify())
else:
    print(f"Erro na solicitação. Código de status: {response.status_code}")
