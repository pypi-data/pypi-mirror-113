import Xlib
import Xlib.X
import Xlib.display
import Xlib.error
import ewmh
from . import xrandr


def get_focused_workspace():
    desktop = ewmh.EWMH()
    # Try to get focused monitor via xrandr (will use its own display instance).
    try:
        monitors = xrandr.get_monitors()
        if monitors:
            cursor = desktop.root.query_pointer()
            for monitor in monitors:
                right = monitor['left'] + monitor['width']
                bottom = monitor['top'] + monitor['height']
                if (monitor['left'] <= cursor.root_x <
                        right) and (monitor['top'] <= cursor.root_y < bottom):
                    return monitor
            return monitors[0]
    except Exception:
        print('Browser/X11: Could not fetch monitors via XRandr')
    # Get desktop geometry via free desktop standard (fallback).
    geometry = desktop.getDesktopGeometry()
    return {
        'left': 0,
        'top': 0,
        'width': geometry[0],
        'height': geometry[1],
    }


def _center_window(desktop, window, width, height, workspace):
    desktop.setWmState(window, 0, '_NET_WM_STATE_MAXIMIZED_VERT')
    desktop.setWmState(window, 0, '_NET_WM_STATE_MAXIMIZED_HORZ')
    desktop.setWmState(window, 0, '_NET_WM_STATE_HIDDEN')
    desktop.setWmState(window, 0, '_NET_WM_STATE_BELOW')
    desktop.setWmState(window, 0, '_NET_WM_STATE_FULLSCREEN')
    desktop.setMoveResizeWindow(
        window,
        x=workspace['left'] + int((workspace['width'] - width) / 2),
        y=workspace['top'] + int((workspace['height'] - height) / 2),
        w=width,
        h=height,
    )
    desktop.setWmState(window, 1, '_NET_WM_STATE_DEMANDS_ATTENTION')
    window.set_input_focus(Xlib.X.RevertToParent, Xlib.X.CurrentTime)
    desktop.setActiveWindow(window)
    desktop.display.flush()
    desktop.display.sync()


def _get_window_title(desktop, window):
    return str(desktop.getWmName(window) or window.get_wm_name() or '')


def find_and_center_window(title, width, height, workspace):
    desktop = ewmh.EWMH()

    def _visit_window(window):
        try:
            if title in _get_window_title(desktop, window):
                _center_window(desktop, window, width, height, workspace)
                return True
            for child in window.query_tree().children:
                if _visit_window(child):
                    return True
        except Xlib.error.BadWindow:
            print('Browser/X11: Failed visiting window')

        return False

    return _visit_window(desktop.root)
