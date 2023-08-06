import ctypes
import ctypes.util
from ctypes import (
    POINTER,
    CFUNCTYPE,
    Structure,
    c_char_p,
    c_int,
    c_int32,
    c_long,
    c_ubyte,
    c_uint,
    c_uint32,
    c_ulong,
    c_ushort,
    c_void_p,
)


class _Display(Structure):
    pass


class _Event(Structure):
    _fields_ = [
        ('type', c_int),
        ('display', POINTER(_Display)),
        ('serial', c_ulong),
        ('error_code', c_ubyte),
        ('request_code', c_ubyte),
        ('minor_code', c_ubyte),
        ('resourceid', c_void_p),
    ]


class _XWindowAttributes(Structure):
    _fields_ = [
        ('x', c_int32),
        ('y', c_int32),
        ('width', c_int32),
        ('height', c_int32),
        ('border_width', c_int32),
        ('depth', c_int32),
        ('visual', c_ulong),
        ('root', c_ulong),
        ('class', c_int32),
        ('bit_gravity', c_int32),
        ('win_gravity', c_int32),
        ('backing_store', c_int32),
        ('backing_planes', c_ulong),
        ('backing_pixel', c_ulong),
        ('save_under', c_int32),
        ('colourmap', c_ulong),
        ('mapinstalled', c_uint32),
        ('map_state', c_uint32),
        ('all_event_masks', c_ulong),
        ('your_event_mask', c_ulong),
        ('do_not_propagate_mask', c_ulong),
        ('override_redirect', c_int32),
        ('screen', c_ulong),
    ]


class _XRRModeInfo(Structure):
    pass


class _XRRScreenResources(Structure):
    _fields_ = [
        ('timestamp', c_ulong),
        ('configTimestamp', c_ulong),
        ('ncrtc', c_int),
        ('crtcs', POINTER(c_long)),
        ('noutput', c_int),
        ('outputs', POINTER(c_long)),
        ('nmode', c_int),
        ('modes', POINTER(_XRRModeInfo)),
    ]


class _XRRCrtcInfo(Structure):
    _fields_ = [
        ('timestamp', c_ulong),
        ('x', c_int),
        ('y', c_int),
        ('width', c_int),
        ('height', c_int),
        ('mode', c_long),
        ('rotation', c_int),
        ('noutput', c_int),
        ('outputs', POINTER(c_long)),
        ('rotations', c_ushort),
        ('npossible', c_int),
        ('possible', POINTER(c_long)),
    ]


_ERROR = None


@CFUNCTYPE(c_int, POINTER(_Display), POINTER(_Event))
def _error_handler(_, event):
    global _ERROR
    evt = event.contents
    _ERROR = {
        'type': evt.type,
        'serial': evt.serial,
        'error_code': evt.error_code,
        'request_code': evt.request_code,
        'minor_code': evt.minor_code,
    }
    return 0


def _error_check(retval, func, args):
    global _ERROR
    details = _ERROR
    _ERROR = None
    if retval != 0 and not details:
        return args
    raise Exception('{}() failed'.format(func.__name__),
                    details={
                        'retval': retval,
                        'args': args,
                        'details': details
                    })


xlib = None
xrandr = None


def _initialize():
    global xlib
    global xrandr

    # Setup X11 library.
    if xlib is None:
        # Load library.
        xlib_name = ctypes.util.find_library('X11')
        if not xlib_name:
            raise Exception('No X11 library found.')
        xlib = ctypes.cdll.LoadLibrary(xlib_name)

        # Configure library.
        xlib.XSetErrorHandler.argtypes = [c_void_p]
        xlib.XSetErrorHandler.restype = c_int
        xlib.XSetErrorHandler(_error_handler)

        xlib.XDefaultRootWindow.argtypes = [POINTER(_Display)]
        xlib.XDefaultRootWindow.restype = POINTER(_XWindowAttributes)
        xlib.XDefaultRootWindow.errcheck = _error_check

        xlib.XOpenDisplay.argtypes = [c_char_p]
        xlib.XOpenDisplay.restype = POINTER(_Display)
        xlib.XOpenDisplay.errcheck = _error_check

        xlib.XQueryExtension.argtypes = [
            POINTER(_Display),
            c_char_p,
            POINTER(c_int),
            POINTER(c_int),
            POINTER(c_int),
        ]
        xlib.XQueryExtension.restype = c_uint
        xlib.XQueryExtension.errcheck = _error_check

    # Setup Xrandr library.
    if xrandr is None:
        # Load library.
        xrandr_name = ctypes.util.find_library('Xrandr')
        if not xrandr_name:
            raise Exception('No Xrandr extension found.')
        xrandr = ctypes.cdll.LoadLibrary(xrandr_name)

        # Configure library.
        xrandr.XRRFreeCrtcInfo.argtypes = [POINTER(_XRRCrtcInfo)]
        xrandr.XRRFreeCrtcInfo.restype = c_void_p
        xrandr.XRRFreeCrtcInfo.errcheck = _error_check

        xrandr.XRRFreeScreenResources.argtypes = [POINTER(_XRRScreenResources)]
        xrandr.XRRFreeScreenResources.restype = c_void_p
        xrandr.XRRFreeScreenResources.errcheck = _error_check

        xrandr.XRRGetCrtcInfo.argtypes = [
            POINTER(_Display),
            POINTER(_XRRScreenResources), c_long
        ]
        xrandr.XRRGetCrtcInfo.restype = POINTER(_XRRCrtcInfo)
        xrandr.XRRGetCrtcInfo.errcheck = _error_check

        xrandr.XRRGetScreenResources.argtypes = [
            POINTER(_Display), POINTER(_Display)
        ]
        xrandr.XRRGetScreenResources.restype = POINTER(_XRRScreenResources)
        xrandr.XRRGetScreenResources.errcheck = _error_check

        xrandr.XRRGetScreenResourcesCurrent.argtypes = [
            POINTER(_Display), POINTER(_Display)
        ]
        xrandr.XRRGetScreenResourcesCurrent.restype = POINTER(
            _XRRScreenResources)
        xrandr.XRRGetScreenResourcesCurrent.errcheck = _error_check


def _has_extension(display, extension):
    major_opcode_return = c_int()
    first_event_return = c_int()
    first_error_return = c_int()
    try:
        xlib.XQueryExtension(
            display,
            extension.encode('latin1'),
            ctypes.byref(major_opcode_return),
            ctypes.byref(first_event_return),
            ctypes.byref(first_error_return),
        )
    except Exception:
        return False
    else:
        return True


def get_monitors():
    # Ensure we are initialized.
    _initialize()

    # Get display and root window.
    display = xlib.XOpenDisplay(c_char_p(0))
    root = xlib.XDefaultRootWindow(display)

    # Ensure RANDR extension is available.
    if not _has_extension(display, 'RANDR'):
        raise Exception('Xrandr extension not found.')

    # Get screen resources.
    try:
        res = xrandr.XRRGetScreenResourcesCurrent(
            display, ctypes.cast(root, POINTER(_Display))).contents
    except AttributeError:
        res = xrandr.XRRGetScreenResources(
            display, ctypes.cast(root, POINTER(_Display))).contents

    # Iterate monitors.
    monitors = []
    try:
        for i in range(res.ncrtc):
            # Fetch monitor info.
            mon = xrandr.XRRGetCrtcInfo(display, res, res.crtcs[i]).contents
            try:
                if mon.noutput != 0:
                    monitors.append({
                        'left': int(mon.x),
                        'top': int(mon.y),
                        'width': int(mon.width),
                        'height': int(mon.height),
                    })
            finally:
                xrandr.XRRFreeCrtcInfo(mon)
    finally:
        xrandr.XRRFreeScreenResources(res)

    return monitors
