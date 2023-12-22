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

def get_lane_players_stats(soup, lane):

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
files = ["late_lolesports_1.txt"]
# for file_name in os.listdir(os.path.join(script_directory, '..', 'data', 'raw')):
for file_name in files:
    # Ignorar arquivos que não terminam com '.txt'
    if not file_name.endswith('.txt'):
        continue

    # Obter o html do arquivo
    html = get_html_file(file_name)

    # Criar o objeto BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    print(f"Arquivo: {file_name}")

    stats_team_summary = soup.find('div', {'class': 'StatsTeamsSummary'})
    
    # Get dragons stats
    dragons = stats_team_summary.find('div', {'class': 'dragons'})

    blue_team_dragons = dragons.find_all('div', {'class': 'blue-team'})
    red_team_dragons = dragons.find_all('div', {'class': 'red-team'})

    blue_team_dragons_list = []
    for blue_team_dragon in blue_team_dragons:

        dragon_divs = blue_team_dragon.find_all('div')

        for div in dragon_divs:
            if 'class' in div.attrs:
                classes = div['class']
                blue_team_dragons_list.append(classes[1])
    
    red_team_dragons_list = []
    for red_team_dragon in red_team_dragons:

        dragon_divs = red_team_dragon.find_all('div')

        for div in dragon_divs:
            if 'class' in div.attrs:
                classes = div['class']
                red_team_dragons_list.append(classes[1])
    
    # Get gold stats
    gold = stats_team_summary.find('div', {'class': 'gold'})
    totals = gold.find('div', {'class': 'totals'})
    blue_team_gold = totals.find('div', {'class': 'blue-team'}).text
    red_team_gold = totals.find('div', {'class': 'red-team'}).text

    # Get details
    details = stats_team_summary.find('div', {'class': 'details'})
    blue_team_details = details.find('div', {'class': 'blue-team'})
    blue_team_inhibitors = blue_team_details.find('div', {'class': 'stat inhibitors'}).text
    blue_team_barons = blue_team_details.find('div', {'class': 'stat barons'}).text
    blue_team_towers = blue_team_details.find('div', {'class': 'stat towers'}).text
    blue_team_kills = blue_team_details.find('div', {'class': 'stat kills'}).text

    red_team_details = details.find('div', {'class': 'red-team'})
    red_team_inhibitors = red_team_details.find('div', {'class': 'stat inhibitors'}).text
    red_team_barons = red_team_details.find('div', {'class': 'stat barons'}).text
    red_team_towers = red_team_details.find('div', {'class': 'stat towers'}).text
    red_team_kills = red_team_details.find('div', {'class': 'stat kills'}).text

    stats_team_playes = soup.find('div', {'class': 'StatsTeamsPlayers'})

    blue_team = stats_team_playes.find('div', {'class': 'blue-team'})
    print("Blue Team")
    print("Dragons: ", blue_team_dragons_list)
    print("Gold: ", blue_team_gold)
    print("Inhibitors: ", blue_team_inhibitors)
    print("Barons: ", blue_team_barons)
    print("Towers: ", blue_team_towers)
    print("Kills: ", blue_team_kills)
    for lane in lanes:
        get_lane_players_stats(blue_team, lane)

    red_team = stats_team_playes.find('div', {'class': 'red-team'})
    print("Red Team")
    print("Dragons: ", red_team_dragons_list)
    print("Gold: ", red_team_gold)
    print("Inhibitors: ", red_team_inhibitors)
    print("Barons: ", red_team_barons)
    print("Towers: ", red_team_towers)
    print("Kills: ", red_team_kills)
    for lane in lanes:
        get_lane_players_stats(red_team, lane)


    print("\n")
