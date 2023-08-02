import tkinter as tk
from typing import Callable, Protocol, Optional


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

        self._on_start_recording_callback = lambda: print("Start recording")
        self._on_stop_recording_callback = lambda: print("Stop recording")
        self._on_send_record_command = lambda: print("Send record")
        self._on_cancel_record_command = lambda: print("Cancel record")

        self.control_buttons_y = self.window_height / 2 + 250

        self.prepare_cancel_button()
        self.prepare_recording_control_button()
        self.prepare_send_button()

        self.toggle_recording_button(target_is_recording=self.is_recording)
        self.update_audio_choice_controllers_visibility(display=False)

    def prepare_recording_control_button(self):
        self.record_control_button = self.embed_button(
            command=lambda: print("Record"),
            text="Loading...",
            x=self.window_width / 2,
            y=self.control_buttons_y,
        )

    def prepare_cancel_button(self):
        self.cancel_button = self.embed_button(
            command=lambda: print("Cancel"),
            text="Cancel",
            x=self.window_width / 2 - 200,
            y=self.control_buttons_y,
        )

        self.cancel_button["command"] = lambda: self.audio_choice_command_wrapper(
            self._on_cancel_record_command
        )

    def prepare_send_button(self):
        self.send_button = self.embed_button(
            command=lambda: print("Send"),
            text="Send",
            x=self.window_width / 2 + 200,
            y=self.control_buttons_y,
        )
        self.send_button["command"] = lambda: self.audio_choice_command_wrapper(
            self._on_send_record_command
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

    @property
    def on_send_record_command(self) -> Callable:
        return self._on_send_record_command

    @on_send_record_command.setter
    def on_send_record_command(self, callback: Callable) -> None:
        self._on_send_record_command = callback

    @property
    def on_cancel_record_command(self) -> Callable:
        return self._on_cancel_record_command

    @on_cancel_record_command.setter
    def on_cancel_record_command(self, callback: Callable) -> None:
        self._on_cancel_record_command = callback

    def record_control_button_command_wrapper(self, callback: Callable) -> None:
        callback()
        trigger_state_is_recording = self.is_recording
        self.toggle_recording_button()
        self.update_audio_choice_controllers_visibility(
            display=trigger_state_is_recording
        )

    def audio_choice_command_wrapper(self, callback: Callable) -> None:
        callback()
        self.update_audio_choice_controllers_visibility(display=False)

    def update_record_control_button_to_recording_mode(self) -> None:
        self.record_control_button["text"] = "Stop recording"
        self.record_control_button[
            "command"
        ] = lambda: self.record_control_button_command_wrapper(
            self._on_stop_recording_callback
        )

    def update_record_control_button_to_not_recording_mode(self) -> None:
        self.record_control_button["text"] = "Record audio"
        self.record_control_button[
            "command"
        ] = lambda: self.record_control_button_command_wrapper(
            self._on_start_recording_callback
        )

    def toggle_recording_button(
        self, target_is_recording: Optional[bool] = None
    ) -> None:
        if target_is_recording is not None:
            # force
            self.is_recording = target_is_recording
        else:
            # toggle
            self.is_recording = not self.is_recording

        if self.is_recording:
            self.update_record_control_button_to_recording_mode()
        else:
            self.update_record_control_button_to_not_recording_mode()

    def update_audio_choice_controllers_visibility(self, display: bool = True):
        if display:
            # make visible self.cancel_button
            self.cancel_button.place(
                x=self.window_width / 2 - 200,
                y=self.control_buttons_y,
                anchor=tk.CENTER,
            )
            # make visible self.send_button
            self.send_button.place(
                x=self.window_width / 2 + 200,
                y=self.control_buttons_y,
                anchor=tk.CENTER,
            )
        else:
            # make invisible self.cancel_button
            self.cancel_button.place_forget()
            # make invisible self.send_button
            self.send_button.place_forget()
