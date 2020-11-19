import sys
import json

from pyspark import SparkContext

from modules.utils import extract_id, aggregate_items


def main():
    sc = SparkContext()
    lines = sc.textFile('data/claudiepierlot_uk_20200701230904.txt')
    result = lines.map(lambda line: json.loads(line)) \
                  .map(lambda item: (item['ref'], [item])) \
                  .reduceByKey(lambda a, b: a+b) \
                  .map(lambda t: aggregate_items(t[0], t[1])) \
                  .collect()

    print(result) 


if __name__ == "__main__":
    main()



