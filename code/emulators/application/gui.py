import tkinter as tk
import tkintermapview
from typing import Callable
from distance_calculator import calc_distance_km


class ApplicationGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Application")
        self.window.configure(bg="#222")
        self.window_width = 900
        self.window_height = 500
        self.window.geometry(f"{self.window_width}x{self.window_height}")

        self.prepare_map_view()
        self.prepare_map_view_controllers()
        self.prepare_distance_to_target_label()
        self.prepare_recording_control_buttons()

        self.user_gps_coordinates = None
        self.user_marker = None
        self.target_gps_coordinates = None
        self.target_marker = None

    def prepare_map_view(self):
        center_x = self.window_width / 2
        center_y = self.window_height / 2
        self.map_widget_label = tk.LabelFrame(self.window, text="Map")
        self.map_widget_label.place(x=center_x, y=center_y, anchor="center")
        self.map_widget = tkintermapview.TkinterMapView(
            self.map_widget_label, width=400, height=300, corner_radius=0,
        )
        self.map_widget.set_zoom(15)
        self.map_widget.pack()

    def prepare_map_view_controllers(self):
        center_x = self.window_width / 2
        center_y = self.window_height / 2
        center_to_target_button_x = center_x + 300
        center_to_target_button_y = center_y - 50
        center_to_user_button_x = center_x + 308
        center_to_user_button_y = center_y

        self.center_to_target_button = tk.Button(
            self.window,
            text="Center to target",
            font=("Arial", 14, "bold"),
            bg="#4CAF50",
            fg="black",
            relief="raised",
            padx=20,
            pady=10,
            activebackground="#45A049",
            activeforeground="black",
            command=self.center_to_target_gps_coordinates,
        )
        self.center_to_target_button.place(
            x=center_to_target_button_x, y=center_to_target_button_y, anchor="center"
        )

        self.center_to_user_button = tk.Button(
            self.window,
            text="Center to user",
            font=("Arial", 14, "bold"),
            bg="#4CAF50",
            fg="black",
            relief="raised",
            padx=20,
            pady=10,
            activebackground="#45A049",
            activeforeground="black",
            command=self.center_to_user_gps_coordinates,
        )

        self.center_to_user_button.place(
            x=center_to_user_button_x, y=center_to_user_button_y, anchor="center",
        )

    def prepare_distance_to_target_label(self):
        self.distance_to_target_text_display = tk.StringVar()
        self.distance_to_target_text_display.set("Waiting for data...")

        center_x = self.window_width / 2
        center_y = self.window_height / 2

        label_x = center_x
        label_y = center_y - 200

        self.displayed_text_distance_label = tk.Label(
            self.window,
            textvariable=self.distance_to_target_text_display,
            font=("Arial", 18, "bold"),
            fg="white",
            bg="#222",
        )
        self.displayed_text_distance_label.place(x=label_x, y=label_y, anchor="center")

    def prepare_recording_control_buttons(self):
        self.button_coordinates = (450, 450)

        self.start_recording_button = tk.Button(
            self.window,
            text="Start recording",
            font=("Arial", 14, "bold"),
            bg="#4CAF50",
            fg="black",
            relief="raised",
            padx=20,
            pady=10,
            activebackground="#45A049",
            activeforeground="black",
        )
        self.on_start_recording_call = lambda: print("Recording started!")

        self.stop_recording_button = tk.Button(
            self.window,
            text="Stop recording",
            font=("Arial", 14, "bold"),
            bg="#4CAF50",
            fg="black",
            relief="raised",
            padx=20,
            pady=10,
            activebackground="#45A049",
            activeforeground="black",
        )
        self.on_stop_recording_call = lambda: print("Recording stopped!")

        self.toggle_recording_button(recording=False)

    @property
    def on_start_recording_call(self) -> Callable:
        return self.start_recording_callback

    @on_start_recording_call.setter
    def on_start_recording_call(self, callback: Callable) -> None:
        self.start_recording_callback = callback

        def callback_wrapper():
            self.toggle_recording_button(True)
            callback()

        self.start_recording_button["command"] = callback_wrapper

    @property
    def on_stop_recording_call(self) -> Callable:
        return self.stop_recording_callback

    @on_stop_recording_call.setter
    def on_stop_recording_call(self, callback: Callable) -> None:
        self.stop_recording_callback = callback

        def callback_wrapper():
            self.toggle_recording_button(False)
            callback()

        self.stop_recording_button["command"] = callback_wrapper

    def toggle_recording_button(self, recording: bool) -> None:
        if recording:
            self.start_recording_button["state"] = "disabled"
            self.stop_recording_button["state"] = "normal"
            self.start_recording_button.place_forget()
            self.stop_recording_button.place(
                x=self.button_coordinates[0],
                y=self.button_coordinates[1],
                anchor="center",
            )
        else:
            self.start_recording_button["state"] = "normal"
            self.stop_recording_button["state"] = "disabled"
            self.stop_recording_button.place_forget()
            self.start_recording_button.place(
                x=self.button_coordinates[0],
                y=self.button_coordinates[1],
                anchor="center",
            )

    def update_target_gps_coordinates(self, coordinates: tuple[float, float]) -> None:
        self.target_gps_coordinates = coordinates
        self.render_target_gps_marker()
        self.update_distance_to_target_text_display()

    def update_distance_to_target_text_display(self) -> None:
        if self.target_gps_coordinates is None:
            print("No target GPS coordinates")
            return
        if self.user_gps_coordinates is None:
            print("No user GPS coordinates")
            return
        distance_in_km = calc_distance_km(
            self.user_gps_coordinates, self.target_gps_coordinates
        )
        text = f"Distance to target: {distance_in_km:.2f} km"
        self.distance_to_target_text_display.set(text)

    def set_user_gps_coordinates(self, coordinates: tuple[float, float]) -> None:
        first_coordinates_signal = self.user_gps_coordinates is None
        self.user_gps_coordinates = coordinates
        if first_coordinates_signal:
            self.center_to_user_gps_coordinates()
        self.render_user_gps_marker()
        self.update_distance_to_target_text_display()

    def render_target_gps_marker(self):
        if self.target_gps_coordinates is None:
            print("No target GPS coordinates")
            return
        new_target_marker = self.map_widget.set_marker(
            self.target_gps_coordinates[0],
            self.target_gps_coordinates[1],
            text="Target",
        )
        if self.target_marker is not None:
            self.target_marker.delete()
        self.target_marker = new_target_marker

    def render_user_gps_marker(self):
        if self.user_gps_coordinates is None:
            print("No user GPS coordinates")
            return
        new_user_marker = self.map_widget.set_marker(
            self.user_gps_coordinates[0], self.user_gps_coordinates[1], text="You"
        )
        if self.user_marker is not None:
            self.user_marker.delete()
        self.user_marker = new_user_marker

    def center_to_target_gps_coordinates(self) -> None:
        if self.target_gps_coordinates is None:
            print("No target GPS coordinates")
            return
        self.map_widget.set_position(
            self.target_gps_coordinates[0], self.target_gps_coordinates[1]
        )

    def center_to_user_gps_coordinates(self) -> None:
        if self.user_gps_coordinates is None:
            print("No user GPS coordinates")
            return
        self.map_widget.set_position(
            self.user_gps_coordinates[0], self.user_gps_coordinates[1]
        )

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    import threading
    import time

    gui = ApplicationGUI()

    def simulate_updates():
        time.sleep(0.1)
        gui.set_user_gps_coordinates((32.01487634797979, 34.77458326803195))
        time.sleep(1)
        gui.update_target_gps_coordinates((32.01278924606207, 34.77908810682126))
        time.sleep(1)
        # change target location just by a little
        gui.update_target_gps_coordinates((32.01378924606217, 34.77908810682132))
        time.sleep(1)
        gui.update_target_gps_coordinates((32.01478924606237, 34.77908810682136))

    threading.Thread(target=simulate_updates).start()

    gui.run()
