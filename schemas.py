from typing import List
from pydantic import BaseModel
class Line(BaseModel):
    route_id: str
    line_id: str
    line_name: str
    type: int

class Coordinates(BaseModel):
    latitude: float
    longitude: float

class AdjacentStop(BaseModel):
    stop_id: str
    stop_name: str

class Stop(BaseModel): 
    stop_id: str
    stop_name: str
    coordinates: Coordinates
    lines: List[Line]
    adjacent_stops: List[AdjacentStop] 


class StopPagnation(BaseModel): 
    page: int
    page_size: int
    total_stops: int
    total_pages: int
    stops: List[Stop]

