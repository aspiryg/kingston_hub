"""
Kingston Transit Real-Time Data Collector

This module fetches real-time bus location data from Kingston Transit's
GTFS-Realtime API and parses it into a usable format.
"""

from google.transit import gtfs_realtime_pb2
import requests
from datetime import datetime
from typing import List, Dict
import config


class TransitCollector:
    """Collects and parses Kingston Transit real-time data"""
    
    def __init__(self):
        self.vehicle_url = config.KINGSTON_TRANSIT_VEHICLE_POSITIONS
        
    def fetch_vehicle_positions(self) -> List[Dict]:
        """
        Fetches current positions of all active buses in Kingston.
        
        Returns:
            List of dictionaries containing bus information:
            - bus_id: Unique identifier for the bus
            - route_id: Route number (e.g., "1", "2", "12")
            - latitude: Current latitude
            - longitude: Current longitude
            - bearing: Direction bus is facing (degrees)
            - speed: Current speed (m/s)
            - timestamp: When this data was recorded
            - current_stop_sequence: Which stop along the route
            - current_status: STOPPED_AT, IN_TRANSIT_TO, etc.
        """
        try:
            # Create a FeedMessage object to parse the protobuf data
            feed = gtfs_realtime_pb2.FeedMessage()
            
            # Fetch the data from Kingston Transit API
            print(f"Fetching data from: {self.vehicle_url}")
            response = requests.get(self.vehicle_url, timeout=10)
            response.raise_for_status()
            
            # Parse the binary protobuf data
            feed.ParseFromString(response.content)
            
            # Extract vehicle data
            vehicles = []
            for entity in feed.entity:
                if entity.HasField('vehicle'):
                    vehicle = entity.vehicle
                    
                    vehicle_data = {
                        'bus_id': entity.id,
                        'route_id': vehicle.trip.route_id if vehicle.HasField('trip') else None,
                        'trip_id': vehicle.trip.trip_id if vehicle.HasField('trip') else None,
                        'latitude': vehicle.position.latitude if vehicle.HasField('position') else None,
                        'longitude': vehicle.position.longitude if vehicle.HasField('position') else None,
                        'bearing': vehicle.position.bearing if vehicle.HasField('position') else None,
                        'speed': vehicle.position.speed if vehicle.HasField('position') else None,
                        'timestamp': datetime.fromtimestamp(vehicle.timestamp) if vehicle.HasField('timestamp') else datetime.now(),
                        'current_stop_sequence': vehicle.current_stop_sequence if vehicle.HasField('current_stop_sequence') else None,
                        'stop_id': vehicle.stop_id if vehicle.HasField('stop_id') else None,
                        'current_status': self._get_status_name(vehicle.current_status) if vehicle.HasField('current_status') else 'UNKNOWN',
                        'collected_at': datetime.now()
                    }
                    
                    vehicles.append(vehicle_data)
            
            print(f"Successfully collected data for {len(vehicles)} buses")
            return vehicles
            
        except requests.RequestException as e:
            print(f"Error fetching data: {e}")
            return []
        except Exception as e:
            print(f"Error parsing data: {e}")
            return []
    
    
    def explore_feed_structure(self):
        """Print out the complete structure of a vehicle entity"""
        try:
            feed = gtfs_realtime_pb2.FeedMessage()
            response = requests.get(self.vehicle_url, timeout=10)
            response.raise_for_status()
            feed.ParseFromString(response.content)
            
            if feed.entity:
                # Get first vehicle
                entity = feed.entity[0]
                print("\n=== COMPLETE VEHICLE ENTITY STRUCTURE ===\n")
                print(entity)  # This prints ALL fields with their values
            else:
                print("No entities found in the feed.")
                
        except Exception as e:
            print(f"Error: {e}")
    
    def _get_status_name(self, status_code: int) -> str:
        """Convert numeric status code to readable name"""
        status_map = {
            0: 'INCOMING_AT',
            1: 'STOPPED_AT',
            2: 'IN_TRANSIT_TO'
        }
        return status_map.get(status_code, 'UNKNOWN')
    
    def print_vehicle_summary(self, vehicles: List[Dict]):
        """Print a summary of vehicle positions"""
        if not vehicles:
            print("No vehicles currently active")
            return
        
        print(f"\n{'='*80}")
        print(f"Kingston Transit Live Summary - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*80}")
        print(f"Total Active Buses: {len(vehicles)}\n")
        
        # Group by route
        routes = {}
        for v in vehicles:
            route = v['route_id'] or 'Unknown'
            if route not in routes:
                routes[route] = []
            routes[route].append(v)
        
        for route_id in sorted(routes.keys()):
            buses = routes[route_id]
            print(f"Route {route_id}: {len(buses)} bus(es)")
            for bus in buses:
                print(f"  • Bus {bus['bus_id'][:8]}... at ({bus['latitude']:.6f}, {bus['longitude']:.6f})")
                print(f"    Status: {bus['current_status']}, Speed: {bus['speed']:.1f} m/s" if bus['speed'] else f"    Status: {bus['current_status']}")
        
        print(f"{'='*80}\n")


# Quick test function
def test_collector():
    """Test the transit collector"""
    collector = TransitCollector()
    vehicles = collector.fetch_vehicle_positions()
    collector.explore_feed_structure()
    collector.print_vehicle_summary(vehicles)
    return vehicles


if __name__ == "__main__":
    test_collector()