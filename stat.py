import pyspark

from pymongo import MongoClient
from pyspark import SparkContext
from pyspark.sql.types import *
from pyspark.sql import *
from pyspark.sql.functions import *

from modules.utils import get_prices

def main():

    #get the data from mongodb
    #TO DO: scale this part
    client = MongoClient()
    db = client['retviews']
    collection = db['items']

    cursor = collection.find({})
    items = []
    for document in cursor:
        items.append(document)

    sc = SparkContext()     
    prices = sc.parallelize(items) \
               .flatMap(lambda item: get_prices(item))
                
    #construct dataframe
    data_frame_schema = StructType([
        StructField("id", StringType()),
        StructField("color", StringType()),
        StructField("price", FloatType()),
    ])
    row_rdd = prices.map(lambda item: Row(item[0], item[1], item[2]))
    sqlContext = SQLContext(sc)
    df = sqlContext.createDataFrame(row_rdd, data_frame_schema).persist()

    #compute basics stats on all data
    df_stats = df.select(
        avg(col('price')).alias('mean'),
        stddev(col('price')).alias('std'),
        max(col('price')).alias('max'),
        min(col('price')).alias('min')
    ).collect()

    mean_price = df_stats[0]['mean']
    std_price = df_stats[0]['std']
    max_price = df_stats[0]['max']
    min_price = df_stats[0]['min']
    print("mean: ", mean_price, " std: ", std_price)
    print("max: ", max_price, "min: ", min_price)
    
    #compute basics stats by colors 
    df.groupBy("color") \
      .agg(avg("price").alias("average_price"), \
           min("price").alias("min_price"), \
           max("price").alias("max_price"), \
           stddev("price").alias("stddev_price"), \
           count("price").alias("count") \
       ) \
    .show()


if __name__ == "__main__":
    main()


