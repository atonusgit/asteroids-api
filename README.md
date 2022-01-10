# Asteroids API

Deliver asteroid info from Nasa API

## Demo

See [5.22.220.90:8000](http://5.22.220.90:8000)

## Requests

Find all available requests at [5.22.220.90:8000/redoc](http://5.22.220.90:8000/redoc)

### Show closest asteroid

Asteroid API uses fixed dates 19.12.2015 and 26.12.2015 and returns the details of the closest asteroid within that time period.

### Show largest asteroid

Asteroid API uses user provided year to fetch all asteroid data within that year. Requests are made within Nasa's API limits: max range 7 days for each request and max 10 concurrent requests. Asteroid API returns the details of the largest one.

## Cache

Cache has two parts - dictionary variable and cache.json file. The cache.json, if available, is loaded to dictionary at start. Handling cache dictionary is done with public function ***nasa_api.call_via_cache()***

- See cache at ***/show-cache***
- Reset cache with ***/reset-cache***
- Remove cache.json file with ***/reset-cache?purge=1***

## Environment

Demo runs on docker, and within a python virtual environment. .env file holds the Nasa API key.

## Tests

Automated tests are run at two stages:
1. unit tests when building docker image
1. end-to-end tests after demo site is deployed

## Deployment

Demo site is deployed using ansible with

```sh
ansible-playbook -i staging deploy.yaml
```

## Local installation (Linux)

Get your free Nasa API key from [api.nasa.gov](https://api.nasa.gov).

```sh
SECRET=<YOUR NASA API KEY>
INSTALL="$HOME/.tmp"

mkdir $INSTALL
cd $INSTALL
git clone git@github.com:atonusgit/asteroids-api.git
cd asteroids-api
sudo apt install docker
sudo docker build . -t asteroids_api
sudo docker run -p 8000:80 -e NASA_API_KEY=$SECRET asteroids_api
```

All set. Now you're ready to visit [localhost:8000](http://localhost:8000)

For Windows and Mac users, install Docker via [Get Docker](https://docs.docker.com/get-docker/)