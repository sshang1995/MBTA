from fastapi import FastAPI, Query, HTTPException, status
import requests
import os
from dotenv import load_dotenv
import asyncio
import json
import logging 
from schemas import StopPagnation, Stop, Line, AdjacentStop
from typing import List

app = FastAPI()
load_dotenv()
# get API key from .env file
API_Key = os.getenv("MBTA_KEY")
# print(f"print API key:{API_Key}")
if not API_Key:
    raise ValueError("MBTA_KEY environment variable not set")

# Load configuration from config.json
with open("config.json", "r") as file:
    config = json.load(file)
base_url = config["base_url"]

# Set up logging
logging.basicConfig(
    filename='app.log',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


@app.get("/stops", status_code=status.HTTP_200_OK,response_model=StopPagnation)
async def get_stops(page: int = Query(default=1, ge=1), page_size: int = Query(default=10, ge=1, le=100)):
    # Light Rail: represent by route_type 0 
    # Subway (heavy rail): represent by route_type 1
    try:
        url = base_url + config["stops"] 
        response = requests.get(url, headers={"x-api-key": API_Key})
        
        if response.status_code != 200:
            logging.error(f"Failed to fetch stops: {response.status_code} - {response.text}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to fetch stops")

        json_response = response.json()
        all_stops = json_response.get('data', [])
        total_stops = len(all_stops)
        # 265 total stops

        # Pagination logic
        start_index = (page - 1) * page_size
        end_index = start_index + page_size
        if start_index >= total_stops:
            logging.warning(f"Page number {page} * Page size {page_size} out of range. Total stops: {total_stops}")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Page number out of range")
    
        if end_index > total_stops:
            end_index = total_stops
        paginated_stops = all_stops[start_index:end_index]
        stops = await helper_create_stops_response(paginated_stops)
        logging.info(f"Fetched {len(stops)} stops for page {page} with page size {page_size}")

        return {"page": page,
                "page_size": page_size,
                "total_stops": total_stops,
                "total_pages": (total_stops + page_size - 1) // page_size,  # Calculate total pages
                "stops": stops}
            
  
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stops/{stop_name}", status_code=status.HTTP_200_OK,response_model=List[Stop])
async def get_stops_by_name(stop_name:str):
    try:
        url = base_url + config["stops"]
        response = requests.get(url, headers={"x-api-key": API_Key})
        
        if response.status_code != 200:
            logging.error(f"Failed to fetch stops: {response.status_code} - {response.text}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to fetch stops")

        json_response = response.json()
        all_stops = json_response.get('data', [])

        target_stops = []
        for stop in all_stops:
            if stop_name.lower().replace(" ", "") == stop['attributes']['name'].lower().replace(" ", "").replace("/", ""):
                target_stops.append(stop)
        
        stops = await helper_create_stops_response(target_stops)
        logging.info(f"Fetched stop for {stop_name}")
        return stops
             
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def helper_create_stops_response(raw_stops):
    stops = []
    for stop in raw_stops:
        adjacent_stops_for_target_stop = []
        line_response = await get_lines(stop['id'])

        for line in line_response:  
            trips_response = await get_trips(line["route_id"])
        
            for tripid in trips_response.get('tripids', []):
                adjacent_stops_response = await get_adjacent_stops(tripid, stop['id'])
                adjacent_stops_for_target_stop.extend(adjacent_stops_response)   

        # Remove duplicates from adjacent_stops_for_target_stop
        seen = set() 
        unqiue_stops = []
        for adj_stop in adjacent_stops_for_target_stop:
            identifier = tuple(sorted(adj_stop.items()))
            if identifier not in seen:
                seen.add(identifier)
                unqiue_stops.append(adj_stop)


        new_obj  = {
            "stop_id": stop['id'],
            "stop_name": stop['attributes']['name'],
            "coordinates":{
                "latitude": stop['attributes']['latitude'],
                "longitude": stop['attributes']['longitude']
            },
            "lines": line_response,
            "adjacent_stops": unqiue_stops
        }
        stops.append(new_obj)
    return stops


@app.get("/lines/{stop_id}", status_code=status.HTTP_200_OK, response_model=List[Line])
async def get_lines(stop_id:int): 
    url = base_url + config["routes"].format(stop_id)
    response = requests.get(url, headers={"x-api-key": API_Key})
    if response.status_code != 200:
        logging.error(f"Failed to fetch routes for stop {stop_id}: {response.status_code} - {response.text}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to fetch lines")

    json_response = response.json()
    lines = []
    for line in json_response.get('data', []):
        new_response = {
            "route_id": line['id'],
            "line_id": line['relationships']['line']['data']['id'],
            "line_name": line['attributes']['long_name'],
            "type": line['attributes']['type']
        }
        lines.append(new_response)
    return lines
    

@app.get("/route-patterns/{route_id}", status_code=status.HTTP_200_OK)
async def get_trips(route_id: str):
    url = base_url + config["trips"].format(route_id)
    response = requests.get(url, headers={"x-api-key": API_Key})
    if response.status_code != 200:
        logging.error(f"Failed to fetch trips for route {route_id}: {response.status_code} - {response.text}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to fetch trips")

    json_response = response.json()
    tripids = []
    for pattern in json_response.get('data', []):
        tripid = pattern["relationships"]["representative_trip"]["data"]["id"]
        tripids.append(tripid)
    return {"tripids": tripids}
    
@app.get("/adjacent-stops/{trip_id}/{target_stop_id}", status_code=status.HTTP_200_OK, response_model=List[AdjacentStop])
async def get_adjacent_stops(trip_id: str, target_stop_id: str):
    url = base_url + config["schedules"].format(trip_id)
    response = requests.get(url, headers={"x-api-key": API_Key})
    
    if response.status_code != 200:
        logging.error(f"Failed to fetch schedules for trip {trip_id}: {response.status_code} - {response.text}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to fetch adjacent stops")

    json_response = response.json()
    adjacent_stops = []
    schedules = json_response.get('data', [])
    stops = json_response.get('included', [])
    for i in range(len(schedules)):
        if schedules[i]["relationships"]["stop"]["data"]["id"] == target_stop_id: 
            if i > 0:
                prev_stop_id = schedules[i-1]["relationships"]["stop"]["data"]["id"]
                prev_stop = next((x['attributes']["name"] for x in stops if x["id"] == prev_stop_id), None)
                adjacent_stops.append({"stop_id": prev_stop_id, "stop_name": prev_stop}) 
            if i < len(schedules) - 1:
                next_stop_id = schedules[i+1]["relationships"]["stop"]["data"]["id"]
                next_stop = next((x['attributes']["name"] for x in stops if x["id"] == next_stop_id), None)
                adjacent_stops.append({"stop_id": next_stop_id, "stop_name": next_stop}) 

    return adjacent_stops


if __name__ == "__main__":
    asyncio.run(get_stops(1, 1))