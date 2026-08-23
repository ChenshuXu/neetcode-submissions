import math
import sys
from typing import List, Sequence


class Datacenter:
    def __init__(self, latitude: int, longitude: int, capacity: int) -> None:
        self.latitude = latitude
        self.longitude = longitude
        self.capacity = capacity
        self.load = 0
        self.healthy = True


def valid_coordinates(latitude: int, longitude: int) -> bool:
    if latitude < -90:
        return False

    if latitude > 90:
        return False

    if longitude < -180:
        return False

    if longitude > 180:
        return False

    return True


def haversine_distance(
    lat1: int,
    lon1: int,
    lat2: int,
    lon2: int,
) -> float:
    earth_radius_km = 6371

    lat1_rad = lat1 * math.pi / 180
    lat2_rad = lat2 * math.pi / 180
    delta_lat = (lat2 - lat1) * math.pi / 180
    delta_lon = (lon2 - lon1) * math.pi / 180

    a = math.sin(delta_lat / 2) ** 2
    a += math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon / 2) ** 2

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = earth_radius_km * c

    return distance


def register_datacenter(parts, datacenters) -> str:
    if len(parts) != 5:
        return "ERROR"

    name = parts[1]

    try:
        latitude = int(parts[2])
        longitude = int(parts[3])
        capacity = int(parts[4])
    except ValueError:
        return "ERROR"

    if name in datacenters:
        return "ERROR"

    if not valid_coordinates(latitude, longitude):
        return "ERROR"

    if capacity <= 0:
        return "ERROR"

    datacenter = Datacenter(latitude, longitude, capacity)
    datacenters[name] = datacenter

    return "OK"


def set_datacenter_health(parts, datacenters) -> str:
    if len(parts) != 3:
        return "ERROR"

    name = parts[1]
    healthyValue = parts[2]

    if name not in datacenters:
        return "ERROR"

    if healthyValue == "true":
        newHealthStatus = True
    elif healthyValue == "false":
        newHealthStatus = False
    else:
        return "ERROR"

    datacenter = datacenters[name]
    datacenter.healthy = newHealthStatus

    return "OK"


def calculate_distance(parts) -> str:
    if len(parts) != 5:
        return "ERROR"

    try:
        latitude1 = int(parts[1])
        longitude1 = int(parts[2])
        latitude2 = int(parts[3])
        longitude2 = int(parts[4])
    except ValueError:
        return "ERROR"

    distance = haversine_distance(
        latitude1,
        longitude1,
        latitude2,
        longitude2,
    )

    roundedDistance = round(distance)
    result = str(roundedDistance)

    return result


def route_request(parts, datacenters) -> str:
    if len(parts) != 3:
        return "ERROR"

    try:
        latitude = int(parts[1])
        longitude = int(parts[2])
    except ValueError:
        return "ERROR"

    if not valid_coordinates(latitude, longitude):
        return "ERROR"

    healthyDatacenters = []

    for name in datacenters:
        datacenter = datacenters[name]

        if not datacenter.healthy:
            continue

        distance = haversine_distance(
            latitude,
            longitude,
            datacenter.latitude,
            datacenter.longitude,
        )

        candidate = (distance, name)
        healthyDatacenters.append(candidate)

    healthyDatacenters.sort()

    attemptedNames = []

    for candidate in healthyDatacenters:
        name = candidate[1]
        attemptedNames.append(name)

    attemptedOrder = ",".join(attemptedNames)
    selectedName = None
    selectedDistance = None

    for candidate in healthyDatacenters:
        distance = candidate[0]
        name = candidate[1]
        datacenter = datacenters[name]

        if datacenter.load >= datacenter.capacity:
            continue

        selectedName = name
        selectedDistance = distance
        break

    if selectedName is None:
        result = "NONE"

        if attemptedOrder != "":
            result += " "
            result += attemptedOrder

        return result

    selectedDatacenter = datacenters[selectedName]
    selectedDatacenter.load += 1

    roundedDistance = round(selectedDistance)
    result = selectedName
    result += " "
    result += str(roundedDistance)
    result += " "
    result += attemptedOrder

    return result


def process_datacenter_commands(commands: Sequence[str]) -> List[str]:
    datacenters = {}
    results = []

    for command in commands:
        if "," in command:
            parts = command.split(",")
        else:
            parts = command.split()

        if len(parts) == 0:
            results.append("ERROR")
            continue

        operation = parts[0]

        if operation == "REGISTER":
            result = register_datacenter(parts, datacenters)
        elif operation == "SET_HEALTHY":
            result = set_datacenter_health(parts, datacenters)
        elif operation == "DISTANCE":
            result = calculate_distance(parts)
        elif operation == "ROUTE":
            result = route_request(parts, datacenters)
        else:
            result = "ERROR"

        results.append(result)

    return results


def main() -> None:
    commands = []

    for line in sys.stdin:
        command = line.strip()

        if command == "":
            continue

        commands.append(command)

    results = process_datacenter_commands(commands)

    for result in results:
        print(result)


if __name__ == "__main__":
    main()
