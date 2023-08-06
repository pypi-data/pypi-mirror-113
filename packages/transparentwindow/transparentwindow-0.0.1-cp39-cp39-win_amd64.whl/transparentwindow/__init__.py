"""Transparent window

Example:
    import transparentwindow as tw

    tw.SetProcessDpiAwarenessContext()
    tw.show(callback=lambda key: print(key))

"""
__all__ = [
    "capture_transparentwindow",
    "screenshot",
    "SetProcessDpiAwarenessContext",
    "show",
]

import threading
from ctypes import POINTER
from ctypes import WINFUNCTYPE
from ctypes import c_longlong
from ctypes import windll
from ctypes.wintypes import BOOL
from ctypes.wintypes import HWND
from ctypes.wintypes import LPCWSTR
from ctypes.wintypes import POINT
from ctypes.wintypes import RECT
from typing import Any
from typing import Callable
from typing import Tuple

from transparentwindow import _screenshot
from transparentwindow import _transparentwindow


class WindowNotFoundError(Exception):
    pass


def show(
    hwnd: HWND = 0,
    width: int = 640,
    height: int = 480,
    title: str = "Window Title",
    callback: Callable[[int], Any] = None,
    close_callback: Callable[[], None] = None,
) -> None:
    """show a transparent window

    Note:
        This function runs with threading.Lock().
        For concurrent execution,
        please use multiprocessing module instead of threading module.
    """
    with threading.Lock():
        _transparentwindow.show(hwnd, width, height, title, callback)
        if callable(close_callback):
            close_callback()


def FindWindow(
    lpClassName: str = "Transparent_Window@Python", lpWindowName: str = "Window Title"
) -> HWND:
    """return hwnd"""
    prototype = WINFUNCTYPE(HWND, LPCWSTR, LPCWSTR)
    paramflags = (1, "lpClassName", lpClassName), (1, "lpWindowName", lpWindowName)
    FindWindowW = prototype(("FindWindowW", windll.user32), paramflags)
    hwnd = FindWindowW()
    if not hwnd:
        raise WindowNotFoundError("a window is requested but doesn’t exist")
    return hwnd


def SetProcessDpiAwarenessContext(dpiContext: int = -4) -> None:
    """Set the DPI awareness for the current process to the provided value"""
    prototype = WINFUNCTYPE(BOOL, c_longlong)
    paramflags = ((1, "value", dpiContext),)
    func = prototype(("SetProcessDpiAwarenessContext", windll.user32), paramflags)
    func()


def ClientToScreen(hwnd: HWND) -> Tuple[int, int]:
    """return x, y"""
    ClientToScreen_prototype = WINFUNCTYPE(BOOL, HWND, POINTER(POINT))
    ClientToScreen_paramflags = (1, "hwnd", hwnd), (2, "lpPoint")
    func = ClientToScreen_prototype(
        ("ClientToScreen", windll.user32), ClientToScreen_paramflags
    )
    point = func()
    return point.x, point.y


def GetClientRect(hwnd: HWND) -> Tuple[int, int]:
    """return width, height"""
    GetClientRect_prototype = WINFUNCTYPE(BOOL, HWND, POINTER(RECT))
    GetClientRect_paramflags = (1, "hwnd", hwnd), (2, "lprect")
    GetClientRect = GetClientRect_prototype(
        ("GetClientRect", windll.user32), GetClientRect_paramflags
    )
    rect = GetClientRect()
    return rect.right, rect.bottom


def GetWindowRect(hwnd: HWND) -> Tuple[int, int, int, int]:
    """return x, y, width, height"""
    GetWindowRect_prototype = WINFUNCTYPE(BOOL, HWND, POINTER(RECT))
    GetWindowRect_paramflags = (1, "hwnd", hwnd), (2, "lprect")
    GetWindowRect = GetWindowRect_prototype(
        ("GetWindowRect", windll.user32), GetWindowRect_paramflags
    )
    rect = GetWindowRect()
    return rect.left, rect.top, rect.right - rect.left, rect.bottom - rect.top


try:
    import cv2 as cv
    import numpy

    def screenshot(
        x: int = 0, y: int = 0, width: int = 640, height: int = 480
    ) -> numpy.ndarray:
        """return a screen image"""
        raw_data = _screenshot.screenshot(x, y, width, height)
        image = numpy.frombuffer(raw_data, dtype=numpy.uint8).reshape(
            (height, width, 4)
        )
        return cv.flip(cv.cvtColor(image, cv.COLOR_BGRA2BGR), 0)

    def capture_transparentwindow(title: str = "Window Title") -> numpy.ndarray:
        """return a transparentwindow image

        Example:
            img = transparentwindow.capture_transparentwindow("Window Title")
            cv2.imshow("img", img)
            cv2.waitKey(0)
        """
        hwnd = FindWindow(lpWindowName=title)
        x, y = ClientToScreen(hwnd)
        w, h = GetClientRect(hwnd)
        return screenshot(x, y, w, h)


except ImportError:
    pass
