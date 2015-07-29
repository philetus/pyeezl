"""a simple rubber band line drawing interface to demo pyeezl
"""

pyeezl import Eezl

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
    ez = Eezl.Eezl(400, 400, 'rubber bands') 
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

        # start a new rubber band when pointer is pressed
        if event.flavor == Eezl.POINTER_PRESS:
            pressed_flag = True
            band = Line( Point(event.y, event.x), Point(event.y, event.x) )

        # move the end of band when pointer is moved
        elif event.flavor == Eezl.POINTER_MOTION:
            if pressed_flag:
                band.last = Point( event.y, event.x )
                ez.stain() # trigger eezl redraw when band changes

        # append current band to list of lines when pointer is released
        elif event.flavor == Eezl.POINTER_RELEASE:
            lines.append(band)
            pressed_flag = False
            ez.stain() # trigger eezl redraw when band is released

        elif event.flavor == Eezl.KEY_PRESS:
            print( event )

        elif event.flavor == Eezl.GEL:
            gel = event.gel # get gel to draw to

            # draw background
            gel.set_color(*bg_clr)
            gel.coat()

            # draw lines
            gel.set_weight(line_wt)
            gel.set_color(*line_clr)
            for l in lines:
                gel.jump_to(*l.first) # moves cursor without adding to path
                gel.ray_to(*l.last) # also adds straight segment to path
                gel.stroke() # stroke path with current weight and color
                gel.shake() # clear path & return cursor to (0.0, 0.0)

            # if pointer pressed draw band
            if pressed_flag:
                gel.set_weight(band_wt)
                gel.set_color(*band_clr)
                gel.jump_to(*band.first)
                gel.ray_to(*band.last)
                gel.stroke() # stroke path with current weight and color
                gel.shake() # clear path

            # signal that gel is ready to render to screen
            gel.ship() # artists ship ;)

        else:
            print( "unfamiliar event flavor: '{!s}'!".format(event) )

if __name__ == "__main__":
    main()