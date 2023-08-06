import Xlib
import Xlib.error
import ewmh
import os


def _focus_window(desktop, window):
    desktop.setWmState(window, 0, '_NET_WM_STATE_HIDDEN')
    desktop.setWmState(window, 0, '_NET_WM_STATE_BELOW')
    desktop.setWmState(window, 1, '_NET_WM_STATE_DEMANDS_ATTENTION')
    window.set_input_focus(Xlib.X.RevertToParent, Xlib.X.CurrentTime)
    desktop.setActiveWindow(window)
    desktop.display.flush()
    desktop.display.sync()


def _get_window_pid(desktop, window):
    try:
        return desktop.getWmPid(window)
    except TypeError:
        pass


def focus_process_window():
    pid = os.getpid()
    desktop = ewmh.EWMH()

    def _visit_window(window):
        try:
            if _get_window_pid(desktop, window) == pid:
                _focus_window(desktop, window)
                return True
            for child in window.query_tree().children:
                if _visit_window(child):
                    return True
        except Xlib.error.BadWindow:
            print('Focus/X11: Failed visiting window')

        return False

    return _visit_window(desktop.root)
