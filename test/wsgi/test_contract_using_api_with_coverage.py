import pytest

from specmatic.core.specmatic import Specmatic
from specmatic.utils import get_project_root
from test.apps.flask import app

app_host = "127.0.0.1"
app_port = 5000
stub_host = "127.0.0.1"
stub_port = 8080
PROJECT_ROOT = get_project_root()
expectation_json_file = PROJECT_ROOT + '/test/data/expectation.json'


class TestContract:
    pass


Specmatic() \
    .with_project_root(PROJECT_ROOT) \
    .with_stub(stub_host, stub_port, [expectation_json_file]) \
    .with_wsgi_app(app, app_host, app_port) \
    .test_with_flask_app_coverage(TestContract) \
    .run()

if __name__ == '__main__':
    pytest.main()
