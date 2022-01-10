from fastapi.testclient import TestClient

from .context import endpoints
from .context import globals_vars

client = TestClient(endpoints.app)


def test_get_root():
    # given
    route = "/"

    # when
    response = client.get(route)

    # then
    assert response.status_code == 200
    assert response.json() == globals_vars.root_msg


def test_get_closest_asteroid():
    # given
    route = "/show-closest-asteroid"

    # when
    response = client.get(route)

    # then
    assert response.status_code == 200
    assert response.json()


def test_get_largest_asteroid():
    # given
    route = "/show-largest-asteroid?year=2022"

    # when
    response = client.get(route)

    # then
    assert response.status_code == 200
    assert response.json()
