import PySimpleGUI as sg
import pandas as pd
import numpy as np
import sklearn.metrics.pairwise as sk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from ast import literal_eval

movieDetailsDf = pd.read_csv("detailsDataset.csv") 

def show_table(data, header_list, fn):
    movieArr = pd.read_csv("finalDataset.csv") .to_numpy()
    layout = [
        [sg.Table(values=data,
                  headings=header_list,
		  row_height=30,
                  display_row_numbers=False,
		  background_color='gray',
                  auto_size_columns=True,
		  enable_events=True,
		  pad=20,
                  num_rows=min(25, len(data)),
		  key='_selectedRow_'),
	],
	[sg.Button('Recommend Movie', key='_select_'), sg.Text("Number of Movie Recommendation: "), sg.OptionMenu(values=['3', '5', '10', '15'], default_value="3", key="_dropdownMenu_")]
    ]

    window = sg.Window(fn, layout, grab_anywhere=False)
    # --- EVENT LOOP ---
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        if event == '_select_':
            similarity = sk.cosine_similarity([movieArr[values['_selectedRow_'][0] + 1]], \
		np.delete(movieArr, values['_selectedRow_'][0] + 1, 0))
            num = int(values['_dropdownMenu_'])
            ind = np.argpartition(similarity[0], -num)[-num:]
            open_window(ind, values['_selectedRow_'][0] + 1) 
    window.close()

def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg


def open_window(ind, selectedInd):
    header_list = list(movieDetailsDf.columns)
    data = movieDetailsDf.loc[ind].values.tolist()
    col2 = [
	[sg.Canvas(key='figCanvas'), sg.Canvas(key='figCanvas1')],
	[sg.Canvas(key='figCanvas3')]
    ]
    col1 =[
	[sg.Text("Selected Movie", justification='center')],
	[
		sg.Text("Title: "),
		sg.Text(movieDetailsDf.loc[selectedInd, "primaryTitle"])
	],
	[
		sg.Text("Adult Movie: "),
		sg.Text(movieDetailsDf.loc[selectedInd, "isAdult"])
	],
	[
		sg.Text("Year: "),
		sg.Text(movieDetailsDf.loc[selectedInd, "startYear"])
	],
	[
		sg.Text("Genres: "),
		sg.Text(movieDetailsDf.loc[selectedInd, "genres"])
	],
	[
		sg.Text("Directors: "),
		sg.Text(movieDetailsDf.loc[selectedInd, "directors"])
	],
        [sg.Table(values=data,
                  headings=header_list,
		  row_height=30,
		  pad=20,
		  background_color='gray',
                  display_row_numbers=False,
                  auto_size_columns=True,
		  enable_events=True,
                  num_rows=min(25, len(data)),
		  key='_selectedRow_'),],
        [sg.Canvas(key='figCanvas2'), ]
	
    ]
    layout = [
	[sg.Frame(layout=col1, title=""), sg.Column(col2, vertical_alignment='c')]
    ]
    window = sg.Window("Recommended Movie List", layout, grab_anywhere=False, finalize=True)
# Draw start year graph
    fig = plt.figure(figsize=(4,4))
    plt.hist(movieDetailsDf.loc[ind, "startYear"])
    plt.title("Recommended movie's years distributions")
    plt.xlabel("Start Year")
    plt.ylabel("Frequency")
    draw_figure(window['figCanvas'].TKCanvas, fig)

# Draw type of movie graph
    fig = plt.figure(figsize=(4,4))
    plt.hist(["Adult Movie" if item == 1 else "Non-Adult Movie" for item in movieDetailsDf.loc[ind, "isAdult"].to_numpy()])
    plt.title("Recommended movie's adult type distributions")
    plt.xlabel("Type of Movie")
    plt.ylabel("Frequency")
    draw_figure(window['figCanvas1'].TKCanvas, fig)

    fig = plt.figure(figsize=(7.5,5))
    arr = []
    for item in movieDetailsDf.loc[ind, "genres"].to_numpy():
        arr = arr + literal_eval(item)
    plt.hist(arr)
    plt.title("Recommended movie's genres distributions")
    plt.xlabel("Genres")
    plt.ylabel("Frequency")
    draw_figure(window['figCanvas3'].TKCanvas, fig)

    fig = plt.figure(figsize=(9,3))
    arr = []
    for item in movieDetailsDf.loc[ind, "directors"].to_numpy():
        arr = arr + literal_eval(item)
    plt.hist(arr)
    plt.xlabel("Directors")
    plt.title("Recommended movie's directors distributions")
    plt.ylabel("Frequency")
    draw_figure(window['figCanvas2'].TKCanvas, fig)

    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
    window.close()

def main():   
    header_list = list(movieDetailsDf.columns)
    data = movieDetailsDf[1:].values.tolist()
    show_table(data,header_list,"Movie List")

# Executes main
if __name__ == '__main__':
    main()