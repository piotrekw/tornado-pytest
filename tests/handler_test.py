import requests

from fixtures import test_server


def test(test_server):
    response = requests.get(test_server('/'))
    assert response.status_code == 200

    json = response.json()
    assert 'status' in json
    assert json['status'] == 'ok'
