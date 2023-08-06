import os
import os.path
import shutil
from multiprocessing.dummy import Pool as ThreadPool
from threading import Event, Lock
from zipfile import ZipFile

import requests
from requests.exceptions import RequestException

from ..api.update import UpdateAPI


class UpdateService(object):

    def __init__(
        self,
        product,
        package,
        current,
        download_cache,
        cb_update_status,
        cb_download_progress,
        cb_download_completed,
        cb_extract_progress,
        cb_extract_completed,
        cb_error,
    ):
        self._product = product
        self._package = package
        self._current = current
        self._download_cache = download_cache
        self._cb_update_status = cb_update_status
        self._cb_download_progress = cb_download_progress
        self._cb_download_completed = cb_download_completed
        self._cb_extract_progress = cb_extract_progress
        self._cb_extract_completed = cb_extract_completed
        self._cb_error = cb_error
        self._update = None
        self._pool = ThreadPool(2)
        self._cancel = Event()
        self._lock = Lock()
        self._result = None

    def check(self):
        with self._lock:
            if self._result and not self._result.ready():
                return

            self._cancel.clear()
            self._result = self._pool.apply_async(
                func=self._check,
                args=(self._product, self._package, self._current),
                error_callback=print,
            )

    def _check(self, product, package, current):
        if self._cancel.is_set():
            return

        update = UpdateAPI().check(product, package, current)

        with self._lock:
            if update['available']:
                self._update = {
                    'version': update['version'],
                    'name': update['name'],
                    'url': update['url'],
                }

                path = os.path.join(self._download_cache, update['name'])
                self._cb_update_status(
                    update['version'],
                    os.path.exists(path),
                )

            else:
                self._update = None

    def download(self):
        with self._lock:
            if not self._update or (self._result and not self._result.ready()):
                return

            os.makedirs(self._download_cache, exist_ok=True)

            version = self._update['version']
            url = self._update['url']
            path = os.path.join(self._download_cache, self._update['name'])

            self._cancel.clear()
            self._result = self._pool.apply_async(
                func=self._download,
                args=(version, path, url),
                error_callback=self._cb_error,
            )

    def _download(self, version, path, url):
        if self._cancel.is_set():
            return

        # Delete existing files
        path_tmp = path + '.download'

        try:
            os.remove(path)
        except OSError:
            pass

        try:
            os.remove(path_tmp)
        except OSError:
            pass

        print("Downloading {} to {}".format(url, path))

        # Get file size
        response = requests.head(url=url, timeout=60)
        response.raise_for_status()

        total = int(response.headers['Content-Length'])
        self._cb_download_progress(0, total)

        # Download file
        response = requests.get(url=url, stream=True, timeout=60)
        response.raise_for_status()

        downloaded = 0

        with open(path_tmp, 'wb') as file:
            for data in response.iter_content(chunk_size=1024 * 1024):
                if self._cancel.is_set():
                    return

                file.write(data)
                downloaded += len(data)
                self._cb_download_progress(downloaded, total)

        if downloaded != total:
            raise RequestException('File size does not match header')

        os.rename(path_tmp, path)

        self._cb_download_completed()
        self._cb_update_status(version, True)

    def extract(self, target):
        with self._lock:
            if not self._update or (self._result and not self._result.ready()):
                return

            path = os.path.join(self._download_cache, self._update['name'])
            if not os.path.exists(path):
                return

            self._cancel.clear()
            self._result = self._pool.apply_async(
                func=self._extract,
                args=(path, target),
                error_callback=self._cb_error,
            )

    def _extract(self, path, target):
        if self._cancel.is_set():
            return

        print("Extracting {} to {}".format(path, target))

        # clear subfolders
        with ZipFile(path) as zip:
            folders = map(os.path.dirname, zip.namelist())

            for folder in filter(bool, set(folders)):
                if self._cancel.is_set():
                    return

                destination = os.path.join(target, folder)
                if os.path.isdir(destination):
                    shutil.rmtree(destination)

        # determine total size
        with ZipFile(path) as zfile:
            total = sum(zinfo.file_size for zinfo in zfile.filelist)
        self._cb_extract_progress(0, total)

        # extract files
        extracted = 0
        with ZipFile(path) as zip:
            for info in zip.filelist:
                if self._cancel.is_set():
                    return

                if not info.is_dir():
                    name = info.filename
                    destination = os.path.join(target, name)

                    zip.extract(info, target)
                    extracted += os.path.getsize(destination)
                    self._cb_extract_progress(extracted, total)

        self._cb_extract_completed(target)

    def cancel(self):
        self._cancel.set()
