#! /usr/bin/env python3
# coding: utf-8

from pymongo import MongoClient
from pyspark import SparkContext
from pyspark.sql.types import *
from pyspark.sql import *
from pyspark.sql.functions import *
import matplotlib.pyplot as plt

from modules.utils import get_prices

def main():

    # get the data from mongodb
    # TO DO: scale this part
    client = MongoClient()
    db = client['retviews']
    collection = db['items']

    cursor = collection.find({})
    items = []
    for document in cursor:
        items.append(document)

    # initialize rdd
    sc = SparkContext()     
    prices = sc.parallelize(items) \
               .flatMap(lambda item: get_prices(item))
                
    #construct dataframe
    data_frame_schema = StructType([
        StructField("id", StringType()),
        StructField("color", StringType()),
        StructField("price", FloatType()),
    ])
    rows_rdd = prices.map(lambda item: Row(item[0], item[1], item[2]))
    sqlContext = SQLContext(sc)
    df = sqlContext.createDataFrame(rows_rdd, data_frame_schema) \
                   .persist()

    #compute basics stats on all data
    df_stats = df.select(
        avg(col('price')).alias('mean'),
        stddev(col('price')).alias('std'),
        max(col('price')).alias('max'),
        min(col('price')).alias('min')
    ).collect()

    print("Basics stats on all data :")
    print("mean: ", df_stats[0]['mean'])
    print("std: ", df_stats[0]['std'])
    print("max: ", df_stats[0]['max'])
    print("min: ", df_stats[0]['min'])
    
    # compute basics stats by colors 
    colors_df = df.groupBy("color") \
                  .agg(avg("price").alias("average_price"), \
                       min("price").alias("min_price"), \
                       max("price").alias("max_price"), \
                       stddev("price").alias("stddev_price"), \
                       count("price").alias("count"), \
                       collect_list("price").alias("list")) \
                  .orderBy("count", ascending = False) \
                  .persist()
    
    # show basics stats by colors
    colors_df.show()

    # plots basics stats for 4 colors
    data = colors_df.collect()[0:4]
    data = [(d['color'], d['list']) for d in data]

    fig, axs = plt.subplots(2, 2)
    axs[0, 0].boxplot(data[0][1])
    axs[0, 0].set_title(data[0][0])
    axs[0, 1].boxplot(data[1][1])
    axs[0, 1].set_title(data[1][0])
    axs[1, 0].boxplot(data[2][1])
    axs[1, 0].set_title(data[2][0])
    axs[1, 1].boxplot(data[3][1])
    axs[1, 1].set_title(data[3][0])

    for ax in axs.flat:
        ax.set(ylabel='price')

    for ax in axs.flat:
        ax.label_outer()
    
    plt.show()

if __name__ == "__main__":
    main()
