using Microsoft.EntityFrameworkCore;
using KingstonHub.Api.Models;

namespace KingstonHub.Api.Data
{
    public class TransitDbContext : DbContext
    {
        public TransitDbContext(DbContextOptions<TransitDbContext> options)
            : base(options)
        {
        }

        public DbSet<VehiclePosition> VehiclePositions { get; set; } = null!;

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            base.OnModelCreating(modelBuilder);

            // Configure indexes (matching Python models)
            modelBuilder.Entity<VehiclePosition>()
                .HasIndex(v => new { v.BusId, v.Timestamp })
                .HasDatabaseName("idx_bus_timestamp");

            modelBuilder.Entity<VehiclePosition>()
                .HasIndex(v => new { v.RouteId, v.Timestamp })
                .HasDatabaseName("idx_route_timestamp");
        }
    }
}