"""
Purpose: Contains predefined road network data with locations and traffic-weighted edges.
This module provides the graph structure and location list for the traffic predictor.
"""

from typing import Dict, List, Tuple, Optional


def get_road_network() -> Dict[str, Dict[str, int]]:
    """
    Returns a predefined road network as a weighted adjacency list graph.
    
    Structure:
    {
        'Location': {
            'Neighbor': weight (traffic congestion score)
        }
    }
    
    Weight interpretation:
    - Lower weight = Less traffic, faster route
    - Higher weight = More traffic, slower route
    - Weight represents approximate travel time in minutes
    """
    
    # Define the road network for Narwana, Haryana
    # Narwana is a town in Jind district (29.5960° N, 76.1150° E)
    # Travel times are estimated based on typical small town geography
    # NOTE: For accurate distances, run: python fetch_distances.py with Google Maps API key
    # Or measure manually using Google Maps and update these values
    
    road_network = {
        'Railway Station': {
            'Bus Stand': 4,
            'Patram Nagar': 3,
            'K M College': 5,
            'Arya Up Nagar': 6
        },
        'Patram Nagar': {
            'Railway Station': 3,
            'Kishan Chand Colony': 3,
            'Bus Stand': 4,
            'Birbal Nagar': 4
        },
        'Kishan Chand Colony': {
            'Patram Nagar': 3,
            'Mittal Eye Hospital': 3,
            'Model Town': 4,
            'Nehru Park': 5
        },
        'Mittal Eye Hospital': {
            'Kishan Chand Colony': 3,
            'Nehru Park': 2,
            'Bus Stand': 5,
            'S D Kanya Mahavidhlya': 4
        },
        'Nehru Park': {
            'Mittal Eye Hospital': 2,
            'Kishan Chand Colony': 5,
            'Model Town': 3,
            'Arya Senior Secondary School': 4,
            'Bus Stand': 4
        },
        'Model Town': {
            'Nehru Park': 3,
            'Kishan Chand Colony': 4,
            'Birbal Nagar': 4,
            'Arya Up Nagar': 5
        },
        'Birbal Nagar': {
            'Model Town': 4,
            'Patram Nagar': 4,
            'Arya Up Nagar': 3,
            'S.D. Model School': 5
        },
        'Bus Stand': {
            'Railway Station': 4,
            'Patram Nagar': 4,
            'Nehru Park': 4,
            'Mittal Eye Hospital': 5,
            'Arya Senior Secondary School': 6,
            'K M College': 6
        },
        'Arya Up Nagar': {
            'Railway Station': 6,
            'Model Town': 5,
            'Birbal Nagar': 3,
            'S.D. Model School': 4,
            'K M College': 5
        },
        'Arya Senior Secondary School': {
            'Nehru Park': 4,
            'Bus Stand': 6,
            'S.D. Model School': 3,
            'S D Kanya Mahavidhlya': 5
        },
        'S.D. Model School': {
            'Arya Senior Secondary School': 3,
            'Birbal Nagar': 5,
            'Arya Up Nagar': 4,
            'K M College': 4,
            'S D Kanya Mahavidhlya': 6
        },
        'K M College': {
            'Railway Station': 5,
            'Bus Stand': 6,
            'Arya Up Nagar': 5,
            'S.D. Model School': 4,
            'S D Kanya Mahavidhlya': 3
        },
        'S D Kanya Mahavidhlya': {
            'K M College': 3,
            'S.D. Model School': 6,
            'Arya Senior Secondary School': 5,
            'Mittal Eye Hospital': 4
        }
    }
    
    return road_network


def get_locations() -> List[str]:
    """
    Returns a sorted list of all available locations in the network.
    Used for populating dropdown menus in the UI.
    """
    road_network = get_road_network()
    locations = sorted(list(road_network.keys()))
    return locations


def get_edge_list(road_network: Optional[Dict[str, Dict[str, int]]] = None) -> List[Tuple[str, str, int]]:
    """
    Returns all edges in the graph as a list of tuples.
    Format: [(source, destination, weight), ...]
    Useful for visualization purposes.
    
    Args:
        road_network: Optional road network dict. If None, uses default network.
    """
    if road_network is None:
        road_network = get_road_network()
    
    edges = []
    
    # Avoid duplicates by tracking processed edges
    processed = set()
    
    for source, neighbors in road_network.items():
        for destination, weight in neighbors.items():
            # Create a normalized edge identifier (bidirectional)
            edge_id = tuple(sorted([source, destination]))
            if edge_id not in processed:
                edges.append((source, destination, weight))
                processed.add(edge_id)
    
    return edges


def update_traffic_weight(road_network: Dict[str, Dict[str, int]], source: str, destination: str, new_weight: int) -> Dict[str, Dict[str, int]]:
    """
    Updates the traffic weight for a specific edge in the network.
    Useful for simulating real-time traffic changes.
    
    Args:
        road_network: The current road network dictionary
        source: Starting location
        destination: Ending location
        new_weight: New traffic weight value
    
    Returns:
        Updated road network
    """
    if source in road_network and destination in road_network[source]:
        road_network[source][destination] = new_weight
    
    # Update reverse direction if it exists (bidirectional road)
    if destination in road_network and source in road_network[destination]:
        road_network[destination][source] = new_weight
    
    return road_network