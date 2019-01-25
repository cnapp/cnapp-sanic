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

from sanic import response


LOGGER = logging.getLogger(__name__)


def make_webservice_response(content, status_code=200):
    """Creates the HTTP response.

    Args:
        content ([dict]): The content to send.
        status_code ([int], optional): Defaults to 200. The HTTP status code.
        message ([string], optional): Defaults to None. The response message

    Returns:
        A HTTP response.
    """

    LOGGER.info("Response to send: %d %s", status_code, content)
    return response.json(
        content,
        headers={'X-Served-By': 'sanic'},
        status=status_code
    )
