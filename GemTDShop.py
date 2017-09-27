import urllib.request
from bs4 import BeautifulSoup
import json
from datetime import datetime

from shop_index import *


def format_title(sale_id=None):
    # Get the item on sale by getting the id form all 3 dicts
    sale_name = {**HEROES, **ABILITY, **EFFECTS}[sale_id]
    # The type is indikated by the first character of the id
    sale_type = TYPE[sale_id[0]]
    return "    [Shop] {0} ({2} on Sale: {1})"\
        .format(datetime.today().strftime('%d-%m-%Y'), sale_name, sale_type)


def format_item_output(item: dict, sale=None):
    price = item['price']
    rarity = str(item['rarity']).split('_')[0]
    out = "Price: {0:3} shells\tRarity: {1}"
    if sale == item['id']:
        price = int(price/2)
        out += "\t  -!! ON SALE !!-"

    return out.format(price, rarity)


def format_lines_of_shop(shop_elements, sale_id):
    for k, v in shop_elements.items():
        if k in HEROES.keys():
            yield "    Hero:      {0:<16} {1}\n".format(HEROES[k], format_item_output(shop_elements[k], sale_id))
        elif k in ABILITY.keys():
            yield "    Ability:   {0:<16} {1}\n".format(ABILITY[k], format_item_output(shop_elements[k], sale_id))
        elif k in EFFECTS.keys():
            yield "    Effect:    {0:<16} {1}\n".format(EFFECTS[k], format_item_output(shop_elements[k], sale_id))
        else:
            yield "    Lucky Box: {0:<16} {1}\n".format("Box", format_item_output(shop_elements[k], sale_id))


def main():
    url = "http://101.200.189.65:430/gemtd/goods/list/v1/@0"  # @steam ID lets you check for this id
    # url = "http://101.200.189.65:430/gemtd/goods/list/v1?hehe=0.3792814633343369"
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html, "lxml")

    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()  # rip it out

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

    #read out the shop items(dict) and the sale ID(str)
    shop_elements = obj['list']
    sale_id = obj['onsale']

    print(format_title(sale_id))
    print("    Today's Heroes and Abilities are:")
    print(*format_lines_of_shop(shop_elements, sale_id), sep='')


if __name__ == '__main__':
    main()

