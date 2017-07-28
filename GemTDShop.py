import urllib.request
from bs4 import BeautifulSoup
import json
from datetime import datetime

from shop_index import HEROES, SKILLS, EFFECTS


def get_output(item: dict, sale=None):
    price = item['price']
    rarity = str(item['rarity']).split('_')[0]
    out = "Price: {0:3} shells\tRarity: {1}"
    if sale == item['id']:
        price = int(price/2)
        out += "\t  !! ON SALE !!"

    return out.format(price, rarity)


if __name__ == '__main__':
    url = "http://101.200.189.65:430/gemtd/goods/list/v1?hehe=0.3792814633343369"
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html, "lxml")

    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()    # rip it out

    # get text
    text = soup.get_text()

    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)
    # create json string from text of website
    json_str = '{0}'.format(text)
    # create dict from json
    obj = json.loads(json_str)


    shop_elements = obj['list']
    sale_id = obj['onsale']

    print("    Shop of {0}".format(datetime.today().strftime('%Y-%m-%d')))
    if str(sale_id).startswith('e'):
        print("    Lame visual effect on sale today. Come back tomorrow\n    ")

    print("    Today's Heroes and Abilities are:")
    for k, v in shop_elements.items():
        if k in HEROES.keys():
            print("    Hero:      {:<15}".format(HEROES[k]), get_output(shop_elements[k], sale_id))
        elif k in SKILLS.keys():
            print("    Ability:   {:<15}".format(SKILLS[k]), get_output(shop_elements[k], sale_id))
        elif k in EFFECTS.keys():
            print("    Effect:    {:<15}".format(EFFECTS[k]), get_output(shop_elements[k], sale_id))
        else:
            print("    Lucky Box: {:<15}".format("Box"),get_output(shop_elements[k], sale_id))


