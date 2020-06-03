from schema import Schema, Optional, SchemaError
from exceptions import RoutificParamsError

"""
    Defines and validates visits, which are locations that must be visited.
"""

VISIT_SCHEMA = Schema({
    "location": {
        "lat": float,
        "lng": float,
        Optional("name"): str
    },
    Optional("start", default="00:00"): str,
    Optional("end", default="23:59"): str,
    Optional("duration"): int,
    Optional("demand"): str,
    Optional("priority"): str,
    Optional("type"): str,
    Optional("time_windows", default=[]): list
})


class Visit():
    """ Represents a location that must be visited in the route
    """

    def __init__(self, params):
        try:
            valid_params = VISIT_SCHEMA.validate(params)
        except BaseException:
            raise RoutificParamsError("Invalid or incomplete parameters")

        self.lat = valid_params["location"]["lat"]
        self.lng = valid_params["location"]["lng"]
        self.name = valid_params["location"].get("name", None)
        self.start = valid_params["start"]
        self.end = valid_params["end"]
        self.duration = valid_params.get("duration", None)
        self.demand = valid_params.get("demand", None)
        self.priority = valid_params.get("priority", None)
        self.type = valid_params.get("type", None)
        self.time_windows = valid_params.get("time_windows", None)

    def __repr__(self) -> str:
        if self.name:
            return f"<Visit: {self.name}>"
        else:
            return f"<Visit: {self.lat}, {self.lng}>"

    def to_api(self) -> dict:
        """ Returns a dict that can be sent to the Routific API
        """

        ret = {
            "location": {
                "lat": self.lat,
                "lng": self.lng,
                "name": self.name
            },
            "start": self.start,
            "end": self.end,
            "duration": self.duration,
            "demand": self.demand,
            "priority": self.priority,
            "type": self.type,
            "time_windows": self.time_windows
        }

        # Remove "None" as there is no purpose in sending them to API
        return {k: v for k, v in ret.items() if v}
