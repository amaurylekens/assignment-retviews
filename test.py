#! /usr/bin/env python3
# coding: utf-8

import os
import json

import pytest

from modules.utils import aggregate_items, get_prices, filter_colors
from modules.validation import validate

# load items data
with open("test_data/items.json", "r") as f:
    items = json.load(f)

# load aggregated items data
with open("test_data/aggregated_items.json", "r") as f:
    a_items = json.load(f)


# test aggregate_items()
test_values = [(item_id, item_list, a_items[item_id])
               for item_id, item_list in items.items()]


@pytest.mark.parametrize('item_id, items, expected', test_values)
def test_aggregate_items(item_id, items, expected):
    assert aggregate_items(item_id, items) == expected


# test get_prices()
with open('test_data/test_get_prices.json') as f:
    data = json.load(f)
test_values = data['test_values']
test_values = [(a_items[v[0]], v[1] if
                v[1] != '' else None,
                [tuple(l) for l in v[2]])
               for v in test_values]


@pytest.mark.parametrize('item, colors, expected', test_values)
def test_get_prices(item, colors, expected):
    assert get_prices(item, colors) == expected


# test filter_colors()
with open('test_data/test_filter_colors.json') as f:
    data = json.load(f)
test_values = data['test_values']
print(test_values)
test_values = [(a_items[v[0]], v[1], v[2])
               for v in test_values]


@pytest.mark.parametrize('item, colors, expected', test_values)
def test_filter_colors(item, colors, expected):
    assert filter_colors(item, colors) == expected


# test validate()
with open('test_data/test_validate.json') as f:
    data = json.load(f)
test_values = data['test_values']
test_values = [tuple(v) for v in test_values]


@pytest.mark.parametrize('item, expected', test_values)
def test_validate(item, expected):
    assert validate(item) == expected
