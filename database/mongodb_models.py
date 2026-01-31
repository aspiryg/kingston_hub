"""
MongoDB models for Kingston Transit data
"""

from pymongo import MongoClient, ASCENDING
from datetime import datetime
from typing import List, Dict
import config


class MongoDBManager:
    """Manages MongoDB connections and operations"""
    
    def __init__(self, connection_string: str = None):
        self.connection_string = connection_string or config.MONGODB_URL
        self.client = MongoClient(self.connection_string)
        self.db = self.client[config.MONGODB_DATABASE]
        self.vehicle_positions = self.db['vehicle_positions']
        
    def create_indexes(self):
        """Create indexes for faster queries"""
        self.vehicle_positions.create_index([('bus_id', ASCENDING), ('timestamp', ASCENDING)])
        self.vehicle_positions.create_index([('route_id', ASCENDING), ('timestamp', ASCENDING)])
        self.vehicle_positions.create_index([('timestamp', ASCENDING)])
        print("MongoDB indexes created successfully")
        
    def save_vehicle_positions(self, vehicles: list):
        """Save vehicle position data to MongoDB"""
        try:
            # Filter out vehicles with missing essential data
            valid_vehicles = [
                v for v in vehicles 
                if v.get('bus_id') and v.get('latitude') is not None and v.get('longitude') is not None and v.get('timestamp')
            ]
            
            if len(valid_vehicles) < len(vehicles):
                skipped = len(vehicles) - len(valid_vehicles)
                print(f"Skipping {skipped} vehicles without position data")
            
            if valid_vehicles:
                self.vehicle_positions.insert_many(valid_vehicles)
                print(f"Saved {len(valid_vehicles)} vehicle positions to MongoDB")
                return True
            return False
            
        except Exception as e:
            print(f"Error saving to MongoDB: {e}")
            return False
    
    def get_latest_positions(self, limit: int = 100):
        """Get the most recent vehicle positions"""
        try:
            positions = list(self.vehicle_positions.find().sort('timestamp', -1).limit(limit))
            return positions
        except Exception as e:
            print(f"Error fetching latest positions: {e}")
            return []
    
    def get_route_history(self, route_id: str, hours: int = 24):
        """Get historical data for a specific route"""
        from datetime import timedelta
        try:
            cutoff_time = datetime.now() - timedelta(hours=hours)
            positions = list(self.vehicle_positions.find({
                'route_id': route_id,
                'timestamp': {'$gte': cutoff_time}
            }).sort('timestamp', -1))
            return positions
        except Exception as e:
            print(f"Error fetching route history: {e}")
            return []
    
    def get_statistics(self):
        """Get database statistics"""
        try:
            total = self.vehicle_positions.count_documents({})
            unique_buses = len(self.vehicle_positions.distinct('bus_id'))
            unique_routes = len(self.vehicle_positions.distinct('route_id'))
            
            # Get date range
            first_doc = self.vehicle_positions.find_one(sort=[('timestamp', ASCENDING)])
            last_doc = self.vehicle_positions.find_one(sort=[('timestamp', -1)])
            
            return {
                'total': total,
                'unique_buses': unique_buses,
                'unique_routes': unique_routes,
                'first_timestamp': first_doc['timestamp'] if first_doc else None,
                'last_timestamp': last_doc['timestamp'] if last_doc else None
            }
        except Exception as e:
            print(f"Error getting statistics: {e}")
            return None
    
    def close(self):
        """Close MongoDB connection"""
        self.client.close()