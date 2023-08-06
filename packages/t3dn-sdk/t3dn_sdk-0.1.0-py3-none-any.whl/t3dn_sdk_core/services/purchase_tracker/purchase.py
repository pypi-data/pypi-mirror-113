import time
from threading import Lock, Event
from multiprocessing.dummy import Pool as ThreadPool
from ...utils.decorators import retry
from ...utils.browser import get_focused_workspace, popup_url
from ...exceptions.api_exception import APIException
from requests.exceptions import RequestException, HTTPError
from ...api.purchase_tracker import PurchaseTrackerAPI
from ...models.purchase_tracker import PurchaseTrackerModel


class PurchaseTrackerPurchaseService(object):
    '''Service for creating purchase tracker and polling status.'''

    def __init__(self, cb_start, cb_open, cb_finish, cb_cancel, cb_error):
        '''Initialize purchase service.

        Args:
            cb_start (function): Function that gets called to confirm
                purchase has started, takes no arguments.
            cb_open (function): Function that gets called to confirm
                checkout has opened, takes no arguments.
            cb_finish (function): Function that gets called when purchase
                is finished, takes purchase tracker token.
            cb_cancel (function): Function that gets called to confirm
                purchase is cancelled, takes no arguments.
            cb_error (function): Function that gets called if an error
                occurs, takes exception.
        '''
        self._cb_start = cb_start
        self._cb_open = cb_open
        self._cb_finish = cb_finish
        self._cb_cancel = cb_cancel
        self._cb_error = cb_error

        self._workspace = None
        self._tracker = None
        self._lock = Lock()

        self._result = None
        self._cancel = Event()
        self._pool = ThreadPool(1)

    def purchase(self, catalog=None, product=None, wait_time=3, auth=None):
        '''Start the purchase process.

        Use either catalog or product, not both.

        Args:
            catalog (str): Catalog ID.
            product (str): Product ID.
            wait_time (int): Number of seconds to delay response.
            auth (dict): The credentials optionally used to access this route.
        '''
        if self._result is None or self._result.ready():
            self._cancel.clear()

            self._result = self._pool.apply_async(
                func=self._purchase,
                args=(catalog, product, wait_time, auth),
                error_callback=self._cb_error,
            )

    def _purchase(self, catalog, product, wait_time, auth):
        self._cb_start()

        with self._lock:
            self._workspace = get_focused_workspace()  # As soon as possible.
            self._tracker = self._create_tracker(catalog, product, auth)

        self._open_webbrowser()
        self._poll_status(wait_time, auth)

        if self._cancel.is_set():
            self._cb_cancel()
        else:
            self._cb_finish(self._tracker.token)

    @retry((APIException, RequestException, HTTPError), logging=True)
    def _create_tracker(self, catalog, product, auth) -> PurchaseTrackerModel:
        if self._cancel.is_set():
            return PurchaseTrackerModel()

        return PurchaseTrackerAPI().create(catalog, product, auth)

    def _open_webbrowser(self):
        if self._cancel.is_set():
            return

        popup_url(
            self._tracker.url,
            self._tracker.detect_title,
            self._tracker.apply_size,
            self._workspace,
        )

        self._cb_open()

    def _poll_status(self, wait_time, auth):
        while True:
            try:
                if self._cancel.is_set():
                    return

                status = PurchaseTrackerAPI().get_status(
                    self._tracker.token,
                    wait_time,
                    auth,
                )

            except (APIException, RequestException) as e:
                if self._cancel.is_set():
                    return

                print(e)
                time.sleep(wait_time)

            else:
                if self._cancel.is_set():
                    return

                if status == 'completed':
                    return

    def reopen_checkout(self):
        '''Open the checkout again, without cancelling the ongoing purchase.'''
        if self._result is None or self._result.ready():
            return

        if self._cancel.is_set():
            return

        with self._lock:
            if not self._tracker:
                return

            popup_url(
                self._tracker.url,
                self._tracker.detect_title,
                self._tracker.apply_size,
                self._workspace,
            )

    def cancel(self):
        '''Cancel the purchase process.'''
        self._cancel.set()
