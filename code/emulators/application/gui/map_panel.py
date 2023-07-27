import tkinter as tk
import PIL
import os
import tkintermapview
from typing import Callable, Protocol
from distance_calculator import calc_distance_km
from route_calculator import get_graph_from_point, calculate_shortest_path, TravelMode

MAX_DISTANCE_TO_pet_TO_SHOW_PATH_KM = 1.0


class EmbedButtonFn(Protocol):
    def __call__(self, command: Callable, text: str, x: float, y: float) -> tk.Button:
        ...


class EmbedTextFn(Protocol):
    def __call__(self, text: str, x: float, y: float) -> tk.StringVar:
        ...


def new_tk_image(path: str, size: tuple[int, int]) -> PIL.ImageTk.PhotoImage:
    image = PIL.Image.open(path)
    image = image.resize(size)
    return PIL.ImageTk.PhotoImage(image)


class MapPanelGUI:
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

        self.prepare_gps_marker_images()
        self.prepare_map_view_loading_indicator()
        self.prepare_map_update_message_label()
        self.prepare_map_long_distance_message_label()
        self.prepare_map_view()
        self.prepare_map_view_controllers()
        self.prepare_distance_to_pet_label()

        self.user_gps_coordinates = None
        self.user_marker = None
        self.pet_gps_coordinates = None
        self.pet_marker = None

        self.travel_mode = TravelMode.WALKING
        self.user_coordinate_during_latest_map_route_generation = None

        self.route_visibility = False
        self.latest_map_route = None
        self.latest_path = None

    def prepare_gps_marker_images(self):
        self.pet_marker_image = new_tk_image(
            os.path.join(
                os.path.dirname(os.path.abspath(__file__)), "assets", "dog-area.png"
            ),
            (50, 50),
        )

        self.user_marker_image = new_tk_image(
            os.path.join(
                os.path.dirname(os.path.abspath(__file__)), "assets", "person.png"
            ),
            (50, 50),
        )

    def prepare_map_view(self):
        center_x = self.window_width / 2
        center_y = self.window_height / 2
        self.map_widget_label = tk.LabelFrame(self.window, text="Map")
        self.map_widget_label.place(x=center_x, y=center_y, anchor="center")
        self.map_widget = tkintermapview.TkinterMapView(
            self.map_widget_label,
            width=400,
            height=300,
            corner_radius=0,
        )
        self.map_widget.set_zoom(15)
        self.map_widget.pack()

        self.display_map_widget(display=False)

    def prepare_map_view_controllers(self):
        center_x = self.window_width / 2
        center_y = self.window_height / 2

        center_buttons_x = center_x + 300
        y_offet = 50

        self.center_to_pet_button = self.embed_button(
            command=self.center_to_pet_gps_coordinates,
            text="Center to pet",
            x=center_buttons_x,
            y=center_y - y_offet,
        )

        self.center_to_user_button = self.embed_button(
            command=self.center_to_user_gps_coordinates,
            text="Center to user",
            x=center_buttons_x + 5,
            y=center_y,
        )

        self.route_visibility_button = self.embed_button(
            command=self.toggle_route_visibility,
            text="Route view control",
            x=center_buttons_x + 21,
            y=center_y + y_offet,
        )

    def prepare_map_view_loading_indicator(self):
        self.map_loading_indicator_text_display = self.embed_text(
            text="Loading map...",
            x=self.window_width / 2,
            y=self.window_height / 2 - 200,
        )

    def update_map_update_message_label(self, message: str):
        self.map_update_message_text_display.set(message)

    def prepare_map_update_message_label(self):
        self.map_update_message_text_display = self.embed_text(
            text="",
            x=self.window_width / 2,
            y=self.window_height / 2 + 205,
        )

    def update_map_long_distance_message_text(self, message: str) -> None:
        self.map_long_distance_message_text_display.set(message)

    def prepare_map_long_distance_message_label(self):
        self.map_long_distance_message_text_display = self.embed_text(
            text="",
            x=self.window_width / 2,
            y=self.window_height / 2 + 175,
        )

    def prepare_distance_to_pet_label(self):
        self.distance_to_pet_text_display = self.embed_text(
            text="Waiting for data...",
            x=self.window_width / 2,
            y=self.window_height / 2 - 200,
        )

    def display_map_widget(self, display: bool) -> None:
        if display:
            self.map_loading_indicator_text_display.set("")
        else:
            self.map_loading_indicator_text_display.set("Loading map...")

    def update_pet_gps_coordinates(self, coordinates: tuple[float, float]) -> None:
        self.pet_gps_coordinates = coordinates
        self.render_pet_gps_marker()
        self.update_distance_to_pet_text_display()
        self.sync_path_from_user_to_pet()

    def update_distance_to_pet_text_display(self) -> None:
        if self.pet_gps_coordinates is None:
            print("Cannot calculate distance to pet without pet GPS coordinates")
            return
        if self.user_gps_coordinates is None:
            print("Cannot calculate distance to pet without user GPS coordinates")
            return
        distance_in_km = calc_distance_km(
            self.user_gps_coordinates, self.pet_gps_coordinates
        )
        text = f"Aerial Distance to pet: {distance_in_km:.2f} km"
        self.distance_to_pet_text_display.set(text)

    def update_user_gps_coordinates(self, coordinates: tuple[float, float]) -> None:
        first_coordinates_signal = self.user_gps_coordinates is None
        self.user_gps_coordinates = coordinates
        self.update_map_route()
        if first_coordinates_signal:
            self.display_map_widget(display=True)
            self.center_to_user_gps_coordinates()
        self.render_user_gps_marker()
        self.update_distance_to_pet_text_display()
        self.sync_path_from_user_to_pet()

    def render_pet_gps_marker(self):
        if self.pet_gps_coordinates is None:
            print("Cannot render pet marker, no pet GPS coordinates")
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
            print("Cannot render user marker, no user GPS coordinates")
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
            print("Cannot center to pet, no pet GPS coordinates")
            return
        self.map_widget.set_position(
            self.pet_gps_coordinates[0], self.pet_gps_coordinates[1]
        )

    def center_to_user_gps_coordinates(self) -> None:
        if self.user_gps_coordinates is None:
            print("Cannot center to user, no user GPS coordinates")
            return
        self.map_widget.set_position(
            self.user_gps_coordinates[0], self.user_gps_coordinates[1]
        )

    def update_map_route(self) -> None:
        if self.route_visibility is False:
            return

        if self.user_gps_coordinates is None:
            print("Cannot update map route, no user GPS coordinates")
            return
        # calculate if we need to update the map graph
        if self.latest_map_route is not None and self.latest_path is not None:
            if (
                self.user_coordinate_during_latest_map_route_generation is not None
                and calc_distance_km(
                    self.user_gps_coordinates,
                    self.user_coordinate_during_latest_map_route_generation,
                )
                < MAX_DISTANCE_TO_pet_TO_SHOW_PATH_KM * 3 / 4
            ):
                return
        # update the map route
        self.update_map_update_message_label("Updating map route...")
        self.latest_map_route = get_graph_from_point(
            center_point=self.user_gps_coordinates,
            dist=int(MAX_DISTANCE_TO_pet_TO_SHOW_PATH_KM * 1000),
            travel_mode=self.travel_mode,
        )
        self.user_coordinate_during_latest_map_route_generation = (
            self.user_gps_coordinates
        )
        self.sync_path_from_user_to_pet()
        self.update_map_update_message_label("")
        self.center_to_user_gps_coordinates()

    def sync_path_from_user_to_pet(self) -> None:
        if self.route_visibility is False:
            return
        if self.user_gps_coordinates is None:
            print("Cannot sync path from user to pet: no user GPS coordinates")
            return
        if self.pet_gps_coordinates is None:
            print("Cannot sync path from user to pet: no pet GPS coordinates")
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

        if self.latest_map_route is None:
            print("Cannot sync path from user to pet: no map route")
            return
        new_latest_path = self.map_widget.set_path(
            calculate_shortest_path(
                self.latest_map_route,
                self.user_gps_coordinates,
                self.pet_gps_coordinates,
            )
        )
        if self.latest_path is not None:
            self.latest_path.delete()
        self.latest_path = new_latest_path

    def toggle_route_visibility(self) -> None:
        self.route_visibility = not self.route_visibility
        if self.latest_path is not None:
            self.latest_path.delete()
            self.latest_path = None
        if self.route_visibility:
            self.sync_path_from_user_to_pet()
