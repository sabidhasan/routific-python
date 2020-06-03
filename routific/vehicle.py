from schema import Schema, Optional, SchemaError
from exceptions import RoutificParamsError

VEHICLE_SCHEMA = Schema({
    "start_location": {
        "lat": float,
        "lng": float,
        Optional("name"): str
    },
    Optional("end_location", default={}): {
        "lat": float,
        "lng": float,
        Optional("name"): str
    },
    Optional("shift_start", default="00:00"): str,
    Optional("shift_end", default="23:59"): str,
    Optional("capacity"): int,
    Optional("type"): str,
    Optional("speed"): float,
    Optional("min_visits"): int,
    Optional("strict_start"): str,
    Optional("breaks", list): list
})

class Vehicle():
    """ Represents a vehicle used for the route
    """

    def __init__(self, params):
        try:
            valid_params = VEHICLE_SCHEMA.validate(params)
        except BaseException:
            raise RoutificParamsError("Invalid or incomplete parameters")

        self.start_lat = valid_params["start_location"]["lat"]
        self.start_lng = valid_params["start_location"]["lng"]
        self.start_name = valid_params["start_location"].get("name", "")
        self.end_lat = valid_params["end_location"].get("lat", None)
        self.end_lng = valid_params["end_location"].get("lng", None)
        self.end_name = valid_params["end_location"].get("name", "")
        self.shift_start = valid_params["shift_start"]
        self.shift_end = valid_params["shift_end"]
        self.capacity = params.get("capacity", None)
        self.type = params.get("type", None)
        self.speed = params.get("speed", None)
        self.min_visits = params.get("min_visits", None)
        self.strict_start = params.get("strict_start", None)
        self.breaks = params.get("strict_start", [])

    def __repr__(self) -> str:
        return f"<Vehicle: {self.start_name or 'unnamed'} to {self.end_name or 'unnamed'}>"

    def to_api(self) -> dict:
        ret = {
            "start_location": {
                "lat": self.start_lat,
                "lng": self.start_lng,
                "name": self.start_name
            },
            "shift_start": self.shift_start,
            "shift_end": self.shift_end,
            "capacity": self.capacity,
            "type": self.type,
            "speed": self.speed,
            "min_visits": self.min_visits,
            "strict_start": self.strict_start,
            "breaks": self.breaks,
        }

        if self.end_lat and self.end_lng:
            ret["end_location"] = {
                "lat": self.end_lat,
                "lng": self.end_lng,
                "name": self.end_name
            }

        return {k: v for k, v in ret.items() if v}
