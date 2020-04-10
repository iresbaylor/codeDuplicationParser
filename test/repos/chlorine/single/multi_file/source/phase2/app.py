from pyspark.sql import SparkSession

from common.data import get_batting_team_data
from common.parse_args import parse_args
from common.players import process_teams
from common.rc import calculate_rc, calculate_rc27
from common.print import write_phase


def phase2(app_name):
    # Read the arguments
    args = parse_args()

    if args.year < 2017 or args.year > 2018:
        print("Year must be 2017 or 2018")
        return 1

    # Initialize Spark
    spark = SparkSession.builder.appName(app_name).getOrCreate()

    batting_team_data = get_batting_team_data(spark, args.year, args.min)
    data = batting_team_data.rdd.map(map_coefficients)
    dataframe = spark.createDataFrame(data, schema=["playerID", "RC", "RC27"])
    player_data = process_teams(spark, dataframe, args.attribute)
    write_phase(player_data, args.number, 2)


def map_coefficients(data):
    # Coefficients taken from the result of linear regression
    a = 0.46883885947526854
    b = 0.5256809788921046
    c = 0.12652211466103797
    d = 0.0

    player_id = data["playerID"]
    rc = calculate_rc(data, b, c, d) / a
    rc27 = calculate_rc27(data, rc)
    return player_id, rc, rc27
