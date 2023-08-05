from pyspark.sql import SparkSession
spark = SparkSession.builder.getOrCreate()

def run():
    print(spark.sparkContext.parallelize([1,2]).sum())
