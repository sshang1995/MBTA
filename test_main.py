import pytest
from httpx import AsyncClient
from main import app
import asyncio

base_url = 'http://127.0.0.1:8000'
@pytest.mark.asyncio
async def test_get_stops_pagnation():
    async with AsyncClient(base_url=base_url,timeout=30.0) as client:
        response = await client.get("/stops", params={"page": 1, "page_size": 10})
        assert response.status_code == 200
        data = response.json()
        assert data["page"] == 1
        assert data["page_size"] == 10
        assert len(data["stops"]) == 10

@pytest.mark.asyncio
async def test_get_stop_Boylston():
    async with AsyncClient(base_url=base_url,timeout=40.0) as client:
        response = await client.get("/stops/Boylston")
        assert response.status_code == 200
        data = response.json()
        for stop in data: 
            assert "boylston" == stop["stop_name"].lower()
            # assert stop["coordinates"]["latitude"] == 42.353214
            # assert stop["coordinates"]["longitude"] == -71.064545
            for line in stop["lines"]:
                assert line["line_name"] == 'Green Line B' or line["line_name"] == 'Green Line C' \
                or line["line_name"] == 'Green Line D'  or line["line_name"] == 'Green Line E'

            for adjacent_stop in stop["adjacent_stops"]:
                assert adjacent_stop["stop_name"] == 'Arlington' or adjacent_stop["stop_name"] == 'Park Street'

@pytest.mark.asyncio
async def test_get_stop_Wollaston():
    async with AsyncClient(base_url=base_url,timeout=40.0) as client:
        response = await client.get("/stops/Wood Island")
        assert response.status_code == 200
        data = response.json()
        for stop in data: 
            assert "wood island" == stop["stop_name"].lower()
            # assert stop["coordinates"]["latitude"] == 42.353214
            # assert stop["coordinates"]["longitude"] == -71.064545
            for line in stop["lines"]:
                assert line["line_id"] == 'line-Blue'

            for adjacent_stop in stop["adjacent_stops"]:
                assert adjacent_stop["stop_name"] == 'Airport' or adjacent_stop["stop_name"] == 'Orient Heights' 

# if __name__ == "__main__":
#     asyncio.run(test_get_stop_Boylston())