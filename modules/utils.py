#! /usr/bin/env python3
# coding: utf-8

from typing import List, Dict, Tuple


def aggregate_items(item_id: str, items: List[Dict]) -> Dict:

    """Build aggregated item from
       the individuals items

       :param item_id: common id of the items
       :param items: list of items
       :return: dict with data of the aggregated item"""

    a_item = dict()
    a_item['item_id'] = item_id
    a_item['title'] = items[0]['main_title']['en']
    a_item['description'] = items[0]['description']['en']

    a_item['colors'] = {}

    for item in items:
        item_color = item['details']['colors'][0]

        # build color data
        color_data = {}

        # get and store images for the color
        images = item['images'][item_color]
        color_data['images'] = images

        # get and store prices for the color
        color_data['price'] = {}
        price_data = item['price_hierarchy'][item_color]
        current_price = float(price_data['price']['GBP'])
        color_data['price']['current'] = current_price

        # check if there is previous price
        if price_data['previous_price']['GBP'] != '':
            previous_price = float(price_data['previous_price']['GBP'])
            color_data['price']['discount'] = 1
        else:
            previous_price = current_price
            color_data['price']['discount'] = 0

        color_data['price']['previous'] = previous_price
        color_data['price']['delta'] = previous_price-current_price

        a_item['colors'][item_color] = color_data

    return a_item


def filter_colors(item: Dict, colors: List[str]) -> bool:

    """Say if a aggregated item has a model for each
       of the specified colors

       :param item: a dict with the item data
       :param colors: list of the names of the specified colors
       :return: boolean, True if there is the color"""

    has_color = True
    # loop through the specified colors and check
    # if the color is in the aggregated item
    for color in colors:
        if color not in list(item['colors'].keys()):
            has_color = False
            break

    return has_color


def get_prices(item: Dict, colors: List[str] = None) -> List[Tuple[str,
                                                             str, float]]:

    """Return the price for the one or several
       colors of a item

       :param item: a dict with the item data
       :param colors: list of names of the specified colors,
                      if None, return data for all colors
       :return: list of tuples (item_id, color, price),
                if all specified color doesn't exist return
                empty list"""

    item_id = item['item_id']
    prices = []

    for color, data in item['colors'].items():
        if (colors is None) or (color in colors):
            price = data['price']['current']
            prices.append((item_id, color, price))

    return prices
