# Copyright (C) 2019 Nicolas Lamirault <nicolas.lamirault@gmail.com>

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import time

import sanic
import sanic_openapi

from cnapps.api import health as health
from cnapps.api import version as version
from cnapps.middleware.metrics import prometheus
from cnapps import version as app_version


LOGGER = logging.getLogger(__name__)


def creates_app():
    """Create the application

    Returns:
        [sanic.Sanic]: the main application
    """

    LOGGER.info("Create application %s", app_version.RELEASE)
    app = sanic.Sanic(__name__)
    app.static('/static', './static')
    app.blueprint(version.bp)
    app.blueprint(health.bp)
    setup_openapi(app)
    setup_metrics(app)

    return app


def setup_openapi(app):
    """Setup OpenAPI.

    Args:
        app [sanic.Sanic]: the main application
    """
    app.blueprint(sanic_openapi.openapi_blueprint)
    app.blueprint(sanic_openapi.swagger_blueprint)
    app.config.API_VERSION = app_version.RELEASE
    app.config.API_TITLE = 'CNAPP API'
    app.config.API_DESCRIPTION = 'CNAPP API'
    app.config.API_TERMS_OF_SERVICE = 'Use with caution!'
    app.config.API_PRODUCES_CONTENT_TYPES = ['application/json']
    app.config.API_CONTACT_EMAIL = 'nicolas.lamirault@gmail.com'


def setup_metrics(app):
    """Setup metrics for Prometheus.

    Args:
        app [sanic.Sanic]: the main application
    """

    LOGGER.debug("Setup Prometheus metrics")
    app.blueprint(prometheus.REST)

    @app.middleware('request')
    async def add_key(request):
        LOGGER.debug("Metric for request %s", request)
        request['__START_TIME__'] = time.time()

    @app.middleware('response')
    async def custom_banner(request, response):
        LOGGER.debug("Metric for response %s", request)
        lat = time.time() - request['__START_TIME__']
        prometheus.REQUEST_LATENCY.labels(request.method, request.path).observe(lat)
        prometheus.REQUEST_COUNT.labels(request.method, request.path, response.status).inc()

