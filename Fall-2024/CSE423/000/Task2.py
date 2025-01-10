from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import math
import time

W_Width, W_Height = 800,800

point_list = []
direction = [1, -1]
freeze = False
create_new = False
blink = False


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

def generate_point(x, y):
    global point_list
    if (x<165 and x>-165) and (y<100 and y>-50):
        point_list.append([x,y, [random.random(), random.random(), random.random()], random.choice([0.02, -0.02]), random.choice([0.02, -0.02])])

def draw_points():
    global point_list
    for i in point_list:
        x, y, color,s1,s2 = i
        if not blink:
            glPointSize(10) #pixel size. by default 1 thake
            glBegin(GL_POINTS)
            glColor3f(*color) #konokichur color set (RGB)
            glVertex2f(x,y) #jekhane show korbe pixel
            glEnd()

        else:
            glPointSize(10) #pixel size. by default 1 thake
            glBegin(GL_POINTS)
            glColor3f(0, 0, 0)
            glVertex2f(x,y) #jekhane show korbe pixel
            # time.sleep(0.01)
            # glEnd()

            # glPointSize(10) #pixel size. by default 1 thake
            # glBegin(GL_POINTS)
            # glColor3f(*color)
            # glVertex2f(x,y) #jekhane show korbe pixel
            glEnd()
            
            
            # glVertex2f(x,y) #jekhane show korbe pixel

            # time.sleep(0.000001)

            # glColor3f(*color)
            # time.sleep(0.000001)
            # glVertex2f(x,y) #jekhane show korbe pixel
        


def drawline():
    glLineWidth(5) #pixel size. by default 1 thake
    glBegin(GL_LINES)
    glColor3f(1,1,1)
    glVertex2d(-165,100)
    glColor3f(1, 1, 1)
    glVertex2d(165,100)
    glEnd()

    glLineWidth(5) #pixel size. by default 1 thake
    glBegin(GL_LINES)
    glColor3f(1, 1, 1) #konokichur color set (RGB)
    glVertex2d(165,100)
    glColor3f(1,1,1)
    glVertex2d(165,-50)
    glEnd()

    glLineWidth(5) #pixel size. by default 1 thake
    glBegin(GL_LINES)
    glColor3f(1, 1, 1) #konokichur color set (RGB)
    glVertex2d(165,-50)
    glColor3f(1,1,1)
    glVertex2d(-165,-50)
    glColor3f(1, 1, 1)

    glEnd()

    glLineWidth(5) #pixel size. by default 1 thake
    glBegin(GL_LINES)
    glColor3f(1, 1, 1) #konokichur color set (RGB)
    glVertex2d(-165,-50)
    glColor3f(1,1,1)
    glVertex2d(-165,100)
    glColor3f(1,1,1)

    glEnd()


def keyboardListener(key, x, y):
    global freeze
    if key==b' ':
        freeze = not freeze
    glutPostRedisplay()

def specialKeyListener(key, x, y):
    global point_list
    if key=='w':
        print(1)
    if key==GLUT_KEY_UP:
        for i in range(len(point_list)):
            print(point_list[i][3])
            point_list[i][3] += 0.001
            point_list[i][4] += 0.001
        print("Speed Increased")
    if key== GLUT_KEY_DOWN:		#// up arrow key
        for i in range(len(point_list)):
            point_list[i][3] -= 0.001
            point_list[i][4] -= 0.001
            print(point_list[i][3])

        print("Speed Decreased")
    glutPostRedisplay()


def mouseListener(button, state, x, y):	#/#/x, y is the x-y of the screen (2D)
    global blink
    if button==GLUT_LEFT_BUTTON:
        if(state == GLUT_DOWN):    # 		// 2 times?? in ONE click? -- solution is checking DOWN or UP
            blink = not blink
            
        
    if button == GLUT_RIGHT_BUTTON:
        if(state == GLUT_UP):
            c_x, c_y = convert_coordinate(x,y)
            generate_point(c_x,c_y)

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

    global ballx, bally, ball_size
    # draw_points(ballx, bally, ball_size)
    # for i in range(-200, 200, 10):
    #     draw_rain_lines(i,rlist[i%10][0],i,rlist[i%10][1])
    drawline()
    draw_points()



    if(create_new):
        m,n = create_new
        glBegin(GL_POINTS)
        glColor3f(0.7, 0.8, 0.6)
        glVertex2f(m,n)
        glEnd()


    glutSwapBuffers()



def animate():
    #//codes for any changes in Models, Camera
    glutPostRedisplay()
    global point_list
    if not freeze:
        for i in range(len(point_list)):
            x, y, color, sx, sy = point_list[i] 

            # if blink:
            #     old_color = color
            #     r, g, b = color
            #     if r==0 and g==0 and b==0:
            #         point_list[i][3] = old_color
            #     else:  
            #             if r==0:
            #                 pass
            #             else:
            #                 r -= 0.1
            #             if g==0:
            #                 pass
            #             else:
            #                 g -= 0.1
            #             if b==0:
            #                 pass
            #             else:
            #                 b -= 0.1

            #     # point_list[i][3] = [r/2, g/2, b/2]
            #     # # time.sleep(0.0001)
            #     # point_list[i][3] = [0, 0, 0]
            #     # # time.sleep(0.0001)
            #     # point_list[i][3] = old_color


            x += sx
            y += sy
            if x >= 165 or x <= -165:
                sx*= -1
            if y >= 100 or y <= -50:
                sy*= -1
            
            point_list[i] = [x, y, color, sx, sy]




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
