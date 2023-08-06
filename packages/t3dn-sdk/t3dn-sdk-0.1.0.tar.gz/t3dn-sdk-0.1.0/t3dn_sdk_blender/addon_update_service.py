import bpy
import os
import stat
import sys
import time
from collections import namedtuple
from pathlib import Path
from threading import Lock

import addon_utils
from t3dn_sdk_core.services.update_service import UpdateService
from t3dn_sdk_core.utils.purchase_tracker import (calculate_percentage,
                                                  convert_bytes_to_text)

from . import queue
from .ui import tag_redraw

_last_tag_redraw = time.time()


def _throttled_tag_redraw(force):
    global _last_tag_redraw
    now = time.time()
    if force or not _last_tag_redraw or (now - _last_tag_redraw) > 0.5:
        queue.put(tag_redraw)
        _last_tag_redraw = now


def _get_addon_name(caller_package):
    return caller_package.split('.')[0]


def _get_addon_version(name):
    return '.'.join([[str(i)
                      for i in addon.bl_info.get('version', (0, 0, 0))]
                     for addon in addon_utils.modules()
                     if addon.__name__ == name][0])


def _get_addons_dir(caller_file, caller_name):
    return Path(caller_file).parents[caller_name.count('.')].resolve()


def _retry(func, tries, ignore):
    for i in range(tries):
        try:
            func()
            break
        except:
            if i >= tries - 1:
                if not ignore:
                    raise
                return
            time.sleep(2)


def _rmtree(top):
    if not os.path.exists(top):
        return

    for root, dirs, files in os.walk(top, topdown=False):
        for name in files:
            filename = os.path.join(root, name)
            if os.path.exists(filename):
                _retry(lambda: os.chmod(filename, stat.S_IWUSR), 10, True)
                _retry(lambda: os.remove(filename), 10, False)
        for name in dirs:
            dirname = os.path.join(root, name)
            if os.path.exists(dirname):
                _retry(lambda: os.chmod(dirname, stat.S_IWUSR), 10, True)
                _retry(lambda: os.rmdir(dirname), 10, False)

    _retry(lambda: os.rmdir(top), 10, False)


AddonUpdateState = namedtuple('AddonUpdateState', [
    'update_version',
    'update_downloaded',
    'activity',
    'progress',
    'status_text',
])


class AddonUpdateService():

    def __init__(self, caller_file, caller_package, caller_name, product):
        self._addon = _get_addon_name(caller_package)
        self._addons_dir = _get_addons_dir(caller_file, caller_name)
        self._updates_dir = self._addons_dir.joinpath(
            '../addons_updates').resolve()

        self._service = UpdateService(
            product,
            self._addon,
            _get_addon_version(self._addon),
            self._updates_dir.joinpath('download'),
            self._cb_update_status,
            self._cb_download_progress,
            self._cb_download_completed,
            self._cb_extract_progress,
            self._cb_extract_completed,
            self._cb_error,
        )

        self._lock = Lock()
        self._update_version = None
        self._update_downloaded = False
        self._activity = None
        self._progress = None
        self._status_text = None

    def get_state(self):
        with self._lock:
            return AddonUpdateState(
                self._update_version,
                self._update_downloaded,
                self._activity,
                self._progress,
                self._status_text,
            )

    def _cb_update_status(self, version, downloaded):
        with self._lock:
            self._update_version = version
            self._update_downloaded = downloaded
        _throttled_tag_redraw(True)

    def _cb_download_progress(self, downloaded, total):
        with self._lock:
            self._activity = 'DOWNLOAD'
            self._progress = calculate_percentage(downloaded, total)
            self._status_text = '{} of {} downloaded'.format(
                convert_bytes_to_text(downloaded),
                convert_bytes_to_text(total),
            )
        _throttled_tag_redraw(False)

    def _cb_download_completed(self):
        with self._lock:
            self._activity = None
            self._progress = 0
            self._status_text = None
        _throttled_tag_redraw(True)

    def _cb_extract_progress(self, extracted, total):
        with self._lock:
            self._activity = 'INSTALL'
            self._progress = calculate_percentage(extracted, total)
            self._status_text = '{} of {} installed'.format(
                convert_bytes_to_text(extracted),
                convert_bytes_to_text(total),
            )
        _throttled_tag_redraw(False)

    def _cb_extract_completed(self, target):
        with self._lock:
            self._activity = 'INSTALL'
            self._progress = 100
            self._status_text = 'Activating new version...'
        _throttled_tag_redraw(True)

        def swap_addon():
            # Disable old addon
            print('Disabling add-on {}'.format(self._addon))
            addon_utils.disable(
                module_name=self._addon,
                default_set=False,
            )

            def swap_addon_2():
                # Ensure addon modules are purged
                for m in list(sys.modules.keys()):
                    if m == self._addon or m.startswith(self._addon + '.'):
                        print('Removing module {}'.format(m))
                        del sys.modules[m]

                # Delete old addon
                addon_dir = self._addons_dir.joinpath(self._addon)
                print('Deleting {}'.format(addon_dir))
                _rmtree(addon_dir)

                # Move new addon to addons folder
                new_addon_dir = target.joinpath(self._addon)
                print('Moving {} to {}'.format(new_addon_dir, self._addons_dir))
                os.makedirs(self._addons_dir, exist_ok=True)
                os.rename(new_addon_dir, self._addons_dir.joinpath(self._addon))
                _rmtree(target)

                # Refreshing addons
                print('Refreshing add-ons')
                bpy.ops.preferences.addon_refresh()

                # Enable new addon
                def swap_addon_3():
                    print('Enabling add-on {}'.format(self._addon))
                    addon_utils.enable(
                        module_name=self._addon,
                        default_set=True,
                        persistent=True,
                    )

                bpy.app.timers.register(swap_addon_3,
                                        first_interval=2,
                                        persistent=True)

            bpy.app.timers.register(swap_addon_2,
                                    first_interval=2,
                                    persistent=True)

        queue.put(swap_addon)

    def _cb_error(self, error):
        print(error)
        with self._lock:
            self._activity = 'ERROR'
            self._progress = 0
            self._status_text = str(error)

    def check(self):
        self._service.check()

    def download(self):
        self._service.download()

    def install(self):
        os.makedirs(self._updates_dir, exist_ok=True)
        self._service.extract(
            self._updates_dir.joinpath('extract_{}'.format(int(time.time()))))

    def cancel(self):
        self._service.cancel()
