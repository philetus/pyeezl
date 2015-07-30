from OpenGL import GL as gl
import glfw

def on_key(window, key, scancode, action, mods):
    if( key == glfw.KEY_ESCAPE and action == glfw.PRESS ):
        glfw.set_window_should_close( window, True )

def main():

    glfw.init()

    window = glfw.create_window( 640, 480, "glfw triangle", None, None )
    
    glfw.make_context_current( window )
    glfw.swap_interval( 1 )
    glfw.set_key_callback( window, on_key )

    while not glfw.window_should_close( window ):

        # set up model view
        width, height = glfw.get_framebuffer_size( window )
        ratio = width / float(height)
        gl.glViewport( 0, 0, width, height )
        gl.glClear( gl.GL_COLOR_BUFFER_BIT )
        gl.glMatrixMode( gl.GL_PROJECTION )
        gl.glLoadIdentity()
        gl.glOrtho( -ratio, ratio, -1.0, 1.0, 1.0, -1.0 )
        gl.glMatrixMode( gl.GL_MODELVIEW )
        gl.glLoadIdentity()
        gl.glRotatef( float(glfw.get_time()) * 50.0, 0.0, 0.0, 1.0 )

        # draw triangle
        gl.glBegin(gl.GL_TRIANGLES);
        gl.glColor3f( 1.0, 0.0, 0.0 )
        gl.glVertex3f( -0.6, -0.4, 0.0 )
        gl.glColor3f( 0.0, 1.0, 0.0 )
        gl.glVertex3f( 0.6, -0.4, 0.0 )
        gl.glColor3f( 0.0, 0.0, 1.0 )
        gl.glVertex3f( 0.0, 0.6, 0.0 )
        gl.glEnd()

        # swap buffers
        glfw.swap_buffers(window)

        # poll for events
        glfw.poll_events()
    
    glfw.destroy_window(window)
    glfw.terminate()

if __name__ == "__main__":
    main()
