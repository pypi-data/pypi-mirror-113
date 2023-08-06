import ctypes
from ctypes import wintypes

shcore = ctypes.windll.shcore
user32 = ctypes.windll.user32
shlwapi = ctypes.OleDLL('shlwapi')
WNDENUMPROC = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)


def get_default_browser_path():
    '''
    On windows, return the default browser for 'https' urls
    returns: example '"C:\\Program Files\\Mozilla Firefox\\firefox.exe" -osint -url "%1"'
    '''
    # The array gets nitialized to zero automatically. Use + 1 to ensure
    # a '\0' character at the end.
    size = wintypes.DWORD(1024)
    cmd = (ctypes.c_wchar * (size.value + 1))()
    # get command associated to html files
    if not shlwapi.AssocQueryStringW(0x400, 1, u'.html', u'open', cmd,
                                     ctypes.byref(size)) == 0:
        return None
    cmd = cmd.value
    if not cmd:
        return None
    # Extract executable path from command.
    quotes = cmd[0] == '"'
    end = cmd.find('"' if quotes else ' ', 1)
    if end == -1:
        return cmd[1 if quotes else 0:]
    return cmd[1 if quotes else 0:end]


def _get_windows():
    windows = []

    def enum_cb(hwnd, lparam):
        length = user32.GetWindowTextLengthW(hwnd) + 1
        buffer = ctypes.create_unicode_buffer(length)
        if user32.GetWindowTextW(hwnd, buffer, length) != 0:
            windows.append((
                hwnd,
                buffer.value,
            ))
        return True

    user32.EnumWindows(WNDENUMPROC(enum_cb), 0)
    return windows


def _find_window(title):
    match = [wnd for wnd in _get_windows() if title.lower() in wnd[1].lower()]
    if match:
        return match[0][0]


def _get_focused_monitor():
    '''
    Get the monitor based on the cursor location.
    '''
    point = ctypes.wintypes.POINT(0, 0)
    user32.GetCursorPos(ctypes.byref(point))
    return user32.MonitorFromPoint(point, 0x00000002)


def _get_windows_scale(monitor):
    '''
    Get the size of the apps and text.
    '''
    # TODO: Set the process to be DPI aware temporarily in case it's not.
    scale = ctypes.c_int(0)
    shcore.GetScaleFactorForMonitor(monitor, ctypes.byref(scale))
    return scale.value / 100


def get_focused_workspace():
    monitor = _get_focused_monitor()

    # get workspace of monitor
    class _RECT(ctypes.Structure):
        _fields_ = [
            ('left', wintypes.LONG),
            ('top', wintypes.LONG),
            ('right', wintypes.LONG),
            ('bottom', wintypes.LONG),
        ]

    class _MONITORINFO(ctypes.Structure):
        _fields_ = [
            ('size', wintypes.DWORD),
            ('monitor', _RECT),
            ('work', _RECT),
            ('flags', wintypes.DWORD),
        ]

    info = _MONITORINFO(
        ctypes.sizeof(_MONITORINFO),
        _RECT(0, 0, 0, 0),
        _RECT(0, 0, 0, 0),
        0,
    )

    if user32.GetMonitorInfoW(monitor, ctypes.byref(info)):
        return {
            'scale': _get_windows_scale(monitor),
            'workspace': info.work,
        }


def _center_window(wnd, width, height, workspace):
    # scale, workspace = workspace['scale'], workspace['workspace']
    # width = min(int(width * scale), workspace.right - workspace.left)
    # height = min(int(height * scale), workspace.bottom - workspace.top)
    # user32.ShowWindow(wnd, 1)
    # succeeded = user32.MoveWindow(
    #     wnd,
    #     ctypes.c_int(int((workspace.left + workspace.right - width) / 2)),
    #     ctypes.c_int(int((workspace.top + workspace.bottom - height) / 2)),
    #     width,
    #     height,
    #     1,
    # )
    # return succeeded and user32.SetForegroundWindow(wnd)
    return user32.SetForegroundWindow(wnd)


def find_and_center_window(title, width, height, workspace):
    wnd = _find_window(title)
    return wnd and _center_window(wnd, width, height, workspace)
