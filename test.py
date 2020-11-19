import json

f = open('claudiepierlot_uk_20200701230904.txt', 'r')
content = [json.loads(x) for x in f.readlines()]

print(content[0]['price_hierarchy'])

#for x in content:
#    print(x['details']['colors'][0])
   
