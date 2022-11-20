# @author sera

import pymem
import wmi  # to query list of running processes

import traceback   # for exception stacktracing

pm = None
pangya_version = 'none'

pvt_exe = 'pym.exe'


def process_path(path, type='float', return_address=False):
    address = path[0] + pm.process_base.lpBaseOfDll
    for i in path[1:]:
        address = pm.read_int(address) + i
    if return_address:
        return address
    else:  # default float
        if type == 'int':
            return pm.read_int(address)
        if type == 'string':
            return pm.read_string(address, 12)
        return pm.read_float(address)


def read_variable(variable, return_address=False):
    type = variables[pangya_version][variable][0]
    path = variables[pangya_version][variable][1]
    return(process_path(path, type, return_address))


def write_variable(variable, value):
    type = variables[pangya_version][variable][0]
    path = variables[pangya_version][variable][1]

    if type == 'int':  # default float
        return(pm.write_int(process_path(path, type, return_address=True), value))    
    return(pm.write_float(process_path(path, type, return_address=True), value))



variables = {
    's4': {
        'dist': ['float', [0x7229D8, 0x1C, 0x18, 0x14, 0x14,   0x0,   0x0,  0x1C0, 0x0, 0x34, 0x18]],
         'sin': ['float', [0x7229D8, 0x1C, 0x20, 0x24, 0x18,   0x0, 0x1DC,  0x70]],
         'cos': ['float', [0x7229D8,  0x8,  0xC, 0x28, 0x30,   0x0, 0x1DC,  0x68]],
        'spin': ['float', [0x7229D8, 0x1C, 0x20, 0x3C, 0x44,  0x30,   0x0,  0x24]],
       'curve': ['float', [0x7229D8, 0x1C, 0x10, 0x28, 0x3C,  0x30,   0x0,  0x20]],
      'height': ['float', [0x7229D8, 0x1C, 0x20, 0x18,  0x0, 0x1C0,   0x0,  0x20]],
       't_hud': ['int', [0x7229D8, 0x1C, 0x20, 0x10,  0x0,   0x0, 0x1C4,  0x84]],
     'windstr': ['string', [0x7229D8, 0x1C, 0x20, 0x18,  0x0, 0x1C8,  0x14,   0x0]],
      'slope1': ['float', [0x7229D8, 0x9C, 0x28, 0x20, 0x18,   0x0, 0x1C4,  0x1C]],
      'slope2': ['float', [0x7229D8, 0x1C, 0x20, 0x3C,  0x0,   0x0, 0x1C4,  0x24]],
     'caliper': ['float', [0x7229D8, 0x1C, 0x20, 0x24, 0x48,   0x0,  0x14,  0xF0]],
      'calset': ['float', [0x7229D8, 0x1C, 0x20, 0x24, 0x18,   0x0, 0x3DC,  0x20]],
      'calcur': ['float', [0x7229D8, 0x1C, 0x20, 0x24, 0x18,   0x0, 0x3DC,  0x20]],  # silly "temporary" workaround
        'chat': ['string', [0x7229D8, 0x20, 0xE8, 0x10, 0xEC,  0x78,  0x34,  0xC0]],
         'aim': ['float', [0x7229D8, 0x1C, 0x18, 0x14, 0x14,   0x0,   0x0, 0x1C0, 0x0, 0x34, 0x40]],
      'zoom_y': ['float', [0x7253C0]],
     'zerosin': ['float', [0x7253A0]],
     'zerocos': ['float', [0x725398]],
      'ball_x': ['float', [0x670604]],  # "static", not "dynamic"
      'ball_y': ['float', [0x670608]],
      'ball_z': ['float', [0x67060C]],
       'pin_x': ['float', [0x71F33C]],
       'pin_y': ['float', [0x71F340]],
       'pin_z': ['float', [0x71F344]],
    'grid_rad': ['float', [0x7229D8, 0x24, 0x10C]],
      'course': ['int', [0x6630C0]],
       'pname': ['string', [0x6A002C, 0xFA8]],
        'sin2': ['float', [0x7229D8, 0x1C, 0x20, 0x10, 0x0, 0x0, 0x1DC, 0x68]],
    },

    'pvt': {
        'dist': ['float', [0xAC79E0, 0x8, 0x10,  0x30,  0x0, 0x218,   0x0, 0x48, 0x2C]],
      'height': ['float', [0xAC79E0, 0x8, 0x10,  0x30,  0x0, 0x218,   0x0, 0x34]],
         'sin': ['float', [0xAC79E0, 0x1C, 0x20,  0x14, 0x18,   0x0, 0x234, 0xB4]],
         'cos': ['float', [0xAC79E0, 0x1C, 0x20,  0x14, 0x18,   0x0, 0x234, 0xAC]],
        'spin': ['float', [0xAC79E0, 0x1C, 0x20,  0x14, 0x28,   0x0,   0x0, 0x1C]],
       'curve': ['float', [0xAC79E0, 0x1C, 0x20,  0x14, 0x28,   0x0,   0x0, 0x18]],
      'slope1': ['float', [0xAC79E0, 0x1C, 0x20,  0x14, 0x18,   0x0, 0x21C, 0x1C]],
      'slope2': ['float', [0xAC79E0, 0x1C, 0x20,  0x14, 0x18,   0x0, 0x21C, 0x24]],
     'caliper': ['float', [0xAC79E0, 0x1C, 0x20,  0x14, 0x18,   0x0, 0x46C, 0x52C]],
      'calset': ['float', [0xAC79E0, 0x1C, 0x20,  0x14, 0x18,   0x0, 0x46C, 0x530]],
      'calcur': ['float', [0xAC79E0, 0x1C, 0x20,  0x14, 0x48,   0x0,  0x14, 0x100]],
        'last': ['float', [0xAC79E0, 0x1C,  0x0,  0x10, 0x10,   0x0,   0x0, 0x218, 0x4, 0x48]],
         'aim': ['float', [0xAC79E0, 0x1C, 0x20,  0x14, 0x10,   0x0,   0x0, 0x218, 0x0, 0x48, 0x54]],
     'windstr': ['string', [0xAC79E0, 0x8, 0x10,  0x30,  0x0, 0x220,  0x28,  0x0]],
       't_hud': ['int', [0xAC79E0, 0x1C, 0x20,  0x14, 0x18,   0x0, 0x21C, 0xAC]],  # terrain number, visual only
    'accuracy': ['float', [0xA4035C]],  # lol
      'zoom_y': ['float', [0xAC97C8]],
     'zerosin': ['float', [0xAC97A8]],
     'zerocos': ['float', [0xAC97A0]],
      'ball_x': ['float', [0xA1107C]],
      'ball_y': ['float', [0xA11080]],
      'ball_z': ['float', [0xA11084]],
    'ball_y_d': ['float', [0xA10FB4]],  # dynamic
       'pin_x': ['float', [0xAC445C]],
       'pin_y': ['float', [0xAC4460]],
       'pin_z': ['float', [0xAC4464]],
        'wind': ['float', [0xA3CFD4, 0x34, 0x30, 0x10, 0x2C, 0x18]], # wind struct. todo this
    'grid_rad': ['float', [0xA3CFD4, 0x34, 0x30, 0x10, 0x2C, 0x18, 0x14, 0x14, 0x14, 0x14, 0x0, 0x0, 0x3064]],
      'course': ['int', [0xCF13A4, 0x258, 0x2B4]],
    'char_aim': ['float', [0xAC79E0, 0x0, 0x78, 0x0, 0x68]],
    },
}



def write_bytes_anywhere(base, offsets, byte_value, length):
    base += pm.process_base.lpBaseOfDll
    for i in range(length):
        pm.write_bytes(process_offsets(base, offsets, return_address=True), byte_value, 1)
        base += 1


def write_bytearray(address, byte_array):
    pm.write_bytes(address, byte_array, len(byte_array))


def find_pattern_address(pattern, temp_base=0xAC79E0):
    count = 0
    found = False
    while not found and count < 1000:
        result_tuple = pymem.pattern.scan_pattern_page(pm.process_handle, temp_base, pattern)
        if result_tuple[1] is None:
            temp_base = result_tuple[0]
            count += 1
        else:
            found = True
        
    return result_tuple[1]



def init():
    global pm, pangya_version
    w = wmi.WMI()
    
    if len(w.Win32_Process(name="ProjectG.exe")) == 1:
        pangya_version = 's4'
    
    elif len(w.Win32_Process(name=pvt_exe)) == 1:
        pangya_version = 'pvt'
   
    try:
        if pangya_version == 'pvt':
            pm = pymem.Pymem(pvt_exe)

        elif pangya_version == 's4':
            pm = pymem.Pymem('ProjectG.exe')

    except:
        print("memory launch exception")
        traceback.print_exc()
