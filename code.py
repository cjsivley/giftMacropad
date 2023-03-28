#Codey's Macro Keyboard
#For work friends 2022
# Code adopted from adafruit macropad example project

import time #for debounce
import board
from digitalio import DigitalInOut, Direction, Pull
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode as CCC

led = DigitalInOut(board.LED)
led.direction = Direction.OUTPUT
led.value = True

kbd = Keyboard(usb_hid.devices)
cc = ConsumerControl(usb_hid.devices)

MEDIA = 1
KEY = 2

'''To customize your key maps, change the below as according to:
https://docs.circuitpython.org/projects/hid/en/latest/api.html#adafruit-hid-keycode-keycode
or
https://docs.circuitpython.org/projects/hid/en/latest/api.html#adafruit_hid.consumer_control_code.ConsumerControlCode

Note that keycodes must be flagged with KEY and ConsumerControlCodes must be flagged with MEDIA.
'''

keymap = {

    (0): (KEY, (Keycode.GUI, Keycode.D)),
    (1): (KEY, (Keycode.GUI, Keycode.V)),
    (2): (KEY, [Keycode.F11]),
    (3): (KEY, [Keycode.F10]),
    (4): (KEY, [Keycode.F5]),
    (5): (MEDIA, CCC.MUTE)
}

'''
other handy shortcuts
(Keycode.CTRL, Keycode.ALT, Keycode.DELETE) ctrl+alt+delete
(Keycode.GUI, Keycode.E) Open file explorer
(Keycode.GUI, Keycode.TAB) Open task switcher

check out: https://support.microsoft.com/en-us/windows/keyboard-shortcuts-in-windows-dcc61a57-8ff0-cffe-9796-cb9706c75eec
'''

pins = (
    board.GP0,
    board.GP1,
    board.GP2,
    board.GP3,
    board.GP4,
    board.GP21
)

#set up pins so that closing to ground = button pressed
switches = []
for i in range(len(pins)):
    switch = DigitalInOut(pins[i])
    switch.direction = Direction.INPUT
    switch.pull = Pull.UP
    switches.append(switch)

#encoder pin declaration

stepPin = DigitalInOut(board.GP19)
dirPin = DigitalInOut(board.GP20)
stepPin.direction = Direction.INPUT
dirPin.direction = Direction.INPUT
stepPin.pull = Pull.UP
dirPin.pull = Pull.UP

switchState = [0, 0, 0, 0, 0, 0]
rotaryState = True

while True:
    #check rotary encoder
    if rotaryState != stepPin.value:
        if stepPin.value == False:
            if dirPin.value == False:
                try:
                    cc.send(CCC.VOLUME_DECREMENT)
                except:
                    pass
            else:
                try:
                    cc.send(CCC.VOLUME_INCREMENT)
                except:
                    pass
        rotaryState = stepPin.value
    
    #check buttons
    for i in range(6):
        if switchState[i] == 0:
            if not switches[i].value:
                try:
                    if keymap[i][0] == KEY:
                        kbd.press(*keymap[i][1])
                    else:
                        cc.send(keymap[i][1])
                except ValueError:  # deals w six key limit
                    pass
                switchState[i] = 1

        if switchState[i] == 1:
            if switches[i].value:
                try:
                    if keymap[i][0] == KEY:
                        kbd.release(*keymap[i][1])

                except ValueError:
                    pass
                switchState[i] = 0

    time.sleep(0.003)  # debounce
