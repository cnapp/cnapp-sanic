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

import sanic

from cnapps.api import health as health
from cnapps.api import version as version
from cnapps import version as app_version


LOGGER = logging.getLogger(__name__)


def creates_app():
    """Create the application

    Returns:
        [sanic.Sanic]: the main application
    """

    LOGGER.info("Create application %s", app_version.RELEASE)
    app = sanic.Sanic()
    app.static('/static', './static')
    app.blueprint(version.bp)
    app.blueprint(health.bp)

    return app