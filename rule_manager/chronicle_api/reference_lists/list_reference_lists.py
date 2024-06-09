# Copyright 2024 Google LLC
#
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
#
"""Retrieve a list of reference lists.

API reference:
https://cloud.google.com/chronicle/docs/reference/rest/v1alpha/projects.locations.instances.referenceLists/list
"""

import os
from typing import Mapping, Any, List, Tuple

from google.auth.transport import requests


def list_reference_lists(
    http_session: requests.AuthorizedSession,
    page_size: int | None = None,
    page_token: str | None = None,
    view: str | None = "REFERENCE_LIST_VIEW_FULL",
) -> Tuple[List[Mapping[str, Any]], str]:
  """Retrieve a list of reference lists.

  Args:
      http_session: Authorized session for HTTP requests.
      page_size (optional): Maximum number of reference lists to return. Must be
        non-negative, and is capped at a server-side limit of 1000. A
        server-side default of 100 is used if the size is 0 or a None value.
      page_token (optional): Page token from a previous ListReferenceLists call
        used for pagination. The first page is retrieved if the token is the
        empty string or a None value.
      view (optional): The scope of fields to populate for the ReferenceList
        being returned. Reference:
        https://cloud.google.com/chronicle/docs/reference/rest/v1alpha/ReferenceListView

  Returns:
      List of reference lists and a page token for the next page of reference
      lists, if there are any.

  Raises:
      requests.exceptions.HTTPError: HTTP request resulted in an error
      (response.status_code >= 400).
  """
  url = f"{os.environ['CHRONICLE_API_BASE_URL']}/{os.environ['CHRONICLE_INSTANCE']}/referenceLists"
  params = {"page_size": page_size, "page_token": page_token, "view": view}

  response = http_session.request(method="GET", url=url, params=params)

  if response.status_code >= 400:
    print(response.text)
    response.raise_for_status()

  response_json = response.json()

  return response_json.get("referenceLists"), response_json.get("nextPageToken")
