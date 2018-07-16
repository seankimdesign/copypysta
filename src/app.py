import pyperclip
import time
import platform
from copycache import CopyCache
from pynput import keyboard

active_keys = []
cache = CopyCache()
controller = keyboard.Controller()
paste_occurred = False
user_os = platform.system().lower()

copy_keys = {'ctrl', 'c'}
paste_keys = {'ctrl', '`'}
os_paste_command = [keyboard.Key.ctrl, 'v']

if user_os == 'darwin':
    copy_keys = {'cmd', 'ç'}
    paste_keys = {'ctrl'}
    os_paste_command = [keyboard.Key.cmd, 'v']


def on_press(key):
    key_name = normalize(key)
    active_keys.append(key_name)
    detect_operations()


def on_release(key):
    global paste_occurred
    key_name = normalize(key)
    while key_name in active_keys:
        active_keys.remove(key_name)
        paste_occurred = False


def normalize(key):
    try:
        key_name = key.char.lower()
    except AttributeError:
        key_name = str(key)
        if "ctrl" in key_name:
            key_name = "ctrl"
        if "cmd" in key_name:
            key_name = "cmd"
    return key_name


def detect_operations():
    copy_occurred = detect_copy()
    if not copy_occurred and len(cache) > 0:
        detect_paste()


def detect_copy():
    if copy_keys.issubset(active_keys):
        time.sleep(0.1)
        copy_value = pyperclip.paste()
        if copy_value != cache.retrieve(0):
            cache.shift(copy_value)
        return True
    return False


def detect_paste():
    if paste_keys.issubset(active_keys):
        index = get_first_int()
        if index == 0:
            perform_purge()
        elif 0 < index < len(cache):
            value = cache.retrieve(index)
            pyperclip.copy(value)
            perform_paste()
            time.sleep(0.1)
            pyperclip.copy(cache.retrieve(0))


def get_first_int():
    for key_name in active_keys:
        try:
            return int(key_name)
        except ValueError:
            pass
    return -1


def perform_paste():
    global paste_occurred
    if not paste_occurred:
        [controller.press(k) for k in os_paste_command]
        [controller.release(k) for k in os_paste_command]
        paste_occurred = True


def perform_purge():
    cache.flush()
    pyperclip.copy("")


# print('Copypysta application started')


with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()
