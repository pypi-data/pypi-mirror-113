import os, shutil, time
from zipfile import ZipFile, is_zipfile
from threading import Event, Lock
from multiprocessing.dummy import Pool as ThreadPool


class PurchaseTrackerInstallService(object):
    '''Service for installing purchase tracker files.'''

    def __init__(
        self,
        cb_start,
        cb_map,
        cb_progress,
        cb_finish,
        cb_cancel,
        cb_error,
    ):
        '''Initialize install service.

        Args:
            cb_start (function): Function that gets called to confirm
                install has started, takes no arguments.
            cb_map (function): Function that maps files to destinations,
                takes list of file names,
                returns list of PurchaseTrackerMappingModel.
            cb_progress (function): Function that gets called when progress
                is updated, takes number of bytes for progress and total.
            cb_finish (function): Function that gets called when install
                is finished, takes list of destination paths,
                including files that were inside zip files.
            cb_cancel (function): Function that gets called to confirm
                installtion is cancelled, takes no arguments.
            cb_error (function): Function that gets called if an error
                occurs, takes exception.
        '''
        self._cb_start = cb_start
        self._cb_map = cb_map
        self._cb_progress = cb_progress
        self._cb_finish = cb_finish
        self._cb_cancel = cb_cancel
        self._cb_error = cb_error

        self._total = None  # Total number of bytes to install.
        self._progress = None  # Total number of bytes installed.
        self._destinations = None  # List of paths for installed files.

        self._lock = Lock()
        self._result = None
        self._cancel = Event()
        self._pool = ThreadPool(4)

    def install(self, folder):
        '''Start the installation process.

        Args:
            folder (str): Folder with files to install.
        '''
        if self._result is None or self._result.ready():
            self._cancel.clear()

            self._result = self._pool.apply_async(
                func=self._install,
                args=(folder,),
                error_callback=self._cb_error,
            )

    def _install(self, folder):
        self._cb_start()

        self._total = 0
        self._progress = 0
        self._destinations = []

        _, _, names = next(os.walk(folder))
        paths = [os.path.join(folder, name) for name in names]
        mappings = self._cb_map(names)

        if len(paths) != len(mappings):
            raise Exception('there must be one mapping per path')

        self._pool.map(
            func=self._get_size,
            iterable=paths,
        )

        self._pool.starmap(
            func=self._prepare_destination,
            iterable=zip(paths, mappings),
        )

        result = self._pool.starmap_async(
            func=self._install_file,
            iterable=zip(paths, mappings),
            error_callback=print,
        )

        while not result.ready():
            time.sleep(0.25)

            with self._lock:
                self._cb_progress(self._progress, self._total)

        result.get()  # If an exception occurred, this will raise it.
        self._remove_folder(folder)  # Remove temp folder regardless of cancel.

        if self._cancel.is_set():
            self._cb_cancel()
        else:
            self._cb_finish(self._destinations)

    def _get_size(self, path):
        if self._cancel.is_set():
            return

        if is_zipfile(path):
            with ZipFile(path) as zfile:
                size = sum(zinfo.file_size for zinfo in zfile.filelist)
        else:
            size = os.path.getsize(path)

        with self._lock:
            self._total += size

    def _prepare_destination(self, path, mapping):
        if self._cancel.is_set():
            return

        if mapping.clear_subdirs and is_zipfile(path):
            with ZipFile(path) as zfile:
                folders = map(os.path.dirname, zfile.namelist())

                for folder in filter(bool, set(folders)):
                    if self._cancel.is_set():
                        return

                    destination = os.path.join(mapping.folder, folder)
                    if os.path.isdir(destination):
                        shutil.rmtree(destination)

    def _install_file(self, path, mapping):
        if self._cancel.is_set():
            return

        if is_zipfile(path):
            with ZipFile(path) as zfile:
                for zinfo in zfile.filelist:
                    if self._cancel.is_set():
                        return

                    if not zinfo.is_dir():
                        name = zinfo.filename
                        destination = os.path.join(mapping.folder, name)

                        zfile.extract(zinfo, mapping.folder)
                        size = os.path.getsize(destination)

                        with self._lock:
                            self._destinations.append(destination)
                            self._progress += size

            os.remove(path)

        else:
            if not os.path.isdir(mapping.folder):
                os.mkdir(mapping.folder)

            name = os.path.basename(path)
            destination = os.path.join(mapping.folder, name)

            if os.path.isfile(destination):
                os.remove(destination)

            shutil.move(path, destination)
            size = os.path.getsize(destination)

            with self._lock:
                self._destinations.append(destination)
                self._progress += size

    def _remove_folder(self, folder):
        if os.path.isdir(folder):
            try:
                shutil.rmtree(folder)
            except Exception as e:
                print(e)

    def cancel(self):
        '''Cancel the install process.'''
        self._cancel.set()
