import json

import pytest

from utils import aggregate_items


f = open('test_items.json', 'r')
values = json.load(f)
f.close()

f = open('expected.json', 'r')
expected = json.load(f)
f.close()

test_values = [(item_id, items, expected[item_id]) for item_id, items in values.items()]


@pytest.mark.parametrize('item_id, items, expected', test_values)
def test_aggregate_items(item_id, items, expected):
    assert aggregate_items(item_id, items) == expected
    

   
