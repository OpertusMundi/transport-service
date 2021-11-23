import os
from transport_service import create_app

# Setup/Teardown

app = create_app()

def setup_module():
    print(" == Setting up tests for %s"  % (__name__))
    app.config['TESTING'] = True
    pass

def teardown_module():
    print(" == Tearing down tests for %s"  % (__name__))
    pass

# Tests

json_input = {
    "shape": [
        {"lat":37.983841,"lon":23.735741,"type":"break"},
        {"lat":37.983704,"lon":23.735298,"type":"via"},
        {"lat":37.983578,"lon":23.734848,"type":"via"},
        {"lat":37.983551,"lon":23.734253,"type":"break"},
        {"lat":37.983555,"lon":23.734116,"type":"via"},
        {"lat":37.983589,"lon":23.733315,"type":"via"},
        {"lat":37.983719,"lon":23.732445,"type":"via"},
        {"lat":37.983818,"lon":23.731712,"type":"via"},
        {"lat":37.983776,"lon":23.731506,"type":"via"},
        {"lat":37.983696,"lon":23.731369,"type":"break"}
    ],
    "costing": "bicycle"
}

routes_input = {
    "locations": [
        {"lat":40.271946,"lon":22.502501,"city":"Katerini"},
        {"lat":37.950001,"lon":23.850000,"city":"Paiania"}
    ],
    "toll_booth_penalty": 100,
    "language": "el-GR",
    "units": "miles",
    "use_tolls": 0,
    "date_time": {
        "type": 1,
        "value": "2021-11-23T00:19"
    }
}

def test_get_documentation_1():
    """Functional - Get documentation"""
    with app.test_client() as client:
        res = client.get('/', query_string=dict(), headers=dict())
        assert res.status_code == 200
        r = res.get_json()
        assert r.get('openapi') is not None
        assert r.get('paths') is not None
        paths = ['/isoline/isodistance', '/isoline/isochrone', '/map_matching/trace_route', '/map_matching/trace_attributes', '/route/auto', '/route/taxi', '/route/bus', '/route/truck', '/route/bicycle', '/route/bikeshare', '/route/motor_scooter', '/route/motorcycle', '/route/pedestrian', '/route/transit']
        for path in paths:
            assert r['paths'].get(path) is not None

def test_health_1():
    """Functional - Check health"""
    with app.test_client() as client:
        res = client.get('/health', query_string=dict(), headers=dict())
        assert res.status_code == 200
        r = res.get_json()
        assert r.get('status') == 'OK'

def test_isodistance_1():
    """Functional - Test isodistance"""
    query_string = {"lat": 37.96874466, "lon": 23.71061085, "range-0": 5, "color-0": "ff0000", "range-1": 10, "color-1": "00ff00", "polygons": "true", "costing": "pedestrian"}
    with app.test_client() as client:
        res = client.get('/isoline/isodistance', query_string=query_string, headers=dict())
        assert res.status_code == 200
        r = res.get_json()
        assert r['type'] == 'FeatureCollection'
        assert len(r['features']) == 2
        assert r['features'][0]['properties']['metric'] == 'distance'
        assert r['features'][0]['geometry']['type'] == 'Polygon'

def test_isochrone_1():
    """Functional - Test isochrone"""
    query_string = {"lat": 37.96874466, "lon": 23.71061085, "range-0": 15, "color-0": "ff0000", "range-1": 30, "color-1": "00ff00", "costing": "pedestrian"}
    with app.test_client() as client:
        res = client.get('/isoline/isochrone', query_string=query_string, headers=dict())
        assert res.status_code == 200
        r = res.get_json()
        assert r['type'] == 'FeatureCollection'
        assert len(r['features']) == 2
        assert r['features'][0]['properties']['metric'] == 'time'
        assert r['features'][0]['geometry']['type'] == 'LineString'

def test_mapmatching_1():
    """Functional - Test traceRoute map matching with json input"""
    with app.test_client() as client:
        res = client.post('/map_matching/trace_route', json=json_input, content_type='application/json')
        assert res.status_code == 200
        r = res.get_json()
        assert r.get('trip') is not None
        assert r['trip'].get('locations') is not None
        assert r['trip'].get('legs') is not None
        assert r['trip']['legs'][0].get('maneuvers') is not None
        assert r['trip']['legs'][0]['maneuvers'][0].get('travel_mode') is not None
        assert r['trip']['legs'][0]['maneuvers'][0]['travel_mode'] == 'bicycle'
        assert r['trip'].get('summary') is not None
        assert r['trip'].get('status') is not None
        assert r['trip']['status'] == 0

def test_mapmatching_2():
    """Functional - Test traceRoute map matching with file input"""
    dirname = os.path.dirname(__file__)
    csv_file = os.path.join(dirname, '..', 'test_data', 'shape.csv')
    data = {
        "shape": (open(csv_file, 'rb'), 'shape.csv'),
        "costing": "bicycle"
    }
    with app.test_client() as client:
        res = client.post('/map_matching/trace_route', data=data, content_type='multipart/form-data')
        assert res.status_code == 200
        r = res.get_json()
        assert r.get('trip') is not None
        assert r['trip'].get('locations') is not None
        assert r['trip'].get('legs') is not None
        assert r['trip']['legs'][0].get('maneuvers') is not None
        assert r['trip']['legs'][0]['maneuvers'][0].get('travel_mode') is not None
        assert r['trip']['legs'][0]['maneuvers'][0]['travel_mode'] == 'bicycle'
        assert r['trip'].get('summary') is not None
        assert r['trip'].get('status') is not None
        assert r['trip']['status'] == 0

def test_mapmatching_3():
    """Funcional - Test traceAttributes map matching with json input"""
    with app.test_client() as client:
        res = client.post('/map_matching/trace_attributes', json=json_input, content_type='application/json')
        assert res.status_code == 200
        r = res.get_json()
        assert r.get('matched_points') is not None
        assert r.get('edges') is not None
        assert r.get('admins') is not None
        assert r.get('raw_score') is not None
        assert r.get('shape') is not None
        assert r.get('confidence_score') is not None
        assert r.get('osm_changeset') is not None

def test_mapmatching_4():
    """Functional - Test traceAttributes map matching with file input"""
    dirname = os.path.dirname(__file__)
    csv_file = os.path.join(dirname, '..', 'test_data', 'shape.csv')
    data = {
        "shape": (open(csv_file, 'rb'), 'shape.csv'),
        "costing": "pedestrian"
    }
    with app.test_client() as client:
        res = client.post('/map_matching/trace_attributes', data=data, content_type='multipart/form-data')
        assert res.status_code == 200
        r = res.get_json()
        assert r.get('matched_points') is not None
        assert r.get('edges') is not None
        assert r.get('admins') is not None
        assert r.get('raw_score') is not None
        assert r.get('shape') is not None
        assert r.get('confidence_score') is not None
        assert r.get('osm_changeset') is not None

def test_routes_1():
    """Functional - Test routes"""
    with app.test_client() as client:
        res = client.post('/route/auto', json=routes_input, content_type='application/json')
        assert res.status_code == 200
        r = res.get_json()
        assert r.get('trip') is not None
        assert r['trip'].get('locations') is not None
        assert r['trip'].get('legs') is not None
        assert r['trip']['legs'][0].get('maneuvers') is not None
        assert r['trip']['legs'][0]['maneuvers'][0].get('travel_mode') is not None
        assert r['trip']['legs'][0]['maneuvers'][0]['travel_mode'] == 'drive'
        assert r['trip']['legs'][0]['maneuvers'][0]['travel_type'] == 'car'
        assert r['trip'].get('summary') is not None
        assert r['trip'].get('status') is not None
        assert r['trip']['status'] == 0
