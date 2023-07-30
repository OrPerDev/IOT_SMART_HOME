import tkinter as tk
from typing import Callable, Protocol


class EmbedButtonFn(Protocol):
    def __call__(self, command: Callable, text: str, x: float, y: float) -> tk.Button:
        ...


class RecordControlGUI:
    def __init__(
        self,
        window: tk.Tk,
        window_width: int,
        window_height: int,
        embed_button: EmbedButtonFn,
    ):
        self.window = window
        self.embed_button = embed_button
        self.window_width = window_width
        self.window_height = window_height

        self.is_recording = False

        self._on_start_recording_callback = lambda: print("Audio Recording started!")

        self._on_stop_recording_callback = lambda: print("Audio Recording stopped!")

        self.command = lambda: None

        self.prepare_recording_control_button()

        self.toggle_recording_button(recording=self.is_recording)

    def prepare_recording_control_button(self):
        self.button_coordinates = (self.window_width / 2, self.window_height / 2 + 250)

        self.record_control_button = self.embed_button(
            command=self.command_wrapper,
            text="Loading...",
            x=self.button_coordinates[0],
            y=self.button_coordinates[1],
        )

    @property
    def on_start_recording_callback(self) -> Callable:
        return self._on_start_recording_callback

    @on_start_recording_callback.setter
    def on_start_recording_callback(self, callback: Callable) -> None:
        self._on_start_recording_callback = callback

    @property
    def on_stop_recording_callback(self) -> Callable:
        return self._on_stop_recording_callback

    @on_stop_recording_callback.setter
    def on_stop_recording_callback(self, callback: Callable) -> None:
        self._on_stop_recording_callback = callback

    def command_wrapper(self) -> None:
        self.command()
        self.toggle_recording_button(not self.is_recording)

    def toggle_recording_button(self, recording: bool) -> None:
        self.is_recording = recording
        if recording:
            self.record_control_button["text"] = "Stop recording"
            self.command = self._on_stop_recording_callback
        else:
            self.record_control_button["text"] = "Record audio"
            self.command = self._on_start_recording_callback
