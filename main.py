"""
Main script to collect and store Kingston Transit data
"""

from data_collectors.transit_collector import TransitCollector
from database.models import DatabaseManager
import time
from datetime import datetime


def collect_once():
    """Collect data one time"""
    print(f"\n{'='*80}")
    print(f"Starting data collection at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*80}\n")
    
    # Initialize
    collector = TransitCollector()
    db = DatabaseManager()
    db.create_tables()
    
    # Collect and save
    vehicles = collector.fetch_vehicle_positions()
    collector.print_vehicle_summary(vehicles)
    
    if vehicles:
        db.save_vehicle_positions(vehicles)
    else:
        print("No vehicles to save")


def collect_continuously(interval_seconds: int = 30):
    """Collect data continuously at specified interval"""
    print(f"Starting continuous collection (every {interval_seconds} seconds)")
    print("Press Ctrl+C to stop\n")
    
    collector = TransitCollector()
    db = DatabaseManager()
    db.create_tables()
    
    try:
        while True:
            print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Collecting data...")
            
            vehicles = collector.fetch_vehicle_positions()
            if vehicles:
                db.save_vehicle_positions(vehicles)
                print(f"✓ Saved {len(vehicles)} bus positions")
            else:
                print("✗ No data collected")
            
            print(f"Waiting {interval_seconds} seconds until next collection...")
            time.sleep(interval_seconds)
            
    except KeyboardInterrupt:
        print("\n\nStopping data collection. Goodbye!")


def show_statistics():
    """Show statistics from collected data"""
    from database.models import VehiclePosition
    from sqlalchemy import func
    
    db = DatabaseManager()
    session = db.Session()
    
    try:
        # Total records
        total = session.query(func.count(VehiclePosition.id)).scalar()
        
        # Unique buses
        unique_buses = session.query(func.count(func.distinct(VehiclePosition.bus_id))).scalar()
        
        # Unique routes
        unique_routes = session.query(func.count(func.distinct(VehiclePosition.route_id))).scalar()
        
        # Date range
        first = session.query(func.min(VehiclePosition.timestamp)).scalar()
        last = session.query(func.max(VehiclePosition.timestamp)).scalar()
        
        print(f"\n{'='*80}")
        print("Database Statistics")
        print(f"{'='*80}")
        print(f"Total position records: {total:,}")
        print(f"Unique buses tracked: {unique_buses}")
        print(f"Unique routes: {unique_routes}")
        if first and last:
            print(f"Data range: {first} to {last}")
            duration = last - first
            print(f"Duration: {duration}")
        print(f"{'='*80}\n")
        
    finally:
        session.close()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "once":
            collect_once()
        elif command == "continuous":
            interval = int(sys.argv[2]) if len(sys.argv) > 2 else 30
            collect_continuously(interval)
        elif command == "stats":
            show_statistics()
        else:
            print("Unknown command. Use: once, continuous, or stats")
    else:
        # Default: collect once
        collect_once()