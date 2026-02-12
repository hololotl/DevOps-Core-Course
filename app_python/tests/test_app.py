import re
from app import app


def test_index_contains_expected_fields():
    client = app.test_client()
    headers = {"User-Agent": "pytest-client"}
    resp = client.get('/', headers=headers)
    assert resp.status_code == 200
    data = resp.get_json()

    # Top-level sections
    assert 'service' in data
    assert 'system' in data
    assert 'runtime' in data
    assert 'request' in data
    assert 'endpoints' in data

    # service fields
    svc = data['service']
    assert svc.get('name') == 'devops-info-service'
    assert 'version' in svc
    assert svc.get('framework') == 'Flask'

    # system fields
    sysinfo = data['system']
    assert 'hostname' in sysinfo
    assert isinstance(sysinfo.get('cpu_count'), int)

    # runtime fields
    rt = data['runtime']
    assert isinstance(rt.get('uptime_seconds'), int)
    assert isinstance(rt.get('uptime_human'), str)
    # ISO timestamp roughly matches pattern
    assert re.match(r"\d{4}-\d{2}-\d{2}T", rt.get('current_time'))

    # request fields reflect our test client
    req = data['request']
    assert req.get('method') == 'GET'
    assert req.get('path') == '/'
    assert req.get('user_agent') == 'pytest-client'


def test_health_endpoint():
    client = app.test_client()
    resp = client.get('/health')
    assert resp.status_code == 200
    data = resp.get_json()

    assert data.get('status') == 'healthy'
    assert 'timestamp' in data
    assert isinstance(data.get('uptime_seconds'), int)


def test_404_error_structure():
    client = app.test_client()
    resp = client.get('/this-route-does-not-exist')
    assert resp.status_code == 404
    data = resp.get_json()
    assert data.get('error') == 'Not Found'
    assert 'message' in data
