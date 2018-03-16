import urllib.request

import math
from bs4 import BeautifulSoup
import json
from datetime import datetime, timedelta

from shop_index import *

SHOP_URL = "http://101.200.189.65:430/gemtd/201803/goods/list/@0" # @steam ID lets you check for your id
# SHOP_URL = "http://101.200.189.65:430/gemtd/goods/list/v2/@0"  # Old Shop URL
# SHOP_URL = "http://101.200.189.65:430/gemtd/goods/list/v1/@0"  # Old Shop URL
# SHOP_URL = "http://101.200.189.65:430/gemtd/goods/list/v1?hehe=0.3792814633343369"


def calculate_time_until_refresh():
    """
    Calculates the duration until the next shop update,
    right no not in use
    :return: number, in hours
    """
    today = datetime.utcnow()

    if today.hour < 21:
        update_time = datetime(today.year, today.month, today.day, 21, 0, 0, 0)
    else:
        tomorrow = today + timedelta(days=1)
        update_time = datetime(tomorrow.year, tomorrow.month, tomorrow.day, 21, 0, 0, 0)

    diff = update_time-today

    return divmod(diff.seconds,3600)[0]%2


def format_title(sale_id=None, time_to_refresh="??"):
    """
    This function creates a string containing the date of today, the sale item and its type (Hero, Ability, Effect)
    Useful for title of an reddit thread.
    :param sale_id: the id of todays sale
    :return: String, formattet title containing current date and current item on sale
    """

    # Get the item on sale by getting the id form all 3 dicts
    sale_name = COMBINED[sale_id]
    # The type is indicated by the first character of the id
    sale_type = TYPE[sale_id[0]]

    # Return the formated title
    return "    [Shop] {0} ({2} on Sale: {1}) [{3}h till refresh]"\
        .format(datetime.today().strftime('%d-%m-%Y'),
                sale_name,
                sale_type,
                time_to_refresh)


def format_item_output(item: dict, sale_id=None):
    item_id = item['id']
    price = item['price']
    rarity = str(item['rarity']).split('_')[0]
    

    out = "    {0:7}:\t {1:<16}\t {2:3} shells\t Rarity: {3}\n"
    if price > 800:
        out = "    {0:7}:\t {1:<16}\t {2:3} blocks\t Rarity: {3}\n"
    if sale_id == item_id:
        price = int(price/2)

        out = "    --------     On Sale:      ----------------\n" + out+\
              "    --------                   ----------------\n"

    return out.format(TYPE[item_id[0]], COMBINED[item_id], price, rarity)


def format_lines_of_shop(shop_elements, sale_id):
    for k, v in shop_elements.items():
        if k in COMBINED.keys():
            yield format_item_output(v, sale_id)
        elif k != 'h0':
            yield "    {0}\n".format(v)


def main():

    html = urllib.request.urlopen(SHOP_URL).read()
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

    # read out the shop items(dict) and the sale ID(str)
    shop_elements = obj['list']
    sale_id = obj['onsale']
    time_to_refresh = str(math.floor(obj['expire'] / 60 / 60))

    print(format_title(sale_id, time_to_refresh))
    print("    Today's Heroes and Abilities are:")
    print(*format_lines_of_shop(shop_elements, sale_id), sep='')


if __name__ == '__main__':
    main()

