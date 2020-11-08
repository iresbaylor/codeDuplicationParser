from common.io import read_csv_table


def process_teams(spark, team_data, sort_attribute):
    data = join_teams(spark, team_data)
    return sort_teams(data, sort_attribute)


def join_teams(spark, team_data):
    player_data = read_csv_table(spark, "People")
    return team_data.join(player_data, team_data["playerID"] == player_data["playerID"])


def join_pitching_teams(spark, team_data):
    player_data = read_csv_table(spark, "People")
    return team_data.join(player_data, team_data["playerID"] == player_data["playerID"])\
        .select(team_data["playerID"],
                player_data["nameFirst"],
                player_data["nameLast"],
                team_data["H"],
                team_data["HR"],
                team_data["BB"])


def sort_teams(player_data, sort_attribute):
    if sort_attribute == 'RC':
        return player_data.sort(player_data["RC"], ascending=False)
    elif sort_attribute == 'RC27':
        return player_data.sort(player_data["RC27"], ascending=False)
    else:
        print("Invalid sort attribute given")
        return None