import re
from typing import List

from specmatic.coverage.app_route_adapter import AppRouteAdapter
from specmatic.coverage.coverage_route import CoverageRoute


class FlaskAppRouteAdapter(AppRouteAdapter):
    def to_coverage_routes(self) -> List[CoverageRoute]:
        routes = []
        for route in self.app.url_map.iter_rules():
            if route.endpoint != 'static':  # Exclude static routes
                route_url = str(route)
                methods = route.methods
                print(f"\nStarted adapting route: {route_url} with methods: {methods}")
                route_url = self.convert_to_spring_actuator_url_format(route_url)
                routes.append(self.process_route(route_url, methods))
        return routes

    def convert_to_spring_actuator_url_format(self, flask_route_url):
        pattern = r'<\w+:(\w+)>'
        return re.sub(pattern, r'{\1}', flask_route_url)