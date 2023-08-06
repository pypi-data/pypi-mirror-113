import os
import subprocess
import sys
import webbrowser
import threading
import time
import uuid
from .webserver import create_transaction

_is_windows = False
_is_macos = False
_is_x11 = False

if sys.platform in ('win32', 'cygwin'):
    try:
        from . import windows
        _is_windows = True
    except ImportError:
        print('Browser: Could not activate Windows support')
    except Exception as e:
        print(e)
        print('Browser: Could not activate Windows support')

elif sys.platform == 'darwin':
    try:
        from . import macos
        _is_macos = True
    except ImportError:
        print('Browser: Could not activate macOS support')
    except Exception as e:
        print(e)
        print('Browser: Could not activate macOS support')

elif os.environ.get('DISPLAY'):
    try:
        from . import x11
        _is_x11 = True
    except ImportError:
        print('Browser: Could not activate X11 support')
    except Exception as e:
        print(e)
        print('Browser: Could not activate X11 support')


def _which(program):
    '''
    Get the path to the web browser executable. This is a replacement of
        `shutil.which` as it's not available in python 2.7.

    Args:
        program (str): Name of the program to get the path

    Returns:
        The path to the default browser.
    '''
    path = os.getenv('PATH')

    for get_path in path.split(os.path.pathsep):
        get_path = os.path.join(get_path, program)

        if os.path.exists(get_path) and os.access(get_path, os.X_OK):
            return get_path


_x11_openers = [
    'xdg-open',
    'sensible-browser',
    'x-www-browser',
    'gnome-open',
    'kde-open',
]


def _open_browser_fallback(url):
    '''
    Launch the default system browser.

    Args:
        url (url): The URL.
    '''

    if _is_windows or sys.platform.startswith('win32'):
        print('Browser/Fallback: os.startfile url={0}'.format(url))
        os.startfile(url)
        return True

    elif _is_macos or sys.platform.startswith('darwin'):
        opener_path = _which('open')
        if opener_path:
            print('Browser/Fallback: Launching open {0}'.format(url))
            with open(os.devnull, 'wb') as devnull:
                return subprocess.Popen(['open', url],
                                        stdout=devnull,
                                        stderr=devnull).poll() in (None, 0)
        return False

    elif _is_x11 or sys.platform.startswith('linux'):
        for opener in _x11_openers:
            opener_path = _which(opener)
            if opener_path:
                print('Browser/Fallback: Launching {0} {1}'.format(
                    opener_path, url))
                with open(os.devnull, 'wb') as devnull:
                    return subprocess.Popen([opener_path, url],
                                            stdout=devnull,
                                            stderr=devnull).poll() in (None, 0)
        return False

    return False


_supported_browsers = {
    'brave': ['--new-window', '{url}'],
    'firefox': ['-new-window', '{url}'],
    'chrome': ['--new-window', '--app={url}'],
    'chromium': ['--new-window', '--app={url}'],
    'msedge': ['--new-window', '{url}'],  # App mode does not work with paypal.
    'opera': ['--new-window', '{url}'],
    'vivaldi': ['--new-window', '{url}'],
}

_macos_supported_browsers = {
    'chrome': _supported_browsers['chrome'],
}


def _open_new_browser_window(url):

    # Find default browser
    if _is_windows:
        browser = windows.get_default_browser_path()
    elif _is_macos:
        browser = macos.get_default_browser_path()
    else:
        browser = webbrowser.get().basename
        if browser:
            browser = _which(browser)

    if not browser:
        return False

    # Generate detect token
    token = os.path.join(
        os.path.basename(os.path.dirname(browser)),
        os.path.basename(browser),
    ).lower()

    # Find out if we support that browser
    if _is_macos:
        supported = _macos_supported_browsers
    else:
        supported = _supported_browsers

    args = []
    for name, args in supported.items():
        if name in token:
            break
    else:
        return False

    args = [arg.format(url=url) for arg in args]

    # Launch browser
    if _is_macos:
        args = ['open', '-n', '-a', browser, '--args'] + args
    else:
        args = [browser] + args

    try:
        print('Browser/Supported: Launching {0}'.format(' '.join(args)))
        with open(os.devnull, 'wb') as devnull:
            if subprocess.Popen(args, stdout=devnull,
                                stderr=devnull).poll() not in (None, 0):
                return False
    except OSError:
        return False

    return True


def popup_url(url, detect_title, apply_size, workspace):
    '''
    Open the provided URL in the web browser, preferably in a dialog manner.
    Try to center the browser window.

    Args:
        url (str): URL to be opened in the web browser.
        detect_title (str): Title used to detect the web browser window.
        apply_size (tuple): Set width and height of web browser window.
        workspace: Target workspace for the web browser window.
    '''

    # Create a local url and an event we can wait for
    trx_event, local_url = create_transaction(url, detect_title)

    # Launch browser
    # new_window = _open_new_browser_window(local_url)
    # if not new_window:
    if not _open_browser_fallback(local_url):
        raise Exception('Could not launch browser')

    # Wait for the success signal
    if not trx_event.wait(60):
        raise Exception('Browser did not open')

    # Lets try to find and center the window
    find_and_center_window = None

    if _is_windows:
        find_and_center_window = windows.find_and_center_window
    # elif _is_x11:
    #     find_and_center_window = x11.find_and_center_window

    # if new_window and find_and_center_window:
    if find_and_center_window:

        def find_and_center_window_thread():
            print('Browser: Finding and centering window...')
            start = time.time()
            while True:
                # Find and center the window
                if find_and_center_window(
                        detect_title,
                        apply_size[0],
                        apply_size[1],
                        workspace,
                ):
                    print('Browser: Window successfuly centered')
                    return
                # No result yet, wait a bit.
                time.sleep(0.1)
                # If we waited more than x seconds, we just stop doing it.
                if (time.time() - start) >= 30:
                    print('Browser: Could not find window')
                    return

        thread = threading.Thread(target=find_and_center_window_thread)
        thread.start()


def get_focused_workspace():
    if _is_windows:
        return windows.get_focused_workspace()

    elif _is_x11:
        return x11.get_focused_workspace()

    return None
