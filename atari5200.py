#!/usr/bin/python

import os, struct, array
from fcntl import ioctl

SDL_JOY_0_SELECT = 8
SDL_JOY_0_START = 9
SDL_JOY_0_TRIGGER1 = 0
SDL_JOY_0_TRIGGER2 = 1
SDL_JOY_0_ASTERISK = 2
SDL_JOY_0_HASH = 3
SDL_JOY_0_SECOND_AXIS = 2

# Iterate over the joystick devices.
# print('Available devices:')

devices = sorted(os.listdir('/dev/input'))
joysticks = []
for fn in devices:
    if fn.startswith('js'):
        # print('  /dev/input/%s' % fn)
        joysticks.append("/dev/input/%s" % fn)

joysticks = sorted(joysticks)

print "First joystick is %s" % joysticks[0]

# Open the joystick device.
fn = joysticks[0]
# print('Opening %s...' % fn)
jsdev = open(fn, 'rb')

buf = array.array('c', ['\0'] * 64)
ioctl(jsdev, 0x80006a13 + (0x10000 * len(buf)), buf) # JSIOCGNAME(len)
js_name = ("%s" % buf.tostring()).partition(b'\0')[0]
# print('Device name: %s' % js_name)

jsdev.close()
js_cfg = "/opt/retropie/configs/all/retroarch-joypads/%s.cfg" % js_name.replace(" ", "")
print "Getting Retroarch configuration for %s" % js_cfg

# print(js_cfg)
f = open("%s" % js_cfg, "r")
content = f.read()
lines = content.split("\n")
for line in lines:
    if line:
        p = line.replace(" ", "").split("=")
        # print "Processing %s" % p[0]
        if p[0] == "input_select_btn":
            SDL_JOY_0_SELECT = p[1].replace('"', '')
        elif p[0] == "input_start_btn":
            SDL_JOY_0_START = p[1].replace('"', '')
        elif p[0] == "input_a_btn":
            SDL_JOY_0_TRIGGER1 = p[1].replace('"', '')
        elif p[0] == "input_b_btn":
            SDL_JOY_0_TRIGGER2 = p[1].replace('"', '')
        elif p[0] == "input_x_btn":
            SDL_JOY_0_ASTERISK = p[1].replace('"', '')
        elif p[0] == "input_y_btn":
            SDL_JOY_0_HASH = p[1].replace('"', '')
        elif p[0] == "input_r_x_minus_axis":
            SDL_JOY_0_SECOND_AXIS = p[1].replace('"', '').replace("-", "")
f.close()

atari800_cfg = "/home/pi/.atari800.cfg"
print "Updating configuration in %s with" % atari800_cfg
print "SDL_JOY_0_SELECT=%s" % SDL_JOY_0_SELECT
print "SDL_JOY_0_START=%s" % SDL_JOY_0_START
print "SDL_JOY_0_TRIGGER1=%s" % SDL_JOY_0_TRIGGER1
print "SDL_JOY_0_TRIGGER2=%s" % SDL_JOY_0_TRIGGER2
print "SDL_JOY_0_ASTERISK=%s" % SDL_JOY_0_ASTERISK
print "SDL_JOY_0_HASH=%s" % SDL_JOY_0_HASH
print "SDL_JOY_0_SECOND_AXIS=%s" % SDL_JOY_0_SECOND_AXIS


f = open("%s" % atari800_cfg, "r")
content = f.read()
f.close()

new_data = ""
lines = content.split("\n")
for line in lines:
    if line.startswith("SDL_JOY_0_SELECT"):
        line = "SDL_JOY_0_SELECT=%s" % SDL_JOY_0_SELECT
    elif line.startswith("SDL_JOY_0_START"):
        line = "SDL_JOY_0_START=%s" % SDL_JOY_0_START
    elif line.startswith("SDL_JOY_0_TRIGGER1"):
        line = "SDL_JOY_0_TRIGGER1=%s" % SDL_JOY_0_TRIGGER1
    elif line.startswith("SDL_JOY_0_TRIGGER2"):
        line = "SDL_JOY_0_TRIGGER2=%s" % SDL_JOY_0_TRIGGER2
    elif line.startswith("SDL_JOY_0_ASTERISK"):
        line = "SDL_JOY_0_ASTERISK=%s" % SDL_JOY_0_ASTERISK
    elif line.startswith("SDL_JOY_0_HASH"):
        line = "SDL_JOY_0_HASH=%s" % SDL_JOY_0_HASH
    elif line.startswith("SDL_JOY_0_SECOND_AXIS="):
        line = "SDL_JOY_0_SECOND_AXIS=%s" % SDL_JOY_0_SECOND_AXIS
    new_data += line + "\n"

# print new_data

f = open("%s" % atari800_cfg, 'w')
f.write(new_data)
f.close()
