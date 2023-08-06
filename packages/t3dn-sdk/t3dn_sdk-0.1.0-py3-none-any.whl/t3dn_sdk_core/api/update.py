from ..exceptions.api_exception import APIException
from ..utils import config
from .base_api import BaseAPI


class UpdateAPI(BaseAPI):

    def __init__(self):
        super(UpdateAPI, self).__init__(1)

    def _build_url(self, path):
        return '{}/{}/{}'.format(
            config.get_api_url(),
            'enrollmentcontroller',
            path,
        )

    def check(self, product, package, current, auth=None):
        response = self._execute_request(
            'post',
            'update/{}/{}'.format(product, package),
            params={
                'current': current,
            },
            auth=auth,
        )

        if response.successful():
            return response.body
        else:
            raise APIException(response)
