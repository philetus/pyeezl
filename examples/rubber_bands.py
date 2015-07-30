"""a simple rubber band line drawing interface to demo pyeezl
"""

from pyeezl.eezl import Eezl

class Point:
    """simple point class for demo
    """

    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

    def __str__(self):
        return "Point( {:.1f}, {:.1f} )".format(self.x, self.y)

    def __iter__(self):
        for c in (self.x, self.y):
            yield c


class Line:
    """simple line class for demo
    """

    def __init__(self, first, last):
        self.first = Point(*first)
        self.last = Point(*last)

    def __str__(self):
        return "Line( first={!s}, last={!s} )".format(self.first, self.last)

    def __iter__(self):
        for p in (self.first, self.last):
            yield p

class Bands( Eezl ):

    def __init__( self, width, height ):
        Eezl.__init__( self, width, height, "rubber bands" )

        # create some variables to track state
        self.pressed_flag = False # boolean to track pointer state
        self.band = None # track current rubber band state
        self.lines = [] # list of lines created so far

        # set up variables to control visual appearance
        self.bg_clr = [1.0, 1.0, 1.0, 1.0]
        self.line_wt = 10.0
        self.line_clr = [1.0, 0.0, 0.0, 0.6]
        self.band_wt = 6.0
        self.band_clr = [0.0, 0.0, 0.0, 0.4]

    def on_gel( self, g ): # draw window contents to gel

        # draw background
        g.set_color(*self.bg_clr)
        g.coat()

        # draw lines
        g.set_weight(self.line_wt)
        g.set_color(*self.line_clr)
        for l in self.lines:
            g.jump_to(*l.first) # moves cursor without adding to path
            g.ray_to(*l.last) # also adds straight segment to path
            g.stroke() # stroke path with current weight and color
            g.shake() # clear path & return cursor to (0.0, 0.0)

        # if pointer pressed draw band
        if self.pressed_flag:
            g.set_weight(self.band_wt)
            g.set_color(*self.band_clr)
            g.jump_to(*self.band.first)
            g.ray_to(*self.band.last)
            g.stroke() # stroke path with current weight and color
            g.shake() # clear path

    def on_pointer_press( self, x, y ):
        self.pressed_flag = True
        self.band = Line( Point(x, y), Point(x, y) )

    def on_pointer_motion( self, x, y ):
        if self.pressed_flag:
            self.band.last = Point( x, y )
            self.stain() # trigger eezl redraw when band changes

    def on_pointer_release( self, x, y ):
        if self.band is not None:
            self.lines.append( self.band )
        self.pressed_flag = False
        self.stain() # trigger eezl redraw when band is released

    def on_key_press( self, key ):
        print( "key pressed: {}".format(key) )


if __name__ == "__main__":

    ez = Bands( 400, 400 )
    while not ez.should_quit():
        ez.poll_events()
    ez.quit()
