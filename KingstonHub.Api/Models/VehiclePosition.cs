using System;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace KingstonHub.Api.Models
{
    [Table("vehicle_positions")]
    public class VehiclePosition
    {
        [Key]
        [Column("id")]
        public int Id { get; set; }

        [Required]
        [Column("bus_id")]
        [MaxLength(50)]
        public string BusId { get; set; } = string.Empty;

        [Column("route_id")]
        [MaxLength(20)]
        public string? RouteId { get; set; }

        [Column("trip_id")]
        [MaxLength(100)]
        public string? TripId { get; set; }

        [Required]
        [Column("latitude")]
        public double Latitude { get; set; }

        [Required]
        [Column("longitude")]
        public double Longitude { get; set; }

        [Column("bearing")]
        public double? Bearing { get; set; }

        [Column("speed")]
        public double? Speed { get; set; }

        [Required]
        [Column("timestamp")]
        public DateTime Timestamp { get; set; }

        [Column("current_stop_sequence")]
        public int? CurrentStopSequence { get; set; }

        [Column("stop_id")]
        [MaxLength(50)]
        public string? StopId { get; set; }

        [Column("current_status")]
        [MaxLength(20)]
        public string? CurrentStatus { get; set; }

        [Column("collected_at")]
        public DateTime CollectedAt { get; set; }
    }
}