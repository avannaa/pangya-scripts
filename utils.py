import const
import screenshot

import cv2
import ctypes
import time
import math
import scipy.interpolate
import numpy
import skimage.morphology
import wmi  # for s4-check by process name
import memory
import pythoncom

time_on = False


def timeprint(s):
    if time_on:
        print(s)


def clamp(n, min_n, max_n):
    return max(min(max_n, n), min_n)


def check_if_s4():
    pythoncom.CoInitialize()
    w = wmi.WMI()
    is_s4 = False
    if len(w.Win32_Process(name="ProjectG.exe")) == 1:
        is_s4 = True
    return is_s4


def cal_p_to_index(p):
    return 500.0 - (100.0-p)*3.6

def cal_index_to_p(i):
    return (i-140)/3.6


# angle utils
def angle_and_quad_from_sin_cos(sin, cos, fit_to_90=True, transpose=True):  # gets quad
    sin = clamp(sin, -1, +1)
    cos = clamp(cos, -1, +1)
    if sin >= 0 and cos <= 0:
        q = 1
    elif sin >= 0 and cos >= 0:
        q = 2
    elif sin <= 0 and cos <= 0:
        q = 3
    else:
        q = 4

    if fit_to_90:  # fit result into a 0-90 range
        sin = abs(sin)

    a = math.degrees(math.asin(sin))
    if transpose:  # flips axes, e.g. 0 becomes 90, 60 becomes 30
        a = 90-a
    
    return a, q


def angle_360_from_sin_cos(sin, cos): # engineer notation. 0 on right
    sin = clamp(sin, -1, +1)
    cos = clamp(cos, -1, +1)
    return math.degrees(math.atan2(sin, cos))


def subtract_angles_360(angle1, angle2):
    diff = angle1 - angle2
    if diff > 180:
        diff -= 360
    elif diff < -180:
        diff += 360
    return diff


def percs_list_from_cal_list(cal):  # generates a list with percs only, surprisingly useful
    l = [i[0] for i in cal]
    return l


def build_calipers_table(power):
    n_cal = const.N_CAL-1  
    cal = []

    for i in reversed(range(0,n_cal+1)):
        f = i/n_cal
        cal.append([f*100, power*f])

    # only after the table is done, we round things up. this avoids things like 266.00000000000034, this used to be important for some reason
    for i in range(len(cal)):
        cal[i][1] = round(cal[i][1], 2)

    return cal


def memory_to_pb(value):  # 1400x900 only
    pb = value - 680.0  # only works for this resolution
    pb /= 67.5
    return abs(pb)


def pixel_to_y(pixel):  # for collecting data. 1400x900 only
    base = 699.5
    ten_p = 67.45  # amount of pixels in 10% of the powerbar (aka 1 pb)
    pb_measure = abs(base-pixel) / ten_p
    return pb_measure * const.PB


def hwi_from_screenshot(src_img):
    lower = numpy.array([0, 25, 216])  # ([0, 33, 226])
    upper = numpy.array([60, 53, 255])
    magic_mask = cv2.inRange(src_img, lower, upper)
    
    # morphology. unclear if this is all that amazing
    # 2 levels of erosion then 1 dilation
    magic_mask = skimage.morphology.dilation(skimage.morphology.erosion(skimage.morphology.erosion(magic_mask)))

    white_pixels = numpy.argwhere(magic_mask == 255)
    white_y = [i[0] for i in white_pixels]
    index_lowest_white_y = numpy.where(white_y == max(white_y))[0]

    avg_x = 0.0
    pixels = []
    for i in index_lowest_white_y:
        pixels.append(white_pixels[i][1])
        avg_x += white_pixels[i][1]
    avg_x /= len(index_lowest_white_y)

    print("%.4f" % pixel_to_y(avg_x))

    cv2.imwrite("out.png", magic_mask)


def press_key(hex_keycode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hex_keycode, 0x0008, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def release_key(hex_keycode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hex_keycode, 0x0008 | 0x0002, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def interp1d(v, l1, l2, type='quadratic'):
    f = scipy.interpolate.interp1d(l1, l2, kind=type, fill_value='extrapolate')
    return f(v)


def gen_interp2d(l1, l2, l3, type='clough'):
    t0 = time.time()
    if type == 'linear':
        f = scipy.interpolate.LinearNDInterpolator(numpy.array([l1,l2]).T, l3)
    else:
        f = scipy.interpolate.CloughTocher2DInterpolator(numpy.array([l1,l2]).T, l3)
    t1 = time.time() - t0
    timeprint("time interp2d: %.4f" % t1)
    return f


def hdict_to_lists(dict, key1, key2):  # converts a dict in tables_hdist or tables_hmod format to three lists, for usage with bilinear interpolation
    l1 = []; l2 = []; l3 = []
    for k in dict.keys():  # k = outer key in the dictionary (percentage, in h-cases)
        for pos in range(len(dict[k][key1])):  # pos = position in the outer value list. get the value from the same position in the inner keys
            l1.append(float(k))            # the outer key itself
            l2.append(dict[k][key1][pos])  # appends val from inner key 1
            l3.append(dict[k][key2][pos])  # appends val from inner key 2
    return l1, l2, l3


def ss_and_save(n):
    img = screenshot.take()
    cv2.imwrite('ss' + str(n) + '.png', img)
    return img

def area_cropper(img, coords):  # pass x1 x2 y1 y2
    img = img[coords[2]:coords[3], coords[0]:coords[1]]  # y1 y2 x1 x2
    return img
