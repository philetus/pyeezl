import queue

class Gel:
    """
    """

    def __init__( self, nvg, height, breadth, time ):
        self._nvg = nvg
        self.height = height
        self.breadth = breadth
        self.time = time
        self._shipq = queue.Queue() # queue to listen for ship signal on

    def ship( self ):
        self._shipq.put(True)

    def jump_to( self, y, x ):
        """moves cursor position to (y, x) without changing path
        """
        self._nvg.moveTo(x, y)

    def ray_to( self, y, x ):
        """moves cursor position to (y, x) and adds straight line to path
        """
        self._nvg.lineTo(x, y)

    def bez_to( self, qy, qx, py, px, y, x ):
        """adds bezier curve with control points (qy, qx) & (py, px) to path
        """
        self._nvg.bezierTo( self, qx, qy, px, py, x, y )

    def coat( self ):
        """fill entire gel with current color
        """
        self._nvg.beginPath()
        self._nvg.rect( 0, 0, self.breadth, self.height )
        self._nvg.fill()
        self._nvg.beginPath()

    def seal( self ):
        """close current subpath with straight line
        """
        self._nvg.closePath()

    def stroke( self ):
        """imprint a line to gel in current color & weight along path
        """
        self._nvg.stroke()

    def fill( self ):
        """imprint a shape to gel in current color inside path
        """
        self._nvg.fill()

    def shake( self ):
        """clear current path
        """
        self._nvg.beginPath()

    def set_color( self, r=0.0, g=0.0, b=0.0, a=1.0 ):
        """set current color to rgba value in range [0.0-1.0]
        """
        self._nvg.setColor( r, g, b, a )

    def set_weight( self, weight ):
        """set current line weight
        """
        self._nvg.setWeight( weight )

