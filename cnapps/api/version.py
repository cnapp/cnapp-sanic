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
from sanic.response import json
from sanic_openapi import doc

from cnapps.api import commons
from cnapps import version


LOGGER = logging.getLogger(__name__)

bp = sanic.Blueprint("version", url_prefix='/version')


@bp.route("", methods=["GET"])
@doc.summary("Application version API")
@doc.produces({"version": str})
async def version_status(request):
    """Display application version.

    Returns:
        A HTTP response in JSON (application/json content-type)
    """

    LOGGER.info("Get version")
    return commons.make_webservice_response({"version": version.RELEASE})
