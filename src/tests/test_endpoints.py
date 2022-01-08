from .context import endpoints
from fastapi.testclient import TestClient

client = TestClient(endpoints.app)


def test_get_root():
    # given
    route = "/"

    # when
    response = client.get(route)

    # then
    assert response.status_code == 200
    assert response.json() == ["Hello world!"]


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
    route = "/show-largest-asteroid"

    # when
    response = client.get(route)

    # then
    assert response.status_code == 200
    assert response.json()
