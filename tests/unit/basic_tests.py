# Setup/Teardown
def setup_module():
    print(" == Setting up tests for %s"  % (__name__))
    pass

def teardown_module():
    print(" == Tearing down tests for %s"  % (__name__))
    pass

# Tests

def test_drop_nones():
    """Unit - Test _dropNones"""
    from transport_service.api.requests.routing import _dropNones
    test_data1 = {'key1': 1, 'key2': None}
    test_data2 = {**test_data1, 'key3': {**test_data1}}
    test_data = {**test_data2, 'key4': [test_data1, test_data2]}
    def get_all_values(d):
        if isinstance(d, dict):
            for v in d.values():
                yield from get_all_values(v)
        elif isinstance(d, list):
            for v in d:
                yield from get_all_values(v)
        else:
            yield d
    values = list(get_all_values(test_data))
    assert None in values
    values = list(get_all_values(_dropNones(test_data)))
    assert None not in values
