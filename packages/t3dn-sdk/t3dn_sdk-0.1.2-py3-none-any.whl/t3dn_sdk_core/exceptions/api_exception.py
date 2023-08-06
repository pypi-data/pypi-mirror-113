from ..api.base_api import StatusCode

_status_messages = {
    StatusCode.Successful: 'The request was handled successfully.',
    StatusCode.Unauthorized: 'The request does not have valid authorization.',
    StatusCode.NotFound: 'The requested data does not exist.',
    StatusCode.ResourceExists: 'The posted data already exists.',
    StatusCode.Invalid: 'The request has missing, malformed or invalid data.',
}


class APIException(Exception):

    def __init__(self, response, body=None):
        super(APIException, self).__init__(body)
        self.status_code = response.status_code
        self.body = body

        if self.body is None and self.status_code in _status_messages:
            self.body = _status_messages[self.status_code]

    def __str__(self):
        return 'Status Code: {} -> {}'.format(self.status_code, self.body)
