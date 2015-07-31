from pyglfw import pyglfw as glfw
from OpenGL import GL as gl
from pynanovg import pynanovg as nvg
import queue
import threading
from pyeezl import gel

# edge flavors
OUTSIDE = 0
INSIDE = 1

class Eezl:
    """
    """

    def __init__( self, width, height, title='eezl' ):

        print( "creating eezl" )
        self._width = width
        self._height = height
        self._title = title
        self._clear_color = [0.0, 0.0, 0.0, 1.0]

        self._stainq = queue.Queue( 1 ) # queue to signal for redraw

        # init glfw
        if not glfw.init():
            raise Exception("couldnt init glfw!")

        # create window
        self._win = glfw.Window(width, height, title)
        if not self._win:
            glfw.terminate()
            raise Exception("couldnt create glfw window!")

        self._win.make_current()
        self._win.swap_interval( 1 ) # 0 -> go fast / 1 -> pause first

        self._nvg = nvg.Context()

        # setup gl context
        gl.glEnable( gl.GL_POINT_SPRITE )
        gl.glEnable( gl.GL_VERTEX_PROGRAM_POINT_SIZE ) # overwrite pointsize
        gl.glBlendFunc( gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA )
        gl.glEnable( gl.GL_BLEND )
        gl.glClearColor( *self._clear_color )

        # register glfw.window callbacks
        self._win.set_window_size_callback( self._on_resize )
        self._win.set_window_close_callback( self._on_close )
        self._win.set_key_callback( self._on_key )
        self._win.set_mouse_button_callback( self._on_button )
        self._win.set_cursor_pos_callback( self._on_pos )

        # init window size
        self._on_resize( self._win, self._width, self._height )

    def poll_events( self ):
        glfw.poll_events()
        try:
            if self._stainq.get_nowait():
                self._produce_gel()
        except queue.Empty:
            pass

    def should_quit( self ):
        """check if eezl wants to quit
        """
        return self._win.should_close

    def quit( self ):
        """cleanup eezl window when finished
        """
        self._win.close()
        glfw.terminate()

    def stain( self ):
        """send signal to redraw window
        """
        # if redraw has already been requested just return
        try:
            self._stainq.put_nowait( True )
        except queue.Full:
            pass

    def on_gel( self, g ):
        pass

    def on_pointer_press( self, x, y ):
        pass

    def on_pointer_motion( self, x, y ):
        pass

    def on_pointer_release( self, x, y ):
        pass

    def on_key_press( self, key ):
        pass

    def on_key_release( self, key ):
        pass

    def _produce_gel( self ):
        """setup graphics context for gel and put it on event pipe
        """
        self._win.make_current()

        t = glfw.get_time()
        g = gel.Gel( self._nvg, self._width, self._height, t)

        self._clear_screen()
        self._nvg.beginFrame( self._width, self._height, self._px_ratio )

        # call draw handler
        self.on_gel( g )

        self._nvg.endFrame()
        self._win.swap_buffers()

    def _clear_screen( self ):
        gl.glClearColor( *self._clear_color )
        gl.glClear( gl.GL_COLOR_BUFFER_BIT 
                    | gl.GL_DEPTH_BUFFER_BIT
                    | gl.GL_STENCIL_BUFFER_BIT )

    def _on_resize( self, win, width, height ):
        self._width = width
        self._height = height

        # calculate pix ratio for when framebuffer != window
        self._win.make_current()
        self._px_ratio = ( self._win.framebuffer_size[0] 
                           / float(self._win.size[0]) )

        # signal for window redraw
        self.stain()

    def _on_close( self, win ):
        self._win.should_close = True

    def _on_key( self, win, key, scancode, action, mods ):
        if action == glfw.PRESS:
            self.on_key_press( key )
        else:
            self.on_key_release( key )

    def _on_button( self, win, button, action, mods ):
        x, y = self._win.cursor_pos
        if action == self._win.PRESS:
            self.on_pointer_press(x, y)
        else:
            self.on_pointer_release(x, y)

    def _on_pos( self, win, x, y ):
        self.on_pointer_motion(x, y)


