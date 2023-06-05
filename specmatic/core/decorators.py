from specmatic.core.specmatic_stub import SpecmaticStub
from specmatic.core.specmatic_test import SpecmaticTest
from specmatic.generators.pytest_generator import PyTestGenerator
from specmatic.servers.asgi_app_server import ASGIAppServer
from specmatic.servers.wsgi_app_server import WSGIAppServer
from specmatic.utils import get_junit_report_file_path


def specmatic_stub(host: str = '127.0.0.1', port: int = 0, project_root: str = '', expectations=None,
                   specmatic_json_file: str = ''):
    def decorator(cls):
        try:
            cls.stub = SpecmaticStub(host, port, project_root, specmatic_json_file)
            cls.stub.set_expectations(expectations)
        except Exception as e:
            if hasattr(cls, 'stub'):
                cls.stub.stop()
            if hasattr(cls, 'app'):
                cls.app.stop()
            print(f"Error: {e}")
            raise e
        return cls

    return decorator


def specmatic_contract_test(host: str = '127.0.0,1', port: int = 0, project_root: str = '',
                            specmatic_json_file: str = ''):
    def decorator(cls):
        try:
            test_host = host
            test_port = port
            if test_port == 0:
                if hasattr(cls, 'app'):
                    app = cls.app
                    test_host = app.host
                    test_port = app.port

            SpecmaticTest(test_host, test_port, project_root, specmatic_json_file).run()
            PyTestGenerator(cls, get_junit_report_file_path()).generate()
            return cls
        except Exception as e:
            if hasattr(cls, 'stub'):
                cls.stub.stop()
            if hasattr(cls, 'app'):
                cls.app.stop()
            print(f"Error: {e}")
            raise e
        finally:
            if hasattr(cls, 'stub'):
                cls.stub.stop()
            if hasattr(cls, 'app'):
                cls.app.stop()

    return decorator


def start_wsgi_app(app, host: str = '127.0.0.1', port: int = 0):
    def decorator(cls):
        try:
            cls.app = WSGIAppServer(app, host, port)
            cls.app.start()
            return cls
        except Exception as e:
            if hasattr(cls, 'stub'):
                cls.stub.stop()
            if hasattr(cls, 'app'):
                cls.app.stop()
            print(f"Error: {e}")
            raise e

    return decorator


def start_asgi_app(app_module: str, host: str = '127.0.0.1', port: int = 0):
    def decorator(cls):
        try:
            cls.app = ASGIAppServer(app_module, host, port)
            cls.app.start()
            return cls
        except Exception as e:
            if hasattr(cls, 'stub'):
                cls.stub.stop()
            if hasattr(cls, 'app'):
                cls.app.stop()
            print(f"Error: {e}")
            raise e

    return decorator
