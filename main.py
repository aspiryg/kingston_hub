"""
Main script to collect and store Kingston Transit data
"""

from data_collectors.transit_collector import TransitCollector
from database.mongodb_models import MongoDBManager
import time
from datetime import datetime


def collect_once():
    """Collect data one time"""
    print(f"\n{'='*80}")
    print(f"Starting data collection at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*80}\n")
    
    # Initialize
    collector = TransitCollector()
    db = MongoDBManager()
    db.create_indexes()
    
    # Collect and save
    vehicles = collector.fetch_vehicle_positions()
    collector.print_vehicle_summary(vehicles)
    
    if vehicles:
        db.save_vehicle_positions(vehicles)
    else:
        print("No vehicles to save")
    
    db.close()


def collect_continuously(interval_seconds: int = 30):
    """Collect data continuously at specified interval"""
    print(f"Starting continuous collection (every {interval_seconds} seconds)")
    print("Press Ctrl+C to stop\n")
    
    collector = TransitCollector()
    db = MongoDBManager()
    db.create_indexes()
    
    try:
        while True:
            print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Collecting data...")
            
            vehicles = collector.fetch_vehicle_positions()
            if vehicles:
                db.save_vehicle_positions(vehicles)
            else:
                print("✗ No data collected")
            
            print(f"Waiting {interval_seconds} seconds until next collection...")
            time.sleep(interval_seconds)
            
    except KeyboardInterrupt:
        print("\n\nStopping data collection. Goodbye!")
    finally:
        db.close()


def show_statistics():
    """Show statistics from collected data"""
    db = MongoDBManager()
    
    try:
        stats = db.get_statistics()
        
        if stats:
            print(f"\n{'='*80}")
            print("Database Statistics")
            print(f"{'='*80}")
            print(f"Total position records: {stats['total']:,}")
            print(f"Unique buses tracked: {stats['unique_buses']}")
            print(f"Unique routes: {stats['unique_routes']}")
            if stats['first_timestamp'] and stats['last_timestamp']:
                print(f"Data range: {stats['first_timestamp']} to {stats['last_timestamp']}")
                duration = stats['last_timestamp'] - stats['first_timestamp']
                print(f"Duration: {duration}")
            print(f"{'='*80}\n")
        else:
            print("Could not retrieve statistics")
            
    finally:
        db.close()


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