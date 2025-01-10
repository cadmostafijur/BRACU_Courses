from OpenGL.GL import *
from OpenGL.GLUT import *
import time

x_axis = 150


def drawPoints(x, y):
    glPointSize(2.0)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()


def midPointCircle(X, Y, r):
    d = 1 - r
    x = 0
    y = r
    while x <= y:
        x += 1
        if d < 0:
            d += 2 * x + 3
        else:
            y -= 1
            d += 2 * (x - y) + 5
        drawPoints(X + x, Y + y)
        drawPoints(X - x, Y + y)
        drawPoints(X + x, Y - y)
        drawPoints(X - x, Y - y)
        drawPoints(X + y, Y + x)
        drawPoints(X - y, Y + x)
        drawPoints(X + y, Y - x)
        drawPoints(X - y, Y - x)


def translation():
    global x_axis
    x_axis += 50
    y_axis = 700
    Rad = 200
    glColor3f(1.0, 1.0, 1.0)
    midPointCircle(x_axis, y_axis, Rad)
    for i in range(40):
        midPointCircle(x_axis, y_axis, Rad-i)
    glColor3f(0.0, 0.0, 0.0)
    midPointCircle(x_axis, y_axis, Rad - 40)
    glColor3f(0.0, 0.0, 1.0)
    midPointCircle(x_axis, y_axis, Rad - 80)
    for i in range(80, 120):
        midPointCircle(x_axis, y_axis, Rad - i)
    glColor3f(1.0, 0.0, 0.0)
    midPointCircle(x_axis, y_axis, Rad - 120)
    for i in range(120, 160):
        midPointCircle(x_axis, y_axis, Rad-i)
    glColor3f(1.0, 1.0, 0.0)
    midPointCircle(x_axis, y_axis, Rad - 160)
    for i in range(160, 200):
        midPointCircle(x_axis, y_axis, Rad - i)


def iterate():
    glViewport(0, 0, 1000, 1000)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 1000, 0.0, 1000, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()

    translation()

    glutSwapBuffers()


glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(1000, 1000)
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"Archery Simulation")
t = 12
for i in range(t):
    glutDisplayFunc(showScreen)
    showScreen()
    time.sleep(0.05)
glutDisplayFunc(showScreen)

glutMainLoop()
