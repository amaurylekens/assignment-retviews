def extract_id(item):

    """Extract the item id from the dict with 
       the item data

       :param item: dict with the item data
       :return: the id of the item"""
    
    i_start = item['product_id'].find('dwvar_')
    i_end = item['product_id'].find('_color')

    product_id = item['product_id'][i_start+len('dwvar_'):i_end]
    return product_id

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

        #build color specification
        color_spec = {}

        #images
        images = item['images'][item_color]
        color_spec['images'] = images

        #price
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
        
