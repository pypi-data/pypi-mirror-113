from requests import request
from requests.auth import HTTPBasicAuth
from json import dumps
from enum import IntEnum
from ..utils import config
from ..utils.session_store import SessionStore


class StatusCode(IntEnum):
    Successful = 200,
    Unauthorized = 401,
    NotFound = 404,
    ResourceExists = 409,
    Invalid = 422


class _APIResponse(object):

    def __init__(self, status_code, body):
        self.status_code = status_code
        self.body = body

    def successful(self):
        return 200 <= self.status_code < 300

    def __repr__(self):
        return 'status_code: {}\nbody: {}'.format(
            self.status_code,
            dumps(self.body, indent=2),
        )


class BaseAPI(object):

    def __init__(self, version):
        self._version = version

    def _build_url(self, path):
        return '{}/v{}/{}'.format(
            config.get_api_url(),
            self._version,
            path,
        )

    def _execute_request(
        self,
        method,
        path,
        params=None,
        request_body=None,
        auth=None,
    ):
        '''Execute a request with the given arguments.

        Args:
            method (str): The HTTP verb to call.
            path (str): The path to execute this request on.
            params (list of tuples): Parameters to be used in the query
                portion of this request.
            request_body (str): The payload we are sending.
                Assume everything is json for now.
            auth (dict): The credentials needed to access this route.

        Returns:
            _APIResponse: The response for this request.
        '''

        url = self._build_url(path)

        headers = {'accept': 'application/json'}

        if request_body is not None:
            headers['content-type'] = 'application/json; charset=utf-8'

        if auth is None:
            auth = SessionStore.get()

        if auth is not None:
            credentials = HTTPBasicAuth(
                auth.get('email'),
                auth.get('password'),
            )
        else:
            credentials = None

        response = request(
            method,
            url,
            json=request_body,
            headers=headers,
            params=params,
            auth=credentials,
        )

        content_type = response.headers.get('content-type', '')
        if content_type.startswith('application/json') and response.content:
            response_body = response.json()
        else:
            response_body = response.text

        return _APIResponse(response.status_code, response_body)
