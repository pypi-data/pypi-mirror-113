from .base_api import BaseAPI
from ..exceptions.api_exception import APIException
from ..utils import config
from ..models.purchase_tracker import (
    PurchaseTrackerModel,
    PurchaseTrackerFileModel,
)


class PurchaseTrackerAPI(BaseAPI):
    '''API that allows the user to work with purchase trackers.'''

    def __init__(self):
        super(PurchaseTrackerAPI, self).__init__(1)
        self._route_name = 'purchase-tracker'

    def _build_url(self, path):
        return '{}/{}/{}'.format(
            config.get_api_url(),
            'checkoutcontroller',
            path,
        )

    def create(self, catalog=None, product=None, auth=None):
        '''Create a purchase tracker.

        Use either catalog or product, not both.

        Args:
            catalog (str): Catalog ID.
            product (str): Product ID.
            auth (dict): The credentials optionally used to access this route.

        Returns:
            PurchaseTrackerModel: The new purchase tracker
                including a token, URL, window title and size.
        '''

        request_body = {}
        if catalog:
            request_body['catalog'] = catalog
        if product:
            request_body['product'] = product

        path = self._route_name
        response = self._execute_request(
            'post',
            path,
            request_body=request_body,
            auth=auth,
        )

        if response.successful():
            return PurchaseTrackerModel.from_dict(response.body)
        else:
            raise APIException(response)

    def get_status(self, token, wait_time=None, auth=None):
        '''Get purchase tracker status.

        Args:
            token (str): Token for the purchase tracker.
            wait_time (int): Number of seconds to delay the response.
            auth (dict): The credentials optionally used to access this route.

        Returns:
            str: 'completed' if the purchase is done, 'pending' otherwise.
        '''

        path = '{}/{}/status'.format(self._route_name, token)

        params = []
        if wait_time is not None:
            params.append(('waitTime', wait_time))

        response = self._execute_request('get', path, params=params, auth=auth)

        if response.successful():
            return response.body.get('status')
        else:
            raise APIException(response)

    def get_files(self, token, auth=None):
        '''Get purchase tracker files.

        Args:
            token (str): Token for the purchase tracker.
            auth (dict): The credentials optionally used to access this route.

        Returns:
            list of PurchaseTrackerFileModel: Purchase tracker
                files including filename and URL.
        '''

        path = '{}/{}/files'.format(self._route_name, token)
        response = self._execute_request('get', path, auth=auth)

        if response.successful():
            return [
                PurchaseTrackerFileModel.from_dict(data)
                for data in response.body
            ]
        else:
            raise APIException(response)
