import requests
from bs4 import BeautifulSoup

positions = []
base_html = "https://www.op.gg/champions"
positions +=["jungle","adc","mid","top","support"]
url_path = "?region=global&tier=platinum_plus&hl=zh_TW&position="
hero_url_path = "/build?region=global&tier=platinum_plus&hl=zh_TW"
tier1_list = []
tier2_list = []
hero_rune_dic = {}
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
hero_item_dic = {}

def setHeroBuild(name, en_name, position):
    RuneResponse = requests.get(base_html+"/" + en_name + "/" + position + hero_url_path, headers=headers)
    RuneHtml = RuneResponse.text
    if RuneResponse.status_code == 200:
        pass
    else:
        print(RuneResponse.status_code)
        return "0"
    RuneSoup = BeautifulSoup(RuneHtml, 'html.parser')
    Runes = RuneSoup.find('div', "css-1soapw6 e12igh9s6").find_all('img')
    runeSet = "Runes:"
    for rune in Runes:
        runeSet += " " + rune.get('alt') + " "
    Items = RuneSoup.find('div', "css-37vh9h e11yrp6z2").find_all('img')
    itemSet = "Items:"
    for item in Items:
        itemSet += " " + item.get('alt') + " "
    hero_item_dic[name] = itemSet
    hero_rune_dic[name] = runeSet

for position in positions:    
    tier1_list = []
    tier2_list = []
    print("--------------------------")
    print("Position : " + position)
    response = requests.get(base_html+url_path+position, headers=headers)
    html = response.text
    if response.status_code == 200:
        pass
    else:
        print(response.status_code)
    soup = BeautifulSoup(html, 'html.parser')
    allHeros = soup.find_all('tr')
    for item in allHeros:
        name = item.find('td', "css-cym2o0 e1oulx2j6")
        if (name == None):
            continue
        else:
            en_name = name.find('a').get("href").split('/')[2]
            tier = item.find('td','css-ew1afn e1oulx2j3')
            if (tier.text[-1] == "1"):
                tier1_list.append(name.text)
                setHeroBuild(name.text, en_name, position)
            elif (tier.text[-1] == "2"):
                tier2_list.append(name.text)
                setHeroBuild(name.text, en_name, position)
    print("\nTier1:")
    for tier1Name in tier1_list:
        print(tier1Name + " " + hero_rune_dic[tier1Name] + " " + hero_item_dic[tier1Name])
    print("\nTier2:")
    for tier2Name in tier2_list:
        print(tier2Name + " " + hero_rune_dic[tier2Name] + " " + hero_item_dic[tier2Name])