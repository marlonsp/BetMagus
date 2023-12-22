import os
from bs4 import BeautifulSoup

# Obter o diretório do script atual
script_directory = os.path.dirname(os.path.abspath(__file__))

def get_html_file(file_name):
    # Construir o caminho completo para o arquivo 'lolesports.txt' dentro da pasta 'data/raw'
    file_path = os.path.join(script_directory, '..', 'data', 'raw', file_name)

    # Abrir o arquivo
    with open(file_path, 'r', encoding='utf-8') as file:
        html = file.read()
    
    return html

def get_lane_players_stats(html, soup, lane):

    if lane == 'top':
        # Tratamento especial devido as classes obtidas como o crawler
        lane_players = soup.find_all('div', {'class': f'player top selected primary'})
        lane_players += soup.find_all('div', {'class': f'player top selected primary dead'})
        lane_players += soup.find_all('div', {'class': f'player top selected secondary'})
        lane_players += soup.find_all('div', {'class': f'player top selected secondary dead'})

    else:
        # Encontrar todos os elementos com a classe 'player {lane}' para ambos os times
        lane_players = soup.find_all('div', {'class': f'player {lane}'})

        # Encontrar todos os elementos com a classe 'player {lane} dead' para ambos os time
        lane_players += soup.find_all('div', {'class': f'player {lane} dead'})

    # Iterar sobre os jogadores jungle encontrados
    for lane_player in lane_players:
        # Obter o nome do jogador
        player_name = lane_player.find('div', {'class': 'name'}).text

        # Obter as estatísticas de kills, deaths e assists
        kda_element = lane_player.find('div', {'class': 'stat kda'})
        kills = kda_element.find('span', {'class': 'kills'}).text
        deaths = kda_element.find('span', {'class': 'deaths'}).text
        assists = kda_element.find('span', {'class': 'assists'}).text

        # Obter as estatísticas de cs e gold
        cs_element = lane_player.find('div', {'class': 'stat cs'})
        cs = cs_element.text

        gold_element = lane_player.find('div', {'class': 'stat gold'})
        gold = gold_element.text

        print(f"{player_name} KDA: {kills}/{deaths}/{assists} CS: {cs} Gold: {gold}")

lanes = ['top', 'jungle', 'mid', 'bottom', 'support']
# lanes = ['bottom']

#ler cada arquivo da pasta raw
for file_name in os.listdir(os.path.join(script_directory, '..', 'data', 'raw')):
    # Ignorar arquivos que não terminam com '.txt'
    if not file_name.endswith('.txt'):
        continue

    # Obter o html do arquivo
    html = get_html_file(file_name)

    # Criar o objeto BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    print(f"Arquivo: {file_name}")
    for lane in lanes:
        print(f"Jogadores {lane}:")
        get_lane_players_stats(html, soup, lane)
    print("\n")
