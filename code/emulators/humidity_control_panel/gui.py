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

        # initialize the label for the displayed text
        self.displayed_text_label = tk.Label(
            self.window,
            textvariable=self.displayed_text,
            font=("Arial", 18),
            bg="#222",
        )
        self.displayed_text_label.pack(pady=20)

        # initialize the button
        self.adjust_humidity_button = tk.Button(
            self.window,
            text="Adjust humidity",
            font=("Arial", 14, "bold"),
            command=lambda: print("Humidity adjustment button clicked!"),
            bg="#ffffff",
            fg="#222",
            relief="flat",
            padx=10,
            pady=5,
            activebackground="#ffffff",
            activeforeground="#222",
        )
        self.adjust_humidity_button.pack(pady=10)

        # window title
        self.window.title("Humidity Control")

        # center the window on the screen
        window_width = 400
        window_height = 300
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x_coordinate = int((screen_width / 2) - (window_width / 2))
        y_coordinate = int((screen_height / 2) - (window_height / 2))
        self.window.geometry(
            f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}"
        )

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
