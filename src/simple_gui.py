import PySimpleGUI as sg
import pathlib
import asyncio
import sys
import tkinter as tk
from tkinter import filedialog

import auswertung

size = 11
height = 1
file_path = ""

layout = [
    [sg.Text('select root folder', size=(size + 10,height), background_color="blue")],
    [sg.Text('selected path:', size=(size,height)), sg.InputText(pathlib.Path().resolve(), key="csv_root_filepath", size=(size + 50, height)),
     sg.Button("open path dialog", key="button_openfiledialog", size=(size, height))],
    [sg.Check('pixel plot', key='do_pixel_plot', default=False, visible=True), sg.Check('array plot', key='do_array_plot', default=False, visible=True), sg.Check('summary plot', key='do_summary_plot', default=True, visible=True)],
    # [sg.Button("generate", key="button_generate_plots", size=(size, height))],
    [sg.Check('correction', key='do_correction', default=False, visible=True)],
    [sg.Text('ready', key='info', size=(size,height), background_color="green")]
]


async def main_window():
    global file_path, event_dict

    sg.theme("Dark")
    window = sg.Window('vlad plot slave', layout, size=(700, 180))
    win = window
    while True:
        window.refresh()
        event, values = window.read(timeout=0)
        if event == sg.WINDOW_CLOSED:
            break

        # Routine ---------------------------------
        if event == "button_openfiledialog":
            root = tk.Tk()
            root.withdraw()

            file_path = filedialog.askdirectory()
            plot_factory = auswertung.Auswertung(file_path, values["do_pixel_plot"], values["do_array_plot"], values["do_summary_plot"], values["do_correction"])
            win["info"].Update("processing....")
            await asyncio.sleep(0.1)
            success = await plot_factory.build()
            win["info"].Update("done")
            print('\033[91m' + 'work done. closing...' + '\033[0m')
            sg.Popup(success)

            sys.exit(0)
            window.close()
            #win["csv_root_filepath"].Update(file_path)

        if event == "button_generate_plots":
            i = 0

        await asyncio.sleep(0.1)

    window.close()
    sys.exit(0)
