from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import math

W_Width, W_Height = 800,1000

A = [250, 238]
B = [235, 225]
C = [243, 237]
D = [240, 228]
E = [237, 230]
gfx = [A, B, C, D, E]
rfx = []
for i in range(-200, 200, 20):
    rfx.append(gfx[random.randint(0,4)]+[i, i])

speed = .8
color = 0
bg_color = 1
create_new = False


class point:
    def __init__(self):
        self.x=0
        self.y=0
        self.z=0


def crossProduct(a, b):
    result=point()
    result.x = a.y * b.z - a.z * b.y
    result.y = a.z * b.x - a.x * b.z
    result.z = a.x * b.y - a.y * b.x

    return result

def convert_coordinate(x,y):
    global W_Width, W_Height
    a = x - (W_Width/2)
    b = (W_Height/2) - y 
    return a,b

def draw_points(x, y, s):
    glPointSize(s) #pixel size. by default 1 thake
    glBegin(GL_POINTS)
    glVertex2f(x,y) #jekhane show korbe pixel
    glEnd()




def drawShapes():
    glBegin(GL_TRIANGLE_STRIP)
    glVertex2d(-170,100)
    glColor3f(0.439, 0.235, 0.02)
    glVertex2d(170,100)
    glColor3f(0.439, 0.235, 0.02)
    glVertex2d(0,160)
    glEnd()

    glBegin(GL_QUADS)
    glVertex2d(-165,100)
    glColor3f(0.439, 0.235, 0.02)
    glVertex2d(165,100)
    glColor3f(0.439, 0.235, 0.02)
    glVertex2d(165,-50)
    glColor3f(0.439, 0.235, 0.02)
    glVertex2d(-165,-50)
    glEnd()

    glBegin(GL_QUADS)
    glColor3f(1, 1, 1)
    glVertex2d(100,60)
    glColor3f(1, 1, 1)
    glVertex2d(140,60)
    glColor3f(1, 1, 1)
    glVertex2d(140,20)
    glColor3f(1, 1, 1)
    glVertex2d(100, 20)
    glEnd()


    glBegin(GL_QUADS)
    glColor3f(1, 1, 1)
    glVertex2d(-110,30)
    glColor3f(1, 1, 1)
    glVertex2d(-60,30)
    glColor3f(1, 1, 1)
    glVertex2d(-60,-45)
    glColor3f(1, 1, 1)
    glVertex2d(-110, -45)
    glEnd()


def drawline():
    glLineWidth(2) #pixel size. by default 1 thake
    glBegin(GL_LINES)
    glColor3f(0, 0, 0) #konokichur color set (RGB)
    glVertex2f(100,40) #jekhane show korbe pixel
    glColor3f(0, 0, 0) #konokichur color set (RGB)
    glVertex2f(140,40) #jekhane show korbe pixel
    glEnd()

    glLineWidth(2) #pixel size. by default 1 thake
    glBegin(GL_LINES)
    glColor3f(0, 0, 0) #konokichur color set (RGB)
    glVertex2f(120,60) #jekhane show korbe pixel
    glColor3f(0, 0, 0) #konokichur color set (RGB)
    glVertex2f(120,20) #jekhane show korbe pixel
    glEnd()

    #Door lines

    glLineWidth(3) #pixel size. by default 1 thake
    glBegin(GL_LINES)
    glColor3f(0, 0, 0) #konokichur color set (RGB)
    glVertex2f(-110,30) #jekhane show korbe pixel
    glColor3f(0, 0, 0) #konokichur color set (RGB)
    glVertex2f(-60,30) #jekhane show korbe pixel
    glEnd()

    glLineWidth(3) #pixel size. by default 1 thake
    glBegin(GL_LINES)
    glColor3f(0, 0, 0) #konokichur color set (RGB)
    glVertex2d(-60,30)
    glColor3f(0, 0, 0)
    glVertex2d(-60,-45)
    glEnd()
    
    
    glLineWidth(3) #pixel size. by default 1 thake
    glBegin(GL_LINES)
    glColor3f(0, 0, 0) #konokichur color set (RGB)
    glVertex2d(-60,-45)
    glColor3f(0, 0, 0)
    glVertex2d(-110, -45)
    glEnd()

    glLineWidth(3) #pixel size. by default 1 thake
    glBegin(GL_LINES)
    glColor3f(0, 0, 0) #konokichur color set (RGB)
    glVertex2d(-110, -45)
    glColor3f(0, 0, 0)
    glVertex2d(-110,30)
    glEnd()

    #Window Lines
    glLineWidth(3) #pixel size. by default 1 thake
    glBegin(GL_LINES)
    glColor3f(0, 0, 0) #konokichur color set (RGB)
    glVertex2d(100,60)
    glColor3f(0, 0, 0)
    glVertex2d(140,60)

    glEnd()


    glLineWidth(3) #pixel size. by default 1 thake
    glBegin(GL_LINES)
    glColor3f(0, 0, 0) #konokichur color set (RGB)
    glVertex2d(140,60)
    glColor3f(0, 0, 0)
    glVertex2d(140,20)
    glEnd()

    glLineWidth(3) #pixel size. by default 1 thake
    glBegin(GL_LINES)
    glColor3f(0, 0, 0) #konokichur color set (RGB)
    glVertex2d(140,20)
    glColor3f(0, 0, 0)
    glVertex2d(100, 20)
    glEnd()

    glLineWidth(3) #pixel size. by default 1 thake
    glBegin(GL_LINES)
    glColor3f(0, 0, 0) #konokichur color set (RGB)
    glVertex2d(100, 20)
    glColor3f(0, 0, 0)
    glVertex2d(100,60)
    glEnd()

    #Fine detailing
    glLineWidth(5) #pixel size. by default 1 thake
    glBegin(GL_LINES)
    glColor3f(0, 0, 0) #konokichur color set (RGB)
    glVertex2d(-170,100)
    glColor3f(0, 0, 0)
    glVertex2d(170,100)
    glEnd()
        
    glLineWidth(5) #pixel size. by default 1 thake
    glBegin(GL_LINES)
    glColor3f(0, 0, 0) #konokichur color set (RGB)
    glVertex2d(170,100)
    glColor3f(0,0,0)
    glVertex2d(0,160)
    glEnd()

    glLineWidth(5) #pixel size. by default 1 thake
    glBegin(GL_LINES)
    glColor3f(0, 0, 0) #konokichur color set (RGB)
    glVertex2d(0,160)
    glColor3f(0,0,0)
    glVertex2d(-170,100)
    glEnd()

    #____________

    glLineWidth(5) #pixel size. by default 1 thake
    glBegin(GL_LINES)
    glVertex2d(-165,100)
    glColor3f(0, 0, 0)
    glVertex2d(165,100)
    glEnd()

    glLineWidth(5) #pixel size. by default 1 thake
    glBegin(GL_LINES)
    glColor3f(0, 0, 0) #konokichur color set (RGB)
    glVertex2d(165,100)
    glColor3f(0,0,0)
    glVertex2d(165,-50)
    glEnd()

    glLineWidth(5) #pixel size. by default 1 thake
    glBegin(GL_LINES)
    glColor3f(0, 0, 0) #konokichur color set (RGB)
    glVertex2d(165,-50)
    glColor3f(0,0,0)
    glVertex2d(-165,-50)
    glEnd()

    glLineWidth(5) #pixel size. by default 1 thake
    glBegin(GL_LINES)
    glColor3f(0, 0, 0) #konokichur color set (RGB)
    glVertex2d(-165,-50)
    glColor3f(0,0,0)
    glVertex2d(-165,100)
    glEnd()
    


def draw_rain_lines(gfx, s=2):
    global color
    for i in range(-200, 200, 20):
        glLineWidth(s) #pixel size. by default 1 thake
        glBegin(GL_LINES)
        a, b, c, d = rfx[random.randint(0,19)]
        glColor3f(color, color, color) #konokichur color set (RGB)
        glVertex2f(c,a) #jekhane show korbe pixel
        glVertex2f(d,b) #jekhane show korbe pixel
        glEnd()


def keyboardListener(key, x, y):
    global color, bg_color
    if key==b'f':
        print("It's daytime")
        color = 1
        bg_color = 0
    if key==b'g':
        print("It's night time")
        color = 0
        bg_color = 1

    glutPostRedisplay()

def specialKeyListener(key, x, y):
    global speed
    if key=='w':
        print(1)
    if key==GLUT_KEY_LEFT:
        for i in rfx:
            i[3] -= 2
        print("Bended leftward")
    if key== GLUT_KEY_RIGHT:		#// up arrow key
        for i in rfx:
            i[3] += 2
        print("Bended rightward")
    glutPostRedisplay()
    # if key==GLUT_KEY_RIGHT:
        
    # if key==GLUT_KEY_LEFT:
        

    # if key==GLUT_KEY_PAGE_UP:
       
    # if key==GLUT_KEY_PAGE_DOWN:
        
    # case GLUT_KEY_INSERT:
    #   
    #
    # case GLUT_KEY_HOME:
    #     
    # case GLUT_KEY_END:
    #   


def display():
    #//clear the display
    global bg_color
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(bg_color, bg_color, bg_color,0);	#//color black
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


    # global ballx, bally, ball_size
    # draw_points(ballx, bally, ball_size)
    drawShapes()
    drawline()
    draw_points(-69, -10, 5)
    draw_rain_lines(gfx)


    # if(create_new):
    #     m,n = create_new
    #     glBegin(GL_POINTS)
    #     glColor3f(0.7, 0.8, 0.6)
    #     glVertex2f(m,n)
    #     glEnd()


    glutSwapBuffers()


def animate():
    #//codes for any changes in Models, Camera
    glutPostRedisplay()
    glutPostRedisplay()
    global gfx
    for i in rfx:
        i[0] = (i[0]-speed)%240
        i[1] = (i[1]-speed)%240

def init():
    #//clear the screen
    glClearColor(0,0,0,0)
    #//load the PROJECTION matrix
    glMatrixMode(GL_PROJECTION)
    #//initialize the matrix
    glLoadIdentity()
    #//give PERSPECTIVE parameters
    gluPerspective(104,	1,	1,	1000.0)
    # **(important)**aspect ratio that determines the field of view in the X direction (horizontally). The bigger this angle is, the more you can see of the world - but at the same time, the objects you can see will become smaller.
    #//near distance
    #//far distance


glutInit()
glutInitWindowSize(W_Width, W_Height)
glutInitWindowPosition(1000, 0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB) #	//Depth, Double buffer, RGB color

# glutCreateWindow("My OpenGL Program")
wind = glutCreateWindow(b"OpenGL Coding Practice")
init()

glutDisplayFunc(display)	#display callback function
glutIdleFunc(animate)	#what you want to do in the idle time (when no drawing is occuring)
glutKeyboardFunc(keyboardListener)
glutSpecialFunc(specialKeyListener)
glutMainLoop()		#The main loop of OpenGL
