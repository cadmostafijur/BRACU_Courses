from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import math
import time
W_Width, W_Height = 800,800
pt_lt = []
dt = [1, -1]
freezz = False
cnew = False
blink = False
class point:
    def __init__(self):
        self.xp=0
        self.yp=0
        self.zp=0
def crossProduct(a, b):
    result=point()
    result.xp = a.yp * b.zp - a.zp * b.yp
    result.yp = a.zp * b.xp - a.xp * b.zp
    result.zp = a.xp * b.yp - a.yp * b.xp
    return result
def convert_coordinate(xp,yp):
    global W_Width, W_Height
    m = xp - (W_Width/2)
    n = (W_Height/2) - yp 
    return m,n
def gen_point(xp, yp):
    global pt_lt
    if (xp<200 and xp>-200) and (yp<100 and yp>-50):
        pt_lt.append([xp,yp, [random.random(), random.random(), random.random()], random.choice([0.02, -0.02]), random.choice([0.02, -0.02])])
def draw_points():
    global pt_lt
    for i in pt_lt:
        xp, yp, color,sp1,sp2 = i
        if not blink:
            glPointSize(10) #pixel size. by default 1 thake
            glBegin(GL_POINTS)
            glColor3f(*color) #konokichur color set (RGB)
            glVertex2f(xp,yp) #jekhane show korbe pixel
            glEnd()
        else:
            glPointSize(10) #pixel size. by default 1 thake
            glBegin(GL_POINTS)
            glColor3f(0, 0, 0)
            glVertex2f(xp,yp) #jekhane show korbe pixel
            glEnd()
def drawline():
    glLineWidth(5) #pixel size. by default 1 thake
    glBegin(GL_LINES)
    glColor3f(1,1,1)
    glVertex2d(-200,100)
    glColor3f(1, 1, 1)
    glVertex2d(200,100)
    glEnd()
    glLineWidth(5) #pixel size. by default 1 thake
    glBegin(GL_LINES)
    glColor3f(1, 1, 1) #konokichur color set (RGB)
    glVertex2d(200,100)
    glColor3f(1,1,1)
    glVertex2d(200,-50)
    glEnd()
    glLineWidth(5) #pixel size. by default 1 thake
    glBegin(GL_LINES)
    glColor3f(1, 1, 1) #konokichur color set (RGB)
    glVertex2d(200,-50)
    glColor3f(1,1,1)
    glVertex2d(-200,-50)
    glColor3f(1, 1, 1)
    glEnd()
    glLineWidth(5) #pixel size. by default 1 thake
    glBegin(GL_LINES)
    glColor3f(1, 1, 1) #konokichur color set (RGB)
    glVertex2d(-200,-50)
    glColor3f(1,1,1)
    glVertex2d(-200,100)
    glColor3f(1,1,1)
    glEnd()
def keyboardListener(key, xp, yp):
    global freezz
    if key==b' ':
        freezz = not freezz
    glutPostRedisplay()
def specialKeyListener(key, xp, yp):
    global pt_lt
    if key=='w':
        print(1)
    if key==GLUT_KEY_UP:
        for i in range(len(pt_lt)):#downkey
            print(pt_lt[i][3])
            pt_lt[i][3] += 0.002
            pt_lt[i][4] += 0.002
        print("speed increased")
    if key== GLUT_KEY_DOWN:		#// upkey
        for i in range(len(pt_lt)):
            pt_lt[i][3] -= 0.002
            pt_lt[i][4] -= 0.002
            print(pt_lt[i][3])
        print("speed decreased")
    glutPostRedisplay()
def mouseListener(button, state, xp, yp):
    global blink
    if button==GLUT_LEFT_BUTTON:
        if(state == GLUT_DOWN):    # left rigtht left
            blink = not blink
    if button == GLUT_RIGHT_BUTTON:
        if(state == GLUT_UP):
            c_x, c_y = convert_coordinate(xp,yp)
            gen_point(c_x,c_y)
    glutPostRedisplay()

def display():
    #//clear the display
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0,0,0,0);	#//color black
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    #//load the correct matrix -- MODEL-VIEW matrix
    glMatrixMode(GL_MODELVIEW)
    #//initialize the matrix
    glLoadIdentity()
    #//now give three info
    #//1. where is the camera (viewer)?
    #//2. where is the camera looking?
    #//3. Which direction is the camera's UP direction?
    gluLookAt(0,0,200,	0,0,0,	0,1,0)
    glMatrixMode(GL_MODELVIEW)

    global ball_x, ball_y, ball_size
    # draw_points(ball_x, ball_y, ball_size)
    drawline()
    draw_points()
    if(cnew):
        m,n = cnew
        glBegin(GL_POINTS)
        glColor3f(0.6, 0.2, 0.9)
        glVertex2f(m,n)
        glEnd()
    glutSwapBuffers()
def animate():
    #//codes for any changes in Models, Camera
    glutPostRedisplay()
    global pt_lt
    if not freezz:
        for i in range(len(pt_lt)):
            xp, yp, color, sxp, syp = pt_lt[i] 
            xp += sxp
            yp += syp
            if xp >= 200 or xp <= -200:
                sxp*= -1
            if yp >= 100 or yp <= -50:
                syp*= -1
            
            pt_lt[i] = [xp, yp, color, sxp, syp]

def init():
    #//clear the screen
    glClearColor(0,0,0,0)
    #//load the PROJECTION matrix
    glMatrixMode(GL_PROJECTION)
    #//initialize the matrix
    glLoadIdentity()
    #//give PERSPECTIVE parameters
    gluPerspective(104,	1,	1,	1000.0)
    # aspect ratio that determines the
    #  field of view in the X direction (horizontally). 
    # The bigger this angle is, the more you can see of the world - 
    # but at the same time, the 
    # objects you can see will become smaller.
    #near_dist
    #far_dist

glutInit()
glutInitWindowSize(W_Width, W_Height)
glutInitWindowPosition(1000, 200)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB) #	//Depth, Double buffer, RGB color
# glutCreateWindow("My OpenGL Program")
wind = glutCreateWindow(b"OpenGL Coding Practice")
init()
glutDisplayFunc(display)	#display callback function
glutIdleFunc(animate)	#what you want to do in the idle time (when no drawing is occuring)
glutKeyboardFunc(keyboardListener)
glutSpecialFunc(specialKeyListener)
glutMouseFunc(mouseListener)
glutMainLoop()		#The main loop of OpenGL
