using KingstonHub.Api.Models.DTOs;

namespace KingstonHub.Api.Services
{
    public interface ITransitService
    {
        Task<List<VehicleDto>> GetAllCurrentVehiclesAsync();
        Task<VehicleDto?> GetVehicleByIdAsync(string busId);
        Task<List<RouteDto>> GetAllRoutesAsync();
        Task<List<VehicleDto>> GetVehiclesByRouteAsync(string routeId);
        Task<VehicleHistoryDto?> GetVehicleHistoryAsync(string busId, int hours = 24);
    }
}