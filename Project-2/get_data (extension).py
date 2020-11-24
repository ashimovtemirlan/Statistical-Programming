import requests
from bs4 import BeautifulSoup
import pandas as pd

### Pretending that it is a browser
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'}

players_dict = {'Name': [], 'Country': [], 'Current Rating': [], 'Potential Rating': [], 'Height (cm)': [],
                'Weight (kg)': [], 'Preferred Foot': [], 'Birth Date': [], 'Age': [], 'Preferred Positions': [],
                'Player Work Rate': [], 'Weak Foot': [], 'Skill Moves': [], 'Value (€)': [], 'Wage (€)': [],
                'Team': [], 'Position': [], 'Kit Number': [], 'On loan from': [], 'Joined Club': [], 'Contract Length': [],
                'Ball Control': [], 'Dribbling': [], 'Marking': [], 'Slide Tackle': [], 'Stand Tackle': [],
                'Aggression': [], 'Reactions': [], 'Att. Position': [], 'Interceptions': [], 'Vision': [],
                'Composure': [], 'Crossing': [], 'Short Pass': [], 'Long Pass': [], 'Acceleration': [],
                'Stamina': [], 'Strength': [], 'Balance': [], 'Sprint Speed': [], 'Agility': [],
                'Jumping': [], 'Heading': [], 'Shot Power': [], 'Finishing': [], 'Long Shots': [],
                'Curve': [], 'FK Acc.': [], 'Penalties': [], 'Volleys': [], 'GK Positioning': [],
                'GK Diving': [], 'GK Handling': [], 'GK Kicking': [], 'GK Reflexes': [], 'Specialities':[],
                'Traits': []}

def preferred_positions(tags):
    if len(tags) == 1:
        return tags[0].get_text()
    else:
        return ' '.join([tag.get_text() for tag in tags])

def on_loan_from(string):
    if 'On loan from' in string:
        return string[13:]
    else:
        return 'No'

def specialities(string):
    if 'Specialities' in string:
        return string.replace('\n', ', ')[20:-6]
    else:
        return 'No'

def traits(string):
    if 'Traits' in string:
        return string.replace('\n', ', ')[14:-6]
    else:
        return 'No'

def parse_player(url):
    html = requests.get(url, headers = headers).content.decode()
    soup = BeautifulSoup(html, features = 'lxml')
    table_1 = soup.find('div', {'class': 'row pt-3'})
    table_2 = soup.find_all('div', {'class': 'col-12 col-sm-6 col-lg-6 team'})[-1]
    table_3 = soup.find('div', {'class': 'row grid'})('p')[:34]
    table_4 = soup.find_all('div', {'class': 'col-12 col-md-4 item'})[-2]
    table_5 = soup.find_all('div', {'class': 'col-12 col-md-4 item'})[-1]

    players_dict['Name'] += [table_1.find('div', {'class': 'align-self-center pl-3'}).find('h1').get_text()[:-8]]
    players_dict['Country'] += [table_1.find('div', {'class': 'align-self-center pl-3'}).find('h2').get_text()]
    players_dict['Current Rating'] += [table_1.find('span', {'class': 'float-right'}).get_text()[:2]]
    players_dict['Potential Rating'] += [table_1.find('span', {'class': 'float-right'}).get_text()[-2:]]
    players_dict['Height (cm)'] += [table_1.find_all('span', {'class': 'data-units data-units-metric'})[0].get_text()[:-3]]
    players_dict['Weight (kg)'] += [table_1.find_all('span', {'class': 'data-units data-units-metric'})[1].get_text()[:-3]]
    players_dict['Preferred Foot'] += [table_1.find_all('p', {'class': ''})[2].get_text()[15:]]
    players_dict['Birth Date'] += [table_1.find_all('p', {'class': ''})[3].get_text()[11:]]
    players_dict['Age'] += [table_1.find_all('p', {'class': ''})[4].get_text()[4:]]
    players_dict['Preferred Positions'] += [preferred_positions(table_1.find_all('p', {'class': ''})[5].find_all('a'))]
    players_dict['Player Work Rate'] += [table_1.find_all('p', {'class': ''})[6].get_text()[17:]]
    players_dict['Weak Foot'] += [len(table_1.find_all('p', {'class': ''})[7].find_all('i', {'class': 'fas fa-star fa-lg'}))]
    players_dict['Skill Moves'] += [len(table_1.find_all('p', {'class': ''})[8].find_all('i', {'class': 'fas fa-star fa-lg'}))]
    players_dict['Value (€)'] += [table_1.find_all('p', {'class': 'data-currency data-currency-euro'})[0].get_text()[7:].replace('.', '')]
    players_dict['Wage (€)'] += [table_1.find_all('p', {'class': 'data-currency data-currency-euro'})[1].get_text()[6:].replace('.', '')]

    players_dict['Team'] += [table_2.find('h5').get_text()[1:]]
    players_dict['Position'] += [table_2.find('div', {'class': 'card-body'}).find_all('p')[0].get_text()[9:]]
    players_dict['Kit Number'] += [table_2.find('div', {'class': 'card-body'}).find_all('p')[1].get_text()[11:]]
    players_dict['On loan from'] += [on_loan_from(table_2.find('div', {'class': 'card-body'}).find_all('p')[2].get_text())]
    players_dict['Joined Club'] += [table_2.find('div', {'class': 'card-body'}).find_all('p')[-2].get_text()[16:]]
    players_dict['Contract Length'] += [table_2.find('div', {'class': 'card-body'}).find_all('p')[-1].get_text()[16:]]

    players_dict['Ball Control'] += [table_3[0].get_text()[13:]]
    players_dict['Dribbling'] += [table_3[1].get_text()[10:]]
    players_dict['Marking'] += [table_3[2].get_text()[8:]]
    players_dict['Slide Tackle'] += [table_3[3].get_text()[13:]]
    players_dict['Stand Tackle'] += [table_3[4].get_text()[13:]]
    players_dict['Aggression'] += [table_3[5].get_text()[11:]]
    players_dict['Reactions'] += [table_3[6].get_text()[10:]]
    players_dict['Att. Position'] += [table_3[7].get_text()[14:]]
    players_dict['Interceptions'] += [table_3[8].get_text()[14:]]
    players_dict['Vision'] += [table_3[9].get_text()[7:]]
    players_dict['Composure'] += [table_3[10].get_text()[10:]]
    players_dict['Crossing'] += [table_3[11].get_text()[9:]]
    players_dict['Short Pass'] += [table_3[12].get_text()[11:]]
    players_dict['Long Pass'] += [table_3[13].get_text()[10:]]
    players_dict['Acceleration'] += [table_3[14].get_text()[13:]]
    players_dict['Stamina'] += [table_3[15].get_text()[8:]]
    players_dict['Strength'] += [table_3[16].get_text()[9:]]
    players_dict['Balance'] += [table_3[17].get_text()[8:]]
    players_dict['Sprint Speed'] += [table_3[18].get_text()[13:]]
    players_dict['Agility'] += [table_3[19].get_text()[8:]]
    players_dict['Jumping'] += [table_3[20].get_text()[8:]]
    players_dict['Heading'] += [table_3[21].get_text()[8:]]
    players_dict['Shot Power'] += [table_3[22].get_text()[11:]]
    players_dict['Finishing'] += [table_3[23].get_text()[10:]]
    players_dict['Long Shots'] += [table_3[24].get_text()[11:]]
    players_dict['Curve'] += [table_3[25].get_text()[6:]]
    players_dict['FK Acc.'] += [table_3[26].get_text()[8:]]
    players_dict['Penalties'] += [table_3[27].get_text()[10:]]
    players_dict['Volleys'] += [table_3[28].get_text()[8:]]
    players_dict['GK Positioning'] += [table_3[29].get_text()[15:]]
    players_dict['GK Diving'] += [table_3[30].get_text()[10:]]
    players_dict['GK Handling'] += [table_3[31].get_text()[12:]]
    players_dict['GK Kicking'] += [table_3[32].get_text()[11:]]
    players_dict['GK Reflexes'] += [table_3[33].get_text()[12:]]

    players_dict['Specialities'] += [specialities(table_4.get_text())]
    players_dict['Traits'] += [traits(table_5.get_text())]

def parse_players(url):
    html = requests.get(url, headers = headers).content.decode()
    soup = BeautifulSoup(html, features = 'lxml')
    table = soup.find('table', {'class': 'table table-striped table-players'})
    players = table.find_all('td', {'data-title': 'Name'})
    for player in players:
        parse_player('https://www.fifaindex.com' + player.find('a').get('href'))
        #break

for i in range(1, 99):
    parse_players('https://www.fifaindex.com/players/fifa20/' + str(i) + '/?league=19&league=53&league=16&league=13&league=31&order=desc')
    #break
    print('Parsed', i, 'out of 98 pages.')

data = pd.DataFrame(players_dict)
data.to_excel('players (extension).xlsx')
print(data)
