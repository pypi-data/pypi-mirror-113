import sys
import os

_is_windows = False
_is_macos = False
_is_x11 = False

if sys.platform in ('win32', 'cygwin'):
    try:
        from . import windows
        _is_windows = True
    except ImportError:
        print('Focus: Could not activate Windows support')
    except Exception as e:
        print(e)
        print('Focus: Could not activate Windows support')

elif sys.platform == 'darwin':
    try:
        from . import macos
        _is_macos = True
    except ImportError:
        print('Focus: Could not activate macOS support')
    except Exception as e:
        print(e)
        print('Focus: Could not activate macOS support')

elif os.environ.get('DISPLAY'):
    try:
        from . import x11
        _is_x11 = True
    except ImportError:
        print('Focus: Could not activate X11 support')
    except Exception as e:
        print(e)
        print('Focus: Could not activate X11 support')


def focus_process_window():
    if _is_windows:
        return windows.focus_process_window()
    elif _is_macos:
        return macos.focus_application()
    elif _is_x11:
        return x11.focus_process_window()

    return False
