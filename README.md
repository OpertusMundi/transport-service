# Transport-Service

## Description

*Transport service* is a wrapper on services around the OSM (or OSM-like) network. It supports:

- **isodistance** and **isochrone** operations, which compute areas that are reachable within specified distance or time intervals from a location, and return the reachable regions as contours of polygons or lines that can be displayed on a map,
- **map-matching**, which turns a path into a route with narrative instructions or retrieves the attribute values from that matched line,
- **routing**, which returns detailed navigation and trip information,
- **geocoding** and **reverse geocoding** (work in progress).

## Installation

### Dependencies

* Python 3.8
* Running Valhalla service

### Install package
```
Install service with pip:
```
pip install git+https://github.com/OpertusMundi/transport-service.git
```
Install separately the Python required packages:
```
pip install -r requirements.txt -r requirements-production.txt
```
### Set environment

The following environment variables should be set:
* `FLASK_ENV`<sup>*</sup>: `development` or `production`.
* `FLASK_APP`<sup>*</sup>: `transport_service` (if running as a container, this will be always set).
* `SECRET_KEY`<sup>*</sup>: The application secret key.
* `CORS`: List or string of allowed origins (*default*: '*').
* `LOGGING_CONFIG_FILE`<sup>*</sup>: The logging configuration file.
* `VALHALLA_URL`<sup>*</sup>: Valhalla service endpoint.

<sup>*</sup> Required.

## Usage

For details about using the service API, you can browse the full [OpenAPI documentation](https://opertusmundi.github.io/transport-service/).

## Build and run as a container

Copy `.env.example` to `.env` and configure (e.g `FLASK_ENV` variable).

Copy `compose.yml.example` to `compose.yml` (or `docker-compose.yml`) and adjust to your needs (e.g. specify volume source locations etc.).

Build:

    docker-compose -f compose.yml build

Prepare the following files/directories:

   * `./secrets/secret_key`: file needed (by Flask) for signing/encrypting session data.
   * `./logs`: a directory to keep logs.

Start application:

    docker-compose -f compose.yml up


## Run tests

Copy `compose-testing.yml.example` to `compose-testing.yml` and adjust to your needs. This is a just a docker-compose recipe for setting up the testing container.

Run nosetests (in an ephemeral container):

    docker-compose -f compose-testing.yml run --rm --user "$(id -u):$(id -g)" nosetests -v
