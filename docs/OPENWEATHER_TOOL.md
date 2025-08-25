# OpenWeatherTool Documentation

## Overview

The `OpenWeatherTool` provides comprehensive weather data integration with the OpenWeatherMap API. This tool enables AI assistants to access current weather conditions, forecasts, weather alerts, air pollution data, geocoding services, and historical weather data for any location worldwide.

## Features

### 🌤️ Weather Data
- **Current Weather**: Get real-time weather conditions for any location
- **Weather Forecast**: Access 5-day weather forecasts with hourly data
- **Weather Alerts**: Retrieve severe weather warnings and alerts
- **Weather History**: Access historical weather data for analysis

### 🌍 Location Services
- **Geocoding**: Convert location names to coordinates
- **Reverse Geocoding**: Convert coordinates to location names
- **Multi-format Support**: City names, coordinates, ZIP codes

### 🌬️ Environmental Data
- **Air Pollution**: Get air quality index and pollution data
- **Multiple Units**: Metric, Imperial, and Kelvin temperature units
- **Multi-language**: Support for 40+ languages

## Actions

### 1. `get_current_weather`
Get current weather conditions for a location.

**Parameters:**
- `location` (string, optional): City name, ZIP code, or coordinates
- `latitude` (number, optional): Latitude coordinate
- `longitude` (number, optional): Longitude coordinate
- `units` (string, optional): Units system - "metric", "imperial", or "kelvin" (default: "metric")
- `lang` (string, optional): Language code (e.g., "en", "es", "fr")

**Example:**
```json
{
  "action": "get_current_weather",
  "location": "London",
  "units": "metric",
  "lang": "en"
}
```

### 2. `get_weather_forecast`
Get weather forecast for up to 16 days.

**Parameters:**
- `location` (string, optional): City name, ZIP code, or coordinates
- `latitude` (number, optional): Latitude coordinate
- `longitude` (number, optional): Longitude coordinate
- `days` (number, optional): Number of days (1-16, default: 5)
- `units` (string, optional): Units system
- `lang` (string, optional): Language code
- `exclude` (string, optional): Exclude parts - "current,minutely,hourly,daily,alerts"

**Example:**
```json
{
  "action": "get_weather_forecast",
  "location": "New York",
  "days": 7,
  "units": "imperial"
}
```

### 3. `get_weather_alerts`
Get weather alerts and warnings for a location.

**Parameters:**
- `location` (string, optional): City name, ZIP code, or coordinates
- `latitude` (number, optional): Latitude coordinate
- `longitude` (number, optional): Longitude coordinate
- `units` (string, optional): Units system
- `lang` (string, optional): Language code

**Example:**
```json
{
  "action": "get_weather_alerts",
  "location": "Miami",
  "units": "metric"
}
```

### 4. `get_air_pollution`
Get air pollution data for coordinates.

**Parameters:**
- `latitude` (number, required): Latitude coordinate
- `longitude` (number, required): Longitude coordinate

**Example:**
```json
{
  "action": "get_air_pollution",
  "latitude": 40.7128,
  "longitude": -74.0060
}
```

### 5. `get_geocoding`
Convert location names to coordinates.

**Parameters:**
- `location` (string, required): City name, address, or location
- `limit` (number, optional): Number of results (1-5, default: 1)

**Example:**
```json
{
  "action": "get_geocoding",
  "location": "Tokyo",
  "limit": 3
}
```

### 6. `get_reverse_geocoding`
Convert coordinates to location names.

**Parameters:**
- `latitude` (number, required): Latitude coordinate
- `longitude` (number, required): Longitude coordinate
- `limit` (number, optional): Number of results (1-10, default: 1)

**Example:**
```json
{
  "action": "get_reverse_geocoding",
  "latitude": 35.6762,
  "longitude": 139.6503,
  "limit": 3
}
```

### 7. `get_weather_history`
Get historical weather data for coordinates.

**Parameters:**
- `latitude` (number, required): Latitude coordinate
- `longitude` (number, required): Longitude coordinate
- `dt` (number, required): Unix timestamp for the date

**Example:**
```json
{
  "action": "get_weather_history",
  "latitude": 48.8566,
  "longitude": 2.3522,
  "dt": 1640995200
}
```

## Response Format

### Success Response
```json
[
  {
    "success": true,
    "data": {
      "location": "London, GB",
      "temperature": 15.2,
      "description": "scattered clouds",
      "humidity": 72,
      "wind_speed": 3.6,
      "pressure": 1013,
      "visibility": 10000
    }
  }
]
```

### Error Response
```json
[
  {
    "success": false,
    "error": "OpenWeatherMap API key not configured"
  }
]
```

## Key Data Points

### Current Weather
- Temperature (current, feels like, min, max)
- Weather description and icon
- Humidity and pressure
- Wind speed and direction
- Visibility and cloud cover
- Sunrise and sunset times

### Forecast Data
- Daily and hourly forecasts
- Temperature ranges
- Precipitation probability
- Wind conditions
- UV index

### Air Pollution
- Air Quality Index (AQI)
- PM2.5 and PM10 levels
- Ozone, NO2, SO2, CO levels
- Health recommendations

### Location Data
- Coordinates (lat/lon)
- Country and state
- Local names
- Timezone information

## Integration

### Environment Variables
```bash
# Required for API access
OPENWEATHER_API_KEY=your_api_key_here
```

### API Setup
1. Sign up at [OpenWeatherMap](https://openweathermap.org/api)
2. Get your API key from the dashboard
3. Set the `OPENWEATHER_API_KEY` environment variable
4. Free tier includes 1,000 calls/day

### Rate Limits
- **Free Tier**: 1,000 calls/day
- **Paid Tiers**: 10,000+ calls/day
- **Call Frequency**: 1 call per 10 minutes for current weather

## Testing

### Individual Tool Test
```bash
python scripts/test_openweather_tool.py
```

### Comprehensive Test
```bash
python scripts/test_all_tools.py
```

### Expected Behavior
- Returns API key errors without proper credentials
- Validates required parameters
- Handles missing location/coordinates
- Supports all unit systems and languages

## Error Handling

### Common Errors
- **401 Unauthorized**: Invalid or missing API key
- **404 Not Found**: Location not found
- **429 Too Many Requests**: Rate limit exceeded
- **400 Bad Request**: Invalid parameters

### Parameter Validation
- Location or coordinates required for weather data
- Latitude/longitude required for air pollution
- Timestamp required for weather history
- Valid unit systems: metric, imperial, kelvin

## Use Cases

### Weather Monitoring
- Get current conditions for travel planning
- Monitor weather for outdoor activities
- Check air quality for health concerns

### Location Services
- Convert addresses to coordinates
- Find nearby locations
- Validate location data

### Historical Analysis
- Weather pattern analysis
- Climate trend research
- Historical event correlation

### Integration Scenarios
- Travel planning applications
- Weather-dependent scheduling
- Environmental monitoring
- Location-based services

## Advanced Features

### Multi-language Support
```json
{
  "action": "get_current_weather",
  "location": "Paris",
  "lang": "fr"
}
```

### Custom Units
```json
{
  "action": "get_weather_forecast",
  "location": "Los Angeles",
  "units": "imperial"
}
```

### Exclude Data
```json
{
  "action": "get_weather_forecast",
  "location": "Chicago",
  "exclude": "current,minutely"
}
```

## Best Practices

### API Key Management
- Store API keys securely in environment variables
- Rotate keys regularly
- Monitor usage to avoid rate limits

### Caching
- Cache weather data for 10-15 minutes
- Cache geocoding results for longer periods
- Implement exponential backoff for retries

### Error Handling
- Always check for API key configuration
- Validate location parameters
- Handle rate limiting gracefully
- Provide fallback data when possible

### Performance
- Use coordinates when available (faster)
- Limit forecast days to needed range
- Exclude unnecessary data parts
- Batch requests when possible

## Troubleshooting

### API Key Issues
```bash
# Check if API key is set
echo $OPENWEATHER_API_KEY

# Test API key manually
curl "https://api.openweathermap.org/data/2.5/weather?q=London&appid=YOUR_API_KEY"
```

### Location Issues
- Use specific city names with country codes
- Verify coordinates are valid
- Check for typos in location names

### Rate Limiting
- Monitor daily call count
- Implement request caching
- Use paid tiers for higher limits

### Data Accuracy
- Weather data updates every 10 minutes
- Forecast accuracy decreases with time
- Historical data may have gaps

## Examples

### Travel Planning
```json
{
  "action": "get_weather_forecast",
  "location": "Tokyo, JP",
  "days": 7,
  "units": "metric",
  "lang": "en"
}
```

### Air Quality Check
```json
{
  "action": "get_air_pollution",
  "latitude": 35.6762,
  "longitude": 139.6503
}
```

### Location Lookup
```json
{
  "action": "get_geocoding",
  "location": "Times Square, New York",
  "limit": 1
}
```

The OpenWeatherTool provides comprehensive weather data integration for AI assistants, enabling weather-aware applications and services.
