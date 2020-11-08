def read_csv_table(spark, tablename):
    return spark.read.format("csv").option("header", "true").option("inferSchema", "true") \
        .load("hdfs://localhost:8020/user/baseball/core/" + tablename + ".csv")


def read_generated_csv_table(spark, tablename):
    return spark.read.format("csv").option("header", "true").option("inferSchema", "true")\
        .load("hdfs://localhost:8020/user/wood/" + tablename + ".csv")


def write_data(data, file):
    data.write.csv("hdfs://localhost:8020/user/wood/" + file, mode="overwrite", header=True)
