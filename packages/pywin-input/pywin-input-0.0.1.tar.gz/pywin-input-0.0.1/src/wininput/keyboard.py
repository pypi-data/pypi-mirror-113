from ctypes import c_short, c_char, c_uint8, c_int32, c_int, c_uint, c_uint32, c_long, Structure, WINFUNCTYPE, POINTER
from ctypes.wintypes import WORD, DWORD, BOOL, HHOOK, MSG, LPWSTR, WCHAR, WPARAM, LPARAM, LONG, HMODULE, LPCWSTR, HINSTANCE, HWND
import ctypes
ULONG_PTR = POINTER(DWORD)

KEYEVENTF_EXTENDEDKEY = 0x01
KEYEVENTF_KEYUP = 0x02
KEYEVENTF_UNICODE = 0x04
KEYEVENTF_SCANCODE = 0x08

# 
INPUT_MOUSE = 0
INPUT_KEYBOARD = 1
INPUT_HARDWARE = 2

# Mouse Input
class MOUSEINPUT(ctypes.Structure):
    _fields_ = (('dx', LONG),
                ('dy', LONG),
                ('mouseData', DWORD),
                ('dwFlags', DWORD),
                ('time', DWORD),
                ('dwExtraInfo', ULONG_PTR))

# Keyboard input
class KEYBDINPUT(ctypes.Structure):
    _fields_ = (('wVk', WORD),
                ('wScan', WORD),
                ('dwFlags', DWORD),
                ('time', DWORD),
                ('dwExtraInfo', ULONG_PTR))

# Hardware input
class HARDWAREINPUT(ctypes.Structure):
    _fields_ = (('uMsg', DWORD),
                ('wParamL', WORD),
                ('wParamH', WORD))

class _INPUTunion(ctypes.Union):
    _fields_ = (('mi', MOUSEINPUT),
                ('ki', KEYBDINPUT),
                ('hi', HARDWAREINPUT))

class INPUT(ctypes.Structure):
    _fields_ = (('type', DWORD),
                ('union', _INPUTunion))

# SendInput function
user32 = ctypes.WinDLL('user32', use_last_error = True)
SendInput = user32.SendInput
SendInput.argtypes = [c_uint, POINTER(INPUT), c_int]
SendInput.restype = c_uint

#
def send_text(character):
    '''
    Send a string which is not represented in the keyboard. 
    For example the Japanese character, unicode character, etc. 
    '''
    
    # This code and related structures are based on
    # http://stackoverflow.com/a/11910555/252218
    surrogates = bytearray(character.encode('utf-16le'))
    presses = []
    releases = []
    for i in range(0, len(surrogates), 2):
        higher, lower = surrogates[i:i+2]
        structure = KEYBDINPUT(0, (lower << 8) + higher, KEYEVENTF_UNICODE, 0, None)
        presses.append(INPUT(INPUT_KEYBOARD, _INPUTunion(ki=structure)))
        structure = KEYBDINPUT(0, (lower << 8) + higher, KEYEVENTF_UNICODE | KEYEVENTF_KEYUP, 0, None)
        releases.append(INPUT(INPUT_KEYBOARD, _INPUTunion(ki=structure)))

    inputs = presses + releases
    nInputs = len(inputs)
    LPINPUT = INPUT * nInputs
    pInputs = LPINPUT(*inputs)
    cbSize = c_int(ctypes.sizeof(INPUT))
    SendInput(nInputs, pInputs, cbSize)


def send_virtual_key(vk):
    '''
    Send a virtual key. For example, the enter, tab, insert, etc virtual key.
    '''

    presses = []
    releases = []

    structure = KEYBDINPUT(vk, 0, 0, 0, None)
    presses.append(INPUT(INPUT_KEYBOARD, _INPUTunion(ki=structure)))
    structure = KEYBDINPUT(vk, 0, KEYEVENTF_KEYUP, 0, None)
    releases.append(INPUT(INPUT_KEYBOARD, _INPUTunion(ki=structure)))

    inputs = presses + releases
    nInputs = len(inputs)
    LPINPUT = INPUT * nInputs
    pInputs = LPINPUT(*inputs)
    cbSize = c_int(ctypes.sizeof(INPUT))
    SendInput(nInputs, pInputs, cbSize)
