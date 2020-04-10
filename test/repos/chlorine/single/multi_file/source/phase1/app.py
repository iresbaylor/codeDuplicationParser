from pyspark.sql import SparkSession

from common.data import get_batting_team_data
from common.parse_args import parse_args
from common.players import process_teams
from common.print import write_phase
from common.rc import calculate_rc_base, calculate_rc27, get_val

"""
https://spark.apache.org/docs/latest/rdd-programming-guide.html
https://www.foxsports.com/mlb/stats?season=2018&category=BATTING+II&group=1&sort=4&time=0&pos=0&qual=1&sortOr
"""


def phase1(app_name):
    # Read the arguments
    args = parse_args()

    # Initialize Spark
    spark = SparkSession.builder.appName(app_name).getOrCreate()

    batting_team_data = get_batting_team_data(spark, args.year, args.min)
    data = batting_team_data.rdd.map(map_rc)
    dataframe = spark.createDataFrame(data, schema=["playerID", "RC", "RC27"])
    player_data = process_teams(spark, dataframe, args.attribute)
    write_phase(player_data, args.number, 1)


def map_rc(data):
    player_id = data["playerID"]
    rc, rc_27 = calc_park_adjusted_rc(data)
    return player_id, rc, rc_27


def calc_park_adjusted_rc(data):
    rc = calculate_rc_base(data)
    rc_27 = calculate_rc27(data, rc)
    bpf = get_val(data, "BPF_team", 100)
    # / 100 to adjust for percentage, / 2 to factor out away games
    adjusted_bpf = bpf / 100
    halved_bpf = (adjusted_bpf - 1) / 2 + adjusted_bpf
    return rc / halved_bpf, rc_27 / halved_bpf
