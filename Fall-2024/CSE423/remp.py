from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

# Global variables for animation and color
a = 0
b = 0
h_red, h_green, h_blue = 0.7, 0.4, 0.2  # House color
bg_top_red, bg_top_green, bg_top_blue = 0.5, 0.8, 1.0  # Sky gradient top
bg_bottom_red, bg_bottom_green, bg_bottom_blue = 1.0, 1.0, 1.0  # Sky gradient bottom

def draw_gradient_background():
    """Draw a gradient background representing the sky."""
    glBegin(GL_QUADS)
    glColor3f(bg_top_red, bg_top_green, bg_top_blue)  # Top of the sky
    glVertex2f(0, 500)
    glVertex2f(500, 500)
    glColor3f(bg_bottom_red, bg_bottom_green, bg_bottom_blue)  # Bottom of the sky
    glVertex2f(500, 0)
    glVertex2f(0, 0)
    glEnd()

def draw_points(x, y):
    """Draw points for customization."""
    glPointSize(5)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()

def draw_lines(x, y, a, b, width=8, color=(0.0, 0.0, 0.0)):
    """Draw thick lines for the house structure."""
    glLineWidth(width)
    glColor3f(*color)
    glBegin(GL_LINES)
    glVertex2f(x, y)
    glVertex2f(a, b)
    glEnd()

def draw_raindrop(x, y):
    """Draw individual raindrops."""
    global b
    glColor4f(0.5, 0.5, 1.0, 0.7)  # Semi-transparent blue
    glLineWidth(2)
    glBegin(GL_LINES)
    glVertex2f(x, y + b)
    glVertex2f(x - a, y - 15 + b)
    glEnd()

def draw_rain():
    """Draw falling raindrops."""
    for _ in range(150):  # Number of raindrops
        x = random.randint(0, 500)
        y = random.randint(0, 500)
        draw_raindrop(x, y)

def draw_house():
    """Draw the main house structure."""
    # Roof
    draw_lines(100, 300, 400, 300, 10, (0.8, 0.4, 0.2))  # Roof Base
    draw_lines(100, 300, 250, 400, 10, (0.8, 0.4, 0.2))  # Left Roof
    draw_lines(250, 400, 400, 300, 10, (0.8, 0.4, 0.2))  # Right Roof

    # House body
    glColor3f(h_red, h_green, h_blue)
    glBegin(GL_QUADS)
    glVertex2f(110, 100)
    glVertex2f(390, 100)
    glVertex2f(390, 300)
    glVertex2f(110, 300)
    glEnd()

    # Door
    draw_lines(180, 100, 180, 210, 4, (0.5, 0.25, 0.1))  # Left Door
    draw_lines(240, 100, 240, 210, 4, (0.5, 0.25, 0.1))  # Right Door
    draw_lines(180, 210, 240, 210, 4, (0.5, 0.25, 0.1))  # Top Door

    # Windows
    glColor3f(0.8, 0.9, 1.0)  # Light blue windows
    glBegin(GL_QUADS)
    glVertex2f(290, 220)
    glVertex2f(350, 220)
    glVertex2f(350, 280)
    glVertex2f(290, 280)
    glEnd()

    draw_lines(290, 250, 350, 250, 2, (0.0, 0.0, 0.0))  # Window divider horizontal
    draw_lines(320, 280, 320, 220, 2, (0.0, 0.0, 0.0))  # Window divider vertical

def specialKeyListener(key, x, y):
    """Handle special key inputs."""
    global a
    if key == GLUT_KEY_LEFT:
        a += 1  # Simulate wind pushing raindrops left
    if key == GLUT_KEY_RIGHT:
        a -= 1  # Simulate wind pushing raindrops right
    glutPostRedisplay()

def iterate():
    glViewport(0, 0, 500, 500)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 500, 0.0, 500, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()

    # Draw background, rain, and house
    draw_gradient_background()
    draw_rain()
    draw_house()

    glutSwapBuffers()

def animate():
    """Handle animation updates."""
    global b
    b = (b + 1) % 500
    glutPostRedisplay()

glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(500, 500)
glutInitWindowPosition(0, 0)
glutCreateWindow(b"Sweet Home with Rain")
glutDisplayFunc(showScreen)
glutIdleFunc(animate)
glutSpecialFunc(specialKeyListener)
glutMainLoop()
# from OpenGL.GL import *
# from OpenGL.GLUT import *
# from OpenGL.GLU import *
# import random

# # Global variables for animation and color
# a = 0
# b = 0
# h_red, h_green, h_blue = 0.7, 0.4, 0.2  # House color
# bg_top_red, bg_top_green, bg_top_blue = 0.5, 0.8, 1.0  # Sky gradient top
# bg_bottom_red, bg_bottom_green, bg_bottom_blue = 1.0, 1.0, 1.0  # Sky gradient bottom

# def draw_gradient_background():
#     """Draw a gradient background representing the sky."""
#     glBegin(GL_QUADS)
#     glColor3f(bg_top_red, bg_top_green, bg_top_blue)  # Top of the sky
#     glVertex2f(0, 500)
#     glVertex2f(500, 500)
#     glColor3f(bg_bottom_red, bg_bottom_green, bg_bottom_blue)  # Bottom of the sky
#     glVertex2f(500, 0)
#     glVertex2f(0, 0)
#     glEnd()

# def draw_points(x, y):
#     """Draw points for customization."""
#     glPointSize(5)
#     glBegin(GL_POINTS)
#     glVertex2f(x, y)
#     glEnd()

# def draw_lines(x, y, a, b, width=8, color=(0.0, 0.0, 0.0)):
#     """Draw thick lines for the house structure."""
#     glLineWidth(width)
#     glColor3f(*color)
#     glBegin(GL_LINES)
#     glVertex2f(x, y)
#     glVertex2f(a, b)
#     glEnd()

# def draw_raindrop(x, y):
#     """Draw individual raindrops."""
#     global b
#     glColor4f(0.5, 0.5, 1.0, 0.7)  # Semi-transparent blue
#     glLineWidth(2)
#     glBegin(GL_LINES)
#     glVertex2f(x, y + b)
#     glVertex2f(x - a, y - 15 + b)
#     glEnd()

# def draw_rain():
#     """Draw falling raindrops."""
#     for _ in range(150):  # Number of raindrops
#         x = random.randint(0, 500)
#         y = random.randint(0, 500)
#         draw_raindrop(x, y)

# def draw_house():
#     """Draw the main house structure."""
#     # Roof
#     draw_lines(100, 300, 400, 300, 10, (0.8, 0.4, 0.2))  # Roof Base
#     draw_lines(100, 300, 250, 400, 10, (0.8, 0.4, 0.2))  # Left Roof
#     draw_lines(250, 400, 400, 300, 10, (0.8, 0.4, 0.2))  # Right Roof

#     # House body
#     glColor3f(h_red, h_green, h_blue)
#     glBegin(GL_QUADS)
#     glVertex2f(110, 100)
#     glVertex2f(390, 100)
#     glVertex2f(390, 300)
#     glVertex2f(110, 300)
#     glEnd()

#     # Door
#     draw_lines(180, 100, 180, 210, 4, (0.5, 0.25, 0.1))  # Left Door
#     draw_lines(240, 100, 240, 210, 4, (0.5, 0.25, 0.1))  # Right Door
#     draw_lines(180, 210, 240, 210, 4, (0.5, 0.25, 0.1))  # Top Door

#     # Windows
#     glColor3f(0.8, 0.9, 1.0)  # Light blue windows
#     glBegin(GL_QUADS)
#     glVertex2f(290, 220)
#     glVertex2f(350, 220)
#     glVertex2f(350, 280)
#     glVertex2f(290, 280)
#     glEnd()

#     draw_lines(290, 250, 350, 250, 2, (0.0, 0.0, 0.0))  # Window divider horizontal
#     draw_lines(320, 280, 320, 220, 2, (0.0, 0.0, 0.0))  # Window divider vertical

# def specialKeyListener(key, x, y):
#     """Handle special key inputs."""
#     global a
#     if key == GLUT_KEY_LEFT:
#         a += 1  # Simulate wind pushing raindrops left
#     if key == GLUT_KEY_RIGHT:
#         a -= 1  # Simulate wind pushing raindrops right
#     glutPostRedisplay()

# def iterate():
#     glMatrixMode(GL_PROJECTION)
#     glLoadIdentity()
#     glOrtho(0.0, 500, 0.0, 500, 0.0, 1.0)
#     glMatrixMode(GL_MODELVIEW)
#     glLoadIdentity()

# def showScreen():
#     glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
#     glLoadIdentity()
#     iterate()

#     # Draw background, rain, and house
#     draw_gradient_background()
#     draw_rain()
#     draw_house()

#     glutSwapBuffers()

# def animate():
#     """Handle animation updates."""
#     global b
#     b = (b + 1) % 500
#     glutPostRedisplay()

# glutInit()
# glutInitDisplayMode(GLUT_RGBA)
# glutInitWindowSize(500, 500)
# glutInitWindowPosition(0, 0)
# glutCreateWindow(b"Sweet Home with Rain")
# glutDisplayFunc(showScreen)
# glutIdleFunc(animate)
# glutSpecialFunc(specialKeyListener)

# # Enable full-screen mode
# glutFullScreen()

# glutMainLoop()
