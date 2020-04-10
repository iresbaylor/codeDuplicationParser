from pyspark.sql.functions import col
from common.io import read_csv_table, read_generated_csv_table


def get_batting_team_data(spark, year, min_atbats):
    batting_data = get_batting_data(spark, year, min_atbats)
    team_data = get_team_data(spark)
    return batting_data.join(team_data, (batting_data['yearID'] == team_data['yearID_team']) &
                             (batting_data['teamID'] == team_data['teamID_team']))


def get_batting_data(spark, year, min_atbats):
    batting_data = read_csv_table(spark, "Batting")
    return batting_data.filter((batting_data['yearID'] == year) & (batting_data['AB'] >= min_atbats))


def get_team_data(spark):
    team_data = read_csv_table(spark, "Teams")
    # Taken from https://stackoverflow.com/questions/33778664/spark-dataframe-distinguish-columns-with-duplicated-name
    return team_data.select(*(col(c).alias(c + "_team") for c in team_data.columns))


def get_pitching_data(spark, year, min_batters):
    pitching_data = read_csv_table(spark, "Pitching")
    return pitching_data.filter((pitching_data['yearID'] == year) & (pitching_data['BFP'] >= min_batters))


def get_generated_pitching_data(spark, year, min_batters):
    pitching_data = read_generated_csv_table(spark, "Pitching")
    return pitching_data.filter((pitching_data['yearID'] == year) & (pitching_data['BF'] >= min_batters))

