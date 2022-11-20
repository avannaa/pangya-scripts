# @ author sera


print('loading science......')

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 

from pynput import keyboard

import utils        # save images, convert pb
import memory_grey  # spin change
import memory_light
import memory
import screenshot

import pymem


def b(boolean):  # quick boolean to int
    return 1 if boolean else 0

listen = True  # whether should listen to inputs or not
    
ss_counter = 1
spinv = 30.0

# l = [100.0, 95.0, 90.0, 85.0, 80.0, 75.0, 70.0, 65.0, 60.0, 55.0, 50.0, 40.0, 30.0, 20.0, 10.0]  # 1w
# l = [100.0, 95.0, 90.0, 85.0, 80.0, 70.0, 60.0, 50.0, 40.0]  # 274
# l = [100.0, 95.0, 90.0, 85.0, 80.0, 75.0, 70.0, 60.0, 50.0, 40.0, 30.0, 20.0]  # 3w
l = [100.0, 90.0, 80.0]  # powershots
# l = [100.0, 95.0, 90.0, 85.0, 80.0]  # 100-80, 5% steps
# l = [100.0, 97.5, 95.0, 90.0, 85.0, 80.0]  # 100-80, 5% steps w/ 97.5
# l = [100.0, 97.5, 95.0]  # high power ones
# l = [95.0, 85.0, 82.5]  # heh
p = 0


def calculate_cal(p):
    return 500.0 - (100.0-p)*3.6

def inc(l, i):
    return (i+1) % len(l)

def dec(l, i):
    return ((i-1) + len(l)) % len(l)


def main_loop():
    memory.init()
    print('-.( \' ~ \' ).-')

    def on_press(key):
        global listen, ss_counter, l, p

        if hasattr(key, 'char'):
            key = key.char

        if key in ['\\']:
            listen = not listen
            print("Listening: %r" % listen)

        if listen:
            if key in ['q']:
                s = memory_light.read('spin')
                c = memory_light.read('curve')
                p = utils.cal_index_to_p(memory_light.read('caliper'))
                pb = memory_light.pb()
                z = memory_light.read('zoom_y')
                print('PB: %.2f | Spin: %.2f | Curve: %.2f | %%: %.2f | Zoom: %.2f' % (pb, s, c, p, z))

            if key in [';']:
                utils.ss_and_save(ss_counter)
                print('saved screenshot to ss' + str(ss_counter) + '.png')
                ss_counter += 1

            if key in ['f']:
                print('ang: %.1f' % utils.angle_and_quad_from_sin_cos(memory.read_variable('sin'), memory.read_variable('cos'))[0])

            if key in ['g']:
                memory_grey.set_spin(+11.0)
                memory_grey.write_variable('curve', -10.0)

            if key in ['b']:
                memory_grey.set_spin(+30.0)

            if key in ['c']:
                utils.hwi_from_screenshot(screenshot.take())

            if key in ['o']:
                print('%.4f' % (memory.read_variable('last')))

            if key in ['t']:
                p = inc(l, p)
                cal = calculate_cal(l[p])
                memory_grey.set_caliper(cal)
                memory.write_variable('spin', spinv)

            if key in ['=']:
                p = dec(l, p)
                cal = calculate_cal(l[p])
                memory_grey.set_caliper(cal)
                memory.write_variable('spin', spinv)

            if key in ['v']:
                print("ball_y", memory_light.read('ball_y_d'))

            if key in ['r']:
                p = 0
                cal = calculate_cal(l[p])
                memory_grey.set_caliper(cal)
                memory.write_variable('spin', spinv)

            if key in ['-']:  # zoom max
                zoom_level = memory.read_variable('zoom_y')
                memory.write_variable('zoom_y', memory.read_variable('pin_y')+16.0)

            if key in ['=']:  # zoom pba
                zoom_level = memory.read_variable('zoom_y')
                memory.write_variable('zoom_y', memory.read_variable('pin_y')+16.0*4)


    def on_release(key):
        if listen:
            if key == keyboard.Key.esc:  # stops listener thread
                return False

    with keyboard.Listener(on_press=on_press, on_release=on_release) as l:
        l.join()


main_loop()
