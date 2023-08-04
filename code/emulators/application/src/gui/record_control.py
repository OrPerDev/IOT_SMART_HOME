import tkinter as tk
from typing import Callable, Protocol, Optional
from common.structs import AudioRecord


class EmbedButtonFn(Protocol):
    def __call__(
        self, command: Callable, text: str, x: float, y: float, **kwargs
    ) -> tk.Button:
        ...


class EmbedTextFn(Protocol):
    def __call__(self, text: str, x: float, y: float) -> tk.StringVar:
        ...


class AudioRecordActionFn(Protocol):
    def __call__(self, record: AudioRecord) -> None:
        ...


class RecordControlGUI:
    def __init__(
        self,
        window: tk.Tk,
        window_width: int,
        window_height: int,
        embed_button: EmbedButtonFn,
        embed_text: EmbedTextFn,
    ):
        self.window = window
        self.embed_button = embed_button
        self.embed_text = embed_text
        self.window_width = window_width
        self.window_height = window_height

        self.is_recording = False

        self.selected_audio_record: Optional[AudioRecord] = None

        self._on_start_recording_callback = lambda *args, **kwargs: print(
            "Start recording"
        )
        self._on_stop_recording_callback = lambda *args, **kwargs: print(
            "Stop recording"
        )
        self._on_send_audio_record_callback = lambda *args, **kwargs: print(
            "Send record"
        )
        self._on_delete_audio_record_callback = lambda *args, **kwargs: print(
            "Delete record"
        )
        self._on_save_audio_record_callback = lambda *args, **kwargs: print(
            "Save audio record"
        )
        self._on_update_audio_record_name_callback = lambda *args, **kwargs: print(
            "Update audio record name"
        )
        self._on_play_audio_record_callback = lambda *args, **kwargs: print(
            "Play audio record"
        )
        self._on_fetch_audio_records_callback = lambda: []

        self.lb = None
        self.lb_scrollbar = None

        self.edit_name_input_box = None

        self.section_y = 0
        self.section_x = self.window_width / 2

        self.section_x_center = (
            self.section_x + (self.window_width - self.section_x) / 2
        )

        self.audio_records_list: list[AudioRecord] = []

        self.prepare_title()

        self.prepare_record_name_edit_input_box()

        self.prepare_recording_control_button()
        self.prepare_delete_button()
        self.prepare_send_button()
        self.prepare_play_button()
        self.prepare_update_name_button()

        self.toggle_recording_button(target_is_recording=self.is_recording)
        self.update_audio_choice_controllers_visibility(display=False)

    def prepare_record_name_edit_input_box(self):
        self.edit_name_input_box = tk.Text(
            self.window,
            height=1,
            width=20,
        )

        self.toggle_record_name_edit_input_box(disabled=True)

    def toggle_record_name_edit_input_box(self, disabled: bool):
        if self.edit_name_input_box is None:
            return

        if disabled:
            self.edit_name_input_box.place_forget()
            self.edit_name_input_box.config(state=tk.DISABLED)
        else:
            self.edit_name_input_box.place(
                x=self.section_x_center,
                y=self.section_y + 300,
                anchor=tk.CENTER,
            )
            self.edit_name_input_box.config(state=tk.NORMAL)

    def create_lb_scollbar(self):
        if self.lb_scrollbar is not None:
            self.lb_scrollbar.place_forget()
            self.lb_scrollbar = None
        self.lb_scrollbar = tk.Scrollbar(
            self.window,
            orient="vertical",
        )
        self.lb_scrollbar.place(
            x=self.section_x_center + 100 + 28,
            y=self.section_y + 186,
            anchor=tk.CENTER,
            height=82,
        )

    def update_audio_records_list(self):
        if self._on_fetch_audio_records_callback is None:
            self.audio_records_list = []
        else:
            self.audio_records_list = self._on_fetch_audio_records_callback()

        # clear listbox
        if self.lb is not None:
            self.lb.delete(0, tk.END)

        # insert new records
        self.lb = tk.Listbox(
            self.window,
            width=30,
            height=5,
            borderwidth=2,
            highlightthickness=0,
            selectmode=tk.SINGLE,
        )

        for record in self.audio_records_list:
            if record.name is None:
                continue
            self.lb.insert(tk.END, record.name)

        self.lb.place(x=self.section_x_center, y=self.section_y + 185, anchor=tk.CENTER)

        self.create_lb_scollbar()
        if self.lb_scrollbar is not None:
            self.lb.config(yscrollcommand=self.lb_scrollbar.set)
            self.lb_scrollbar.config(command=self.lb.yview)

        self.lb.bind("<<ListboxSelect>>", self.on_audio_record_selected)

    def on_audio_record_selected(self, event):
        if self.lb is None:
            self.toggle_record_name_edit_input_box(disabled=True)
            return
        selection = self.lb.curselection()
        if len(selection) == 0:
            self.toggle_record_name_edit_input_box(disabled=True)
            return
        index = selection[0]
        if len(self.audio_records_list) <= index:
            print("Index out of bounds")
            self.toggle_record_name_edit_input_box(disabled=True)
            return
        self.selected_audio_record = self.audio_records_list[index]
        self.update_audio_choice_controllers_visibility(display=True)
        self.toggle_record_name_edit_input_box(disabled=False)

    def prepare_title(self):
        self.embed_text(
            text="Talk to your pet!",
            x=self.section_x_center,
            y=self.section_y + 25,
        )

    def prepare_recording_control_button(self):
        self.record_control_button = self.embed_button(
            command=lambda: print("Record"),
            text="Loading...",
            x=self.section_x_center,
            y=self.section_y + 25 + 50,
        )

    def prepare_delete_button(self):
        self.delete_button = self.embed_button(
            command=lambda: print("Delete"),
            text="Delete",
            x=0,
            y=0,
        )

        self.delete_button["command"] = lambda: self.audio_choice_command_wrapper(
            self._on_delete_audio_record_callback
        )

    def prepare_update_name_button(self):
        self.update_name_button = self.embed_button(
            command=lambda: print("Update"),
            text="Update",
            x=0,
            y=0,
        )

        def update_audio_record_name_callback(record: AudioRecord):
            if self.edit_name_input_box is None:
                print("Cannot update name without input box")
                return
            suggested_name = self.edit_name_input_box.get("1.0", tk.END)
            suggested_name = suggested_name.strip()
            if len(suggested_name) == 0:
                print("Cannot update name to empty string")
                return
            record.name = suggested_name
            self._on_update_audio_record_name_callback(record)
            self.edit_name_input_box.delete("1.0", tk.END)
            self.toggle_record_name_edit_input_box(disabled=True)

        self.update_name_button["command"] = lambda: self.audio_choice_command_wrapper(
            update_audio_record_name_callback
        )

    def prepare_send_button(self):
        self.send_button = self.embed_button(
            command=lambda: print("Send"),
            text="Send",
            x=0,
            y=0,
        )
        self.send_button["command"] = lambda: self.audio_choice_command_wrapper(
            self._on_send_audio_record_callback
        )

    def prepare_play_button(self):
        self.play_button = self.embed_button(
            command=lambda: print("Play"),
            text="Play",
            x=0,
            y=0,
        )
        self.play_button["command"] = lambda: self.audio_choice_command_wrapper(
            self._on_play_audio_record_callback
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
    def on_play_audio_record_callback(self) -> AudioRecordActionFn:
        return self._on_play_audio_record_callback

    @on_play_audio_record_callback.setter
    def on_play_audio_record_callback(self, callback: AudioRecordActionFn) -> None:
        self._on_play_audio_record_callback = callback

    @property
    def on_send_audio_record_callback(self) -> AudioRecordActionFn:
        return self._on_send_audio_record_callback

    @on_send_audio_record_callback.setter
    def on_send_audio_record_callback(self, callback: AudioRecordActionFn) -> None:
        self._on_send_audio_record_callback = callback

    @property
    def on_delete_audio_record_callback(self) -> AudioRecordActionFn:
        return self._on_delete_audio_record_callback

    @on_delete_audio_record_callback.setter
    def on_delete_audio_record_callback(self, callback: AudioRecordActionFn) -> None:
        self._on_delete_audio_record_callback = callback

    @property
    def on_save_audio_record_callback(self) -> Callable:
        return self._on_save_audio_record_callback

    @on_save_audio_record_callback.setter
    def on_save_audio_record_callback(self, callback: Callable) -> None:
        self._on_save_audio_record_callback = callback

    @property
    def on_update_audio_record_name_callback(self) -> AudioRecordActionFn:
        return self._on_update_audio_record_name_callback

    @on_update_audio_record_name_callback.setter
    def on_update_audio_record_name_callback(
        self, callback: AudioRecordActionFn
    ) -> None:
        self._on_update_audio_record_name_callback = callback

    @property
    def on_fetch_audio_records_callback(self) -> Callable:
        return self._on_fetch_audio_records_callback

    @on_fetch_audio_records_callback.setter
    def on_fetch_audio_records_callback(self, callback: Callable) -> None:
        self._on_fetch_audio_records_callback = callback
        self.update_audio_records_list()

    def record_control_button_command_wrapper(self, callback: Callable) -> None:
        callback()
        self.toggle_recording_button()

    def audio_choice_command_wrapper(self, callback: Callable) -> None:
        if self.selected_audio_record is None:
            return
        callback(record=self.selected_audio_record)
        self.update_audio_choice_controllers_visibility(display=False)
        self.toggle_record_name_edit_input_box(disabled=True)
        self.update_audio_records_list()

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
            # clear selected audio record side effects
            self.update_audio_choice_controllers_visibility(display=False)
            self.toggle_record_name_edit_input_box(disabled=True)
            # create new audio record
            self.on_save_audio_record_callback()
            # update audio records list
            self.update_audio_records_list()

    def update_audio_choice_controllers_visibility(self, display: bool = True):
        if display:
            button_offset = 35
            button_y_location = self.section_y + 30 + 90
            # make visible self.send_button
            self.send_button.place(
                width=70,
                height=30,
                x=self.section_x_center - button_offset * 3,
                y=button_y_location,
                anchor=tk.CENTER,
            )
            # make visible self.play_button
            self.play_button.place(
                width=70,
                height=30,
                x=self.section_x_center - button_offset * 1,
                y=button_y_location,
                anchor=tk.CENTER,
            )
            # make visible self.update_name_button
            self.update_name_button.place(
                width=70,
                height=30,
                x=self.section_x_center + button_offset * 1,
                y=button_y_location,
                anchor=tk.CENTER,
            )
            # make visible self.delete_button
            self.delete_button.place(
                width=70,
                height=30,
                x=self.section_x_center + button_offset * 3,
                y=button_y_location,
                anchor=tk.CENTER,
            )
        else:
            # make invisible self.delete_button
            self.delete_button.place_forget()
            # make invisible self.send_button
            self.send_button.place_forget()
            # make invisible self.update_name_button
            self.update_name_button.place_forget()
            # make invisible self.play_button
            self.play_button.place_forget()
