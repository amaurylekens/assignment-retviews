import sys
import json

from pyspark import SparkContext

from utils import extract_id, aggregate_items

sc = SparkContext()
lines = sc.textFile('claudiepierlot_uk_20200701230904.txt')
result = lines.map(lambda line: json.loads(line)) \
              .map(lambda item: extract_id(item)) \
              .reduceByKey(lambda a, b: a+b) \
              .map(lambda t: aggregate_items(t)) \
              .collect()

print(result)




