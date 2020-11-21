import os
import json

import pytest

from modules.utils import aggregate_items, get_prices, filter_colors


f = open('items.json', 'r')
items = json.load(f)
f.close()

f = open('aggregated_items.json', 'r')
aggregated_items = json.load(f)
f.close()

test_values = [(item_id, item_list, aggregated_items[item_id]) 
               for item_id, item_list in items.items()]


@pytest.mark.parametrize('item_id, items, expected', test_values)
def test_aggregate_items(item_id, items, expected):
    assert aggregate_items(item_id, items) == expected

test_values = [
  (
    aggregated_items["CFPTO00270"], 
    None, 
    [
      ("CFPTO00270", "ECRU - A004", 175), 
      ("CFPTO00270", "Black - 04", 175)
    ]
  ),

  (
    aggregated_items["CFPTO00270"], 
    ["ECRU - A004"], 
    [
      ("CFPTO00270", "ECRU - A004", 175)
    ]
  ),

  (
    aggregated_items["CFPTO00270"], 
    ["IVORY"], 
    []
  )
]


@pytest.mark.parametrize('item, colors, expected', test_values)
def test_get_prices(item, colors, expected):
    assert get_prices(item, colors) == expected

test_values = [
  (
    aggregated_items["CFPTO00270"], 
    ["ECRU - A004"], 
    True
  ),

  (
    aggregated_items["CFPTO00270"], 
    ["ECRU - A004", "Black - 04"], 
    True
  ),

  (
    aggregated_items["CFPTO00270"], 
    ["IVORY"], 
    False
  )
]


@pytest.mark.parametrize('item, colors, expected', test_values)
def test_filter_colors(item, colors, expected):
    assert filter_colors(item, colors) == expected
    

   
