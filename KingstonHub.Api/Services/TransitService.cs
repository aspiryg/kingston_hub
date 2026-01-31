using Microsoft.EntityFrameworkCore;
using KingstonHub.Api.Data;
using KingstonHub.Api.Models;
using KingstonHub.Api.Models.DTOs;

namespace KingstonHub.Api.Services
{
    public class TransitService : ITransitService
    {
        private readonly TransitDbContext _context;
        private readonly ILogger<TransitService> _logger;

        public TransitService(TransitDbContext context, ILogger<TransitService> logger)
        {
            _context = context;
            _logger = logger;
        }

        /// <summary>
        /// Get the most recent position for all active vehicles
        /// </summary>
        public async Task<List<VehicleDto>> GetAllCurrentVehiclesAsync()
        {
            try
            {
                // Get latest position for each unique bus
                var latestPositions = await _context.VehiclePositions
                    .GroupBy(v => v.BusId)
                    .Select(g => g.OrderByDescending(v => v.Timestamp).First())
                    .Where(v => v.Timestamp >= DateTime.UtcNow.AddMinutes(-10)) // Only last 10 minutes
                    .ToListAsync();

                return latestPositions.Select(MapToDto).ToList();
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error fetching current vehicles");
                throw;
            }
        }

        /// <summary>
        /// Get specific vehicle's current position
        /// </summary>
        public async Task<VehicleDto?> GetVehicleByIdAsync(string busId)
        {
            var position = await _context.VehiclePositions
                .Where(v => v.BusId == busId)
                .OrderByDescending(v => v.Timestamp)
                .FirstOrDefaultAsync();

            return position != null ? MapToDto(position) : null;
        }

        /// <summary>
        /// Get all active routes with vehicle counts
        /// </summary>
        public async Task<List<RouteDto>> GetAllRoutesAsync()
        {
            var recentTime = DateTime.UtcNow.AddMinutes(-10);
            
            var routes = await _context.VehiclePositions
                .Where(v => v.Timestamp >= recentTime && v.RouteId != null)
                .GroupBy(v => v.RouteId)
                .Select(g => new RouteDto
                {
                    RouteId = g.Key!,
                    ActiveVehicles = g.Select(v => v.BusId).Distinct().Count(),
                    Vehicles = g.GroupBy(v => v.BusId)
                                .Select(bg => bg.OrderByDescending(v => v.Timestamp).First())
                                .Select(v => MapToDto(v))
                                .ToList()
                })
                .ToListAsync();

            return routes;
        }

        /// <summary>
        /// Get all vehicles currently on a specific route
        /// </summary>
        public async Task<List<VehicleDto>> GetVehiclesByRouteAsync(string routeId)
        {
            var recentTime = DateTime.UtcNow.AddMinutes(-10);

            var vehicles = await _context.VehiclePositions
                .Where(v => v.RouteId == routeId && v.Timestamp >= recentTime)
                .GroupBy(v => v.BusId)
                .Select(g => g.OrderByDescending(v => v.Timestamp).First())
                .ToListAsync();

            return vehicles.Select(MapToDto).ToList();
        }

        /// <summary>
        /// Get historical movement data for a vehicle
        /// </summary>
        public async Task<VehicleHistoryDto?> GetVehicleHistoryAsync(string busId, int hours = 24)
        {
            var cutoffTime = DateTime.UtcNow.AddHours(-hours);

            var history = await _context.VehiclePositions
                .Where(v => v.BusId == busId && v.Timestamp >= cutoffTime)
                .OrderBy(v => v.Timestamp)
                .ToListAsync();

            if (!history.Any())
                return null;

            return new VehicleHistoryDto
            {
                BusId = busId,
                History = history.Select(v => new HistoryPoint
                {
                    Timestamp = v.Timestamp,
                    Latitude = v.Latitude,
                    Longitude = v.Longitude,
                    Speed = v.Speed,
                    RouteId = v.RouteId
                }).ToList()
            };
        }

        /// <summary>
        /// Helper method to map VehiclePosition entity to DTO
        /// </summary>
        private VehicleDto MapToDto(VehiclePosition position)
        {
            return new VehicleDto
            {
                BusId = position.BusId,
                RouteId = position.RouteId,
                TripId = position.TripId,
                Location = new LocationDto
                {
                    Latitude = position.Latitude,
                    Longitude = position.Longitude
                },
                Speed = position.Speed,
                Bearing = position.Bearing,
                CurrentStatus = position.CurrentStatus,
                StopId = position.StopId,
                LastUpdated = position.Timestamp
            };
        }
    }
}