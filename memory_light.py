import memory
import math
import utils
import const


def read(var):
    return memory.read_variable(var)

def get_ball():
    return [memory.read_variable('ball_x'), memory.read_variable('ball_y'), memory.read_variable('ball_z')]
def get_pin():
    return [memory.read_variable('pin_x'), memory.read_variable('pin_y'), memory.read_variable('pin_z')]


def ang_cam(ball, pin):
    return math.atan2(ball[0]-pin[0], ball[2]-pin[2])
def dist(ball, pin):
    return math.sqrt(math.pow(ball[0]-pin[0], 2) + math.pow(ball[2]-pin[2], 2))


def auto_slope(slope_sign):  # slope sign is 1 or -1
    zsin = memory.read_variable('zerosin')
    zcos = memory.read_variable('zerocos')
    a_zero = utils.angle_360_from_sin_cos(zsin, zcos)

    slope1 = memory.read_variable('slope1')
    slope2 = memory.read_variable('slope2')
    a_diff = math.radians(a_zero)
    slope1_x = slope1*math.cos(a_diff)
    slope2_x = slope2*math.sin(a_diff)
    
    slopex = ( (slope1_x + slope2_x) * 100 * -1 * slope_sign ) * (1 / 0.00875) / 100
    return slopex
    

def pb():
    ball = get_ball()
    pin = get_pin()
    d = dist(ball, pin)
    a = ang_cam(ball, pin)
    grid_rad = memory.read_variable('grid_rad')
    
    # pb calculation
    rad = math.fmod(abs(grid_rad), math.tau)
    if grid_rad < 0:
        rad *= -1
    pb = (d * 0.3125) * math.tan(rad + a) / 1.5 / const.PB * -1

    if utils.check_if_s4():
        pb /= const.S4_WIDEFIX
    return pb


def print_slope():
    zsin = memory.read_variable('zerosin')
    zcos = memory.read_variable('zerocos')
    a_zero = utils.angle_360_from_sin_cos(zsin, zcos)
    slope1 = memory.read_variable('slope1')
    slope2 = memory.read_variable('slope2')
    a_diff = math.radians(a_zero)
    print("v1: %.8f  v2: %.8f     a: %.1f" % (slope1, slope2, a_zero))
    print()
    print('v1x: v1 * cos(a)   |   %+.2f * %+.2f = %+.3f' % (slope1, math.cos(a_diff), slope1*math.cos(a_diff)))
    print('v1y: v1 * sin(a)   |   %+.2f * %+.2f = %+.3f' % (slope1, math.sin(a_diff), slope1*math.sin(a_diff)))
    print('v2x: v2 * sin(a)   |   %+.2f * %+.2f = %+.3f' % (slope2, math.sin(a_diff), slope2*math.sin(a_diff)))
    print('v2y: v2 * cos(a)   |   %+.2f * %+.2f = %+.3f' % (slope2, math.cos(a_diff), slope2*math.cos(a_diff)))

    v1x = slope1*math.cos(a_diff)
    v2x = slope2*math.sin(a_diff)
    
    v1y = slope1*math.sin(a_diff)
    v2y = slope2*math.cos(a_diff)
    
    vx = abs(v1x + v2x) * 100 * 1.145
    vy = abs(v1y + v2y) * 100
    print()
    print('vx: (v1x+v2x) * 100 * 1.146 | (%+.2f+%+.2f) * 100 * 1.146 = %.3f' % (v1x, v2x, abs((v1x+v2x)*100*1.146)))
    print('vy: (v1y+v2y) * 100         | (%+.2f+%+.2f) * 100         = %.3f' % (v1y, v2y, abs((v1y+v2y)*100)))
