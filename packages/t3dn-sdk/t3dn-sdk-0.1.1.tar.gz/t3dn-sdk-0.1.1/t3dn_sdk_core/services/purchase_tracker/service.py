from enum import Enum
from threading import Lock
from .purchase import PurchaseTrackerPurchaseService
from .download import PurchaseTrackerDownloadService
from .install import PurchaseTrackerInstallService
from ...utils.decorators import abstractmethod


class PurchaseTrackerState(Enum):
    '''Possible purchase tracker states.'''
    CAN_PURCHASE = 'CAN_PURCHASE'
    OPENING = 'OPENING'
    PURCHASING = 'PURCHASING'
    CAN_DOWNLOAD = 'CAN_DOWNLOAD'
    DOWNLOADING = 'DOWNLOADING'
    CAN_INSTALL = 'CAN_INSTALL'
    INSTALLING = 'INSTALLING'
    FINISHED = 'FINISHED'


class PurchaseTrackerService(object):
    '''Service for working with a purchase tracker.

    You must overwrite the following methods:
    `_cb_state`, `_cb_filter`, `_cb_map`,
    `_cb_progress`, `_cb_install`, `_cb_error`.
    '''

    def __init__(self, catalog=None, product=None, token=None, folder=None):
        '''Initialize purchase tracker service.

        Use either catalog or product, not both.

        Args:
            catalog (str): Catalog ID.
                Optional if set in purchase call.
            product (str): Product ID.
                Optional if set in purchase call.
            token (str): Purchase tracker token.
                Optional if set by purchase finish or in download call.
            folder (str): Temporary download folder.
                Optional if set by download finish or in install call.
        '''
        self._lock = Lock()

        self._catalog = catalog
        self._product = product
        self._token = token
        self._folder = folder

        self._state = PurchaseTrackerState.CAN_PURCHASE
        self._progress = 0
        self._total = 0

        self._purchase_service = PurchaseTrackerPurchaseService(
            cb_start=self._purchase_start,
            cb_open=self._purchase_open,
            cb_finish=self._purchase_finish,
            cb_cancel=self._purchase_cancel,
            cb_error=self._purchase_error,
        )

        self._download_service = PurchaseTrackerDownloadService(
            cb_start=self._download_start,
            cb_filter=self._cb_filter,
            cb_progress=self._cb_progress,
            cb_finish=self._download_finish,
            cb_cancel=self._download_cancel,
            cb_error=self._download_error,
        )

        self._install_service = PurchaseTrackerInstallService(
            cb_start=self._install_start,
            cb_map=self._cb_map,
            cb_progress=self._cb_progress,
            cb_finish=self._install_finish,
            cb_cancel=self._install_cancel,
            cb_error=self._install_error,
        )

    def purchase(self, catalog=None, product=None, wait_time=3, auth=None):
        '''Start the purchase process.

        Use either catalog or product, not both.

        Args:
            catalog (str): Catalog ID.
                Optional if set in constructor call.
            product (str): Product ID.
                Optional if set in constructor call.
            wait_time (int): Number of seconds to delay response.
            auth (dict): The credentials optionally used to access this route.
        '''
        if catalog is None:
            with self._lock:
                catalog = self._catalog

        if product is None:
            with self._lock:
                product = self._product

        if (catalog is not None) or (product is not None):
            self._purchase_service.purchase(catalog, product, wait_time, auth)

    def _purchase_start(self):
        self._cb_state(PurchaseTrackerState.OPENING)

    def _purchase_open(self):
        self._cb_state(PurchaseTrackerState.PURCHASING)

    def _purchase_finish(self, token):
        with self._lock:
            self._token = token

        self._cb_state(PurchaseTrackerState.CAN_DOWNLOAD)

    def _purchase_cancel(self):
        self._cb_state(PurchaseTrackerState.CAN_PURCHASE)

    def _purchase_error(self, exception):
        self._cb_error(exception)
        self._cb_state(PurchaseTrackerState.CAN_PURCHASE)

    def reopen_checkout(self):
        '''Open the checkout again, without cancelling the ongoing purchase.'''
        self._purchase_service.reopen_checkout()

    def download(self, token=None, auth=None):
        '''Start the download process.

        Args:
            token (str): Purchase tracker token.
                Optional if set by purchase finish or in constructor call.
            auth (dict): The credentials optionally used to access this route.
        '''
        if token is None:
            with self._lock:
                token = self._token

        if token is not None:
            self._download_service.download(token, auth)

    def _download_start(self):
        self._cb_progress(0, 0)
        self._cb_state(PurchaseTrackerState.DOWNLOADING)

    def _download_finish(self, folder):
        with self._lock:
            self._folder = folder

        self._cb_state(PurchaseTrackerState.CAN_INSTALL)

    def _download_cancel(self):
        self._cb_state(PurchaseTrackerState.CAN_DOWNLOAD)

    def _download_error(self, exception):
        self._cb_error(exception)
        self._cb_state(PurchaseTrackerState.CAN_DOWNLOAD)

    def install(self, folder=None):
        '''Start the installation process.

        Args:
            folder (str): Folder with files to install.
                Optional if set by download finish or in constructor call.
        '''
        if folder is None:
            with self._lock:
                folder = self._folder

        if folder is not None:
            self._install_service.install(folder)

    def _install_start(self):
        self._cb_progress(0, 0)
        self._cb_state(PurchaseTrackerState.INSTALLING)

    def _install_finish(self, destinations):
        self._cb_install(destinations)
        self._cb_state(PurchaseTrackerState.FINISHED)

    def _install_cancel(self):
        self._cb_state(PurchaseTrackerState.CAN_INSTALL)

    def _install_error(self, exception):
        self._cb_error(exception)
        self._cb_state(PurchaseTrackerState.CAN_INSTALL)

    def cancel(self):
        self._purchase_service.cancel()
        self._download_service.cancel()
        self._install_service.cancel()

    @property
    def catalog(self):
        with self._lock:
            return self._catalog

    @property
    def product(self):
        with self._lock:
            return self._product

    @property
    def folder(self):
        with self._lock:
            return self._folder

    @property
    def token(self):
        with self._lock:
            return self._token

    @property
    def state(self):
        with self._lock:
            return self._state

    @property
    def progress(self):
        with self._lock:
            return self._progress

    @property
    def total(self):
        with self._lock:
            return self._total

    @abstractmethod
    def _cb_state(self, new_state):
        '''State change callback.

        Set `self._state` here.
        Don't forget to use `self._lock`.

        Args:
            new_state (PurchaseTrackerState): New purchase tracker state.
        '''
        pass

    @abstractmethod
    def _cb_filter(self, files):
        '''Download filter callback.

        Args:
            files (list of PurchaseTrackerFileModel) Downloadable files.

        Returns:
            list of PurchaseTrackerFileModel: Desired files to download.
        '''
        pass

    @abstractmethod
    def _cb_map(self, names):
        '''Install mapping callback.

        Args:
            names (list of str): Names of installable files.

        Returns:
            list of PurchaseTrackerMappingModel: Destinations and options.
        '''
        pass

    @abstractmethod
    def _cb_progress(self, progress, total):
        '''Download and install progress callback.

        Set `self._progress` and `self._total` here.
        Don't forget to use `self._lock`.

        Args:
            progress (int): Number of bytes progressed.
            total (int): Total number of bytes.
        '''
        pass

    @abstractmethod
    def _cb_install(self, destinations):
        '''Install finish callback. Called before state callback.

        Args:
            destinations (list of str): Destinations for the installed files.
        '''
        pass

    @abstractmethod
    def _cb_error(self, exception):
        '''Error callback. Called before state callback.

        Args:
            exception (Exception): Exception that occurred.
        '''
        pass
