import os
from bs4 import BeautifulSoup
import csv

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
    player_stats = []
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

        player_stats = [player_name, kills, deaths, assists, cs, gold]
        # print(f"{player_name} KDA: {kills}/{deaths}/{assists} CS: {cs} Gold: {gold}")

    return player_stats

def get_team_name(soup):
    lane_players = soup.find_all('div', {'class': f'player mid'})
    lane_players += soup.find_all('div', {'class': f'player mid dead'})

    for lane_player in lane_players:
        # Obter o nome do jogador
        player_name = lane_player.find('div', {'class': 'name'}).text

        team_name = player_name.split(" ")[0]

    return team_name

lanes = ['top', 'jungle', 'mid', 'bottom', 'support']
# lanes = ['bottom']

# Construir o caminho completo para o arquivo 'data.csv' dentro da pasta 'data/processed'
file_path = os.path.join(script_directory, '..', 'data', 'processed', 'data.csv')

# Garantir que o diretório 'data/processed' exista
os.makedirs(os.path.dirname(file_path), exist_ok=True)

# Create a cvs file to save the data
with open(file_path, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["game",
                     "blue_team", "blue_team_dragons", "blue_team_gold", "blue_team_inhibitors", "blue_team_barons", "blue_team_towers", "blue_team_kills",
                     "blue_team_top", "blue_team_top_kills", "blue_team_top_deaths", "blue_team_top_assists", "blue_team_top_cs", "blue_team_top_gold",
                     "blue_team_jungle", "blue_team_jungle_kills", "blue_team_jungle_deaths", "blue_team_jungle_assists", "blue_team_jungle_cs", "blue_team_jungle_gold",
                     "blue_team_mid", "blue_team_mid_kills", "blue_team_mid_deaths", "blue_team_mid_assists", "blue_team_mid_cs", "blue_team_mid_gold",
                     "blue_team_bottom", "blue_team_bottom_kills", "blue_team_bottom_deaths", "blue_team_bottom_assists", "blue_team_bottom_cs", "blue_team_bottom_gold",
                     "blue_team_support", "blue_team_support_kills", "blue_team_support_deaths", "blue_team_support_assists", "blue_team_support_cs", "blue_team_support_gold",
                     "red_team", "red_team_dragons", "red_team_gold", "red_team_inhibitors", "red_team_barons", "red_team_towers", "red_team_kills",
                     "red_team_top", "red_team_top_kills", "red_team_top_deaths", "red_team_top_assists", "red_team_top_cs", "red_team_top_gold",
                     "red_team_jungle", "red_team_jungle_kills", "red_team_jungle_deaths", "red_team_jungle_assists", "red_team_jungle_cs", "red_team_jungle_gold",
                     "red_team_mid", "red_team_mid_kills", "red_team_mid_deaths", "red_team_mid_assists", "red_team_mid_cs", "red_team_mid_gold",
                     "red_team_bottom", "red_team_bottom_kills", "red_team_bottom_deaths", "red_team_bottom_assists", "red_team_bottom_cs", "red_team_bottom_gold",
                     "red_team_support", "red_team_support_kills", "red_team_support_deaths", "red_team_support_assists", "red_team_support_cs", "red_team_support_gold"
                     ])

#ler cada arquivo da pasta raw
# files = ["late_lolesports_1.txt"]
for file_name in os.listdir(os.path.join(script_directory, '..', 'data', 'raw')):
# for file_name in files:
    # Ignorar arquivos que não terminam com '.txt'
    if not file_name.endswith('.txt'):
        continue

    # Obter o html do arquivo
    html = get_html_file(file_name)

    # Criar o objeto BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    # print(f"Arquivo: {file_name}")
    # print(" ")

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
    blue_team_name = get_team_name(blue_team)
    # print("Blue Team: ", blue_team_name)
    # print("Dragons: ", blue_team_dragons_list)
    # print("Gold: ", blue_team_gold)
    # print("Inhibitors: ", blue_team_inhibitors)
    # print("Barons: ", blue_team_barons)
    # print("Towers: ", blue_team_towers)
    # print("Kills: ", blue_team_kills)
    blue_team_players_stats = []
    for lane in lanes:
        blue_team_players_stats += get_lane_players_stats(blue_team, lane)

    # print(" ")

    red_team = stats_team_playes.find('div', {'class': 'red-team'})
    red_team_name = get_team_name(red_team)
    # print("Red Team: ", red_team_name)
    # print("Dragons: ", red_team_dragons_list)
    # print("Gold: ", red_team_gold)
    # print("Inhibitors: ", red_team_inhibitors)
    # print("Barons: ", red_team_barons)
    # print("Towers: ", red_team_towers)
    # print("Kills: ", red_team_kills)
    red_team_players_stats = []
    for lane in lanes:
        red_team_players_stats += get_lane_players_stats(red_team, lane)

    # print(" ")
    # print("-----------------------------------------")
    
    # Write the data in the csv file
    with open(file_path, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([file_name,
                         blue_team_name, blue_team_dragons_list, blue_team_gold, blue_team_inhibitors, blue_team_barons, blue_team_towers, blue_team_kills] + blue_team_players_stats +
                         [red_team_name, red_team_dragons_list, red_team_gold, red_team_inhibitors, red_team_barons, red_team_towers, red_team_kills] + red_team_players_stats
                        )