import tkinter as tk
import PIL
import os
import tkintermapview
from typing import Callable
from distance_calculator import calc_distance_km
from route_calculator import get_graph_from_point, calculate_shortest_path, TravelMode

MAX_DISTANCE_TO_pet_TO_SHOW_PATH_KM = 1.0


class ApplicationGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Application")
        self.window.configure(bg="#222")
        self.window_width = 900
        self.window_height = 600
        self.window.geometry(f"{self.window_width}x{self.window_height}")

        self.prepare_gps_marker_images()

        self.prepare_map_view_loading_indicator()
        self.prepare_map_update_message_label()
        self.prepare_map_long_distance_message_label()
        self.prepare_map_view()
        self.prepare_map_view_controllers()
        self.prepare_distance_to_pet_label()
        self.prepare_recording_control_buttons()

        self.user_gps_coordinates = None
        self.user_marker = None
        self.pet_gps_coordinates = None
        self.pet_marker = None

        self.travel_mode = TravelMode.WALKING
        self.user_coordinate_during_latest_map_graph_generation = None
        self.latest_map_graph = None
        self.latest_path = None

    def prepare_gps_marker_images(self):
        self.pet_marker_image = PIL.ImageTk.PhotoImage(
            PIL.Image.open(
                os.path.join(
                    os.path.dirname(os.path.abspath(__file__)), "assets", "dog-area.png"
                )
            ).resize((50, 50))
        )
        self.user_marker_image = PIL.ImageTk.PhotoImage(
            PIL.Image.open(
                os.path.join(
                    os.path.dirname(os.path.abspath(__file__)), "assets", "person.png"
                )
            ).resize((50, 50))
        )

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

        self.display_map_widget(display=False)

    def prepare_map_view_controllers(self):
        center_x = self.window_width / 2
        center_y = self.window_height / 2
        center_to_pet_button_x = center_x + 300
        center_to_pet_button_y = center_y - 50
        center_to_user_button_x = center_x + 308
        center_to_user_button_y = center_y

        self.center_to_pet_button = tk.Button(
            self.window,
            text="Center to pet",
            font=("Arial", 14, "bold"),
            bg="#4CAF50",
            fg="black",
            relief="raised",
            padx=20,
            pady=10,
            activebackground="#45A049",
            activeforeground="black",
            command=self.center_to_pet_gps_coordinates,
        )
        self.center_to_pet_button.place(
            x=center_to_pet_button_x, y=center_to_pet_button_y, anchor="center"
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

    def prepare_map_view_loading_indicator(self):
        self.map_loading_indicator_text_display = tk.StringVar()
        self.map_loading_indicator_text_display.set("Loading map...")
        self.map_loading_indicator = tk.Label(
            self.window,
            textvariable=self.map_loading_indicator_text_display,
            font=("Arial", 18, "bold"),
            fg="white",
            bg="#222",
        )

        label_x = self.window_width / 2
        label_y = self.window_height / 2 - 200

        self.map_loading_indicator.place(x=label_x, y=label_y, anchor="center")

    def update_map_update_message_label(self, message: str):
        self.map_update_message_text_display.set(message)

    def prepare_map_update_message_label(self):
        self.map_update_message_text_display = tk.StringVar()
        self.map_update_message_text_display.set("")

        label_x = self.window_width / 2
        label_y = self.window_height / 2 + 205

        self.map_update_message_label = tk.Label(
            self.window,
            textvariable=self.map_update_message_text_display,
            font=("Arial", 18, "bold"),
            fg="white",
            bg="#222",
        )
        self.map_update_message_label.place(x=label_x, y=label_y, anchor="center")

    def update_map_long_distance_message_text(self, message: str) -> None:
        self.map_long_distance_message_text_display.set(message)

    def prepare_map_long_distance_message_label(self):
        self.map_long_distance_message_text_display = tk.StringVar()
        self.map_long_distance_message_text_display.set("")

        label_x = self.window_width / 2
        label_y = self.window_height / 2 + 175

        self.map_long_distance_message_label = tk.Label(
            self.window,
            textvariable=self.map_long_distance_message_text_display,
            font=("Arial", 18, "bold"),
            fg="yellow",
            bg="#222",
        )
        self.map_long_distance_message_label.place(
            x=label_x, y=label_y, anchor="center"
        )

    def prepare_distance_to_pet_label(self):
        self.distance_to_pet_text_display = tk.StringVar()
        self.distance_to_pet_text_display.set("Waiting for data...")

        center_x = self.window_width / 2
        center_y = self.window_height / 2

        label_x = center_x
        label_y = center_y - 200

        self.displayed_text_distance_label = tk.Label(
            self.window,
            textvariable=self.distance_to_pet_text_display,
            font=("Arial", 18, "bold"),
            fg="white",
            bg="#222",
        )
        self.displayed_text_distance_label.place(x=label_x, y=label_y, anchor="center")

    def prepare_recording_control_buttons(self):
        self.button_coordinates = (self.window_width / 2, self.window_height / 2 + 250)

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

    def display_map_widget(self, display: bool) -> None:
        if display:
            self.map_widget_label.place(
                x=self.window_width / 2, y=self.window_height / 2, anchor="center"
            )
            self.map_loading_indicator.place_forget()
        else:
            self.map_widget_label.place_forget()
            self.map_loading_indicator.place(
                x=self.window_width / 2, y=self.window_height / 2, anchor="center"
            )

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

    def update_pet_gps_coordinates(self, coordinates: tuple[float, float]) -> None:
        self.pet_gps_coordinates = coordinates
        self.render_pet_gps_marker()
        self.update_distance_to_pet_text_display()
        self.sync_path_from_user_to_pet()

    def update_distance_to_pet_text_display(self) -> None:
        if self.pet_gps_coordinates is None:
            print("No pet GPS coordinates")
            return
        if self.user_gps_coordinates is None:
            print("No user GPS coordinates")
            return
        distance_in_km = calc_distance_km(
            self.user_gps_coordinates, self.pet_gps_coordinates
        )
        text = f"Aerial Distance to pet: {distance_in_km:.2f} km"
        self.distance_to_pet_text_display.set(text)

    def set_user_gps_coordinates(self, coordinates: tuple[float, float]) -> None:
        first_coordinates_signal = self.user_gps_coordinates is None
        self.user_gps_coordinates = coordinates
        self.update_map_graph()
        if first_coordinates_signal:
            self.display_map_widget(display=True)
            self.center_to_user_gps_coordinates()
        self.render_user_gps_marker()
        self.center_to_user_gps_coordinates()
        self.update_distance_to_pet_text_display()
        self.sync_path_from_user_to_pet()

    def render_pet_gps_marker(self):
        if self.pet_gps_coordinates is None:
            print("No pet GPS coordinates")
            return
        new_pet_marker = self.map_widget.set_marker(
            self.pet_gps_coordinates[0],
            self.pet_gps_coordinates[1],
            text="Pet",
            icon=self.pet_marker_image,
            icon_anchor="s",
        )
        if self.pet_marker is not None:
            self.pet_marker.delete()
        self.pet_marker = new_pet_marker

    def render_user_gps_marker(self):
        if self.user_gps_coordinates is None:
            print("No user GPS coordinates")
            return
        new_user_marker = self.map_widget.set_marker(
            self.user_gps_coordinates[0],
            self.user_gps_coordinates[1],
            text="You",
            icon=self.user_marker_image,
            icon_anchor="s",
        )
        if self.user_marker is not None:
            self.user_marker.delete()
        self.user_marker = new_user_marker

    def center_to_pet_gps_coordinates(self) -> None:
        if self.pet_gps_coordinates is None:
            print("No pet GPS coordinates")
            return
        self.map_widget.set_position(
            self.pet_gps_coordinates[0], self.pet_gps_coordinates[1]
        )

    def center_to_user_gps_coordinates(self) -> None:
        if self.user_gps_coordinates is None:
            print("No user GPS coordinates")
            return
        self.map_widget.set_position(
            self.user_gps_coordinates[0], self.user_gps_coordinates[1]
        )

    def update_map_graph(self) -> None:
        if self.user_gps_coordinates is None:
            print("No user GPS coordinates")
            return
        # calculate if we need to update the map graph
        if self.latest_map_graph is not None:
            if (
                self.user_coordinate_during_latest_map_graph_generation is not None
                and calc_distance_km(
                    self.user_gps_coordinates,
                    self.user_coordinate_during_latest_map_graph_generation,
                )
                < 0.5
            ):
                return
        # update the map graph
        self.update_map_update_message_label("Updating map graph...")
        self.latest_map_graph = get_graph_from_point(
            center_point=self.user_gps_coordinates,
            dist=int(MAX_DISTANCE_TO_pet_TO_SHOW_PATH_KM * 1000),
            travel_mode=self.travel_mode,
        )
        self.user_coordinate_during_latest_map_graph_generation = (
            self.user_gps_coordinates
        )
        self.sync_path_from_user_to_pet()
        self.update_map_update_message_label("")

    def sync_path_from_user_to_pet(self) -> None:
        if self.user_gps_coordinates is None:
            print("No user GPS coordinates")
            return
        if self.pet_gps_coordinates is None:
            print("No pet GPS coordinates")
            return

        if (
            calc_distance_km(self.user_gps_coordinates, self.pet_gps_coordinates)
            > MAX_DISTANCE_TO_pet_TO_SHOW_PATH_KM
        ):
            self.update_map_long_distance_message_text(
                f"Pet distance limits path visibility; {MAX_DISTANCE_TO_pet_TO_SHOW_PATH_KM} km is accurate, rest shown as straight line for location."
            )
        else:
            self.update_map_long_distance_message_text("")

        if self.latest_map_graph is None:
            print("No latest map graph")
            return
        new_latest_path = self.map_widget.set_path(
            calculate_shortest_path(
                self.latest_map_graph,
                self.user_gps_coordinates,
                self.pet_gps_coordinates,
            )
        )
        if self.latest_path is not None:
            self.latest_path.delete()
        self.latest_path = new_latest_path

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    import threading
    import time

    gui = ApplicationGUI()

    def simulate_updates():
        gui.set_user_gps_coordinates((32.01487634797979, 34.77458326803195))
        time.sleep(1)
        gui.update_pet_gps_coordinates((32.01278924606207, 34.77908810682126))
        time.sleep(1)
        # change pet location just by a little
        gui.update_pet_gps_coordinates((32.01378924606217, 34.77908810682132))
        time.sleep(1)
        gui.update_pet_gps_coordinates((32.0047067, 34.7899158))
        time.sleep(1)
        gui.set_user_gps_coordinates((32.0069655, 34.7847542))

    threading.Thread(target=simulate_updates).start()

    gui.run()
