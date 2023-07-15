import osmnx as ox
import networkx as nx
from enum import Enum


class TravelMode(str, Enum):
    WALKING = "walk"
    DRIVING = "drive"


def get_graph_from_point(
    center_point: tuple[float, float], dist: int, travel_mode: TravelMode
) -> nx.Graph:
    return ox.graph_from_point(
        center_point=center_point, dist=dist, network_type=travel_mode.value,
    )


def calculate_shortest_path(
    graph: nx.Graph, start: tuple[float, float], end: tuple[float, float]
) -> list[tuple[float, float]]:

    # get closes graph nodes to origin and destination
    orig_node = ox.distance.nearest_nodes(graph, start[1], start[0])
    destination_node = ox.distance.nearest_nodes(graph, end[1], end[0])

    # find shortest path based on travel time
    route = nx.shortest_path(graph, orig_node, destination_node, weight="travel_time")

    coordinates = []
    for node in route:
        coordinates.append((graph.nodes[node]["y"], graph.nodes[node]["x"]))

    return [start] + coordinates + [end]
