#! /usr/bin/env python3
# coding: utf-8


def aggregate_items(item_id, items):

    """Build aggregated item from
       the individuals items

       :param item_id: common id of the items
       :param items: list of items
       :return: dict with data of the teraggregated item"""

    a_item = dict()
    a_item['item_id'] = item_id
    a_item['title'] = items[0]['main_title']['en']
    a_item['description'] = items[0]['description']['en']

    a_item['colors'] = {}

    for item in items:
        item_color = item['details']['colors'][0]

        # build color specification
        color_spec = {}

        # images
        images = item['images'][item_color]
        color_spec['images'] = images

        # price
        color_spec['price'] = {}
        price_data = item['price_hierarchy'][item_color]
        current_price = float(price_data['price']['GBP'])
        color_spec['price']['current'] = current_price

        if price_data['previous_price']['GBP'] != '':
            previous_price = float(price_data['previous_price']['GBP'])
            color_spec['price']['discount'] = 1

        else:
            previous_price = current_price
            color_spec['price']['discount'] = 0

        color_spec['price']['previous'] = previous_price
        color_spec['price']['delta'] = previous_price-current_price

        a_item['colors'][item_color] = color_spec

    return a_item


def filter_colors(item, colors):

    """Say if a item has a model with the
       specified color

       :param item: a dict with the item data
       :param specified_color: name of the color
       :return: boolean, True if there is the color"""

    has_color = True
    for color in colors:
        if color not in list(item['colors'].keys()):
            has_color = False
            break

    return has_color


def get_prices(item, colors=None):

    """Return the price for the one or several
       colors of a item

       :param item: a dict with the item data
       :param colors: list of names of the specified colors,
                      if None, return data for all colors
       :return: list of tuples (color, price),
                if all specified color doesn't exist return
                empty list"""

    item_id = item['item_id']
    prices = []

    for color, data in item['colors'].items():
        if (colors is None) or (color in colors):
            price = data['price']['current']
            prices.append((item_id, color, price))

    return prices
