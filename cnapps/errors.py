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
from sanic import response

from cnapps import exceptions


LOGGER = logging.getLogger(__name__)

REST = sanic.Blueprint("errors")



def debug_error(error):
    message = [str(x) for x in error.args]
    if not message:
        message = error.message
    LOGGER.debug("Error: %s", message)


def make_error_response(error_type, message, status_code, description=None):
    content = {
        "success": False,
        "error": {"type": error_type, "message": message, "code": status_code},
    }
    if description:
        content["error"]["description"] = description
    LOGGER.info("Response error: %s", content)
    return response.json(content), status_code


def handle_error(request, error):
    LOGGER.info("Handle error: %s %s", error.__class__.__name__, error)
    return make_error_response(
        error.__class__.__name__, error.message, error.status_code
    )


def add_exceptions_handlers(app):
    app.error_handler.add(exceptions.DatabaseError, handle_error)
    app.error_handler.add(exceptions.APIError, handle_error)
    app.error_handler.add(exceptions.ConfigurationError, handle_error)
    app.error_handler.add(exceptions.UnauthorizedError, handle_error)
    app.error_handler.add(exceptions.ForbiddenError, handle_error)
