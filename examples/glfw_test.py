import time
import os

from OpenGL.GL import glClear
import glfw
import ctypes


GL_COLOR_BUFFER_BIT = 0x00004000
#glClear = glfw.ext.OpenGLWrapper("glClear", None, ctypes.c_uint)


# create icon (simple GLFW logo)
icon = """
................
................
...0000..0......
...0.....0......
...0.00..0......
...0..0..0......
...0000..0000...
................
................
...000..0...0...
...0....0...0...
...000..0.0.0...
...0....0.0.0...
...0....00000...
................
................
"""

icon = [s.strip() for s in icon.split("\n") if s.strip()]
icon_width = len(icon[0])
icon_height = len(icon)
icon_data = "".join([s.replace("0", "\x3f\x60\x60\xff").replace(".", "\x00\x00\x00\x00") for s in icon[::-1]])


def log(msg):
    # print("%06d %s" % (log.eventid, msg))
    log.eventid += 1
    
log.eventid = 0


# callback functions
def on_resize(w, h):
    log("Window resize: %d, %d" % (w, h))
    
    
def on_key(window, key, scancode, action, mods):
    if action:
        print("Key press: %s" % str(scancode))
    else:
        print("Key release: %s" % str(scancode))
    
    
def on_char(char, pressed):
    if pressed:
        log("Char press: %s" % char)
    else:
        log("Char release: %s" % char)
    
    
def on_button(button, pressed):
    if pressed:
        log("Button press: %d" % button)
    else:
        log("Button release: %d" % button)


def on_pos(x, y):
    log("Mouse pos: %d %d" % (x, y))
    
    
def on_scroll(pos):
    log("Scroll: %d" % pos)


def on_close():
    log("Close (press escape to exit)")
    
    return False
    
    
def on_refresh():
    log("Refresh")
    
    glClear(GL_COLOR_BUFFER_BIT)
    glfw.SwapBuffers()


glfw.init()
pm = glfw.get_primary_monitor()
vms = glfw.get_video_modes( pm )
print("Available video modes:\n%s\n" % "\n".join(map(str, vms)))
vm = glfw.get_video_mode( pm )
print( "Desktop video mode:\n%s\n" % str(vm) )
print( "GLFW Version: %d.%d.%d" % glfw.get_version() )

w = glfw.create_window(800, 600, 'test', None, None)

#print("OpenGL version: %d.%d.%d\n" % glfw.get_gl_version())

#glfw.ext.set_icons([(icon_data, icon_width, icon_height)])
glfw.set_window_title(w, "pyglfw test")
#glfw.disable(w, glfw.AUTO_POLL_EVENTS)
#glfw.enable(w, glfw.KEY_REPEAT)

center_x = int(vm[0][0] / 2 - glfw.get_window_size(w)[0] / 2)
center_y = int(vm[0][1] / 2 - glfw.get_window_size(w)[1] / 2)
print( "new window position: {!s}, {!s}".format(center_x, center_y) )
glfw.set_window_pos(w, center_x, center_y)

glfw.set_window_size_callback(w, on_resize)
glfw.set_window_close_callback(w, on_close)
glfw.set_window_refresh_callback(w, on_refresh)
glfw.set_key_callback(w, on_key)
glfw.set_char_callback(w, on_char)
glfw.set_mouse_button_callback(w, on_button)
glfw.set_cursor_pos_callback(w, on_pos)
glfw.set_scroll_callback(w, on_scroll)

while not glfw.window_should_close(w):
    glfw.poll_events()
    
    if glfw.get_key(w, glfw.KEY_E) == glfw.PRESS:
        break
    
    glClear(GL_COLOR_BUFFER_BIT)
    glfw.swap_buffers(w)

glfw.close_window(w)
glfw.terminate()