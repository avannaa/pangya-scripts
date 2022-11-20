# @author aqua, sera

# image conversion imports
import cv2
import numpy

# screenshooter imports
import win32gui  # install pywin32
import win32ui
import win32con


BORDER_SIZE = 8  # left, right and bottom borders
TOP_BORDER = 31  # the top border contains the program name and thus must be treated differently


def find_windowhandle(program_title, winlist):
    window_handle = [(hwnd, title) for hwnd, title in winlist if program_title in title.lower()]
    window_handle = window_handle[0]
    return window_handle[0]


def remove_windows_borders(width, height):  # some hardcoding
    width -= BORDER_SIZE*2            # removes right, left
    height -= TOP_BORDER+BORDER_SIZE  # removes top, bottom
    return width, height

def get_og_dimensions(hwnd):
    l, t, r, b = win32gui.GetWindowRect(hwnd)
    width = r-l
    height = b-t

    return width, height


def take():
    toplist, winlist = [], []
    def enum_cb(hwnd, results):
        winlist.append((hwnd, win32gui.GetWindowText(hwnd)))

    win32gui.EnumWindows(enum_cb, toplist)

    pangya_hwnd = find_windowhandle('pangya ', winlist)
    width, height = get_og_dimensions(pangya_hwnd)
    width, height = remove_windows_borders(width, height)

    # magic
    dc = win32gui.GetWindowDC(pangya_hwnd)  # DC = Device Context
    dc = win32ui.CreateDCFromHandle(dc)
    compat_dc = dc.CreateCompatibleDC()

    screenshot = win32ui.CreateBitmap()
    screenshot.CreateCompatibleBitmap(dc, width, height)

    compat_dc.SelectObject(screenshot)
    compat_dc.BitBlt((0,0), (width,height), dc, (BORDER_SIZE,TOP_BORDER), win32con.SRCCOPY)
    
    # releases dc resources
    dc.DeleteDC()
    compat_dc.DeleteDC()

    # converts PyCBitmap to opencv-friendly numpy array, since we're working with opencv for all image processing
    signedIntsArray = screenshot.GetBitmapBits(True)
    img = numpy.fromstring(signedIntsArray, dtype='uint8')
    img.shape = (height, width, 4)

    img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)
    return img
