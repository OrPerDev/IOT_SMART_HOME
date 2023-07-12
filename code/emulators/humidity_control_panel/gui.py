import tkinter as tk
from typing import Callable


class HumidityControlGUI:
    def __init__(self):
        # initialize the window
        self.window = tk.Tk()

        # set window background color
        self.window.configure(bg="#222")

        # initialize the displayed text
        self.displayed_text = tk.StringVar()
        self.displayed_text.set("Waiting for data...")

        # calculate the radius and center coordinates
        radius = 100
        center_x = 200
        center_y = 150

        # calculate the positions for label and button
        label_x = center_x
        label_y = center_y - radius
        button_x = center_x
        button_y = center_y + radius

        # initialize the label for the displayed text
        self.displayed_text_label = tk.Label(
            self.window,
            textvariable=self.displayed_text,
            font=("Arial", 18, "bold"),
            fg="white",
            bg="#222",
        )
        self.displayed_text_label.place(x=label_x, y=label_y, anchor="center")

        # initialize the button
        self.adjust_humidity_button = tk.Button(
            self.window,
            text="Adjust humidity",
            font=("Arial", 14, "bold"),
            command=lambda: print("Humidity adjustment button clicked!"),
            bg="#4CAF50",
            fg="black",
            relief="raised",
            padx=20,
            pady=10,
            activebackground="#45A049",
            activeforeground="black",
        )
        self.adjust_humidity_button.place(x=button_x, y=button_y, anchor="center")

        # window title
        self.window.title("Humidity Control")

        # set the window size
        window_width = 400
        window_height = 300
        self.window.geometry(f"{window_width}x{window_height}")

    @property
    def on_adjust_humidity_call(self) -> Callable:
        return self.adjust_humidity_button["command"]

    @on_adjust_humidity_call.setter
    def on_adjust_humidity_call(self, callback: Callable):
        self.adjust_humidity_button["command"] = callback

    def update_humidity_level(self, level: float) -> None:
        text = f"Current humidity level: {level}"
        self.displayed_text.set(text)

    def run(self):
        self.window.mainloop()
