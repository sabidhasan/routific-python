import warnings
import requests
from exceptions import RoutificAPIKeyError
from visit import Visit
from vehicle import Vehicle

class Routific():
    """ Defines base Routific class to interact with the API
    """

    # User's API token obtained after signing up for an account
    _API_TOKEN = None
    _URL = f"https://api.routific.com/v1/vrp"

    def __init__(self):
        if not self._validate_token():
            raise RoutificAPIKeyError("Token not supplied")

        # All destinations to be visted for this call
        self._visits = {}
        # Fleet of cars and their properties, being used for optimization
        self._vehicles = {}
        self._options = {}

    @classmethod
    def set_token(cls, token: str) -> None:
        """ Sets the authentication token to use
        """
        cls._API_TOKEN = token
        if not cls._validate_token():
            raise RoutificAPIKeyError("Token not valid")

    @classmethod
    def get_token(cls) -> str:
        return cls._API_TOKEN

    def set_visit(self, id_: str, params: dict) -> None:
        """
            Sets a visit with the specified id and parameters:
                location (required): Object representing the location of the visit.
                    lat: Latitude of this location
                    lng: Longitude of this location
                    name: (optional) Name of the location
                start: the earliest time for this visit. Default value is 00:00, if not specified.
                end: the latest time for this visit. Default value is 23:59, if not specified.
                duration: the length of this visit in minutes
                demand: the capacity that this visit requires
                priority: higher priority visits are more likely to be served
                type: restrict the vehicle that can serve this visit
                time_windows: specify different time-windows for serving the visit. It should be an array of dicts: [ { "start": "08:00", "end": "12:00" } ]
        """
        if id_ in self._visits:
            warnings.warn("ID for this route already exists; overwriting previous definition")

        self._visits[id_] = Visit(params)

    def set_vehicle(self, id_: str, params: dict) -> None:
        """
            Sets a vehicle with the specified ID and parameters:
            start_location (required): Object representing the start location for this vehicle.
                lat: Latitude of this location
                lng: Longitude of this location
                name: (optional) Name of the location
            end_location: Object representing the end location for this vehicle.
                lat: Latitude of this location
                lng: Longitude of this location
                name: (optional) Name of the location
            shift_start: this vehicle's start shift time (e.g. '08:00'). Default value is 00:00, if not specified.
            shift_end: this vehicle's end shift time (e.g. '17:00'). Default value is 23:59, if not specified.
            capacity: the capacity that this vehicle can load
            type: restrict the visit this vehicle can serve
            speed: vehicle speed
            min_visits: minimum number of visits that should be assigned to this vehicle
            strict_start: force the departure time to be shift_start
            breaks: specify breaks for the driver. It should be an array of hashes: [ { "id" => "lunch", "start" => "12:00", "end" => "12:30" } ]        """

        if id_ in self._visits:
            warnings.warn("ID for this route already exists; overwriting previous definition")

        self._vehicles[id_] = Vehicle(params)

    def set_options(self, params: dict) -> None:
        if self._options:
            warnings.warn("Clearing previously set options")
            self._options = {}

        valid_options = [
            "traffic",
            "min_visits_per_vehicle",
            "balance",
            "min_vehicles",
            "shortest_distance",
            "squash_durations",
            "max_vehicle_overtime",
            "max_visit_lateness",
            "polylines"
        ]

        for option in valid_options:
            if option in params:
                self._options[option] = params[option]

    def clear_visits(self) -> None:
        """ Clears all visits
        """
        self._visits = {}

    def clear_vehicles(self) -> None:
        """ Clears all vehicles
        """
        self._vehicles = {}

    def get_route(self) -> dict:
        data = {
            "visits": {name: visit.to_api() for name, visit in self._visits.items()},
            "fleet": {name: veh.to_api() for name, veh in self._vehicles.items()},
        }

        resp = requests.post(self._URL, json=data, headers={
          'Content-Type': 'application/json',
          'Authorization': "bearer " + self.get_token(),
        })

        if resp.status_code != 200:
            raise ConnectionError(f"Unsuccessful response. HTTP Error Code: {resp.status_code}")

        try:
            return resp.json() 
        except BaseException:
            raise TypeError("Invalid JSON returned from Routific")

    @classmethod
    def _validate_token(cls) -> bool:
        return cls._API_TOKEN is not None


if __name__ == "__main__":
    jwt_token = "token"
    
    # Set API token obtained from the routific developer site
    Routific.set_token(jwt_token)
    routific = Routific()

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
    print(results)
