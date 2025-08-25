# GoogleMapsTool Documentation

## Overview

The `GoogleMapsTool` provides comprehensive mapping and location services integration with the Google Maps API. This tool enables AI assistants to access geocoding, directions, places search, distance calculations, elevation data, and timezone information for any location worldwide.

## Features

### 🗺️ Location Services
- **Geocoding**: Convert addresses to coordinates
- **Reverse Geocoding**: Convert coordinates to addresses
- **Multi-language Support**: Results in 40+ languages
- **Global Coverage**: Worldwide location data

### 🚗 Navigation & Directions
- **Route Planning**: Get directions between locations
- **Multiple Travel Modes**: Driving, walking, bicycling, transit
- **Waypoints**: Add intermediate stops to routes
- **Real-time Traffic**: Consider current traffic conditions

### 🏢 Places & Points of Interest
- **Places Search**: Find businesses, landmarks, and locations
- **Place Details**: Get comprehensive information about specific places
- **Nearby Places**: Discover places around a location
- **Type Filtering**: Filter by place types (restaurant, hotel, etc.)

### 📏 Distance & Time Calculations
- **Distance Matrix**: Calculate distances between multiple points
- **Travel Time**: Get estimated travel durations
- **Multiple Units**: Metric and imperial measurements
- **Bulk Calculations**: Handle multiple origins/destinations

### 🌍 Geographic Data
- **Elevation Data**: Get altitude information for coordinates
- **Timezone Information**: Determine timezone for any location
- **Coordinate Validation**: Ensure location data accuracy

## Actions

### 1. `geocode`
Convert an address to coordinates.

**Parameters:**
- `address` (string, required): The address to geocode
- `language` (string, optional): Language code for results (default: "en")

**Example:**
```json
{
  "action": "geocode",
  "address": "1600 Amphitheatre Parkway, Mountain View, CA",
  "language": "en"
}
```

### 2. `reverse_geocode`
Convert coordinates to an address.

**Parameters:**
- `latitude` (number, required): Latitude coordinate
- `longitude` (number, required): Longitude coordinate
- `language` (string, optional): Language code for results (default: "en")

**Example:**
```json
{
  "action": "reverse_geocode",
  "latitude": 37.4220,
  "longitude": -122.0841,
  "language": "en"
}
```

### 3. `get_directions`
Get directions between two locations.

**Parameters:**
- `origin` (string, required): Starting location (address or coordinates)
- `destination` (string, required): Ending location (address or coordinates)
- `waypoints` (string, optional): Intermediate waypoints (comma-separated)
- `mode` (string, optional): Travel mode - "driving", "walking", "bicycling", "transit" (default: "driving")
- `language` (string, optional): Language code for results (default: "en")

**Example:**
```json
{
  "action": "get_directions",
  "origin": "San Francisco, CA",
  "destination": "Mountain View, CA",
  "waypoints": "Palo Alto, CA",
  "mode": "driving",
  "language": "en"
}
```

### 4. `search_places`
Search for places using text queries.

**Parameters:**
- `query` (string, required): Search query
- `latitude` (number, optional): Latitude for location-based search
- `longitude` (number, optional): Longitude for location-based search
- `radius` (number, optional): Search radius in meters (default: 5000)
- `type` (string, optional): Place type filter (restaurant, hotel, etc.)
- `language` (string, optional): Language code for results (default: "en")

**Example:**
```json
{
  "action": "search_places",
  "query": "restaurants in San Francisco",
  "latitude": 37.7749,
  "longitude": -122.4194,
  "radius": 5000,
  "type": "restaurant"
}
```

### 5. `get_place_details`
Get detailed information about a specific place.

**Parameters:**
- `place_id` (string, required): Google Place ID
- `language` (string, optional): Language code for results (default: "en")

**Example:**
```json
{
  "action": "get_place_details",
  "place_id": "ChIJN1t_tDeuEmsRUsoyG83frY4",
  "language": "en"
}
```

### 6. `get_nearby_places`
Find places near a specific location.

**Parameters:**
- `latitude` (number, required): Latitude coordinate
- `longitude` (number, required): Longitude coordinate
- `radius` (number, optional): Search radius in meters (default: 5000)
- `type` (string, optional): Place type filter
- `keyword` (string, optional): Keyword for search
- `language` (string, optional): Language code for results (default: "en")

**Example:**
```json
{
  "action": "get_nearby_places",
  "latitude": 37.7749,
  "longitude": -122.4194,
  "radius": 5000,
  "type": "restaurant",
  "keyword": "pizza"
}
```

### 7. `get_distance_matrix`
Calculate distances and travel times between multiple points.

**Parameters:**
- `origins` (string, required): Starting points (comma-separated or pipe-separated)
- `destinations` (string, required): Ending points (comma-separated or pipe-separated)
- `mode` (string, optional): Travel mode (default: "driving")
- `units` (string, optional): Units - "metric" or "imperial" (default: "metric")
- `language` (string, optional): Language code for results (default: "en")

**Example:**
```json
{
  "action": "get_distance_matrix",
  "origins": "San Francisco, CA|Oakland, CA",
  "destinations": "Mountain View, CA|Palo Alto, CA",
  "mode": "driving",
  "units": "metric"
}
```

### 8. `get_elevation`
Get elevation data for coordinates.

**Parameters:**
- `latitude` (number, required): Latitude coordinate
- `longitude` (number, required): Longitude coordinate

**Example:**
```json
{
  "action": "get_elevation",
  "latitude": 37.7749,
  "longitude": -122.4194
}
```

### 9. `get_timezone`
Get timezone information for coordinates.

**Parameters:**
- `latitude` (number, required): Latitude coordinate
- `longitude` (number, required): Longitude coordinate
- `timestamp` (number, optional): Unix timestamp for timezone lookup

**Example:**
```json
{
  "action": "get_timezone",
  "latitude": 37.7749,
  "longitude": -122.4194,
  "timestamp": 1640995200
}
```

## Response Format

### Success Response
```json
[
  {
    "success": true,
    "data": {
      "status": "OK",
      "results": [
        {
          "formatted_address": "1600 Amphitheatre Parkway, Mountain View, CA 94043, USA",
          "geometry": {
            "location": {
              "lat": 37.4220,
              "lng": -122.0841
            }
          }
        }
      ]
    }
  }
]
```

### Error Response
```json
[
  {
    "success": false,
    "error": "Google Maps API key not configured"
  }
]
```

## Key Data Points

### Geocoding Results
- Formatted address
- Coordinates (latitude/longitude)
- Address components (street, city, state, country)
- Place ID for further queries

### Directions Results
- Route overview
- Step-by-step instructions
- Distance and duration
- Traffic information
- Alternative routes

### Places Results
- Place name and address
- Rating and reviews
- Opening hours
- Contact information
- Photos and maps

### Distance Matrix Results
- Distance between each origin-destination pair
- Travel time estimates
- Route information
- Traffic considerations

### Elevation Results
- Elevation in meters
- Resolution of elevation data
- Location coordinates

### Timezone Results
- Timezone ID
- UTC offset
- Daylight saving time information

## Integration

### Environment Variables
```bash
# Required for API access
GOOGLE_MAPS_API_KEY=your_api_key_here
```

### API Setup
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable the following APIs:
   - Geocoding API
   - Directions API
   - Places API
   - Distance Matrix API
   - Elevation API
   - Time Zone API
4. Create credentials (API key)
5. Set the `GOOGLE_MAPS_API_KEY` environment variable

### Rate Limits
- **Free Tier**: 2,500 requests/day per API
- **Paid Tier**: 100,000+ requests/day
- **Queries per Second**: 10 QPS for most APIs

## Testing

### Individual Tool Test
```bash
python scripts/test_googlemaps_tool.py
```

### Comprehensive Test
```bash
python scripts/test_all_tools.py
```

### Expected Behavior
- Returns API key errors without proper credentials
- Validates required parameters
- Handles missing location/coordinates
- Supports all travel modes and languages

## Error Handling

### Common Errors
- **REQUEST_DENIED**: Invalid or missing API key
- **ZERO_RESULTS**: No results found for query
- **OVER_QUERY_LIMIT**: Rate limit exceeded
- **INVALID_REQUEST**: Invalid parameters
- **NOT_FOUND**: Location not found

### Parameter Validation
- Address required for geocoding
- Coordinates required for reverse geocoding
- Origin/destination required for directions
- Query required for places search
- Place ID required for place details

## Use Cases

### Navigation & Travel
- Route planning for trips
- Real-time directions
- Multi-stop journeys
- Public transit planning

### Location Services
- Address validation
- Coordinate conversion
- Location-based searches
- Geographic data analysis

### Business Applications
- Store locator services
- Delivery route optimization
- Travel time calculations
- Geographic market analysis

### Development & Research
- Geographic data collection
- Location-based features
- Mapping applications
- Spatial analysis

## Advanced Features

### Multi-language Support
```json
{
  "action": "geocode",
  "address": "東京, 日本",
  "language": "ja"
}
```

### Complex Route Planning
```json
{
  "action": "get_directions",
  "origin": "San Francisco, CA",
  "destination": "Los Angeles, CA",
  "waypoints": "Monterey, CA|Santa Barbara, CA",
  "mode": "driving"
}
```

### Bulk Distance Calculations
```json
{
  "action": "get_distance_matrix",
  "origins": "New York, NY|Boston, MA|Philadelphia, PA",
  "destinations": "Washington, DC|Baltimore, MD|Richmond, VA",
  "mode": "driving"
}
```

### Place Type Filtering
```json
{
  "action": "search_places",
  "query": "coffee",
  "type": "cafe",
  "latitude": 37.7749,
  "longitude": -122.4194
}
```

## Best Practices

### API Key Management
- Store API keys securely in environment variables
- Restrict API keys to specific domains/IPs
- Monitor usage to avoid rate limits
- Use different keys for development/production

### Caching
- Cache geocoding results (addresses don't change often)
- Cache place details for frequently accessed locations
- Implement request deduplication
- Use appropriate cache expiration times

### Error Handling
- Always check for API key configuration
- Handle rate limiting gracefully
- Validate location parameters
- Provide fallback options when possible

### Performance
- Use coordinates when available (faster than addresses)
- Batch requests when possible
- Limit search radius to needed area
- Use appropriate place types for filtering

## Troubleshooting

### API Key Issues
```bash
# Check if API key is set
echo $GOOGLE_MAPS_API_KEY

# Test API key manually
curl "https://maps.googleapis.com/maps/api/geocode/json?address=1600+Amphitheatre+Parkway&key=YOUR_API_KEY"
```

### Location Issues
- Use specific addresses with city/state/country
- Verify coordinates are valid (lat: -90 to 90, lng: -180 to 180)
- Check for typos in place names
- Use postal codes for better accuracy

### Rate Limiting
- Monitor daily request count
- Implement exponential backoff for retries
- Use paid tiers for higher limits
- Cache frequently requested data

### Data Accuracy
- Geocoding accuracy varies by region
- Rural areas may have lower precision
- Some addresses may not be found
- Use place IDs for most accurate results

## Examples

### Travel Planning
```json
{
  "action": "get_directions",
  "origin": "Tokyo, Japan",
  "destination": "Kyoto, Japan",
  "mode": "transit",
  "language": "en"
}
```

### Business Location Search
```json
{
  "action": "search_places",
  "query": "Starbucks",
  "latitude": 40.7128,
  "longitude": -74.0060,
  "radius": 10000
}
```

### Geographic Analysis
```json
{
  "action": "get_distance_matrix",
  "origins": "New York, NY",
  "destinations": "Los Angeles, CA|Chicago, IL|Miami, FL",
  "mode": "driving",
  "units": "imperial"
}
```

### Location Validation
```json
{
  "action": "geocode",
  "address": "123 Main Street, Anytown, USA",
  "language": "en"
}
```

The GoogleMapsTool provides comprehensive mapping and location services for AI assistants, enabling location-aware applications and services.
