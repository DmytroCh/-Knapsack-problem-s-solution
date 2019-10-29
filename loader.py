import csv
import os


def read_input_data(relative_dir, file_name):

    script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
    bag_size = -1
    best_result = list()
    items = list()
    with open(script_dir + relative_dir + file_name) as csv_file:
        csv_reader = list(csv.reader(csv_file, delimiter=','))
        line_count = 0
        for row in range(0, len(csv_reader)):
            if row == 0:
                bag_size = int(csv_reader[row][1])
            elif row == len(csv_reader) - 1:
                best_result = list(map(lambda item: int(item), csv_reader[row]))
            else:
                items.append(list(map(lambda item: int(item), csv_reader[row])))
            line_count += 1
        print(f'Processed {line_count} lines.')

    return bag_size, items, best_result

# read_input_data("/data/single/", "p01.csv")
