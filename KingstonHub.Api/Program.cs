using KingstonHub.Api.Data;
using KingstonHub.Api.Services;
using Microsoft.EntityFrameworkCore;

var builder = WebApplication.CreateBuilder(args);

// Add services to the container.
// Learn more about configuring OpenAPI at https://aka.ms/aspnet/openapi
builder.Services.AddOpenApi();
//
builder.Services.AddControllers();
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen(c =>
{
   c.SwaggerDoc("v1", new() { 
    Title = "Kingston Transit API", 
    Version = "v1",
    Description = "Real-time Kingston Transit vehicle tracking API"
    }); 
});

// Add DbContext
builder.Services.AddDbContext<TransitDbContext>(options =>
options.UseSqlite(builder.Configuration.GetConnectionString("DefaultConnection")));


// Add TransitService
builder.Services.AddScoped<ITransitService, TransitService>();


// Configure CORS
var allowedOrigins = builder.Configuration.GetSection("Cors:AllowedOrigins").Get<string[]>();
builder.Services.AddCors(options =>
{
    options.AddPolicy("AllowFrontend", 
    policy =>
    {
        policy.WithOrigins(allowedOrigins ?? [])
              .AllowAnyHeader()
              .AllowAnyMethod();
    });
});

var app = builder.Build();

// Configure the HTTP request pipeline.
if (app.Environment.IsDevelopment())
{
    app.MapOpenApi();
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseHttpsRedirection();
app.UseCors("AllowFrontend");
app.UseAuthorization();
app.MapControllers();

app.Run();
