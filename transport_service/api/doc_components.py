def add_components(spec):
    """Adds the service components to OpenAPI specification.

    Arguments:
        spec (obj): The apispec object.
    """
    import copy

    # Parameters

    spec.components.parameter('lat', 'query', {
        "name": "lat",
        "description": "Latitude of the location in degrees.",
        "required": True,
        "schema": {
            "type": "number",
            "format": "float"
        },
        "example": 37.983841
    })

    spec.components.parameter('lon', 'query', {
        "name": "lon",
        "description": "Longitude of the location in degrees.",
        "required": True,
        "schema": {
            "type": "number",
            "format": "float"
        },
        "example": 23.735741
    })

    spec.components.parameter('costing', 'query', {
        "name": "costing",
        "description": "The costing model that will be used to calculate the route. For more details, see the [Valhalla documentation](https://valhalla.readthedocs.io/en/latest/api/turn-by-turn/api-reference/#costing-models).",
        "required": False,
        "schema": {
            "type": "string",
            "enum": ["auto", "bicycle", "pedestrian", "bikeshare", "bus", "multimodal"]
        },
        "default": "auto"
    })

    spec.components.parameter('rangeDistance', 'query', {
        "name": "range",
        "description": "A list of floating point values specifying the distance in kilometers for the contour.",
        "required": True,
        "schema": {
            "type": "object",
            "additionalProperties": {
                "type": "integer"
            },
            "example": {
                "range-0": 5,
                "range-1": 10,
                "range-2": 25,
                "range-3": 50,
            }
        },
        "style": "form",
        "explode": True
    })

    spec.components.parameter('rangeTime', 'query', {
        "name": "range",
        "description": "A list of floating point values specifying the time in minutes for the contour.",
        "required": True,
        "schema": {
            "type": "object",
            "additionalProperties": {
                "type": "integer"
            },
            "example": {
                "range-0": 15,
                "range-1": 30,
                "range-2": 45,
                "range-3": 60,
            }
        },
        "style": "form",
        "explode": True
    })

    spec.components.parameter('color', 'query', {
        "name": "color",
        "description": "A list of colors for the output of the contour. Specify it as a Hex value (but without the #). If no color is specified, a default color will be assigned to the output.",
        "schema": {
            "type": "object",
            "additionalProperties": {
                "type": "number",
                "format": "float"
            },
            "example": {
                "color-0": "61c250",
                "color-1": "bed600",
                "color-2": "47d5cd",
                "color-3": "cae3e9"
            }
        },
        "style": "form",
        "explode": True
    })

    spec.components.parameter('polygons', 'query', {
        "name": "polygons",
        "description": "A Boolean value to determine whether to return geojson polygons or linestrings as the contours.",
        "schema": {"type": "boolean"},
        "default": "false"
    })

    spec.components.parameter('denoise', 'query', {
        "name": "denoise",
        "description": "A floating point value from 0 to 1 (default of 1) which can be used to remove smaller contours. A value of 1 will only return the largest contour for a given time value. A value of 0.5 drops any contours that are less than half the area of the largest contour in the set of contours for that same time value.",
        "schema": {
            "type": "number",
            "format": "float"
        },
        "default": 1.0
    })

    # Schemata

    isochrone_geojson = {
        "type": "object",
        "description": "The isoline contours as GeoJSON.",
        "properties": {
            "type": {
                "type": "string",
                "example": "FeatureCollection"
            },
            "features": {
                "type": "array",
                "minItems": 0,
                "description": "Each feature represents a contour.",
                "items": {
                    "type": "object",
                    "properties": {
                        "type": {
                            "type": "string",
                            "example": "Feature"
                        },
                        "properties": {
                            "type": "object",
                            "description": "Mainly style properties.",
                            "properties": {
                                "fill": {
                                    "type": "string",
                                    "description": "Hex code color.",
                                    "example": "#ff0000",
                                },
                                "fillOpacity": {
                                    "type": "number",
                                    "format": "float",
                                    "description": "Opacity for the fill color (0-1).",
                                    "example": 0.33
                                },
                                "fill-opacity": {
                                    "type": "number",
                                    "format": "float",
                                    "description": "Opacity for the fill color (0-1).",
                                    "example": 0.33
                                },
                                "fillColor": {
                                    "type": "string",
                                    "description": "Hex code color.",
                                    "example": "#ff0000"
                                },
                                "color": {
                                    "type": "string",
                                    "description": "Hex code color.",
                                    "example": "#ff0000"
                                },
                                "contour": {
                                    "type": "integer",
                                    "description": "The corresponding contour (in km or minutes).",
                                    "example": 15
                                },
                                "opacity": {
                                    "type": "number",
                                    "format": "float",
                                    "description": "Opacity for the fill color (0-1).",
                                    "example": 0.33
                                },
                                "metric": {
                                    "type": "string",
                                    "description": "The metric used to compute the contours: *distance* or *time*.",
                                    "enum": ["distance", "time"]
                                }
                            }
                        },
                        "geometry": {
                            "type": "object",
                            "description": "The geometry of the contour.",
                            "properties": {
                                "type": {
                                    "type": "string",
                                    "description": "The geometry type.",
                                    "enum": ["LineString", "Polygon"],
                                    "example": "LineString"
                                },
                                "coordinates": {
                                    "oneOf": [
                                        {
                                            "type": "array",
                                            "minItems": 2,
                                            "items": {
                                                "type": "array",
                                                "minItems": 2,
                                                "maxItems": 2,
                                                "items": {
                                                    "type": "number",
                                                    "format": "float"
                                                }
                                            }
                                        },
                                        {
                                            "type": "array",
                                            "minItems": 1,
                                            "maxItems": 1,
                                            "items": {
                                                "type": "array",
                                                "minItems": 2,
                                                "items": {
                                                    "type": "array",
                                                    "minItems": 2,
                                                    "maxItems": 2,
                                                    "items": {
                                                        "type": "number",
                                                        "format": "float"
                                                    }
                                                }
                                            }
                                        }
                                    ],
                                    "example": [[23.735611, 38.002935], [23.734611, 38.003316], [23.734406, 38.002949]]
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    spec.components.schema('isochroneGeoJSON', isochrone_geojson)

    shape_json = {
        "type": "array",
        "description": "The shape, a sequence of point locations, that is going to be matched on the map.",
        "minItems": 2,
        "items": {
            "type": "object",
            "description": "Represents one point location.",
            "properties": {
                "lat": {
                    "type": "number",
                    "format": "float",
                    "description": "Latitude of the location in degrees.",
                    "example": 37.983841,
                    "required": True
                },
                "lon": {
                    "type": "number",
                    "format": "float",
                    "description": "Longitude of the location in degrees.",
                    "example": 23.735611,
                    "required": True
                },
                "time": {
                    "type": "integer",
                    "description": "(*Optional*) Time in seconds; it can be a UNIX epoch time or any increasing sequence.",
                    "example": 2,
                    "required": False
                }
            }
        }
    }

    shape_csv = {
        "type": "string",
        "format": "binary",
        "description": "The shape, a sequence of point locations, that is going to be matched on the map, in CSV file format. The CSV should contain 2 columns with the *latitude* and *longitude* of the locations (in degrees). A **time** component is also possible, indicating time in seconds and can be a UNIX epoch time or any increasing sequence. The first row should indicate the corresponding attributes with **lat** and **lon** (and optionally **time**).",
    }
    costing = {
        "type": "string",
        "description": "The costing model that will be used to calculate the route. For more details, see the [Valhalla documentation](https://valhalla.readthedocs.io/en/latest/api/turn-by-turn/api-reference/#costing-models).",
        "enum": ["auto", "auto_shorter", "bicycle", "bus", "pedestrian"],
        "default": "auto"
    }

    filters_enum = ["edge.names", "edge.length", "edge.speed", "edge.road_class", "edge.begin_heading", "edge.end_heading", "edge.begin_shape_index", "edge.end_shape_index", "edge.traversability", "edge.use", "edge.toll", "edge.unpaved", "edge.tunnel", "edge.bridge", "edge.roundabout", "edge.internal_intersection", "edge.drive_on_right", "edge.surface", "edge.sign.exit_number", "edge.sign.exit_branch", "edge.sign.exit_toward", "edge.sign.exit_name", "edge.travel_mode", "edge.vehicle_type", "edge.pedestrian_type", "edge.bicycle_type", "edge.transit_type", "edge.id", "edge.way_id", "edge.weighted_grade", "edge.max_upward_grade", "edge.max_downward_grade", "edge.mean_elevation", "edge.lane_count", "edge.cycle_lane", "edge.bicycle_network", "edge.sac_scale", "edge.shoulder", "edge.sidewalk", "edge.density", "edge.speed_limit", "edge.truck_speed", "edge.truck_route", "node.intersecting_edge.begin_heading", "node.intersecting_edge.from_edge_name_consistency", "node.intersecting_edge.to_edge_name_consistency", "node.intersecting_edge.driveability", "node.intersecting_edge.cyclability", "node.intersecting_edge.walkability", "node.intersecting_edge.use", "node.intersecting_edge.road_class", "node.intersecting_edge.lane_count", "node.elapsed_time", "node.admin_index", "node.type", "node.fork", "node.time_zone", "osm_changeset", "shape", "admin.country_code", "admin.country_text", "admin.state_code", "admin.state_text", "matched.point", "matched.type", "matched.edge_index", "matched.begin_route_discontinuity", "matched.end_route_discontinuity", "matched.distance_along_edge", "matched.distance_from_trace_point"]

    filters_array = {
        "type": "array",
        "description": "An array of filters; allows to filter the response. Depending on the **filter_action** value, these items will be excluded from the response (*exclude*) or the response will be limited to these items (*include*). If no filters are used, all attributes are enabled and returned in the response.",
        "items": {
            "type": "string",
            "description": "Attribute name to exclude or include.",
            "enum": filters_enum
        },
        "example": ["edge.names", "node.intersecting_edge.road_class", "matched.distance_from_trace_point"]
    }

    filters_string = {
        "type": "string",
        "description": "A comma separated list of filters (listed below); allows to filter the response. Depending on the **filter_action** value, these items will be excluded from the response (*exclude*) or the response will be limited to these items (*include*). If no filters are used, all attributes are enabled and returned in the response.\n- " + "\n- ".join(filters_enum),
        "items": {
            "type": "string",
            "description": "Attribute name to exclude or include.",
            "enum": filters_enum
        },
        "example": ["edge.names", "node.intersecting_edge.road_class", "matched.distance_from_trace_point"]
    }

    trace_attributes_form = {
        "type": "object",
        "properties": {
            "shape": shape_json,
            "costing": costing,
            "filters": filters_array,
            "filter_action": {
                "type": "string",
                "description": "Whether to *exclude* or *include* the given **filters**; it will be ignored if no filters are supplied.",
                "enum": ["exclude", "include"],
                "default": "exclude"
            }
        },
        "required": ["shape"]
    }
    spec.components.schema('traceAttributesForm', trace_attributes_form)
    spec.components.schema('traceAttributesFileForm', {
        **trace_attributes_form,
        "properties": {
            **trace_attributes_form["properties"],
            "shape": shape_csv,
            "filters": filters_string
        }
    })

    directions_options = {
            "units": {
                "type": "string",
                "description": "Distance units for output.",
                "default": "kilometers",
                "enum": ["kilometers", "miles"]
            },
            "language": {
                "type": "string",
                "description": "The language of the narration instructions based on the IETF BCP 47 language tag string.",
                "enum": ["bg-BG", "ca-ES", "cs-CZ", "da-DK", "de-DE", "el-GR", "en-GB", "en-US-x-pirate", "en-US", "es-ES", "et-EE", "fi-FI", "fr-FR", "hi-IN", "hu-HU", "it-IT", "ja-JP", "nb-NO", "nl-NL", "pl-PL", "pt-BR", "pt-PT", "ro-RO", "ru-RU", "sk-SK", "sl-SI", "sv-SE", "tr-TR", "uk-UA"],
                "default": "en-US"
            },
            "directions_type": {
                "type": "string",
                "description": "Determines the response level of information.\n- *none*: indicating no maneuvers or instructions should be returned.\n- *maneuvers*: indicating that only maneuvers be returned.\n- *instructions*: indicating that maneuvers with instructions should be returned.",
                "enum": ["none", "maneuvers", "instructions"],
                "default": "instructions"
            }
    }

    trace_route_form = {
        "type": "object",
        "properties": {
            "shape": {
                **shape_json,
                "items": {
                    **shape_json["items"],
                    "properties": {
                        **shape_json["items"]["properties"],
                        "type": {
                            "type": "string",
                            "description": "(*Optional*) *break* values will split the route response into multiple legs. The first and last locations should always have type *break*.",
                            "enum": ["break", "via"],
                            "required": False
                        }
                    }
                }
            },
            "costing": costing,
            "search_radius": {
                "type": "integer",
                "description": "Search radius in meters associated with supplied trace points."
            },
            "interpolation_distance": {
                "type": "integer",
                "description": "Interpolation distance in meters beyond which trace points are merged together."
            },
            "gps_accuracy": {
                "type": "integer",
                "description": "GPS accuracy in meters associated with supplied trace points."
            },
            "breakage_distance": {
                "type": "integer",
                "description": "Breaking distance in meters between trace points."
            },
            **directions_options
        },
        "required": ["shape"]
    }
    spec.components.schema('traceRouteForm', trace_route_form)
    spec.components.schema('traceRouteFileForm', {
        **trace_route_form,
        "properties": {
            **trace_route_form["properties"],
            "shape": {
                **shape_csv,
                "description": shape_csv["description"] + " Optionally, an additional column representing the **type** of each location could be present. Possible values are *break* and *via*. The former (*break*) will split the route response into multiple legs. The first and last locations should always have type *break*."
            }
        }
    })

    road_class_enum = ["motorway", "trunk", "primary", "secondary", "tertiary", "unclassified", "residential", "service_other"]
    locations = {
        "type": "array",
        "description": "Location information.",
        "items": {
            "type": "object",
            "description": "Except of the listed properties, the following can be included in each location **only for convenience**, since they do not impact the routing: *name*, *city*, *state*, *postal_code*, *country*, *phone*, and *url*. This information is carried through the request and returned in the response.",
            "properties": {
                "lat": {
                    "type": "number",
                    "format": "float",
                    "description": "Latitude of the location in degrees.",
                    "example": 37.983841
                },
                "lon": {
                    "type": "number",
                    "format": "float",
                    "description": "Longitude of the location in degrees.",
                    "example": 23.735741
                },
                "type": {
                    "type": "string",
                    "description": "Type of location, either *break*, *through*, *via* or *break_through*. Each type controls two characteristics: whether or not to allow a u-turn at the location and whether or not to generate guidance/legs at the location.\n||U-turns|legs<br/>arrival/departure maneuvers|\n|---|---|---|\n|*break*|???|???|\n|*through*|???|???|\n|*via*|???|???|\n|*break_through*|???|???|\nThe types of the first and last locations are ignored and are treated as *break*s.",
                    "default": "break",
                    "enum": ["break", "through", "via", "break_through"]
                },
                "heading": {
                    "type": "integer",
                    "description": "Preferred direction of travel for the start from the location. This can be useful for mobile routing where a vehicle is traveling in a specific direction along a road, and the route should start in that direction. The heading is indicated in degrees from north in a clockwise direction, where north is 0??, east is 90??, south is 180??, and west is 270??.",
                    "example": 90,
                    "minimum": 0,
                    "maximum": 360
                },
                "heading_tolerance": {
                    "type": "integer",
                    "description": "How close in degrees a given street's angle must be in order for it to be considered as in the same direction of the heading parameter.",
                    "default": 60,
                    "minimum": 0
                },
                "minimum_reachability": {
                    "type": "integer",
                    "description": "Minimum number of nodes (intersections) reachable for a given edge (road between intersections) to consider that edge as belonging to a connected region. When correlating this location to the route network, try to find candidates who are reachable from this many or more nodes (intersections). If a given candidate edge reaches less than this number of nodes its considered to be a disconnected island and we'll search for more candidates until we find at least one that isn't considered a disconnected island. If this value is larger than the configured service limit it will be clamped to that limit.",
                    "default": 50
                },
                "radius": {
                    "type": "integer",
                    "description": "The number of meters about this input location within which edges (roads between intersections) will be considered as candidates for said location. When correlating this location to the route network, try to only return results within this distance (meters) from this location. If there are no candidates within this distance it will return the closest candidate within reason. If this value is larger than the configured service limit it will be clamped to that limit.",
                    "default": 0
                },
                "rank_candidates": {
                    "type": "boolean",
                    "description": "Whether or not to rank the edge candidates for this location. The ranking is used as a penalty within the routing algorithm so that some edges will be penalized more heavily than others. If *true* candidates will be ranked according to their distance from the input and various other attributes. If *false* the candidates will all be treated as equal which should lead to routes that are just the most optimal path with emphasis about which edges were selected.",
                    "default": "false"
                },
                "side": {
                    "type": "object",
                    "description": "Collection of parameters related to the side of street decision.",
                    "properties": {
                        "preferred_side": {
                            "type": "string",
                            "description": "If the location is not offset from the road centerline or is closest to an intersection this option has no effect. Otherwise the determined side of street is used to determine whether or not the location should be visited from the *same*, *opposite* or *either* side of the road with respect to the side of the road the given locale drives on. In Germany (driving on the right side of the road), passing a value of *same* will only allow you to leave from or arrive at a location such that the location will be on your right. In Australia (driving on the left side of the road), passing a value of same will force the location to be on your left. A value of *opposite* will enforce arriving/departing from a location on the opposite side of the road from that which you would be driving on while a value of *either* will make no attempt limit the side of street that is available for the route.",
                            "default": "either",
                            "enum": ["same", "opposite", "either"]
                        },
                        "display_lat": {
                            "type": "number",
                            "format": "float",
                            "description": "Latitude of the map location in degrees. If provided the *lat* and *lon* parameters will be treated as the routing location and the *display_lat* and *display_lon* will be used to determine the side of street. Both *display_lat* and *display_lon* must be provided and valid to achieve the desired effect."
                        },
                        "display_lon": {
                            "type": "number",
                            "format": "float",
                            "description": "Longitude of the map location in degrees. If provided the *lat* and *lon* parameters will be treated as the routing location and the *display_lat* and *display_lon* will be used to determine the side of street. Both *display_lat* and *display_lon* must be provided and valid to achieve the desired effect."
                        },
                        "node_snap_tolerance": {
                            "type": "integer",
                            "description": "During edge correlation this is the tolerance (*in meters*) used to determine whether or not to snap to the intersection rather than along the street, if the snap location is within this distance from the intersection the intersection is used instead.",
                            "default": 5
                        },
                        "street_side_tolerance": {
                            "type": "integer",
                            "description": "If your input coordinate is less than this tolerance (*in meters*) away from the edge centerline then we set your side of street to none otherwise your side of street will be left or right depending on direction of travel",
                            "default": 5
                        },
                        "street_side_max_distance": {
                            "type": "integer",
                            "description": "The maximum distance (*in meters*) away from the edge centerline the input coordinates can be so that they will be used for determining the side of street. Beyond this distance the side of street is set to none."
                        },
                    }
                },
                "search_filter": {
                    "type": "object",
                    "description": "A set of optional filters to exclude candidate edges based on their attribution.",
                    "properties": {
                        "exclude_tunnel": {
                            "type": "boolean",
                            "description": "Whether to exclude roads marked as tunnels.",
                            "default": "false"
                        },
                        "exclude_bridge" : {
                            "type": "boolean",
                            "description": "Whether to exclude roads marked as bridges.",
                            "default": "false"
                        },
                        "exclude_closures": {
                            "type": "boolean",
                            "description": "Whether to exclude roads considered closed due to live traffic closure.\n\n*Note*: This option cannot be set if costing_options.<costing>.ignore_closures is also specified. An error is returned if both options are specified.",
                            "default": "true"
                        },
                        "min_road_class": {
                            "type": "string",
                            "description": "Lowest road class allowed.",
                            "default": "service_other",
                            "enum": road_class_enum
                        },
                        "max_road_class": {
                            "type": "string",
                            "description": "Highest road class allowed.",
                            "default": "motorway",
                            "enum": road_class_enum
                        }
                    }
                }
            }
        }
    }

    generic_options = {
        "maneuver_penalty": {
            "type": "integer",
            "description": "A penalty (*in seconds*) applied when transitioning between roads that do not have consistent naming - in other words, no road names in common. This penalty can be used to create simpler routes that tend to have fewer maneuvers or narrative guidance instructions.",
            "default": 5,
            "minimum": 0
        },
        "gate_cost": {
            "type": "integer",
            "description": "A cost (*in seconds*) applied when a gate with undefined or private access is encountered. This cost is added to the estimated time / elapsed time.",
            "default": 30,
            "minimum": 0
        },
        "gate_penalty": {
            "type": "integer",
            "description": "A penalty (*in seconds*) applied when a gate with no access information is on the road.",
            "default": 300,
            "minimum": 0
        },
        "country_crossing_cost": {
            "type": "integer",
            "description": "A cost (*in seconds) applied when encountering an international border. This cost is added to the estimated and elapsed times. ",
            "default": 600,
            "minimum": 0
        },
        "country_costing_penalty": {
            "type": "integer",
            "description": "A penalty (*in seconds) applied for a country crossing. This penalty can be used to create paths that avoid spanning country boundaries.",
            "default": 0,
            "minimum": 0
        },
        "service_penalty": {
            "type": "integer",
            "description": "A penalty (*in seconds*) applied for transition to generic service road.",
            "default": 15,
            "minimum": 0
        }
    }

    automobile_options = {
        "use_ferry": {
            "type": "number",
            "format": "float",
            "description": "This value indicates the willingness to take ferries. This is a range of values between 0 and 1. Values near 0 attempt to avoid ferries and values near 1 will favor ferries. Note that sometimes ferries are required to complete a route so values of 0 are not guaranteed to avoid ferries entirely.",
            "default": 0.5,
            "minimum": 0.0,
            "maximum": 1.0
        },
        "use_tolls": {
            "type": "number",
            "format": "float",
            "description": "This value indicates the willingness to take roads with tolls. This is a range of values between 0 and 1. Values near 0 attempt to avoid tolls and values near 1 will not attempt to avoid them. Note that sometimes roads with tolls are required to complete a route so values of 0 are not guaranteed to avoid them entirely.",
            "default": 0.5,
            "minimum": 0.0,
            "maximum": 1.0
        },
        "use_living_streets": {
            "type": "number",
            "format": "float",
            "description": "This value indicates the willingness to take living streets. This is a range of values between 0 and 1. Values near 0 attempt to avoid living streets and values near 1 will favor living streets. Note that sometimes living streets are required to complete a route so values of 0 are not guaranteed to avoid living streets entirely.",
            "default": 0.1,
            "minimum": 0.0,
            "maximum": 1.0
        },
        "use_tracks": {
            "type": "number",
            "format": "float",
            "description": "This value indicates the willingness to take track roads. This is a range of values between 0 and 1. Values near 0 attempt to avoid tracks and values near 1 will favor tracks a little bit. Note that sometimes tracks are required to complete a route so values of 0 are not guaranteed to avoid tracks entirely.",
            "default": 0.0,
            "minimum": 0.0,
            "maximum": 1.0
        },
        **generic_options,
        "private_access_penalty": {
            "type": "integer",
            "description": "A penalty (* in seconds*) applied when a gate or bollard with access=private is encountered.",
            "default": 450,
            "minimum": 0
        },
        "toll_booth_cost": {
            "type": "integer",
            "description": "A cost (* in seconds*) applied when a toll booth is encountered. This cost is added to the estimated and elapsed times.",
            "default": 15,
            "minimum": 0
        },
        "toll_booth_penalty": {
            "type": "integer",
            "description": "A penalty (* in seconds*) applied to the cost when a toll booth is encountered. This penalty can be used to create paths that avoid toll roads.",
            "default": 0,
            "minimum": 0
        },
        "ferry_cost": {
            "type": "integer",
            "description": "A cost (* in seconds*) applied when entering a ferry. This cost is added to the estimated and elapsed times.",
            "default": 300,
            "minimum": 0
        },
        "service_factor": {
            "type": "integer",
            "description": "A factor that modifies (multiplies) the cost when generic service roads are encountered.",
            "default": 1,
            "minimum": 0
        },
        "shortest": {
            "type": "boolean",
            "description": "Changes the metric to quasi-shortest, i.e. purely distance-based costing. Note, this will disable all other costings & penalties. Also note, shortest will not disable hierarchy pruning, leading to potentially sub-optimal routes for some costing models.",
            "default": "false"
        },
        "top_speed": {
            "type": "integer",
            "description": "Top speed (*in km/h*) the vehicle can go. Used to avoid roads with higher speeds than this value.",
            "default": 140,
            "minimum": 10,
            "maximum": 252
        },
        "ignore_closures": {
            "type": "boolean",
            "description": "If set to true, ignores all closures, marked due to live traffic closures, during routing. Note: This option cannot be set if *location.search_filter.exclude_closures* is also specified in the request and will return an error.",
            "default": "false"
        },
        "closure_factor": {
            "type": "number",
            "format": "float",
            "description": "A factor that penalizes the cost when traversing a closed edge (eg: if search_filter.exclude_closures is false for origin and/or destination location and the route starts/ends on closed edges). Its value can range from 1.0 - don't penalize closed edges, to 10.0 - apply high cost penalty to closed edges.",
            "default": 9.0,
            "minimum": 1.0,
            "maximum": 10.0
        }
    }

    vehicle_options = {
        **automobile_options,
        "height": {
            "type": "number",
            "format": "float",
            "description": "The height of the vehicle (*in meters*).",
            "example": 1.5,
            "minimum": 0
        },
        "width": {
            "type": "number",
            "format": "float",
            "description": "The width of the vehicle (*in meters*).",
            "example": 2.2,
            "minimum": 0
        },
        "exclude_unpaved": {
            "type": "boolean",
            "description": "This value indicates whether or not the path may include unpaved roads.",
            "default": "false"
        },
        "exclude_cash_only_tolls": {
            "type": "boolean",
            "description": "A boolean value which indicates the desire to avoid routes with cash-only tolls.",
            "default": "false"
        },
        "include_hov2": {
            "type": "boolean",
            "description": "A boolean value which indicates the desire to include HOV roads with a 2-occupant requirement in the route when advantageous.",
            "default": "false"
        },
        "include_hov3": {
            "type": "boolean",
            "description": "A boolean value which indicates the desire to include HOV roads with a 3-occupant requirement in the route when advantageous.",
            "default": "false"
        },
        "include_hov": {
            "type": "boolean",
            "description": "A boolean value which indicates the desire to include tolled HOV roads which require the driver to pay a toll if the occupant requirement isn't met.",
            "default": "false"
        }
    }

    truck_options = {
        **vehicle_options,
        "use_living_streets": {
            **automobile_options['use_living_streets'],
            "default": 0.0
        },
        "service_penalty": {
            **generic_options['service_penalty'],
            "default": 0
        },
        "length": {
            "type": "number",
            "format": "float",
            "description": "The length of the truck (*in meters*).",
            "example": 5.5,
            "minimum": 0
        },
        "weight": {
            "type": "number",
            "format": "float",
            "description": "The weight of the truck (*in metric tons*).",
            "default": 2.5,
            "minimum": 0
        },
        "axle_load": {
            "type": "number",
            "format": "float",
            "description": "The axle load of the truck (*in metric tons*).",
            "example": 1.3,
            "minimum": 0
        },
        "hazmat": {
            "type": "boolean",
            "description": "A value indicating if the truck is carrying hazardous materials.",
            "default": "false"
        }
    }

    bicycle_options = {
        **generic_options,
        "bicycle_type": {
            "type": "string",
            "description": "The type of bicycle:\n- Road: a road-style bicycle with narrow tires that is generally lightweight and designed for speed on paved surfaces.\n- *Hybrid* or City: a bicycle made mostly for city riding or casual riding on roads and paths with good surfaces.\n- *Cross*: a cyclo-cross bicycle, which is similar to a road bicycle but with wider tires suitable to rougher surfaces.\n- *Mountain*: a mountain bicycle suitable for most surfaces but generally heavier and slower on paved surfaces.",
            "enum": ["Road", "Hybrid", "City", "Cross", "Mountain"],
            "default": "Hybrid"
        },
        "cycling_speed": {
            "type": "integer",
            "description": "Cycling speed is the average travel speed along smooth, flat roads. This is meant to be the speed a rider can comfortably maintain over the desired distance of the route. It can be modified (in the costing method) by surface type in conjunction with bicycle type. When no speed is specifically provided, the default speed is determined by the bicycle type and are as follows: *Road* = 25 km/h, Cross = 20 km/h, Hybrid/City = 18 km/h, and Mountain = 16 km/h.",
            "example": 25,
            "minimum": 0
        },
        "use_roads": {
            "type": "number",
            "format": "float",
            "description": "A cyclist's propensity to use roads alongside other vehicles. This is a range of values from 0 to 1, where 0 attempts to avoid roads and stay on cycleways and paths, and 1 indicates the rider is more comfortable riding on roads. Based on the use_roads factor, roads with certain classifications and higher speeds are penalized in an attempt to avoid them when finding the best path.",
            "default": 0.5,
            "minimum": 0.0,
            "maximum": 1.0
        },
        "use_hills": {
            "type": "number",
            "format": "float",
            "description": "A cyclist's desire to tackle hills in their routes. This is a range of values from 0 to 1, where 0 attempts to avoid hills and steep grades even if it means a longer (time and distance) path, while 1 indicates the rider does not fear hills and steeper grades. Based on the use_hills factor, penalties are applied to roads based on elevation change and grade. These penalties help the path avoid hilly roads in favor of flatter roads or less steep grades where available. Note that it is not always possible to find alternate paths to avoid hills (for example when route locations are in mountainous areas).",
            "default": 0.5,
            "minimum": 0.0,
            "maximum": 1.0
        },
        "use_ferry": {**automobile_options['use_ferry']},
        "use_living_streets": {
            **automobile_options['use_living_streets'],
            "default": 0.5
        },
        "avoid_bad_surfaces": {
            "type": "number",
            "format": "float",
            "description": "This value is meant to represent how much a cyclist wants to avoid roads with poor surfaces relative to the bicycle type being used. This is a range of values between 0 and 1. When the value is 0, there is no penalization of roads with different surface types; only bicycle speed on each surface is taken into account. As the value approaches 1, roads with poor surfaces for the bike are penalized heavier so that they are only taken if they significantly improve travel time. When the value is equal to 1, all bad surfaces are completely disallowed from routing, including start and end points.",
            "default": 0.25,
            "minimum": 0.0,
            "maximum": 1.0
        },
        "shortest": {
            "type": "boolean",
            "description": "Changes the metric to quasi-shortest, i.e. purely distance-based costing. Note, this will disable all other costings & penalties. Also note, shortest will not disable hierarchy pruning, leading to potentially sub-optimal routes for some costing models.",
            "default": "false"
        }
    }

    bikeshare_options = {
        **bicycle_options,
        "bss_return_cost": {
            "type": "integer",
            "description": "It is meant to give the time (*in seconds*) will be used to return a rental bike. This value will be displayed in the final directions and used to calculate the whole duation.",
            "default": 120,
            "minimum": 0
        },
        "bss_return_penalty": {
            "type": "integer",
            "description": "It is meant to describe the potential effort (*in seconds*) to return a rental bike. This value won't be displayed and used only inside of the algorithm.",
            "default": 0,
            "minimum": 0
        },
    }

    motor_scooter_options = {
        **automobile_options,
        "top_speed": {
            **automobile_options['top_speed'],
            "minimum": 20,
            "maximum": 120,
            "default": 45
        },
        "use_primary": {
            "type": "number",
            "format": "float",
            "description": "A riders's propensity to use primary roads. This is a range of values from 0 to 1, where 0 attempts to avoid primary roads, and 1 indicates the rider is more comfortable riding on primary roads. Based on the *use_primary* factor, roads with certain classifications and higher speeds are penalized in an attempt to avoid them when finding the best path.",
            "default": 0.5,
            "minimum": 0.0,
            "maximum": 1.0
        },
        "use_hills": {
            "type": "number",
            "format": "float",
            "description": "A riders's desire to tackle hills in their routes. This is a range of values from 0 to 1, where 0 attempts to avoid hills and steep grades even if it means a longer (time and distance) path, while 1 indicates the rider does not fear hills and steeper grades. Based on the *use_hills* factor, penalties are applied to roads based on elevation change and grade. These penalties help the path avoid hilly roads in favor of flatter roads or less steep grades where available. Note that it is not always possible to find alternate paths to avoid hills (for example when route locations are in mountainous areas).",
            "default": 0.5,
            "minimum": 0.0,
            "maximum": 1.0
        }
    }

    motorcycle_options = {
        **automobile_options,
        "use_highways": {
            "type": "number",
            "format": "float",
            "description": "A riders's propensity to prefer the use of highways. This is a range of values from 0 to 1, where 0 attempts to avoid highways, and values toward 1 indicates the rider prefers highways.",
            "default": 1.0,
            "minimum": 0.0,
            "maximum": 1.0
        },
        "use_trails": {
            "type": "number",
            "format": "float",
            "description": "A riders's desire for adventure in their routes. This is a range of values from 0 to 1, where 0 will avoid trails, tracks, unclassified or bad surfaces and values towards 1 will tend to avoid major roads and route on secondary roads.",
            "default": 1.0,
            "minimum": 0.0,
            "maximum": 0.0
        }
    }

    pedestrian_options = {
        "walking_speed": {
            "type": "number",
            "format": "float",
            "description": "Walking speed in km/h.",
            "default": 5.1,
            "minimum": 0.5,
            "maximum": 25.0
        },
        "walkway_factor": {
            "type": "number",
            "format": "float",
            "description": "A factor that modifies the cost when encountering roads classified as footway (no motorized vehicles allowed), which may be designated footpaths or designated sidewalks along residential roads. Pedestrian routes generally attempt to favor using these walkways and sidewalks.",
            "default": 1.0,
            "minimum": 0
        },
        "sidewalk_factor": {
            "type": "number",
            "format": "float",
            "description": "A factor that modifies the cost when encountering roads with dedicated sidewalks. Pedestrian routes generally attempt to favor using sidewalks.",
            "default": 1.0,
            "minimum": 0
        },
        "alley_factor": {
            "type": "number",
            "format": "float",
            "description": "A factor that modifies (multiplies) the cost when alleys are encountered. Pedestrian routes generally want to avoid alleys or narrow service roads between buildings.",
            "default": 2.0,
            "minimum": 0
        },
        "driveway_factor": {
            "type": "number",
            "format": "float",
            "description": "A factor that modifies (multiplies) the cost when encountering a driveway, which is often a private, service road. Pedestrian routes generally want to avoid driveways (private).",
            "default": 5.0,
            "minimum": 0
        },
        "step_penalty": {
            "type": "integer",
            "description": "A penalty (*in seconds*) added to each transition onto a path with steps or stairs. Higher values apply larger cost penalties to avoid paths that contain flights of steps.",
            "default": 0,
            "minimum": 0
        },
        "use_ferry": {**automobile_options['use_ferry']},
        "use_living_streets": {
            **automobile_options['use_living_streets'],
            "default": 0.6
        },
        "use_tracks": {
            **automobile_options['use_tracks'],
            "default": 0.5
        },
        "use_hills": {
            "type": "number",
            "format": "float",
            "description": "This is a range of values from 0 to 1, where 0 attempts to avoid hills and steep grades even if it means a longer (time and distance) path, while 1 indicates the pedestrian does not fear hills and steeper grades. Based on the use_hills factor, penalties are applied to roads based on elevation change and grade. These penalties help the path avoid hilly roads in favor of flatter roads or less steep grades where available. Note that it is not always possible to find alternate paths to avoid hills (for example when route locations are in mountainous areas).",
            "default": 0.5,
            "minimum": 0.0,
            "maximum": 1.0
        },
        "service_penalty": {
            "type": "integer",
            "description": "A penalty (*in seconds*) applied for transition to generic service road.",
            "default": 0,
            "minimum": 0
        },
        "service_factor": {
            "type": "integer",
            "description": "A factor that modifies (multiplies) the cost when generic service roads are encountered.",
            "default": 1,
            "minimum": 0
        },
        "max_hiking_difficulty": {
            "type": "integer",
            "description": "This value indicates the maximum difficulty of hiking trails that is allowed. Values between 0 and 6 are allowed. The values correspond to sac_scale values within OpenStreetMap; [see reference](https://wiki.openstreetmap.org/wiki/Key:sac_scale). The default value is 1 which means that well cleared trails that are mostly flat or slightly sloped are allowed. Higher difficulty trails can be allowed by specifying a higher value.",
            "minimum": 1,
            "maximum": 6,
            "default": 1
        },
        "shortest": {
            **automobile_options['shortest']
        }
    }

    transit_options = {
        "use_bus": {
            "type": "number",
            "format": "float",
            "description": "Range of values from 0 (try to avoid buses) to 1 (strong preference for riding buses).",
            "default": 0.3,
            "minimum": 0,
            "maximum": 1
        },
        "use_rail": {
            "type": "number",
            "format": "float",
            "description": "Range of values from 0 (try to avoid rail) to 1 (strong preference for riding rail).",
            "default": 0.6,
            "minimum": 0,
            "maximum": 1
        },
        "use_transfers": {
            "type": "number",
            "format": "float",
            "description": "Range of values from 0 (try to avoid transfers) to 1 (totally comfortable with transfers).",
            "default": 0.3,
            "minimum": 0,
            "maximum": 1
        },
        "transit_start_end_max_distance": {
            "type": "integer",
            "description": "A pedestrian option (*in meters*) that can be added to the request to extend the defaults. This is the maximum walking distance at the beginning or end of a route.",
            "default": 2145,
            "minimum": 0
        },
        "transit_transfer_max_distance": {
            "type": "integer",
            "description": "A pedestrian option (*in meters*) that can be added to the request to extend the defaults. This is the maximum walking distance between transfers.",
            "default": 800,
            "minimum": 0
        }
    }

    def createRoutingForm(options: dict):
        return {
            "type": "object",
            "properties": {
                "locations": locations,
                **directions_options,
                "date_time": {
                    "type": "object",
                    "description": "This is the local date and time at the location.",
                    "properties": {
                        "type": {
                            "type": "integer",
                            "description": "- 0 - Current departure time.\n- 1 - Specified departure time\n- 2 - Specified arrival time. Not yet implemented for multimodal costing method.\n- 3 - Invariant specified time. Time does not vary over the course of the path.",
                            "enum": [0, 1, 2, 3]
                        },
                        "value": {
                            "type": "string",
                            "format": "date-time",
                            "description": "The date and time is specified in ISO 8601 format (YYYY-MM-DDThh:mm) in the local time zone of departure or arrival."
                        }
                    }
                },
                **options
            },
            "required": ["locations"]
        }

    spec.components.schema('routingVehicleForm', {**createRoutingForm(vehicle_options)})
    spec.components.schema('routingTruckForm', createRoutingForm(truck_options))
    spec.components.schema('routingBicycleForm', createRoutingForm(bicycle_options))
    spec.components.schema('routingBikeshareForm', createRoutingForm(bikeshare_options))
    spec.components.schema('routingMotorScooterForm', createRoutingForm(motor_scooter_options))
    spec.components.schema('routingMotorcycleForm', createRoutingForm(motorcycle_options))
    spec.components.schema('routingPedestrianForm', createRoutingForm(pedestrian_options))
    spec.components.schema('routingTransitForm', createRoutingForm(transit_options))

    # Routes schemata

    trip_summary = {
        "type": "object",
        "description": "Trip or leg summary.",
        "properties": {
            "has_time_restrictions": {
                "type": "boolean",
                "description": "Whether time restrictions exist."
            },
            "min_lat": {
                "type": "number",
                "format": "float",
                "description": "Minimum latitude of a bounding box containing the route or leg.",
                "example": 37.983435
            },
            "min_lon": {
                "type": "number",
                "format": "float",
                "description": "Minimum longitude of a bounding box containing the route or leg.",
                "example": 23.731365
            },
            "max_lat": {
                "type": "number",
                "format": "float",
                "description": "Maximun latitude of a bounding box containing the route or leg.",
                "example": 37.98391
            },
            "max_lon": {
                "type": "number",
                "format": "float",
                "description": "Maximun longitude of a bounding box containing the route or leg.",
                "example": 23.735922
            },
            "time": {
                "type": "number",
                "format": "float",
                "description": "Estimated elapsed time to complete the trip or leg.",
                "example": 382.416
            },
            "length": {
                "type": "number",
                "format": "float",
                "description": "Distance traveled for the entire trip or leg. Units are either miles or kilometers based on the input units specified.",
                "example": 0.541
            },
            "cost": {
                "type": "number",
                "format": "float",
                "description": "The cost of the trip or leg (in seconds).",
                "example": 422.416
            }
        }
    }

    maneuver = {
        "type": "object",
        "properties": {
            "type": {
                "type": "integer",
                "description": "Type of maneuver; one of the following:\n- 0: kNone\n- 1: kStart\n- 2: kStartRight\n- 3: kStartLeft\n- 4: kDestination\n- 5: kDestinationRight\n- 6: kDestinationLeft\n- 7: kBecomes\n- 8: kContinue\n- 9: kSlightRight\n- 10: kRight\n- 11: kSharpRight\n- 12: kUturnRight\n- 13: kUturnLeft\n- 14: kSharpLeft\n- 15: kLeft\n- 16: kSlightLeft\n- 17: kRampStraight\n- 18: kRampRight\n- 19: kRampLeft\n- 20: kExitRight\n- 21: kExitLeft\n- 22: kStayStraight\n- 23: kStayRight\n- 24: kStayLeft\n- 25: kMerge\n- 26: kRoundaboutEnter\n- 27: kRoundaboutExit\n- 28: kFerryEnter\n- 29: kFerryExit\n- 30: kTransit\n- 31: kTransitTransfer\n- 32: kTransitRemainOn\n- 33: kTransitConnectionStart\n- 34: kTransitConnectionTransfer\n- 35: kTransitConnectionDestination\n- 36: kPostTransitConnectionDestination\n- 37: kMergeRight\n- 38: kMergeLeft"
            },
            "instruction": {
                "type": "string",
                "description": "Written maneuver instruction; describes the maneuver.\n\n*Present only when directions_type is not \"none\" or \"maneuvers\".*",
                "example": "Turn right onto Main Street."
            },
            "verbal_pre_transition_instruction": {
                "type": "string",
                "description": "Text suitable for use as a verbal message immediately prior to the maneuver transition.\n\n*Present only when directions_type is not \"none\" or \"maneuvers\".*",
                "example": "Turn right onto North Prince Street, U.S. 2 22."
            },
            "verbal_post_transition_instruction": {
                "type": "string",
                "description": "Text suitable for use as a verbal message immediately after the maneuver transition.\n\n*Present only when directions_type is not \"none\" or \"maneuvers\".*",
                "example": "Continue on U.S. 2 22 for 3.9 miles."
            },
            "street_names": {
                "type": "array",
                "description": "List of street names that are consistent along the entire nonobvious maneuver.",
                "items": {
                    "type": "string",
                    "example": "Main Street"
                }
            },
            "begin_street_names": {
                "type": "array",
                "description": "**When present**, these are the street names at the beginning (transition point) of the nonobvious maneuver (if they are different than the names that are consistent along the entire nonobvious maneuver).",
                "items": {
                    "type": "string",
                    "example": "North Prince Street"
                }
            },
            "time": {
                "type": "number",
                "format": "float",
                "description": "Estimated time along the maneuver in seconds.",
                "example": 26.782
            },
            "length": {
                "type": "number",
                "format": "float",
                "description": "Maneuver length in the units specified.",
                "example": 0.037
            },
            "cost": {
                "type": "number",
                "format": "float",
                "description": "The cost of the path (in seconds).",
                "example": 26.782
            },
            "begin_shape_index": {
                "type": "integer",
                "description": "Index into the list of shape points for the start of the maneuver.",
                "example": 0
            },
            "end_shape_index": {
                "type": "integer",
                "description": "Index into the list of shape points for the end of the maneuver.",
                "example": 1
            },
            "verbal_multi_cue": {
                "type": "boolean",
                "description": "True if the *verbal_pre_transition_instruction* has been appended with the verbal instruction of the next maneuver.\n\n*Present only when directions_type is not \"none\" or \"maneuvers\".*"
            },
            "travel_mode": {
                "type": "string",
                "description": "Travel mode.",
                "enum": ["drive", "pedestrian", "bicycle", "transit"]
            },
            "travel_type": {
                "type": "string",
                "description": "Specific travel type.",
                "enum": ["car", "foot", "road", "tram", "metro", "rail", "bus", "ferry", "cable_car", "gondola", "funicular"]
            },
            "bss_maneuver_type": {
                "type": "string",
                "description": "Used **only** when **travel_mode** is *bikeshare*. Describes bike share maneuver.",
                "enum": ["NoneAction", "RentBikeAtBikeShare", "ReturnBikeAtBikeShare"]
            }
        }
    }

    route_response = {
        "type": "object",
        "description": "Route details.",
        "properties": {
            "trip": {
                "type": "object",
                "description": "A JSON object that contains details about the trip, including locations, a summary with basic information about the entire trip, and a list of legs.",
                "properties": {
                    "locations": {
                        "type": "array",
                        "description": "Location information is returned in the same form as it is entered with some additional fields.",
                        "items": {
                            "type": "object",
                            "description": "Location information is returned in the same form as it is entered with some additional fields.",
                            "properties": {
                                "type": {
                                    "type": "string",
                                    "description": "The type of this location (*break*, *through*, *via* or *break_through*).",
                                    "enum": ["break", "through", "via", "break_through"]
                                },
                                "lat": {
                                    "type": "number",
                                    "format": "float",
                                    "description": "Latitude of the location in degrees.",
                                    "example": 37.983841
                                },
                                "lon": {
                                    "type": "number",
                                    "format": "float",
                                    "description": "Longitude of the location in degrees.",
                                    "example": 23.735741
                                },
                                "original_index": {
                                    "type": "integer",
                                    "description": "The index in the (original) locations as entered.",
                                    "example": 2
                                }
                            }
                        }
                    },
                    "legs": {
                        "type": "array",
                        "description": "A trip contains one or more legs. For n number of break locations, there are n-1 legs.",
                        "items": {
                            "type": "object",
                            "properties": {
                                "maneuvers": {
                                    "type": "array",
                                    "description": "*Present only when directions_type is not \"none\".*",
                                    "items": maneuver
                                },
                                "summary": trip_summary,
                                "shape": {
                                    "type": "string",
                                    "description": "Encoded polyline of the route path.",
                                    "example": "iwimgAcfvgl@rJtUu\\bVn@|AfFtMhRnd@eChBqPlLMHa@d@rArCtGrOdJbVqBlCyTnb@[zBJfC|@~CdDgC`J~R_Nb[uAbCfJbS"
                                }
                            }
                        }
                    },
                    "summary": trip_summary,
                    "status_message": {
                        "type": "string",
                        "description": "Status message.",
                        "example": "Found route between points"
                    },
                    "status": {
                        "type": "integer",
                        "description": "Status code.",
                        "example": 0
                    },
                    "units": {
                        "type": "string",
                        "description": "The specified units of length are returned.",
                        "enum": ["kilometers", "miles"]
                    },
                    "language": {
                        "type": "string",
                        "description": "The language of the narration instructions. If the user specified a language in the directions options and the specified language was supported - this returned value will be equal to the specified value. Otherwise, this value will be the default (en-US) language.",
                        "enum": ["bg-BG", "ca-ES", "cs-CZ", "da-DK", "de-DE", "el-GR", "en-GB", "en-US-x-pirate", "en-US", "es-ES", "et-EE", "fi-FI", "fr-FR", "hi-IN", "hu-HU", "it-IT", "ja-JP", "nb-NO", "nl-NL", "pl-PL", "pt-BR", "pt-PT", "ro-RO", "ru-RU", "sk-SK", "sl-SI", "sv-SE", "tr-TR", "uk-UA"],
                        "example": "en-US"
                    }
                }
            }
        }
    }
    spec.components.schema('routeResponse', route_response)

    # Attributes schema

    mathed_point = {
        "type": "object",
        "description": "Matched result.",
        "properties": {
            "distance_from_trace_point": {
                "type": "number",
                "format": "float",
                "description": "The distance in meters from the trace point to the matched point.\n\n*This value will not exist if this point was unmatched.*",
                "example": 48.706
            },
            "edge_index": {
                "type": "integer",
                "description": "The index of the edge in the list of edges that this matched point is associated with.\n\n*This value will not exist if this point was unmatched.*",
                "example": 0
            },
            "type": {
                "type": "string",
                "description": "Describes the type of this match result.",
                "enum": ["unmatched", "interpolated", "matched"],
                "example": "matched"
            },
            "distance_along_edge": {
                "type": "number",
                "format": "float",
                "description": "The distance along the associated edge for this matched point. For example, if the matched point is halfway along the edge then the value would be 0.5.\n\n*This value will not exist if this point was unmatched.*",
                "example": 0.5
            },
            "begin_route_discontinuity": {
                "type": "boolean",
                "description": "The boolean value is true if this match result is the begin location of a route disconnect.\n\n*This value will not exist if this is false.*",
                "example": "true"
            },
            "end_route_discontinuity": {
                "type": "boolean",
                "description": "The boolean value is true if this match result is the end location of a route disconnect.\n\n*This value will not exist if this is false.*",
                "example": "true"
            },
            "lat": {
                "type": "number",
                "format": "float",
                "description": "The latitude of the matched point.",
                "example": 37.98391
            },
            "lon": {
                "type": "number",
                "format": "float",
                "description": "The longitude of the matched point.",
                "example": 23.735189
            }
        }
    }

    end_node = {
        "type": "object",
        "description": "The node at the end of this edge.",
        "properties": {
            "transition_time": {
                "type": "number",
                "format": "float",
                "description": "Transition time in seconds.",
                "example": 5.729
            },
            "type": {
                "type": "string",
                "description": "Node type",
                "enum": ["street_intersection", "gate", "bollard", "toll_booth", "multi_use_transit_stop", "bike_share", "parking", "motor_way_junction", "border_control"]
            },
            "admin_index": {
                "type": "integer",
                "description": "Index value in the admin list",
                "example": 0
            },
            "elapsed_time": {
                "type": "number",
                "format": "float",
                "description": "Elapsed time of the path to arrive at this node.",
                "example": 2.785
            },
            "time_zone": {
                "type": "string",
                "description": "Time zone string for this node.",
                "example": "Europe/Athens"
            },
            "intersecting_edges": {
                "type": "array",
                "description": "List of intersecting edges at this node.",
                "items": {
                    "type": "object",
                    "description": "Intersecting edge.",
                    "properties": {
                        "road_class": {
                            "type": "string",
                            "description": "Road class.",
                            "enum": [road_class_enum]
                        },
                        "use": {
                            "type": "string",
                            "description": "Use",
                            "enum": ["tram", "road", "ramp", "turn_channel", "track", "driveway", "alley", "parking_aisle", "emergency_access", "drive_through", "culdesac", "cycleway", "mountain_bike", "sidewalk", "footway", "steps", "other", "rail-ferry", "ferry", "rail", "bus", "rail_connection", "bus_connnection", "transit_connection"]
                        },
                        "begin_heading": {
                            "type": "integer",
                            "description": "The direction at the beginning of this intersecting edge. The units are degrees from north in a clockwise direction.",
                            "example": 328
                        },
                        "to_edge_name_consistency": {
                            "type": "boolean",
                            "description": "True if this intersecting edge at the end node has consistent names with the path *to edge*."
                        },
                        "from_edge_name_consistency": {
                            "type": "boolean",
                            "description": "True if this intersecting edge at the end node has consistent names with the path *from edge*."
                        },
                        "driveability": {
                            "type": "string",
                            "description": "Driveability values, if available.",
                            "enum": ["forward", "backward", "both"]
                        },
                        "cyclability": {
                            "type": "string",
                            "description": "Cyclability values, if available.",
                            "enum": ["forward", "backward", "both"]
                        },
                        "walkability": {
                            "type": "string",
                            "description": "Walkability values, if available.",
                            "enum": ["forward", "backward", "both"],
                            "example": "both"
                        }
                    }
                }
            }
        }
    }

    edge = {
        "type": "object",
        "description": "An edge object.",
        "properties": {
            "end_node": end_node,
            "names": {
                "type": "array",
                "description": "List of names.",
                "items": {
                    "type": "string",
                    "example": "Main Street"
                }
            },
            "speed": {
                "type": "integer",
                "description": "Edge speed in the units specified (in kilometers per hour by default).",
                "example": 40
            },
            "road_class": {
                "type": "string",
                "description": "Road class.",
                "enum": road_class_enum
            },
            "begin_heading": {
                "type": "integer",
                "description": "The direction at the beginning of an edge. The units are degrees from north in a clockwise direction.",
                "example": 148
            },
            "begin_shape_index": {
                "type": "integer",
                "description": "Index into the list of shape points for the start of the edge.",
                "example": 1
            },
            "traversability": {
                "type": "string",
                "description": "Traversability",
                "enum": ["forward", "backward", "both"]
            },
            "use": {
                "type": "string",
                "enum": ["tram", "road", "ramp", "turn_channel", "track", "driveway", "alley", "parking_aisle", "emergency_access", "drive_through", "culdesac", "cycleway", "mountain_bike", "sidewalk", "footway", "steps", "other", "rail-ferry", "ferry", "rail", "bus", "rail_connection", "bus_connnection", "transit_connection"]
            },
            "drive_on_right": {
                "type": "boolean",
                "description": "True if the flag is enabled for driving on the right side of the street."
            },
            "surface": {
                "type": "string",
                "description": "Surface description.",
                "enum": ["paved_smooth", "paved", "paved_rough", "compacted", "dirt", "gravel", "path", "impassable"]
            },
            "density": {
                "type": "integer",
                "description": "The relative density along the edge.",
                "example": 15
            },
            "sac_scale": {
                "type": "integer",
                "description": "Classification of hiking trails based on difficulty. Values:\n- 0 - No Sac Scale\n- 1 - Hiking\n- 2 - Mountain hiking\n- 3 - Demanding mountain hiking\n- 4 - Alpine hiking\n- 5 - Demanding alpine hiking\n- 6 - Difficult alpine hiking",
                "example": 2
            },
            "length": {
                "type": "number",
                "format": "float",
                "description": "Edge length in the units specified (default is kilometers).",
                "example": 0.062
            },
            "lane_count": {
                "type": "integer",
                "description": "The number of lanes for this edge.",
                "example": 1
            },
            "end_shape_index": {
                "type": "integer",
                "description": "Index into the list of shape points for the end of the edge.",
                "example": 2
            },
            "shoulder": {
                "type": "boolean",
                "description": "True if the edge has a shoulder."
            },
            "bicycle_network": {
                "type": "integer",
                "description": "The bike network for this edge."
            },
            "max_downward_grade": {
                "type": "integer",
                "description": "The maximum downward slope. A value of 32768 indicates no elevation data is available for this edge.",
                "example": 32768
            },
            "end_heading": {
                "type": "integer",
                "description": "The direction at the end of an edge. The units are degrees from north in a clockwise direction.",
                "example": 148
            },
            "mean_elevation": {
                "type": "integer",
                "description": "The mean or average elevation along the edge. Units are meters by default. If the units are specified as miles, then the mean elevation is returned in feet. A value of 32768 indicates no elevation data is available for this edge.",
                "example": 32768
            },
            "max_upward_grade": {
                "type": "integer",
                "description": "The maximum upward slope. A value of 32768 indicates no elevation data is available for this edge.",
                "example": 32768
            },
            "travel_mode": {
                "type": "string",
                "description": "Travel mode.",
                "enum": ["drive", "pedestrian", "bicycle", "transit"]
            },
            "weighted_grade": {
                "type": "number",
                "format": "float",
                "description": "The weighted grade factor. Valhalla manufactures a *weighted_grade* from elevation data. It is a measure used for hill avoidance in routing - sort of a relative energy use along an edge. But since an edge in Valhalla can possibly go up and down over several hills it might not equate to what most folks think of as grade.",
                "example": 0.0
            },
            "vehicle_type": {
                "type": "string",
                "description": "*Present only for relevant costing models.*",
                "enum": ["car", "motorcycle", "bus", "tractor_trailer"]
            },
            "way_id": {
                "type": "integer",
                "description": "Way identifier of the OpenStreetMap base data.",
                "example": 636757315
            },
            "id": {
                "type": "integer",
                "description": "Identifier of an edge within the tiled, hierarchical graph.",
                "example": 456776850201
            },
            "pedestrian_type": {
                "type": "string",
                "description": "*Present only for relevant costing models.*",
                "enum": ["foot", "wheelchair", "segway"]
            },
            "bicycle_type": {
                "type": "string",
                "description": "*Present only for relevant costing models.*",
                "enum": ["road", "cross", "hybrid", "mountain"]
            },
            "transit_type": {
                "type": "string",
                "description": "*Present only for relevant costing models.*",
                "enum": ["tram", "metro", "rail", "bus", "ferry", "cable_car", "gondola", "funicular"]
            }
        }
    }

    admins = {
        "type": "object",
        "description": "Administrative codes and names.",
        "properties": {
            "state_code": {
                "type": "string",
                "description": "State Code",
                "example": "08"
            },
            "state_text": {
                "type": "string",
                "description": "State name",
                "example": "Ontario"
            },
            "country_text": {
                "type": "string",
                "description": "Country name.",
                "example": "Canada"
            },
            "country_code": {
                "type": "string",
                "description": "Country [ISO 3166-1 alpha-2](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2) code.",
                "example": "CA"
            }
        }
    }

    trace_attributes_response = {
        "type": "object",
        "description": "The result of the map matching.",
        "properties": {
            "matched_points": {
                "type": "array",
                "description": "List of match results. There is a one-to-one correspondence with the input set of latitude, longitude coordinates and this list of match results.",
                "items": mathed_point
            },
            "edges": {
                "type": "array",
                "description": "List of edges associated with input shape.",
                "items": edge
            },
            "admins": {
                "type": "array",
                "description": "List of the administrative codes and names.",
                "items": admins
            },
            "raw_score": {
                "type": "number",
                "format": "float",
                "description": "Raw score of the matching.",
                "example": 100000496.0
            },
            "shape": {
                "type": "string",
                "description": "The encoded polyline of the matched path.",
                "example": "kijmgAixtgl@t\\cVyDppAqPlLMHa@d@rArCtGrOdJbV|FbObAzCl@|AxA`Dh[nt@iZfUoYvTeMmXaCsFkHqPo@yAmAqCxQmNdDgCvKmInKeIn@g@nB_BxA`Dh[nt@iZfUoYvTeMmX"
            },
            "confidence_score": {
                "type": "number",
                "format": "float",
                "description": "Confidence score of matching.",
                "example": 1.0
            },
            "osm_changeset": {
                "type": "integer",
                "description": "Identifier of the OpenStreetMap base data version.",
                "example": 8855162523
            }
        }
    }
    spec.components.schema('traceAttributesResponse', trace_attributes_response)

    # Responses

    validation_error_response = {
        "description": "Form validation error.",
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "description": "The key is the request body key.",
                    "additionalProperties": {
                        "type": "array",
                        "items": {
                            "type": "string",
                            "description": "Description of validation error."
                        }
                    },
                    "example": {
                        "lat": [
                            [
                                "This field is required."
                            ]
                        ]
                    }
                }
            }
        }
    }
    spec.components.response('validationErrorResponse', validation_error_response)

    isochrone_response = {
        "description": "The isoline contours as GeoJSON. The contours are calculated using rasters and are returned as either polygon or line features, depending on the input setting for the polygons parameter.",
        "content": {
            "application/json": {
                "schema": isochrone_geojson
            }
        }
    }
    spec.components.response('isochroneResponse', isochrone_response)

    route_response = {
        "description": "A JSON describing the computed route.",
        "content": {
            "application/json": {
                "schema": route_response
            }
        }
    }
    spec.components.response('routeResponse', route_response)

    spec.components.response('traceAttributesResponse', {
        "description": "A JSON describing the computed attributes.",
        "content": {
            "application/json": {
                "schema": trace_attributes_response
            }
        }
    })
