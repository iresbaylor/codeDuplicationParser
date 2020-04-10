from common.io import write_data


def write_phase(data, num_players, phase):
    if num_players != -1:
        taken_data = data.take(num_players)
    else:
        taken_data = data

    if phase is 1:
        file = "BD"
    elif phase is 2:
        file = "ML"
    elif phase is 3:
        file = "DS"
    else:
        print("Bad phase")
        exit(1)

    selected_data = taken_data.select(taken_data["nameFirst"], taken_data["nameLast"],
                                      taken_data["RC"], taken_data["RC27"])

    write_data(selected_data, file)
