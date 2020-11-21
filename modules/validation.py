import cerberus

def validate(item):
    """Validate de schema of the dict
       with the item data

       :param item: a dict with the item data
       :return: boolean, True if the item schema 
                is valid"""

    schema = {
        'ref': {
            'type': 'string' 
        },
        'images': {
            'type': 'dict'
        },
        ''
        
    }

def validate1(item, colors):

    """Validate de schema of the dict
       with the item data

       :param item: a dict with the item data
       :return: boolean, True if the item schema 
                is valid"""

    schema = {
        'item_id': {
            'type': 'string'
        },
        'title': {
            'type': 'string'
        }
        'description': {
            'type': 'string'
        }
    }

    colors_schema = {
      'type': 'dict', 
      'schema': {}
    }

    for color in colors:
        colors_schema['schema'][color] = {
            'type': 'dict',
            'schema': {
                'images': {
                    'type': 'list'
                },
                'price': {
                    'type': 'dict',
                    'schema': {
                        'current': {
                            'type': 'float',
                        },
                        'discount': {
                            'type': 'boolean',
                        },
                        'previous': {
                            'type': 'float',
                        },
                        'delta': {
                            'type': 'float',
                        } 
                    }
                }    
            }
        }

    schema['color'] = colors_schema


