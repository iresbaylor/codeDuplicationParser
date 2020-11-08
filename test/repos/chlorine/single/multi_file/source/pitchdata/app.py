from contextlib import closing

from bs4 import BeautifulSoup
from pyspark.sql import SparkSession
from requests import get, RequestException

from common.data import get_pitching_data
from common.io import write_data
from common.players import join_pitching_teams

"""
Tutorial used: https://realpython.com/python-web-scraping-practical-introduction
"""


def get_pitch_data(app_name):
    # Initialize Spark
    spark = SparkSession.builder.appName(app_name).getOrCreate()
    pitching_data = get_pitching_data(spark, 2018, 0)
    pitching_player_data = join_pitching_teams(spark, pitching_data)

    pitching_matchups_raw = get_page("PITCHING+MATCHUPS")
    matchup_data_frame = parse_matchups_page(spark, pitching_matchups_raw)
    pitching_matchups_raw = get_page("PITCHING+MATCHUPS&page=2")
    matchup_data_frame.union(parse_matchups_page(spark, pitching_matchups_raw))

    pitching_ii = get_page("PITCHING+II")
    ii_data_frame = parse_ii_page(spark, pitching_ii)
    for i in range(2, 17):
        pitching_ii = get_page("PITCHING+II&page=" + str(i))
        ii_data_frame.union(parse_ii_page(spark, pitching_ii))

    joined_frame = matchup_data_frame.join(ii_data_frame,
                                           (matchup_data_frame["last_name"] == ii_data_frame["last_name"]) &
                                           (matchup_data_frame["first_name"] == ii_data_frame["first_name"]))\
        .select(matchup_data_frame["last_name"],
                matchup_data_frame["first_name"],
                matchup_data_frame["yearID"],
                matchup_data_frame["AB"],
                matchup_data_frame["2B"],
                matchup_data_frame["3B"],
                matchup_data_frame["SB"],
                matchup_data_frame["CS"],
                matchup_data_frame["SH"],
                matchup_data_frame["SF"],
                ii_data_frame["BF"],
                ii_data_frame["IBB"],
                ii_data_frame["HBP"],
                ii_data_frame["GIDP"])\
        .sort(matchup_data_frame["last_name"])

    final_frame = joined_frame.join(pitching_player_data,
                                    (joined_frame["last_name"] == pitching_player_data["nameLast"]) &
                                    (joined_frame["first_name"] == pitching_player_data["nameFirst"]))\
        .select(pitching_player_data["playerID"],
                pitching_player_data["H"],
                pitching_player_data["HR"],
                pitching_player_data["BB"],
                joined_frame["yearID"],
                joined_frame["AB"],
                joined_frame["2B"],
                joined_frame["3B"],
                joined_frame["SB"],
                joined_frame["CS"],
                joined_frame["SH"],
                joined_frame["SF"],
                joined_frame["BF"],
                joined_frame["IBB"],
                joined_frame["HBP"],
                joined_frame["GIDP"])\
        .sort(pitching_player_data["playerID"])
    write_data(final_frame, "Pitching.csv")


def get_page(page):
    url = "https://www.foxsports.com/mlb/stats?season=2018&category=" + page
    try:
        with closing(get(url, stream=True)) as response:
            if valid_response(response):
                return response.content
            else:
                print("No page found")
                return None
    except RequestException as e:
        print("Error: bad request to " + url + ": " + str(e))


def valid_response(response):
    content_type = response.headers["Content-Type"].lower()
    if response.status_code == 200 and content_type is not None and content_type.find("html") > -1:
        return True
    return False


def parse_matchups_page(spark, raw_html):
    pitching_matchups_html = BeautifulSoup(raw_html, "html.parser")
    matchup_data = []
    rows = pitching_matchups_html.select("tr")
    for row in rows:
        data = row.select("td")
        if len(data) > 0:
            name = str(data[0].select("div")[0].select("a")[0].select("span")[0].string).strip(" ")
            names = name.split(",")
            last_name = names[0].strip()
            first_name = names[1].strip()
            yearID = 2018
            ab = int(data[4].string)
            two_b = int(data[6].string)
            three_b = int(data[7].string)
            sb = int(data[9].string)
            cs = int(data[10].string)
            sh = 0
            sf = 0
            matchup_data.append([last_name, first_name, yearID, ab, two_b, three_b, sb, cs, sh, sf])

    return spark.createDataFrame(matchup_data,
                                 schema=["last_name", "first_name", "yearID", "AB", "2B", "3B", "SB", "CS", "SH", "SF"])


def parse_ii_page(spark, raw_html):
    ii_data = []
    for row in BeautifulSoup(raw_html, "html.parser").select("tr"):
        data = row.select("td")
        if len(data) > 0:
            name = str(data[0].select("div")[0].select("a")[0].select("span")[0].string)
            names = name.split(",")
            last_name = names[0].strip()
            first_name = names[1].strip()
            bf = int(data[5].string)
            ibb = int(data[6].string)
            hbp = int(data[7].string)
            gidp = int(data[10].string)
            ii_data.append([last_name, first_name, bf, ibb, hbp, gidp])

    return spark.createDataFrame(ii_data, schema=["last_name", "first_name", "BF", "IBB", "HBP", "GIDP"])
