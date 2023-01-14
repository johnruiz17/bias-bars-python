"""
File: biasbarsgui.py
------------------------
Stanford CS106A Bias Bars
Adapted from the original Bias Bars assignment (created
by Colin Kincaid, Annie Hu, Jennie Yang, and Monica 
Anuforo) by Nick Bowman and Katie Creel

This file defines the functions needed to create the GUI for
the Bias Bars program.

You should not modify any of the contents of this file.
"""

import tkinter


# provided function to build the GUI
def make_gui(top, width, height, word_data, plot_word, search_words):
    """
    Set up the GUI elements for Bias Bars, returning the Canvas to use.
    top is TK root, width/height is canvas size, word_data is Bias Bars Data dict.
    """
    # word entry field
    label = tkinter.Label(top, text="Word To Plot:")
    label.grid(row=0, column=0, sticky='w')
    entry = tkinter.Entry(top, width=40, name='entry', borderwidth=2)
    entry.grid(row=0, column=1, sticky='w')
    entry.focus()
    error_out = tkinter.Text(top, height=2, width=70, name='errorout', borderwidth=2)
    error_out.grid(row=0, column=2, sticky='w')

    # canvas for drawing
    canvas = tkinter.Canvas(top, width=width, height=height, name='canvas')
    canvas.grid(row=1, columnspan=12, sticky='w')

    space = tkinter.LabelFrame(top, width=10, height=10, borderwidth=0)
    space.grid(row=2, columnspan=12, sticky='w')

    # Search field etc. at the bottom
    label = tkinter.Label(top, text="Search:")
    label.grid(row=3, column=0, sticky='w')
    search_entry = tkinter.Entry(top, width=40, name='searchentry')
    search_entry.grid(row=3, column=1, sticky='w')
    search_out = tkinter.Text(top, height=2, width=70, name='searchout', borderwidth=2)
    search_out.grid(row=3, column=2, sticky='w')

    # When <return> key is hit in a text field .. connect to the handle_draw()
    # and handle_search() functions to do the work.
    entry.bind("<Return>", lambda event: handle_plot(entry, canvas, word_data, error_out, plot_word))
    search_entry.bind("<Return>", lambda event: handle_search(search_entry, search_out, word_data, search_words))

    top.update()
    return canvas


def handle_plot(entry, canvas, word_data, error_out, plot):
    """
    (provided)
    Called when <return> key hit in given entry text field.
    Gets search text from given entry, draws results
    to the given canvas.
    """
    text = entry.get()

    error_out.delete('1.0', tkinter.END)
    if not text:
        error_out.insert('1.0', "Please enter a non-empty word.")
    elif " " in text:
        error_out.insert('1.0', "The program cannot search for multiple words at a time. Please enter a single word with no spaces.")
    elif text.lower() not in word_data:
        error_out.insert('1.0', f"{text} is not contained in the word database.")
    else:
        plot(canvas, word_data, text.lower())


def handle_search(search_entry, search_out, word_data, search):
    """
    (provided) Called for <return> key in lower search field.
    Calls biasbarsdata.search_words() and displays results in GUI.
    Gets search target from given search_entry, puts results
    in given search_out text area.
    """
    target = search_entry.get().strip()
    if target:
        # Call the search_words function in biasbarsdata.py
        result = search(word_data, target)
        out = ' '.join(result)
        search_out.delete('1.0', tkinter.END)
        search_out.insert('1.0', out)
