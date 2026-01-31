namespace KingstonHub.Api.Models.DTOs
{
    /// <summary>
    /// Data Transfer Object for Vehicle Position
    /// </summary>
    public class VehicleDto
    {
        public string BusId { get; set; } = string.Empty;
        public string? RouteId { get; set; }
        public string? TripId { get; set; }
        public LocationDto Location { get; set; } = new();
        public double? Speed { get; set; }
        public double? Bearing { get; set; }
        public string? CurrentStatus { get; set; }
        public string? StopId { get; set; }
        public DateTime LastUpdated { get; set; }
    }

    public class LocationDto
    {
        public double Latitude { get; set; }
        public double Longitude { get; set; }
    }

    public class RouteDto
    {
        public string RouteId { get; set; } = string.Empty;
        public int ActiveVehicles { get; set; }
        public List<VehicleDto> Vehicles { get; set; } = new();
    }

     public class VehicleHistoryDto
    {
        public string BusId { get; set; } = string.Empty;
        public List<HistoryPoint> History { get; set; } = new();
    }

    public class HistoryPoint
    {
        public DateTime Timestamp { get; set; }
        public double Latitude { get; set; }
        public double Longitude { get; set; }
        public double? Speed { get; set; }
        public string? RouteId { get; set; }
    }
}