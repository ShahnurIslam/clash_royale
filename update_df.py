import clashroyale
import pandas as pd
from PIL import Image
import requests
from io import BytesIO
from datetime import datetime as dt
import sys
work_token ='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6ImU2MjMxYTYzLTVhNDEtNGJmZC04Y2E3LTg3MzkwMzM0NmM4MSIsImlhdCI6MTU0NjI3NTI1NSwic3ViIjoiZGV2ZWxvcGVyLzg4N2ZhMmZkLWI5MDYtZGVhOS03ZjA2LWQ1ZmFjZmRkMzdlNSIsInNjb3BlcyI6WyJyb3lhbGUiXSwibGltaXRzIjpbeyJ0aWVyIjoiZGV2ZWxvcGVyL3NpbHZlciIsInR5cGUiOiJ0aHJvdHRsaW5nIn0seyJjaWRycyI6WyI4Ni4xMzkuMTA2LjExNyJdLCJ0eXBlIjoiY2xpZW50In1dfQ.xyBbnGjbA2DoToGhNL-6OrtMtYEbmcfl1KlnKrbJMSpwiC-IiNkplZS3tppg00c2q2RqBD1sEJx3uH11Nuhwkw'
home_token ='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjY5N2Y5NmVlLTQwOWItNDY0Yy05OTk2LWY4Y2Y3YWVmYTJhMCIsImlhdCI6MTU1NDU4NDg4MCwic3ViIjoiZGV2ZWxvcGVyLzg4N2ZhMmZkLWI5MDYtZGVhOS03ZjA2LWQ1ZmFjZmRkMzdlNSIsInNjb3BlcyI6WyJyb3lhbGUiXSwibGltaXRzIjpbeyJ0aWVyIjoiZGV2ZWxvcGVyL3NpbHZlciIsInR5cGUiOiJ0aHJvdHRsaW5nIn0seyJjaWRycyI6WyI4Ni4xNTkuNTUuMTczIl0sInR5cGUiOiJjbGllbnQifV19.hJ2M57CwMtaPj3aTukK9W24HhbP2WLiqqb47_vkggIUZmXJVhxrG6dpyGjZ_prxnX88QR7eIu62XsqKAGjwPQA'


ip = sys.argv[1]

if ip == '81.144.132.181':
	token = work_token
else:
	token = home_token

coc = pd.read_csv('coc_battles.csv',index_col= 'battleTime')

cr = clashroyale.official_api.Client(token)

def populate_cards():
    all_cards = cr.get_all_cards()
    card_name = []
    card_image_link = []
    for i in all_cards:
        card_name.append(i['name'])
        x = str(i['iconUrls'])
        card_image_link.append(x[12:-2])
        card_df = pd.DataFrame()
        card_df['card'] = card_name
        card_df['card_image_link'] = card_image_link
    return card_df

card_df = populate_cards()

def show_card_image(card):
    x = card_df.loc[card_df[card_df['card'] == card].index[0],['card_image_link']]
    url = x.values[0]
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    return img

def get_level(player_tag,token): #include the hash
    get_tag = str.replace(player_tag,'#','%23')
    cr = clashroyale.official_api.Client(token)
    player = cr.get_player(get_tag)
    level = player['expLevel']
    return level

battles = cr.get_player_battles('%23ULU0Y80P')
df = pd.DataFrame()
battleTime = []
crowns_won = []
crowns_lost =[]
player_level = []
card1 = []
card2 = []
card3 = []
card4 = []
card5 = []
card6 = []
card7 = []
card8 = []

for i in range(len(battles)):
    type = battles[i].type
    if type == 'PvP':
        battleTime.append(battles[i].battleTime)
        crowns_won.append(battles[i].team[0].crowns)
        crowns_lost.append(battles[i].opponent[0].crowns)
        player_level.append(get_level(battles[i].opponent[0].tag,token))
        card1.append(battles[i].opponent[0].cards[0].name)
        card2.append(battles[i].opponent[0].cards[1].name)
        card3.append(battles[i].opponent[0].cards[2].name)
        card4.append(battles[i].opponent[0].cards[3].name)
        card5.append(battles[i].opponent[0].cards[4].name)
        card6.append(battles[i].opponent[0].cards[5].name)
        card7.append(battles[i].opponent[0].cards[6].name)
        card8.append(battles[i].opponent[0].cards[7].name)
        #x = battles[i].team[0].trophyChange
        #print(x)
df['battleTime'] = battleTime
df['crowns_won'] = crowns_won
df['crowns_lost'] = crowns_lost
df['player_level'] = player_level
df['card_1'] = card1
df['card_2'] = card2
df['card_3'] = card3
df['card_4'] = card4
df['card_5'] = card5
df['card_6'] = card6
df['card_7'] = card7
df['card_8'] = card8
df = df.set_index('battleTime')

coc = coc.append(df[~df.index.isin(coc.index)])
coc.to_csv('coc_battles.csv')
