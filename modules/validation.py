#! /usr/bin/env python3
# coding: utf-8

from typing import Dict

from cerberus import Validator


def validate(item: Dict) -> bool:

    """Validate de schema of the dict
       with the item data

       :param item: a dict with the item data
       :return: boolean, True if the item schema
                is valid"""

    color = item['details']['colors'][0]

    schema = {
        'ref': {
            'type': 'string'
        },
        'description': {
            'type': 'dict',
            'schema': {
                'en': {
                    'type': 'string'
                }
            }
        },
        'main_title': {
            'type': 'dict',
            'schema': {
                'en': {
                    'type': 'string'
                }
            }
        },
        'images': {
            'type': 'dict',
            'schema': {
                color: {
                    'type': 'list',
                    'schema': {
                        'type': 'string',
                        'regex': r'^https?:(.*)'
                    }
                }
            }
        },
        'price_hierarchy': {
            'type': 'dict',
            'schema': {
                'type': {
                    'type': 'string'
                },
                color: {
                    'type': 'dict',
                    'schema': {
                        'price': {
                            'type': 'dict',
                            'schema': {
                                'GBP': {
                                    'type': 'string',
                                    'regex': r'^(?:[1-9]\d*|0)(?:\.\d+)?$'
                                }
                            }
                        },
                        'previous_price': {
                            'type': 'dict',
                            'schema': {
                                'GBP': {
                                    'type': 'string',
                                    'regex': r'^(?:[1-9]\d*|0)(?:\.\d+)?$',
                                    'empty': True
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    # create validator object and allow others fields
    v = Validator(schema)
    v.allow_unknown = True

    return v.validate(item)
