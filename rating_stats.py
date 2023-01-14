"""
File: rating_stats.py
----------------------
This file defines a program that allows a user to calculate
baseline summary statistics about a datafile of professor review
"""


def calculate_rating_stats(filename):
    """
    This function analyzes the professor review data in the given
    file to calculate the percentage of reviews for both men and
    women that fall in the "high rating" bucket, which is a numerical
    rating that is greater than 3.5.

    The resulting information is printed to the console.
    """
    total_female_reviews = 0
    high_female_reviews = 0
    total_male_reviews = 0
    high_male_reviews = 0

    with open(filename) as file:
        next(file)
        for line in file:
            line = line.strip()
            index_1 = line.find(',')
            rating = float(line[0:index_1])
            index_2 = line.find(',', index_1 + 1, len(line))
            gender = line[index_1 + 1:index_2].upper()

            if gender == 'W':
                total_female_reviews += 1
                if rating > 3.5:
                    high_female_reviews += 1
            else:
                total_male_reviews += 1
                if rating > 3.5:
                    high_male_reviews += 1

    female_percentage = round((high_female_reviews / total_female_reviews) * 100)
    male_percentage = round((high_male_reviews / total_male_reviews) * 100)

    print(f'{female_percentage}% of reviews for women in the dataset are high.')
    print(f'{male_percentage}% of reviews for men in the dataset are high.')


def main():
    # Ask the user to input the name of a file
    filename = input("Which data file would you like to load? ")

    # Calculate review distribution statistics by gender for
    # that file. This function should print out the results of
    # the analysis to the console.
    calculate_rating_stats(filename)


if __name__ == '__main__':
    main()
