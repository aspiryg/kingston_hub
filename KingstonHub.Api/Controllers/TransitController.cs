using Microsoft.AspNetCore.Mvc;
using KingstonHub.Api.Services;
using KingstonHub.Api.Models.DTOs;

namespace KingstonHub.Api.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    [Produces("application/json")]
    public class TransitController : ControllerBase
    {
        private readonly ITransitService _transitService;
        private readonly ILogger<TransitController> _logger;

        public TransitController(ITransitService transitService, ILogger<TransitController> logger)
        {
            _transitService = transitService;
            _logger = logger;
        }

        /// <summary>
        /// Get all currently active vehicles
        /// </summary>
        /// <returns>List of vehicles with current positions</returns>
        [HttpGet("vehicles")]
        [ProducesResponseType(typeof(List<VehicleDto>), StatusCodes.Status200OK)]
        public async Task<ActionResult<List<VehicleDto>>> GetAllVehicles()
        {
            try
            {
                var vehicles = await _transitService.GetAllCurrentVehiclesAsync();
                return Ok(vehicles);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error getting all vehicles");
                return StatusCode(500, "Internal server error");
            }
        }

        /// <summary>
        /// Get a specific vehicle by ID
        /// </summary>
        /// <param name="busId">The bus identifier</param>
        [HttpGet("vehicles/{busId}")]
        [ProducesResponseType(typeof(VehicleDto), StatusCodes.Status200OK)]
        [ProducesResponseType(StatusCodes.Status404NotFound)]
        public async Task<ActionResult<VehicleDto>> GetVehicle(string busId)
        {
            var vehicle = await _transitService.GetVehicleByIdAsync(busId);
            
            if (vehicle == null)
                return NotFound($"Vehicle {busId} not found");

            return Ok(vehicle);
        }

        /// <summary>
        /// Get all active routes with vehicle information
        /// </summary>
        [HttpGet("routes")]
        [ProducesResponseType(typeof(List<RouteDto>), StatusCodes.Status200OK)]
        public async Task<ActionResult<List<RouteDto>>> GetAllRoutes()
        {
            var routes = await _transitService.GetAllRoutesAsync();
            return Ok(routes);
        }

        /// <summary>
        /// Get all vehicles on a specific route
        /// </summary>
        /// <param name="routeId">The route identifier (e.g., "1", "12")</param>
        [HttpGet("routes/{routeId}/vehicles")]
        [ProducesResponseType(typeof(List<VehicleDto>), StatusCodes.Status200OK)]
        public async Task<ActionResult<List<VehicleDto>>> GetRouteVehicles(string routeId)
        {
            var vehicles = await _transitService.GetVehiclesByRouteAsync(routeId);
            return Ok(vehicles);
        }

        /// <summary>
        /// Get historical movement data for a vehicle
        /// </summary>
        /// <param name="busId">The bus identifier</param>
        /// <param name="hours">Number of hours of history (default: 24)</param>
        [HttpGet("history/{busId}")]
        [ProducesResponseType(typeof(VehicleHistoryDto), StatusCodes.Status200OK)]
        [ProducesResponseType(StatusCodes.Status404NotFound)]
        public async Task<ActionResult<VehicleHistoryDto>> GetVehicleHistory(
            string busId, 
            [FromQuery] int hours = 24)
        {
            if (hours < 1 || hours > 168) // Max 7 days
                return BadRequest("Hours must be between 1 and 168");

            var history = await _transitService.GetVehicleHistoryAsync(busId, hours);
            
            if (history == null)
                return NotFound($"No history found for vehicle {busId}");

            return Ok(history);
        }
    }
}