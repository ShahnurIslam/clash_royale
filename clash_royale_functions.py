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