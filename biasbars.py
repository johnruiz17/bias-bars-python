"""
File: biasbars.py
---------------------
This program displays the data for the frequency of words in student reviews of professors by gender and level
of rating. The data is dynamically displayed when the user searches a word. Using this program makes it possible to
visualize gender-based disparities in how students review their professors.
"""

import tkinter
import biasbarsdata
import biasbarsgui as gui


# Provided constants to load and plot the word frequency data
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 600

FILENAME = "data/full-data.txt"

VERTICAL_MARGIN = 30
LEFT_MARGIN = 60
RIGHT_MARGIN = 30
LABELS = ["Low Reviews", "Medium Reviews", "High Reviews"]
LABEL_OFFSET = 10
BAR_WIDTH = 75
LINE_WIDTH = 2
TEXT_DX = 10
TEXT_DY = 10
NUM_VERTICAL_DIVISIONS = 7
TICK_WIDTH = 15


def get_centered_x_coordinate(width, idx):
    """
    Given the width of the canvas and the index of the current review
    quality bucket to plot, returns the x coordinate of the centered
    location for the bars and label to be plotted relative to.

    Input:
        width (int): The width of the canvas
        year_index (int): The index of the current label in the LABELS list
    Returns:
        x_coordinate (float): The centered x coordinate of the horizontal line 
                              associated with the specified label.
    >>> round(get_centered_x_coordinate(1000, 0), 1)
    211.7
    >>> round(get_centered_x_coordinate(1000, 1), 1)
    515.0
    >>> round(get_centered_x_coordinate(1000, 2), 1)
    818.3
    """
    # the plotting area is divided into six parts: two smaller areas make up 2/6, and two larger areas make up 4/6
    fraction = (width - (LEFT_MARGIN + RIGHT_MARGIN)) / 6

    # the index determines how many proportional parts are added to the LEFT_MARGIN to get the x_coordinate
    if idx == 0:
        x_coordinate = LEFT_MARGIN + fraction
    elif idx == 1:
        x_coordinate = LEFT_MARGIN + (3 * fraction)
    else:
        x_coordinate = LEFT_MARGIN + (5 * fraction)

    return x_coordinate


def draw_fixed_content(canvas):
    """
    Erases all existing information on the given canvas and then
    draws the fixed background border and x-axis labels on it.

    Input:
        canvas (tkinter Canvas): The canvas on which we are drawing.
    """
    canvas.delete('all')            # delete all existing content from the canvas
    width = canvas.winfo_width()    # get the width of the canvas
    height = canvas.winfo_height()  # get the height of the canvas

    # creates a rectangle that will serve as the plotting area
    canvas.create_rectangle(LEFT_MARGIN, VERTICAL_MARGIN, width - RIGHT_MARGIN, height - VERTICAL_MARGIN, width=LINE_WIDTH)

    # creates evenly spaced labels for low, medium, and high reviews
    for i in range(len(LABELS)):
        x = get_centered_x_coordinate(width, i)
        y = height - VERTICAL_MARGIN + LABEL_OFFSET
        canvas.create_text(x, y, text=LABELS[i], anchor=tkinter.N)


def plot_word(canvas, word_data, word):
    """
    Given a dictionary of word frequency data and a single word, plots
    the distribution of the frequency of this word across gender and 
    rating category.

    Input:
        canvas (tkinter Canvas): The canvas on which we are drawing.
        word_data (dictionary): Dictionary holding word frequency data
        word (str): The word whose frequency distribution you want to plot
    """
    draw_fixed_content(canvas)
    width = canvas.winfo_width()
    height = canvas.winfo_height()

    # We have provided code to calculate the maximum frequency for the specified
    # word from the provided dict 
    gender_data = word_data[word]
    max_frequency = max(max(gender_data[biasbarsdata.KEY_WOMEN]), max(gender_data[biasbarsdata.KEY_MEN]))

    label_list = get_labels(max_frequency)
    tick_offset = TICK_WIDTH / 2
    start = height - VERTICAL_MARGIN
    increment = (height - (2 * VERTICAL_MARGIN)) / NUM_VERTICAL_DIVISIONS
    frequency_to_pixels = (height - (2 * VERTICAL_MARGIN)) / max_frequency

    # creates ticks and labels for the frequencies along the y-axis
    for i in range(NUM_VERTICAL_DIVISIONS):
        y = start - (i * increment)
        canvas.create_line(LEFT_MARGIN - tick_offset, y, LEFT_MARGIN + tick_offset, y, width=LINE_WIDTH)
        canvas.create_text(LEFT_MARGIN - LABEL_OFFSET, y, text=int(label_list[i]), anchor=tkinter.E)

    canvas.create_line(LEFT_MARGIN - tick_offset, VERTICAL_MARGIN, LEFT_MARGIN + tick_offset, VERTICAL_MARGIN,width=LINE_WIDTH)
    canvas.create_text(LEFT_MARGIN - LABEL_OFFSET, VERTICAL_MARGIN, text=int(max_frequency), anchor=tkinter.E)

    # creates bars for the graph as well as a label for men and women
    # frequencies are converted to pixels using frequency_to_pixels conversion factor
    for i in range(3):
        x_coordinate = get_centered_x_coordinate(width, i)
        canvas.create_rectangle(x_coordinate - BAR_WIDTH,
                                start - (word_data[word][biasbarsdata.KEY_WOMEN][i] * frequency_to_pixels),
                                x_coordinate, start, fill='dodgerblue')
        if word_data[word][biasbarsdata.KEY_WOMEN][i] > 0:
            canvas.create_text(x_coordinate - BAR_WIDTH + TEXT_DX,
                                start - (word_data[word][biasbarsdata.KEY_WOMEN][i] * frequency_to_pixels) + TEXT_DY,
                                text=biasbarsdata.KEY_WOMEN)
        canvas.create_rectangle(x_coordinate,
                                start - (word_data[word][biasbarsdata.KEY_MEN][i] * frequency_to_pixels),
                                x_coordinate + BAR_WIDTH, start, fill='orange')
        if word_data[word][biasbarsdata.KEY_MEN][i] > 0:
            canvas.create_text(x_coordinate + TEXT_DX,
                                start - (word_data[word][biasbarsdata.KEY_MEN][i] * frequency_to_pixels) + TEXT_DY,
                                text=biasbarsdata.KEY_MEN)


def get_labels(max_frequency):
    """
    Input: max_frequency value
    Output: a list of labels for the frequency
    """
    label_list = []
    label = 0
    label_increment = max_frequency // NUM_VERTICAL_DIVISIONS
    for i in range(NUM_VERTICAL_DIVISIONS):
        label_list.append(label)
        label += label_increment

    return label_list


def convert_counts_to_frequencies(word_data):
    """
    This code is provided to you! 

    It converts a dictionary 
    of word counts into a dictionary of word frequencies by 
    dividing each count for a given gender by the total number 
    of words found in reviews about professors of that gender.
    """ 
    K = 1000000
    total_words_men = sum([sum(counts[biasbarsdata.KEY_MEN]) for word, counts in word_data.items()])
    total_words_women = sum([sum(counts[biasbarsdata.KEY_WOMEN]) for word, counts in word_data.items()])
    for word in word_data:
        gender_data = word_data[word]
        for i in range(3):
            gender_data[biasbarsdata.KEY_MEN][i] *= K / total_words_men
            gender_data[biasbarsdata.KEY_WOMEN][i] *= K / total_words_women


# main() code is provided for you
def main():
    import sys
    args = sys.argv[1:]
    global WINDOW_WIDTH
    global WINDOW_HEIGHT
    if len(args) == 2:
        WINDOW_WIDTH = int(args[0])
        WINDOW_HEIGHT = int(args[1])

    # Load data
    word_data = biasbarsdata.read_file(FILENAME)
    convert_counts_to_frequencies(word_data)

    # Make window
    top = tkinter.Tk()
    top.wm_title('Bias Bars')
    canvas = gui.make_gui(top, WINDOW_WIDTH, WINDOW_HEIGHT, word_data, plot_word, biasbarsdata.search_words)

    # draw_fixed once at startup so we have the borders and labels
    # even before the user types anything.
    draw_fixed_content(canvas)

    # This needs to be called just once
    top.mainloop()


if __name__ == '__main__':
    main()
