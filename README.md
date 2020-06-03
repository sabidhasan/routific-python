[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# Routific Python Module
This Python class is a client to interact with the [Routific API](http://docs.routific.com/), which is a practical and scalable solution to the Vehicle Routing Problem and Traveling Salesman Problem.

It is a Python port of the Ruby [Routific Gem](https://github.com/routific/routific-gem). Parts of this readme are adapted or copied from that repository's ReadMe. All code is under the MIT Licence.

Please refer to the full documentation for a detailled documentation of the API.

# Usage

Installation is not yet implemented from PyPI. To install locally use dist tools:

```
python setup.py install
```

Remember to require it and set your token before using it. A simple example of a request:

```python
import routific

jwt_token = "some_token"  # Get the token from routific.com by signing up!
Routific.set_token(jwt_token)

routific.set_visit("order_1", {
    "location": {
      "name": "YVR Airport",
      "lat": 49.194713,
      "lng": -123.180684,
    }
})

routific.set_visit("order_2", {
    "location": {
      "name": "Routific HQ",
      "lat": 49.284924,
      "lng": -123.111946,
    }
})

routific.set_vehicle("vehicle_1", {
    "start_location": {
      "name": "800 Kingsway",
      "lat": 49.2553636,
      "lng": -123.0873365
    }
})

routific.set_options({"max_vehicle_overtime": 100})
results = routific.get_route()
```


# Initialization

The Routific constructor accepts no arguments. By default, the API uses version 1 of the API. Change this by changing the `_URL` class property:

```python
  Routific._URL = "https://api.routific.com/v2/vrp"
```


# Methods
#### `routific.set_visit( id, params )`

Sets a visit with the specified id and parameters:

- `location` (*required*): Object representing the location of the visit.
  + lat: Latitude of this location
  + lng: Longitude of this location
  + name: (optional) Name of the location
- `start`: the earliest time for this visit. Default value is 00:00, if not specified.
- `end`: the latest time for this visit. Default value is    23:59, if not specified.
- `duration`: the length of this visit in minutes
- `demand`: the capacity that this visit requires
- `priority`: higher priority visits are more likely to be served
- `type`: restrict the vehicle that can serve this visit
- `time_windows`: specify different time-windows for serving the visit.
It should be an array of hashes: `[ { "start" => "08:00", "end" => "12:00" } ]`

#### `routific.set_vehicle( id, params )`

Sets a vehicle with the specified ID and parameters:
- `start_location` (*required*): Object representing the start location for this vehicle.
  + lat: Latitude of this location
  + lng: Longitude of this location
  + name: (optional) Name of the location
- `end_location`: Object representing the end location for this vehicle.
  + lat: Latitude of this location
  + lng: Longitude of this location
  + name: (optional) Name of the location
- `shift_start`: this vehicle's start shift time (e.g. '08:00'). Default value is 00:00, if not specified.
- `shift_end`: this vehicle's end shift time (e.g. '17:00'). Default value is 23:59, if not specified.
- `capacity`: the capacity that this vehicle can load
- `type`: restrict the visit this vehicle can serve
- `speed`: vehicle speed
- `min_visits`: minimum number of visits that should be assigned to this vehicle
- `strict_start`: force the departure time to be `shift_start`
- `breaks`: specify breaks for the driver.
It should be an array of hashes: `[ { "id" => "lunch", "start" => "12:00", "end" => "12:30" } ]`

#### `routific.set_options( params )`

Sets optional options onto the route requests.
Optional arguments must be one of the following:

- `traffic`
- `min_visits_per_vehicle`
- `balance`
- `min_vehicles`
- `shortest_distance`
- `squash_duration`
- `max_vehicle_overtime`
- `max_visit_lateness`

#### `routific.get_route()`

Returns an optimized route using the previously provided visits, fleet and options.
The request may timeout if the problem is too large.

It returns a route object with the following attributes:
- `status`: A sanity check
- `unserved`: List of visits that could not be scheduled.
- `vehicle_routes`: The optimized schedule
- other attributes that you can find in the [full documentation](https://docs.routific.com)

The `vehicle_routes` attribute is a hash mapping vehicle ID to the corresponding route, represented as an array of waypoints: `{ "vehicle_1" => [ way_point_1, way_point_2, way_point_3, way_point_4 ] }`

The waypoint object has the following attributes:
- `location_id`
- `arrival_time`
- `finish_time`
- other attributes that you can find in the [full documentation](https://docs.routific.com)



# Operations
The Python wrapper only supports the VRP endpoint, and runs in non-async, blocking mode. It calls the VRP endpoint (long version) and waits until the job is processed. It returns the job output.


# Todo
- Unit tests!
- Add `asyncio` support for the polling version of the get_route
- Add more complete API documentation

