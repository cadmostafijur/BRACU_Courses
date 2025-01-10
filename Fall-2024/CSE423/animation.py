from OpenGL.GL import *
from OpenGL.GLUT import *
import random
import time

# Window dimensions
W_Width, W_Height = 500, 800

# Initializing game variables
bullet = []
score = 0
misfires = 0
freeze = False
gameover = 0

# Class representing a bubble in the game
class Bubble:
    def __init__(self):
        self.x = random.randint(-220, 220)  # Random horizontal position
        self.y = 330  # Fixed vertical position
        self.r = random.randint(20, 25)  # Random radius size
        self.color = [1, 1, 0]  # Yellow color

# Class representing the catcher (spaceship)
class Catcher:
    def __init__(self):
        self.x = 0  # Initial horizontal position of the catcher
        self.color = [1, 1, 1]  # White color

# Function to plot a point at (x, y)
def plot_point(x, y):
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()

# Function to convert coordinates based on zone
def convert_t_zone0(x, y, zone):
    if zone == 0:
        return (x, y)
    elif zone == 1:
        return (y, x)
    elif zone == 2:
        return (y, -x)
    elif zone == 3:
        return (-x, y)
    elif zone == 4:
        return (-x, -y)
    elif zone == 5:
        return (-y, -x)
    elif zone == 6:
        return (-y, x)
    elif zone == 7:
        return (x, -y)

# Function to convert coordinates for a different zone (another set of transformations)
def convert_f_zone0(x, y, zone):
    if zone == 0:
        return (x, y)
    elif zone == 1:
        return (y, x)
    elif zone == 2:
        return (-y, x)
    elif zone == 3:
        return (-x, y)
    elif zone == 4:
        return (-x, -y)
    elif zone == 5:
        return (-y, -x)
    elif zone == 6:
        return (y, -x)
    elif zone == 7:
        return (x, -y)

# Function to draw a line using the midpoint algorithm
def midpoint_l(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1

    zone = 0
    if abs(dx) > abs(dy):
        if dx >= 0 and dy >= 0:
            zone = 0
        elif dx < 0 and dy >= 0:
            zone = 3
        elif dx < 0 and dy < 0:
            zone = 4
        elif dx >= 0 and dy < 0:
            zone = 7
    else:
        if dx >= 0 and dy >= 0:
            zone = 1
        elif dx < 0 and dy >= 0:
            zone = 2
        elif dx < 0 and dy < 0:
            zone = 5
        elif dx >= 0 and dy < 0:
            zone = 6

    # Adjust the coordinates for the selected zone
    x1, y1 = convert_t_zone0(x1, y1, zone)
    x2, y2 = convert_t_zone0(x2, y2, zone)

    dx = x2 - x1
    dy = y2 - y1

    d = 2 * dy - dx
    incrE = 2 * dy
    incrNE = 2 * (dy - dx)

    x, y = x1, y1
    x0, y0 = convert_f_zone0(x, y, zone)
    plot_point(x0, y0)

    while x < x2:
        if d <= 0:
            d += incrE
            x += 1
        else:
            d += incrNE
            x += 1
            y += 1
        x0, y0 = convert_f_zone0(x, y, zone)
        plot_point(x0, y0)

# Function to draw a circle using the midpoint circle algorithm
def midpoint_circle(radius, centerX=0, centerY=0):
    glBegin(GL_POINTS)
    x = 0
    y = radius
    d = 1 - radius
    while y > x:
        glVertex2f(x + centerX, y + centerY)
        glVertex2f(x + centerX, -y + centerY)
        glVertex2f(-x + centerX, y + centerY)
        glVertex2f(-x + centerX, -y + centerY)
        glVertex2f(y + centerX, x + centerY)
        glVertex2f(y + centerX, -x + centerY)
        glVertex2f(-y + centerX, x + centerY)
        glVertex2f(-y + centerX, -x + centerY)
        if d < 0:
            d += 2 * x + 3
        else:
            d += 2 * x - 2 * y + 5
            y -= 1
        x += 1
    glEnd()

# Initialize some bubble objects
bubble = [Bubble(), Bubble(), Bubble(), Bubble(), Bubble()]
bubble.sort(key=lambda b: b.x)
catcher = Catcher()

# Function to draw the bullet (white circle)
def draw_bullet():
    global bullet
    glPointSize(2)
    glColor3f(1, 1, 1)
    for i in bullet:
        midpoint_circle(8, i[0], i[1])

# Function to draw all the bubbles in the game
def draw_bubble():
    global bubble
    glPointSize(2)

    for i in range(len(bubble)):
        if i == 0:
            glColor3f(bubble[i].color[0], bubble[i].color[1], bubble[i].color[2])
            midpoint_circle(bubble[i].r, bubble[i].x, bubble[i].y)
        elif (bubble[i - 1].y < (330 - 2 * bubble[i].r - 2 * bubble[i - 1].r)) or (
                abs(bubble[i - 1].x - bubble[i].x) > (2 * bubble[i - 1].r + 2 * bubble[i].r + 10)):
            glColor3f(bubble[i].color[0], bubble[i].color[1], bubble[i].color[2])
            midpoint_circle(bubble[i].r, bubble[i].x, bubble[i].y)

# Function to draw the spaceship (catcher) with thrusters
def draw_spaceship(centerX=0, centerY=-365):
    glPointSize(2)

    # Drawing the spaceship body (blue edges)
    glColor3f(0, 0, 1)
    midpoint_l(centerX - 20, centerY - 20, centerX, centerY + 60)    # left edge
    midpoint_l(centerX, centerY + 60, centerX + 20, centerY - 20)    # right edge
    midpoint_l(centerX - 20, centerY - 20, centerX + 20, centerY - 20)  # base

    # Drawing thrusters (red rectangles)
    glColor3f(1, 0, 0)
    # Left thruster
    midpoint_l(centerX - 15, centerY - 20, centerX - 5, centerY - 20)  # top
    midpoint_l(centerX - 5, centerY - 20, centerX - 5, centerY - 40)  # right
    midpoint_l(centerX - 5, centerY - 40, centerX - 15, centerY - 40)  # bottom
    midpoint_l(centerX - 15, centerY - 40, centerX - 15, centerY - 20)  # left

    # Right thruster
    midpoint_l(centerX + 15, centerY - 20, centerX + 5, centerY - 20)  # top
    midpoint_l(centerX + 5, centerY - 20, centerX + 5, centerY - 40)  # right
    midpoint_l(centerX + 5, centerY - 40, centerX + 15, centerY - 40)  # bottom
    midpoint_l(centerX + 15, centerY - 40, centerX + 15, centerY - 20)  # left

    # Drawing balls (white circles) as part of the spaceship
    glColor3f(1, 1, 1)
    ball_radius = 4  # Ball size
    midpoint_circle(ball_radius, centerX - 5, centerY + 15)  # F ball
    midpoint_circle(ball_radius, centerX + 5, centerY + 15)  # S ball
    midpoint_circle(ball_radius, centerX - 5, centerY + 5)  # F ball
    midpoint_circle(ball_radius, centerX + 5, centerY + 5)  # S ball

# Function to draw all objects in the game (spaceship, bullets, and bubbles)
def draw_object():
    global score, misfires, freeze, bubble
    # Clear the screen
    glClear(GL_COLOR_BUFFER_BIT)

    # Draw spaceship, bullets, and bubbles
    draw_spaceship(catcher.x, -365)
    draw_bullet()
    draw_bubble()

    # Display score, misfires, and game state
    # (Update or draw these texts on screen here)
    # You can implement OpenGL text rendering here as per your need

    # Swap buffers to update the screen
    glutSwapBuffers()

# Function to handle key press events (moving the spaceship and firing bullets)
def keyboard(key, x, y):
    global catcher, bullet
    if key == b' ' and not freeze:  # Spacebar to fire bullet
        bullet.append([catcher.x, -355])  # Add new bullet above the catcher

    # Add code here for handling the movement of the spaceship, etc.

# Main loop to initialize and run the game
def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(W_Width, W_Height)
    glutCreateWindow(b"Spaceship Game")

    # Set up projection and view matrices
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-250, 250, -400, 400, -1, 1)

    # Register drawing function and keyboard event function
    glutDisplayFunc(draw_object)
    glutKeyboardFunc(keyboard)

    # Start the game loop
    glutMainLoop()

# Run the main function
if __name__ == "__main__":
    main()
