import evdev
from evdev import InputDevice, categorize, UInput
from evdev import ecodes as e
import os
import time


default_map = {
    # Top row
    e.KEY_GRAVE: e.KEY_GRAVE,
    e.KEY_1: e.KEY_1,
    e.KEY_2: e.KEY_2,
    e.KEY_3: e.KEY_3,
    e.KEY_4: e.KEY_4,
    e.KEY_5: e.KEY_5,
    e.KEY_6: e.KEY_6,
    e.KEY_7: e.KEY_7,
    e.KEY_8: e.KEY_8,
    e.KEY_9: e.KEY_9,
    e.KEY_0: e.KEY_0,
    e.KEY_MINUS: e.KEY_MINUS,
    e.KEY_EQUAL: e.KEY_EQUAL,
    # Second row
    e.KEY_Q: e.KEY_Q,
    e.KEY_W: e.KEY_W,
    e.KEY_E: e.KEY_E,
    e.KEY_R: e.KEY_R,
    e.KEY_T: e.KEY_T,
    e.KEY_Y: e.KEY_Y,
    e.KEY_U: e.KEY_U,
    e.KEY_I: e.KEY_I,
    e.KEY_O: e.KEY_O,
    e.KEY_P: e.KEY_P,
    e.KEY_LEFTBRACE: e.KEY_LEFTBRACE,
    e.KEY_RIGHTBRACE: e.KEY_RIGHTBRACE,
    e.KEY_BACKSLASH: e.KEY_BACKSLASH,
    # Third row
    e.KEY_A: e.KEY_A,
    e.KEY_S: e.KEY_S,
    e.KEY_D: e.KEY_D,
    e.KEY_F: e.KEY_F,
    e.KEY_G: e.KEY_G,
    e.KEY_H: e.KEY_H,
    e.KEY_J: e.KEY_J,
    e.KEY_K: e.KEY_K,
    e.KEY_SEMICOLON: e.KEY_SEMICOLON,
    e.KEY_APOSTROPHE: e.KEY_APOSTROPHE,
    # Fourth row
    e.KEY_Z: e.KEY_Z,
    e.KEY_X: e.KEY_X,
    e.KEY_C: e.KEY_C,
    e.KEY_V: e.KEY_V,
    e.KEY_B: e.KEY_B,
    e.KEY_N: e.KEY_N,
    e.KEY_M: e.KEY_K,
    e.KEY_COMMA: e.KEY_COMMA,
    e.KEY_DOT: e.KEY_DOT,
    e.KEY_SLASH: e.KEY_SLASH,
    # Special Key
    e.KEY_LEFTSHIFT: e.KEY_LEFTSHIFT,
    e.KEY_RIGHTSHIFT: e.KEY_RIGHTSHIFT,
    e.KEY_LEFTALT: e.KEY_LEFTALT,
    e.KEY_BACKSPACE: e.KEY_BACKSPACE,
    e.KEY_LEFTCTRL: e.KEY_LEFTCTRL,
    e.KEY_RIGHTCTRL: e.KEY_RIGHTCTRL,
    e.KEY_ENTER: e.KEY_ENTER,
}


class KeyEvent:
    def __init__(self, type, code, value):
        self.code = code
        self.type = type
        self.value = value

    def update(self, type, code, value):
        self.code = code
        self.type = type
        self.value = value


if __name__ == "__main__":
    dev = evdev.InputDevice("/dev/input/event3")
    ui = UInput()
    last_space_time = 0
    last_a_time = 0
    time_gap = 0
    dev.grab()

    for event in dev.read_loop():
        if event.type == e.EV_KEY and event.code in default_map:
            output_key = default_map[event.code]
            ui.write(e.EV_KEY, output_key, event.value)
            ui.syn()

        if event.code == e.KEY_SPACE and event.value == 0:
            current_space_time = event.sec + event.usec / 1000000
            space_time_gap = current_space_time - last_space_time
            print("key space time gap: ", space_time_gap)

        if event.code == e.KEY_SPACE and event.value == 1:
            last_space_time = event.sec + event.usec / 1000000

        if event.code == e.KEY_A and event.value == 0:
            current_a_time = event.sec + event.usec / 1000000
            a_time_gap = current_a_time - last_a_time
            print("key a time gap: ", a_time_gap)

        if event.code == e.KEY_A and event.value == 1:
            last_a_time = event.sec + event.usec / 1000000

        if event.code == e.KEY_ESC:
            dev.ungrab()
            os._exit(0)
