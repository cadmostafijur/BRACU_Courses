from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math

W_Width, W_Height = 500, 500

ballx = bally = 0
speed = 0.01
ball_size = 2
create_new = False

special_circle_radius = 5  # Initial radius of the special circle
special_circle_direction = 1  # 1 for expanding, -1 for shrinking
special_circle_y = 200  # Initial Y position of the special circle
points = 0  # Score


class point:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0


def crossProduct(a, b):
    result = point()
    result.x = a.y * b.z - a.z * b.y
    result.y = a.z * b.x - a.x * b.z
    result.z = a.x * b.y - a.y * b.x
    return result


def convert_coordinate(x, y):
    global W_Width, W_Height
    a = x - (W_Width / 2)
    b = (W_Height / 2) - y
    return a, b


def draw_points(x, y, s):
    glPointSize(s)  # pixel size. by default 1 thake
    glBegin(GL_POINTS)
    glVertex2f(x, y)  # jekhane show korbe pixel
    glEnd()


def draw_special_circle():
    global special_circle_radius, special_circle_y
    glColor3f(1.0, 1.0, 0.0)  # Yellow color for the special circle
    glBegin(GL_POLYGON)
    for i in range(360):
        angle = math.radians(i)
        x = special_circle_radius * math.cos(angle)
        y = special_circle_radius * math.sin(angle)
        glVertex2f(x, special_circle_y + y)
    glEnd()


def check_collision(ball_x, ball_y, ball_size):
    global special_circle_radius, special_circle_y, points
    # Check if the ball hits the special circle
    distance = math.sqrt((ball_x) ** 2 + (ball_y - special_circle_y) ** 2)
    if distance <= (special_circle_radius + ball_size):
        points += 10  # Award points for hitting the special circle
        print("Points Awarded! Total Points:", points)


def drawAxes():
    glLineWidth(1)
    glBegin(GL_LINES)
    glColor3f(1.0, 0.0, 0.0)
    glVertex2f(250, 0)
    glVertex2f(-250, 0)
    glColor3f(0.0, 0.0, 1.0)
    glVertex2f(0, 250)
    glVertex2f(0, -250)
    glEnd()

    glPointSize(5)
    glBegin(GL_POINTS)
    glColor3f(0, 1.0, 0.0)
    glVertex2f(0, 0)

    glEnd()


def drawShapes():
    glBegin(GL_TRIANGLES)
    glVertex2d(-170, 170)
    glColor3f(0, 1.0, 0.0)
    glVertex2d(-180, 150)
    glColor3f(1, 0, 0.0)
    glVertex2d(-160, 150)
    glEnd()

    glBegin(GL_QUADS)
    glVertex2d(-170, 120)
    glColor3f(1, 0, 1)
    glVertex2d(-150, 120)
    glColor3f(0, 0, 1)
    glVertex2d(-150, 140)
    glColor3f(0, 1, 0)
    glVertex2d(-170, 140)
    glEnd()


def keyboardListener(key, x, y):
    global ball_size
    if key == b'w':
        ball_size += 1
        print("Size Increased")
    if key == b's':
        ball_size -= 1
        print("Size Decreased")
    glutPostRedisplay()


def specialKeyListener(key, x, y):
    global speed
    if key == 'w':
        print(1)
    if key == GLUT_KEY_UP:
        speed *= .000000002
        print("Speed Increased")
    if key == GLUT_KEY_DOWN:  # // up arrow key
        speed /= .000000002
        print("Speed Decreased")
    glutPostRedisplay()


def mouseListener(button, state, x, y):  # /#/x, y is the x-y of the screen (2D)
    global ballx, bally, create_new
    if button == GLUT_LEFT_BUTTON:
        if (state == GLUT_DOWN):  # // 2 times?? in ONE click? -- solution is checking DOWN or UP
            print(x, y)
            c_X, c_y = convert_coordinate(x, y)
            ballx, bally = c_X, c_y

    if button == GLUT_RIGHT_BUTTON:
        if state == GLUT_DOWN:
            create_new = convert_coordinate(x, y)
    glutPostRedisplay()


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0, 0, 0, 0);  # //color black
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0, 0, 200, 0, 0, 0, 0, 1, 0)
    glMatrixMode(GL_MODELVIEW)

    drawAxes()
    global ballx, bally, ball_size
    draw_points(ballx, bally, ball_size)
    drawShapes()
    draw_special_circle()  # Draw the special circle

    # Collision check with the special circle
    check_collision(ballx, bally, ball_size)

    glutSwapBuffers()


def animate():
    glutPostRedisplay()
    global ballx, bally, speed
    ballx = (ballx + speed) % 180
    bally = (bally + speed) % 180

    # Handle the special circle's dynamic radius and direction
    global special_circle_radius, special_circle_direction, special_circle_y
    if special_circle_radius >= 30:  # Shrink if radius is too large
        special_circle_direction = -1
    elif special_circle_radius <= 5:  # Expand if radius is too small
        special_circle_direction = 1

    special_circle_radius += special_circle_direction * 0.1
    special_circle_y -= 0.5  # Make the circle fall down
    if special_circle_y <= -200:  # Reset position when it goes off-screen
        special_circle_y = 200


def init():
    glClearColor(0, 0, 0, 0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(104, 1, 1, 1000.0)


glutInit()
glutInitWindowSize(W_Width, W_Height)
glutInitWindowPosition(0, 0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)

wind = glutCreateWindow(b"OpenGL Coding Practice")
init()

glutDisplayFunc(display)
glutIdleFunc(animate)

glutKeyboardFunc(keyboardListener)
glutSpecialFunc(specialKeyListener)
glutMouseFunc(mouseListener)

glutMainLoop()
