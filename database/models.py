"""
Database models for Kingston Transit data
"""

from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import config

Base = declarative_base()


class VehiclePosition(Base):
    """Stores historical vehicle position data"""
    __tablename__ = 'vehicle_positions'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    bus_id = Column(String(50), nullable=False)
    route_id = Column(String(20))
    trip_id = Column(String(100))
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    bearing = Column(Float)
    speed = Column(Float)
    timestamp = Column(DateTime, nullable=False)
    current_stop_sequence = Column(Integer)
    stop_id = Column(String(50))
    current_status = Column(String(20))
    collected_at = Column(DateTime, default=datetime.now)
    
    # Indexes for faster queries
    __table_args__ = (
        Index('idx_bus_timestamp', 'bus_id', 'timestamp'),
        Index('idx_route_timestamp', 'route_id', 'timestamp'),
    )


class DatabaseManager:
    """Manages database connections and operations"""
    
    def __init__(self, database_url: str = None):
        self.database_url = database_url or config.DATABASE_URL
        self.engine = create_engine(self.database_url, echo=False)
        self.Session = sessionmaker(bind=self.engine)
        
    def create_tables(self):
        """Create all tables in the database"""
        Base.metadata.create_all(self.engine)
        print("Database tables created successfully")
        
    def save_vehicle_positions(self, vehicles: list):
        """Save vehicle position data to database"""
        session = self.Session()
        try:
            # Filter out vehicles with missing essential data
            valid_vehicles = [
                v for v in vehicles 
                if v.get('bus_id') and v.get('latitude') is not None and v.get('longitude') is not None and v.get('timestamp')
            ]
            
            if len(valid_vehicles) < len(vehicles):
                skipped = len(vehicles) - len(valid_vehicles)
                print(f"Skipping {skipped} vehicles without position data")
            
            for vehicle_data in valid_vehicles:
                position = VehiclePosition(**vehicle_data)
                session.add(position)
            
            session.commit()
            print(f"Saved {len(valid_vehicles)} vehicle positions to database")
            return True
            
        except Exception as e:
            session.rollback()
            print(f"Error saving to database: {e}")
            return False
        finally:
            session.close()
    
    def get_latest_positions(self, limit: int = 100):
        """Get the most recent vehicle positions"""
        session = self.Session()
        try:
            positions = session.query(VehiclePosition)\
                              .order_by(VehiclePosition.timestamp.desc())\
                              .limit(limit)\
                              .all()
            return positions
        finally:
            session.close()
    
    def get_route_history(self, route_id: str, hours: int = 24):
        """Get historical data for a specific route"""
        from datetime import timedelta
        session = self.Session()
        try:
            cutoff_time = datetime.now() - timedelta(hours=hours)
            positions = session.query(VehiclePosition)\
                              .filter(VehiclePosition.route_id == route_id)\
                              .filter(VehiclePosition.timestamp >= cutoff_time)\
                              .order_by(VehiclePosition.timestamp.desc())\
                              .all()
            return positions
        finally:
            session.close()


if __name__ == "__main__":
    # Test database creation
    db = DatabaseManager()
    db.create_tables()