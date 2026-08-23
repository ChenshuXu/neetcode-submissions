# Proximity request routing

You're tasked to build a request routing system for a global payment processing platform that handles transactions for millions of merchants worldwide. Your infrastructure spans multiple datacenters across continents to ensure low latency and high availability for payment processing.

You're tasked to build a request routing system. Your router must select the optimal datacenter based on geographic proximity, health status, and capacity constraints.

## Input/Output Format

Your program reads commands from stdin and writes results to stdout. Each command is on a separate line.

## Output Format Rules

- SUCCESS: Commands return `OK` or structured data as specified
- ERROR: Commands return `ERROR` (no additional message)
- Lists: Comma-separated with no spaces (e.g., `dc1,dc2,dc3`)
- Boolean values: `true` or `false` (lowercase)

# Part 1: Datacenter Registry and Health Management

Build the foundational data structures and APIs for managing datacenter registration and health status.

## Requirements

- Implement datacenter registration with validation
- Validate coordinates: latitude `[-90, 90]`, longitude `[-180, 180]` (for simplicity you can assume these to be integers)
- Validate capacity: must be `> 0`
- Prevent duplicate registrations
- Support health status management
- All datacenters initially registered as healthy with load = 0

## Commands to implement

```text
REGISTER <name> <latitude> <longitude> <capacity>
  - Registers a new datacenter
  - Returns: OK or ERROR
  - Error cases:
    * Datacenter with same name already exists
    * Invalid latitude (not in [-90, 90])
    * Invalid longitude (not in [-180, 180])
    * Invalid capacity (<= 0)

SET_HEALTHY <name> <true|false>
  - Sets datacenter health status
  - Returns: OK or ERROR
  - Error cases:
    * Datacenter does not exist
```

## Example usage

```text
Input:
  REGISTER us-west 38 -122 100
  REGISTER us-east 41 -74 150
  REGISTER eu-west 52 0 200
  SET_HEALTHY us-east false
  REGISTER us-west 50 -100 50
  REGISTER invalid 91 0 100
  REGISTER invalid2 0 0 0

Output:
  OK
  OK
  OK
  OK
  ERROR
  ERROR
  ERROR
```

# Part 2: Distance Calculation

Implement the Haversine formula to calculate great-circle distances between coordinates.

## Requirements

- Calculate great-circle distance using Haversine formula
- Earth's radius: 6371 km
- Return distance as integer (round the value)

To help you, here is the pseudo code for the Haversine formula:

```text
FUNCTION haversine_distance(loc1, loc2):
    CONSTANT earth_radius_km = 6371

    // Convert degrees to radians
    lat1_rad = loc1.latitude * π / 180
    lat2_rad = loc2.latitude * π / 180
    delta_lat = (loc2.latitude - loc1.latitude) * π / 180
    delta_lon = (loc2.longitude - loc1.longitude) * π / 180

    // Haversine formula
    a = sin²(delta_lat / 2) + cos(lat1_rad) * cos(lat2_rad) * sin²(delta_lon / 2)
    c = 2 * atan2(√a, √(1-a))
    distance = earth_radius_km * c
    RETURN distance
END FUNCTION
```

## Commands to implement

```text
DISTANCE <lat1> <lon1> <lat2> <lon2>
  - Calculates great-circle distance between two coordinates
  - Returns: <distance_km> as integer
  - Always returns a value (no error cases for valid integer coordinates)
```

## Example usage

```text
Input:
  DISTANCE 0 0 0 0
  DISTANCE 38 -122 41 -74
  DISTANCE 0 0 10 0
  DISTANCE 36 140 -33 -71

Output:
  0
  4080
  1112
  17167
```

# Part 3: Geographic Routing with Capacity

Implement the core routing algorithm that selects the optimal datacenter based on distance, health, and capacity.

## Requirements

- Route to nearest healthy datacenter with available capacity
- Try datacenters in order of distance (nearest first) until finding one with capacity
- Return attempted datacenters sorted by distance (only healthy DCs)
- Tie-breaking: if equidistant, sort alphabetically by name
- Successful route increments datacenter load by 1
- Datacenter load persists across multiple `ROUTE` commands

## Commands to implement

```text
ROUTE <latitude> <longitude>
  - Routes to nearest healthy datacenter with available capacity
  - Returns: <selected_dc> <distance_km> <attempted_order>
  - Returns: NONE <attempted_order> if no capacity available
  - attempted_order: Only healthy DCs sorted by distance, comma-separated
  - Increments selected datacenter's load by 1
  - All values are integers
```

## Example

```text
Input:
  REGISTER us-west 38 -122 2
  REGISTER us-east 41 -74 100
  ROUTE 38 -122
  ROUTE 38 -122
  ROUTE 38 -122

Output:
  OK
  OK
  us-west 0 us-west,us-east
  us-west 0 us-west,us-east
  us-east 4080 us-west,us-east
```
