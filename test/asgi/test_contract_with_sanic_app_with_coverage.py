import pytest

from specmatic.actuator.sanic_app_route_adapter import SanicAppRouteAdapter
from specmatic.core.specmatic import Specmatic
from specmatic.servers.coverage_server import CoverageServer
from specmatic.utils import get_project_root
from test.apps.sanic_app import app

PROJECT_ROOT = get_project_root()

app_host = "127.0.0.1"
app_port = 8000
stub_host = "127.0.0.1"
stub_port = 8080

expectation_json_file = PROJECT_ROOT + '/test/data/expectation.json'
app_module = PROJECT_ROOT + '/test/sanic_app'


class TestContract:
    pass


Specmatic() \
    .with_project_root(PROJECT_ROOT) \
    .with_stub(stub_host, stub_port, [expectation_json_file]) \
    .with_asgi_app('test.apps.sanic_app:app', app_host, app_port) \
    .test_with_sanic_app_coverage(TestContract, app) \
    .run()

if __name__ == '__main__':
    pytest.main()
