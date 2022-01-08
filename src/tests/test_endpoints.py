import os
from .context import endpoints
from fastapi.testclient import TestClient

client = TestClient(endpoints.app)

# def test_get_root():
#     response = client.get("/")
#     assert response.status_code == 200
#     assert response.json() == ["Hello world!"]


# def test_get_closest_asteroid():
#     response = client.get("/show-closest-asteroid")
#     assert response.status_code == 200
#     assert response.json()
