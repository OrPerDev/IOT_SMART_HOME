import tkinter as tk
from typing import Callable
from .map_panel import MapPanelGUI
from .record_control import RecordControlGUI


class ApplicationGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Application")
        self.window.configure(bg="#222")
        self.window_width = 900
        self.window_height = 600
        self.window.geometry(f"{self.window_width}x{self.window_height}")

        self.map_gui = MapPanelGUI(
            window=self.window,
            window_width=self.window_width,
            window_height=self.window_height,
            embed_button=self.embed_button,
            embed_text=self.embed_text,
        )
        self.record_control_gui = RecordControlGUI(
            window=self.window,
            window_width=self.window_width,
            window_height=self.window_height,
            embed_button=self.embed_button,
        )

    def update_pet_gps_location(self, location: tuple[float, float]) -> None:
        self.map_gui.update_pet_gps_coordinates(location)

    def update_user_gps_location(self, location: tuple[float, float]) -> None:
        self.map_gui.update_user_gps_coordinates(location)

    @property
    def on_start_recording_callback(self) -> Callable:
        return self.record_control_gui.on_start_recording_callback

    @on_start_recording_callback.setter
    def on_start_recording_callback(self, callback: Callable) -> None:
        self.record_control_gui.on_start_recording_callback = callback

    @property
    def on_stop_recording_callback(self) -> Callable:
        return self.record_control_gui.on_stop_recording_callback

    @on_stop_recording_callback.setter
    def on_stop_recording_callback(self, callback: Callable) -> None:
        self.record_control_gui.on_stop_recording_callback = callback

    def run(self):
        self.window.mainloop()

    def embed_button(
        self, command: Callable, text: str, x: float, y: float
    ) -> tk.Button:
        button = tk.Button(
            self.window,
            text=text,
            font=("Arial", 14, "bold"),
            bg="#4CAF50",
            fg="black",
            relief="raised",
            padx=20,
            pady=10,
            activebackground="#45A049",
            activeforeground="black",
            command=command,
        )
        button.place(x=x, y=y, anchor="center")
        return button

    def embed_text(self, text: str, x: float, y: float) -> tk.StringVar:
        text_value_bind = tk.StringVar()
        text_value_bind.set(text)

        label = tk.Label(
            self.window,
            textvariable=text_value_bind,
            font=("Arial", 18, "bold"),
            fg="white",
            bg="#222",
        )
        label.place(x=x, y=y, anchor="center")

        return text_value_bind
