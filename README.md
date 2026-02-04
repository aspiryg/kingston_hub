# KingstonHub - City Services & Transit Platform

## What is this?

This is a personal portfolio project I'm building over the next month to showcase my data engineering and full-stack development skills. The idea is to create a platform that aggregates fragmented public services information in Kingston, Ontario into one unified place. Right now, if you want to know where the bus is, find student housing, check healthcare wait times, or see what events are happening - you have to visit like 5 different websites. This project aims to fix that.

## The Problem

Kingston has tons of public data scattered everywhere - the City's open data portal, transit systems, housing listings, Queen's University services, St. Lawrence College services, healthcare info, provincial databases, etc. It's a mess. Students and residents waste time jumping between different sites just to find basic information. So I thought, why not build something that pulls it all together?

## What I'm Planning to Build

### The Big Picture
A data aggregation platform that scrapes and integrates data from multiple sources, processes it using various algorithms, and serves it through a modern web interface. Think of it as a one-stop-shop for Kingston city services, but also as a showcase of how to handle real-time data pipelines, microservices architecture, and smart data processing.

### Main Components (The Plan)

**1. Data Collection Layer (Python)**
- Web scrapers that pull data from Kingston Open Data API, transit systems, housing sites, healthcare facilities, university services
- ETL pipelines using Apache Airflow to run scheduled jobs (daily housing scrapes, hourly transit updates, weekly healthcare updates)
- Data cleaning and transformation
- Maybe some ML models later for predictions (housing prices, transit delays, etc.)

**2. Backend Services (Mix of Technologies)**
- API Gateway in C# .NET (or maybe Node.js, still deciding) - single entry point that handles authentication, rate limiting, routing
- Multiple microservices:
  - Transit Service - real-time bus tracking, route optimization using graph algorithms (Dijkstra, A*)
  - Housing Service - aggregated listings, price predictions, recommendations
  - Healthcare Service - clinic/hospital info, wait time predictions
  - Events Service - city events, university events, personalized recommendations
- Analytics Service in Python using FastAPI - exposes ML models as REST APIs

**3. Data Storage**
- PostgreSQL for structured data (users, service info, relationships) with PostGIS for geospatial queries
- MongoDB for semi-structured scraped data and flexible schemas
- Redis for caching frequently accessed data
- Maybe Elasticsearch for powerful search capabilities

**4. Message Queue**
- Kafka or RabbitMQ to handle async processing and decouple services
- Event-driven architecture for real-time updates

**5. Frontend (React)**
- Interactive maps showing buses, housing, services using Leaflet/Mapbox
- Real-time dashboards
- Search and filtering
- Data visualizations with charts

**6. Infrastructure**
- Docker containers for everything
- Maybe Kubernetes for orchestration (or just Docker Compose to keep it simple)
- CI/CD with GitHub Actions
- Deploy to Azure/AWS/DigitalOcean
- Monitoring with Prometheus and Grafana

### Cool Features I Want to Add

- **Smart Route Planning** - not just "how do I get there" but "what's the fastest route considering current traffic, bus delays, and my schedule" (imitating Google Maps but localized)
- **Housing Recommendations** - ML-based suggestions based on budget, distance to campus, amenities
- **Wait Time Predictions** - predict healthcare facility wait times using historical data
- **Personalized Alerts** - notify users about relevant events, housing listings, service disruptions
- **Geospatial Analysis** - find nearest services, coverage areas, heatmaps
- **Real-time Updates** - WebSockets for live bus tracking and instant notifications

### Algorithms & Data Structures to Show Off

This is really about demonstrating I can do more than just CRUD apps:

- **Graph algorithms**: Dijkstra's, A* for transit routing
- **Spatial algorithms**: KNN for finding nearest services, Haversine for distance calculations
- **Recommendation systems**: Collaborative filtering, content-based filtering
- **ML models**: Linear regression for price prediction, clustering for grouping similar services, time series analysis
- **Efficient data structures**: Tries for autocomplete, Bloom filters, LRU caches, Priority queues
- **Text processing**: TF-IDF for search, sentiment analysis on reviews

## Current Status - Where We're At Now

### ✅ What's Built
Right now I've got the foundation in place:

1. **Python Data Collector** - Successfully collecting real-time bus data from Kingston Transit's GTFS-Realtime API every 30 seconds. It's working and I can see buses moving around the city!

2. **MongoDB Database** - Set up and storing vehicle positions with proper indexes for fast queries


## Why This Project?

Honestly? I need something impressive to show in interviews. But also, it's actually useful - I live in Kingston and this would genuinely help students and residents. Plus it lets me demonstrate:
- Handling real-time data at scale
- Building microservices architecture
- Working with multiple tech stacks (Python, C#/.NET or Node.js, React)
- Implementing actual algorithms, not just frameworks
- Data engineering and ETL pipelines
- Full-stack development
- System design thinking

It's ambitious for a month but even if I don't finish everything, having a working prototype with real data and some smart features should be solid for my portfolio.

## Tech Stack Summary

**Current**: Python, MongoDB, Express.js/Node.js, TypeScript
**Planned**: React, Redis, PostgreSQL, Apache Airflow, possibly .NET microservices, Docker, maybe Kafka

The stack might change as I build - I'm learning as I go and adjusting based on what makes sense.

---

*This is a work in progress. Started: January 5, 2026. Currently in early development phase. I stopped development temporarily to focus on other priorities but plan to resume soon.*