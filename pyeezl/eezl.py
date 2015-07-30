import glfw
from OpenGL import GL as gl
from pynanovg import pynanovg as nvg
import queue
import threading
from pyeezl import gel

# edge flavors
OUTSIDE = 0
INSIDE = 1

# event flavors
POINTER_PRESS = 0
POINTER_MOTION = 1
POINTER_RELEASE = 2
KEY_PRESS = 3
KEY_RELEASE = 4
FRESH_GEL = 5

class Event:
    def __init__(self, flavor):
        self.flavor = flavor

class Eezl:
    """
    """

    def __init__( self, height, breadth, title='eezl' ):

        print( "creating eezl" )
        self._height = height
        self._breadth = breadth
        self._title = title
        self._clear_color = [0.0, 0.0, 0.0, 1.0]

        self.eventq = queue.Queue() # queue to place events on
        self._stainq = queue.Queue( 1 ) # queue to signal for redraw

        self._event_thread = threading.Thread( target=self._event_loop )
        self._event_thread.run()

    def _event_loop( self ):

        glfw.init()
        self._win = glfw.create_window(
            self._breadth, self._height, self._title, None, None )

        glfw.make_context_current( self._win )
        glfw.swap_interval( 1 )

        self._nvg = nvg.Context()

        # setup gl context
        gl.glEnable( gl.GL_POINT_SPRITE )
        gl.glEnable( gl.GL_VERTEX_PROGRAM_POINT_SIZE ) # overwrite pointsize
        gl.glBlendFunc( gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA )
        gl.glEnable( gl.GL_BLEND )
        gl.glClearColor( *self._clear_color )

        # register callbacks
        glfw.set_window_size_callback( self._win, self._on_resize )
        glfw.set_window_close_callback( self._win, self._on_close )
        glfw.set_key_callback( self._win, self._on_key )
        glfw.set_mouse_button_callback( self._win, self._on_button )
        glfw.set_cursor_pos_callback( self._win, self._on_pos )

        # init window size
        self._on_resize( self._win, self._breadth, self._height )

        # loop and check for events
        while not glfw.window_should_close( self._win ):
            glfw.poll_events()
            try:
                if self._stainq.get_nowait():
                    self._produce_gel()
            except queue.Empty:
                pass

        # cleanup
        glfw.destroy_window(window)
        glfw.terminate()

    def _produce_gel( self ):
        """setup graphics context for gel and put it on event pipe
        """
        glfw.make_context_current( self._win )

        t = glfw.get_time()
        g = gel.Gel( self._nvg, self._height, self._breadth, t)

        self._clear_screen()
        self._nvg.beginFrame( self._breadth, self._height, self._px_ratio )

        e = Event( FRESH_GEL )
        e.gel = g
        self.eventq.put( e )

        # block until shipq receives boolean flag
        if g._shipq.get():
            self._nvg.endFrame()
            glfw.swap_buffers( self._win )

    def _clear_screen( self ):
        gl.glClearColor( *self._clear_color )
        gl.glClear( gl.GL_COLOR_BUFFER_BIT 
                    | gl.GL_DEPTH_BUFFER_BIT
                    | gl.GL_STENCIL_BUFFER_BIT )

    def _on_resize( self, win, breadth, height ):
        assert self._win == win, "window arg doesnt match!"

        self._height = height
        self._breadth = breadth

        # set gl viewport to fill window
        glfw.make_context_current( self._win )
        fb = glfw.get_framebuffer_size( self._win )[0]
        wb = glfw.get_window_size( self._win )[0]
        self._px_ratio = fb / float(wb)
        #h = max( self._height, 1.0 ) * self._px_ratio
        #w = max( self._breadth, 1.0 ) * self._px_ratio
        #gl.glViewport(0, 0, w, h)

        self.stain()

    def _on_close( self, win ):
        assert self._win == win, "window arg doesnt match!"

        glfw.set_window_should_close( self._win, True )

    def _on_key( self, win, key, scancode, action, mods ):
        assert self._win == win, "window arg doesnt match!"

        e = Event( KEY_PRESS )
        e.key = key
        if action != glfw.PRESS:
            e.flavor = KEY_RELEASE

        self.eventq.put(e)

    def _on_button( self, win, button, action, mods ):
        assert self._win == win, "window arg doesnt match!"

        x, y = glfw.get_cursor_position( self._window )
        e = Event( POINTER_PRESS )
        e.y, e.x = y, x
        if action != glfw.PRESS:
            e.flavor = POINTER_RELEASE

        self.eventq.put( e )

    def _on_pos( self, win, x, y ):
        assert self._win == win, "window arg doesnt match!"

        e = Event( POINTER_MOTION )
        e.y, e.x = y, x

        self.eventq.put(e)

    def stain( self ):
        """send signal to redraw window
        """
        # if redraw has already been requested just return
        try:
            self._stainq.put_nowait( True )
        except queue.Full:
            pass


