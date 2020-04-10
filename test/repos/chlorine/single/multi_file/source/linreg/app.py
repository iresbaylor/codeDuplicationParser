from pyspark.ml.feature import VectorAssembler
from pyspark.ml.regression import LinearRegression
from pyspark.sql import SparkSession

from common.data import get_batting_team_data
from common.rc import calculate_rc_constants, calculate_rc_base


def linreg(app_name):
    # Initialize Spark
    spark = SparkSession.builder.appName(app_name).getOrCreate()

    batting_team_data_2017 = get_batting_team_data(spark, 2017, 0)
    constants = batting_team_data_2017.rdd.map(map_constants)
    dataframe = spark.createDataFrame(constants, schema=["t1", "t2", "t3", "RC"])
    # source: https://towardsdatascience.com/building-a-linear-regression-with-pyspark-and-mllib-d065c3ba246a
    assembler = VectorAssembler(inputCols=["t1", "t2", "t3", "RC"], outputCol="features")
    vdata = assembler.transform(dataframe)
    vdata = vdata.select(["features", "t1", "t2", "t3", "RC"])
    lr = LinearRegression(featuresCol="features", labelCol="RC", maxIter=10, regParam=0.3, elasticNetParam=0.8)
    lr_model = lr.fit(vdata)
    print(lr_model.coefficients)


def map_constants(data):
    tb, s1, s2, s3, s4 = calculate_rc_constants(data)
    rc = calculate_rc_base(data)
    if s4 == 0:
        return 0.0, 0.0, 0.0, 0.0

    t1 = (s1 * tb) / s4
    t2 = (s1 * s2) / s4
    t3 = s3 / s4

    return t1, t2, t3, rc
