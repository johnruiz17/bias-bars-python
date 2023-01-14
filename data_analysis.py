"""
File: data_analysis.py
----------------------
This program read in data on cumulative infections of a disease
in different locations, and computes the number of infections
per day at each location.
"""

DATA_POINTS = 7


def load_data(filename):
    """
    The function takes in the name of a datafile (string), which
    contains data on locations and their seven day cumulative number
    of infections.  The function returns a dictionary in which the
    keys are the locations in the data file, and the value associated
    with each key is a list of the (integer) values presenting the
    cumulative number of infections at that location.
    >>> load_data('data/disease1.txt')
    {'Evermore': [1, 1, 1, 1, 1, 1, 1], 'Vanguard City': [1, 2, 3, 4, 5, 6, 7], 'Excelsior': [1, 1, 2, 3, 5, 8, 13]}
    """
    dictionary = {}

    with open(filename) as file:
        for line in file:
            line = line.strip()
            value = []
            index_of_key = line.find(',')
            key = line[0:index_of_key].strip()
            index_start = index_of_key

            # slices each part of the string between commas, gets number, and appends to value list
            for i in range(DATA_POINTS - 1):
                next_comma = line.find(',', index_start + 1, len(line))
                string = line[index_start:next_comma]
                num = get_num(string)
                value.append(num)
                index_start = next_comma

            last_string = line[index_start:len(line)]
            last_num = get_num(last_string)
            value.append(last_num)
            dictionary[key] = value

    return dictionary


def get_num(num_string):
    """
    This function returns a number from a sliced string.
    """
    num = ''
    for i in range(len(num_string)):
        if num_string[i].isdigit():
            num += num_string[i]
    num = int(num)

    return num


def daily_cases(cumulative):
    """
    The function takes in a dictionary of the type produced by the load_data
    function (i.e., keys are locations and values are lists of seven values
    representing cumulative infection numbers).  The function returns a
    dictionary in which the keys are the same locations in the dictionary
    passed in, but the value associated with each key is a list of the
    seven values (integers) presenting the number of new infections each
    day at that location.
    >>> daily_cases({'Test': [1, 2, 3, 4, 4, 4, 4]})
    {'Test': [1, 1, 1, 1, 0, 0, 0]}
    >>> daily_cases({'Evermore': [1, 1, 1, 1, 1, 1, 1], 'Vanguard City': [1, 2, 3, 4, 5, 6, 7], 'Excelsior': [1, 1, 2, 3, 5, 8, 13]})
    {'Evermore': [1, 0, 0, 0, 0, 0, 0], 'Vanguard City': [1, 1, 1, 1, 1, 1, 1], 'Excelsior': [1, 0, 1, 1, 2, 3, 5]}
    """
    dictionary = {}

    for key in cumulative:
        value = []
        prev_value = 0
        case_list = cumulative[key]

        # subtracts the previous cases from the current cases to get new cases
        for i in range(len(case_list)):
            if i == 0:
                value.append(case_list[i])
            else:
                current_value = case_list[i]
                new_cases = current_value - prev_value
                value.append(new_cases)

            prev_value = case_list[i]

        dictionary[key] = value

    return dictionary


def main():
    filename = 'data/disease1.txt'

    data = load_data(filename)
    print(f"Loaded datafile {filename}:")
    print(data)

    print("Daily infections: ")
    print(daily_cases(data))


if __name__ == '__main__':
    main()
