import ctypes
from ctypes import wintypes
import time

kernel32 = ctypes.windll.kernel32
user32 = ctypes.windll.user32

WNDENUMPROC = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)


def focus_process_window():

    this_pid = kernel32.GetCurrentProcessId()
    this_hwnds = []

    def visitor(hwnd, lparam):
        nonlocal this_hwnds
        if user32.IsWindowVisible(hwnd):
            hwnd_pid = wintypes.DWORD()
            user32.GetWindowThreadProcessId(hwnd, ctypes.byref(hwnd_pid))
            if this_pid == hwnd_pid.value:
                this_hwnds.append(hwnd)
        return True

    if not user32.EnumWindows(WNDENUMPROC(visitor), 0):
        print('EnumWindows failed')
        return False

    if not this_hwnds:
        print('window not found')
        return False

    for this_hwnd in this_hwnds:
        try:
            user32.SwitchToThisWindow(this_hwnd, 1)
            print('switched to window')
        except:
            print('NOT switched to window')
        time.sleep(0.1)

    return True
