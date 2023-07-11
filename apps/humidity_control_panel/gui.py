import tkinter as tk
from typing import Callable


class HumidityControlGUI:
    def __init__(self):
        # initialize the window
        self.window = tk.Tk()

        # initialize the displayed text
        self.displayed_text = tk.StringVar()
        self.displayed_text.set("Waiting for data...")
        # initialize the label for the displayed text
        self.displayed_text_label = tk.Label(
            self.window, textvariable=self.displayed_text
        )
        self.displayed_text_label.pack()

        # initialize the button
        self.adjust_humidity_button = tk.Button(self.window, text="Adjust humidity")
        self.adjust_humidity_button.pack()

        # window title
        self.window.title("Humidity control")

        # window size
        self.window.geometry("400x300")

    @property
    def on_adjust_humidiy_call(self) -> Callable:
        return self.adjust_humidity_button["command"]

    @on_adjust_humidiy_call.setter
    def on_adjust_humidiy_call(self, callback: Callable):
        self.adjust_humidity_button["command"] = callback

    def update_humidity_level(self, level: float) -> None:
        text = f"Current humidity level: {level}"
        self.displayed_text.set(text)

    def run(self):
        self.window.mainloop()
