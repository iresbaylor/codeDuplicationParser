from pyspark.sql import SparkSession

from common.data import get_generated_pitching_data
from common.parse_args import parse_args
from common.players import process_teams
from common.print import write_phase
from common.rc import calculate_rc_base, calculate_rc27


def phase3(app_name):
    # Read the arguments
    args = parse_args()

    if args.year != 2018:
        print("Year must be 2018")
        return 1

    # Initialize Spark
    spark = SparkSession.builder.appName(app_name).getOrCreate()

    pitching_data = get_generated_pitching_data(spark, args.year, args.number)
    data = pitching_data.rdd.map(map_pitching_rc)
    dataframe = spark.createDataFrame(data, schema=["playerID", "RC", "RC27"])
    player_data = process_teams(spark, dataframe, args.attribute)
    write_phase(player_data, args.number, 3)


def map_pitching_rc(data):
    player_id = data["playerID"]
    rc = calculate_rc_base(data)
    rc_27 = calculate_rc27(data, rc)
    return player_id, rc, rc_27
