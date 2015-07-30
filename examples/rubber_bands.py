"""a simple rubber band line drawing interface to demo pyeezl
"""

from pyeezl import eezl

class Point:
    """simple point class for demo
    """

    def __init__(self, y=0.0, x=0.0):
        self.y = y
        self.x = x

    def __str__(self):
        return "Point( y={:.1f}, x={:.1f} )".format(self.y, self.x)

    def __iter__(self):
        for c in (self.y, self.x):
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


def main():

    # open eezl window
    ez = eezl.Eezl(400, 400, 'rubber bands') 
    print("created new eezl!")

    # create some variables to track state
    pressed_flag = False # boolean pointer pressed flag to track pointer state
    band = None # track current rubber band state
    lines = [] # list of lines created so far

    # set up variables to control visual appearance
    bg_clr = [1.0, 1.0, 1.0, 1.0]
    line_wt = 10.0
    line_clr = [1.0, 0.0, 0.0, 0.6]
    band_wt = 6.0
    band_clr = [0.0, 0.0, 0.0, 0.4]

    # mainloop
    while True:

        # block until event is pulled from queue
        event = ez.eventq.get() 

        print( "got event {0} flavor {0.flavor}".format(event) )

        # start a new rubber band when pointer is pressed
        if event.flavor == eezl.POINTER_PRESS:
            pressed_flag = True
            band = Line( Point(event.y, event.x), Point(event.y, event.x) )

        # move the end of band when pointer is moved
        elif event.flavor == eezl.POINTER_MOTION:
            if pressed_flag:
                band.last = Point( event.y, event.x )
                ez.stain() # trigger eezl redraw when band changes

        # append current band to list of lines when pointer is released
        elif event.flavor == eezl.POINTER_RELEASE:
            lines.append(band)
            pressed_flag = False
            ez.stain() # trigger eezl redraw when band is released

        elif event.flavor == eezl.KEY_PRESS:
            print( event )

        elif event.flavor == eezl.FRESH_GEL:
            g = event.gel # get gel to draw to

            # draw background
            g.set_color(*bg_clr)
            g.coat()

            # draw lines
            g.set_weight(line_wt)
            g.set_color(*line_clr)
            for l in lines:
                g.jump_to(*l.first) # moves cursor without adding to path
                g.ray_to(*l.last) # also adds straight segment to path
                g.stroke() # stroke path with current weight and color
                g.shake() # clear path & return cursor to (0.0, 0.0)

            # if pointer pressed draw band
            if pressed_flag:
                g.set_weight(band_wt)
                g.set_color(*band_clr)
                g.jump_to(*band.first)
                g.ray_to(*band.last)
                g.stroke() # stroke path with current weight and color
                g.shake() # clear path

            # signal that gel is ready to render to screen
            g.ship() # artists ship ;)

        else:
            print( "unfamiliar event flavor: '{!s}'!".format(event) )

if __name__ == "__main__":
    main()