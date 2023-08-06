import os, requests, shutil, tempfile, time
from threading import Event, Lock
from multiprocessing.dummy import Pool as ThreadPool
from ...utils.decorators import retry
from ...utils.purchase_tracker import convert_bytes_to_text
from ...exceptions.api_exception import APIException
from requests.exceptions import RequestException, HTTPError
from ...api.purchase_tracker import PurchaseTrackerAPI


class PurchaseTrackerDownloadService(object):
    '''Service for downloading purchase tracker files.'''

    def __init__(
        self,
        cb_start,
        cb_filter,
        cb_progress,
        cb_finish,
        cb_cancel,
        cb_error,
    ):
        '''Initialize download service.

        Args:
            cb_start (function): Function that gets called to confirm
                download has started, takes no arguments.
            cb_filter (function): Function that filters files to download
                by name or URL, takes list of PurchaseTrackerFileModel,
                returns list with only the desired files.
            cb_progress (function): Function that gets called when progress
                is updated, takes number of bytes for progress and total.
            cb_finish (function): Function that gets called when download
                is finished, takes download folder path.
            cb_cancel (function): Function that gets called to confirm
                purchase is cancelled, takes no arguments.
            cb_error (function): Function that gets called if an error
                occurs, takes exception.
        '''
        self._cb_start = cb_start
        self._cb_filter = cb_filter
        self._cb_progress = cb_progress
        self._cb_finish = cb_finish
        self._cb_cancel = cb_cancel
        self._cb_error = cb_error

        self._total = None  # Number of bytes to download per file.
        self._progress = None  # Number of bytes downloaded per file.

        self._lock = Lock()
        self._result = None
        self._cancel = Event()
        self._pool = ThreadPool(4)

    def download(self, token, auth=None):
        '''Start the download process.

        Args:
            token (str): Purchase tracker token.
            auth (dict): The credentials optionally used to access this route.
        '''
        if self._result is None or self._result.ready():
            self._cancel.clear()

            self._result = self._pool.apply_async(
                func=self._download,
                args=(token, auth),
                error_callback=self._cb_error,
            )

    def _download(self, token, auth):
        self._cb_start()

        self._total = {}
        self._progress = {}

        folder = tempfile.mkdtemp()
        files = self._cb_filter(self._get_files(token, auth))

        urls = [file.url for file in files]
        paths = [os.path.join(folder, file.filename) for file in files]

        self._pool.map(
            func=self._fetch_header,
            iterable=urls,
        )

        result = self._pool.starmap_async(
            func=self._download_file,
            iterable=zip(urls, paths),
        )

        while not result.ready():
            time.sleep(0.1)

            with self._lock:
                total = sum(self._total.values())
                progress = sum(self._progress.values())
                self._cb_progress(progress, total)

        result.get()  # If an exception occurred, this will raise it.

        if self._cancel.is_set():
            self._remove_folder(folder)
            self._cb_cancel()
        else:
            self._cb_finish(folder)

    @retry((APIException, RequestException, HTTPError), logging=True)
    def _get_files(self, token, auth):
        if self._cancel.is_set():
            return []

        return PurchaseTrackerAPI().get_files(
            token=token,
            auth=auth,
        )

    @retry((APIException, RequestException, HTTPError), logging=True)
    def _fetch_header(self, url):
        if self._cancel.is_set():
            return

        response = requests.head(url=url, timeout=60)
        response.raise_for_status()

        size = int(response.headers['Content-Length'])

        with self._lock:
            self._total[url] = size

    @retry(
        (APIException, RequestException, HTTPError),
        logging=True,
        use_reset=True,
    )
    def _download_file(self, url, path, cb_reset):
        if self._cancel.is_set():
            return

        file_mode = 'wb'

        with self._lock:
            write_total = self._total.get(url, 0)
            write_progress = self._progress.get(url, 0)

        if write_progress:
            response = requests.get(
                url=url,
                stream=True,
                timeout=60,
                headers={'Range': 'bytes={}-'.format(write_progress)},
            )

            if response.status_code == 206:
                progress_text = convert_bytes_to_text(write_progress, ndigits=2)
                print('Resuming download at {}'.format(progress_text))
                file_mode = 'ab'

            else:
                write_progress = 0

                if response.status_code == 200:
                    print('Range request ignored, restarting download')

                elif response.status_code == 416:
                    print('Range request failed, restarting download')
                    response = requests.get(url=url, stream=True, timeout=60)

        else:
            response = requests.get(url=url, stream=True, timeout=60)

        response.raise_for_status()
        cb_reset()

        with open(path, file_mode) as file:
            for data in response.iter_content(chunk_size=1024):
                if self._cancel.is_set():
                    return

                file.write(data)
                write_progress += len(data)

                with self._lock:
                    self._progress[url] = write_progress

        if write_progress != write_total:
            raise RequestException('File size does not match header')

    def _remove_folder(self, folder):
        if os.path.isdir(folder):
            try:
                shutil.rmtree(folder)
            except Exception as e:
                print(e)

    def cancel(self):
        '''Cancel the download process.'''
        self._cancel.set()
