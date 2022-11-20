import memory

print_on = False


def greyprint(s):
    if print_on:
        print(s)


def change_spin(increment):
    spin_inc = read_value('spin') + increment
    spin_inc = -30.0 if spin_inc < -30.0 else +30.0 if spin_inc > +30.0 else spin_inc
    memory.write_variable('spin', spin_inc)
    greyprint("set spin to %.f" % spin_inc)

def set_spin(value):
    value = -30.0 if value < -30.0 else +30.0 if value > +30.0 else value
    memory.write_variable('spin', value)
    greyprint("set spin to %.1f" % value)

def set_caliper(value):
    memory.write_variable('calset', value)
    memory.write_variable('caliper', value)
    memory.write_variable('calcur', value)
    greyprint("set caliper to %d" % value)

def set_slope(value1, value2):
    memory.write_variable('slope1', value1)
    memory.write_variable('slope2', value2)
    print("set slope to: %.1f %.1f" % (value1, value2))

def zoom_max():
    memory.write_variable('zoom_y', memory.read_variable('pin_y')+16.0)

def zoom_pba():
    memory.write_variable('zoom_y', memory.read_variable('pin_y')+16.0+48.0)

def write_variable(variable, value):
    memory.write_variable(variable, value)
