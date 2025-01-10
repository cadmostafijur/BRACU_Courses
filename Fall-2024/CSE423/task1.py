from OpenGL.GL import *
from OpenGL.GLUT import *
import random
import time

#######################################################

############# GLOBAL VARIABLES ####################
W_Width, W_Height = 500, 800

bullet = []
score = 0
misfires = 0
freeze = False
gameover = 0

###################################################################
class Bubble:
    def __init__(self):
        self.x = random.randint(-220, 220)
        self.y = 330
        self.r = random.randint(20, 25)
        self.color = [0, 1, 0]  # Green color for the bubble
        self.size = 1.0  # Initialize size multiplier for blinking

    def update(self):
        self.size = 1.0 + 0.2 * (1 if time.time() % 1 > 0.5 else 0)  # Blink effect

class Catcher:
    def __init__(self):
        self.x = 0
        self.color = [1, 1, 1]

def plot_point(x, y):
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()

def convert_to_zone0(x, y, zone):
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

def convert_from_zone0(x, y, zone):
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

def midpoint_line(x1, y1, x2, y2):
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

    x1, y1 = convert_to_zone0(x1, y1, zone)
    x2, y2 = convert_to_zone0(x2, y2, zone)

    dx = x2 - x1
    dy = y2 - y1

    d = 2 * dy - dx
    incrE = 2 * dy
    incrNE = 2 * (dy - dx)

    x, y = x1, y1
    x0, y0 = convert_from_zone0(x, y, zone)
    plot_point(x0, y0)

    while x < x2:
        if d <= 0:
            d += incrE
            x += 1
        else:
            d += incrNE
            x += 1
            y += 1
        x0, y0 = convert_from_zone0(x, y, zone)
        plot_point(x0, y0)


def midpointcircle(radius, centerX=0, centerY=0):
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

##################################################################

bubble = [Bubble(), Bubble(), Bubble(), Bubble(), Bubble()]
bubble.sort(key=lambda b: b.x)
catcher = Catcher()

def draw_bullet():
    global bullet
    glPointSize(2)
    glColor3f(1, 1, 1)
    for i in bullet:
        midpointcircle(8, i[0], i[1])

def draw_bubble():
    global bubble
    glPointSize(2)

    for i in range(len(bubble)):
        if i == 0:
            glColor3f(bubble[i].color[0], bubble[i].color[1], bubble[i].color[2])
            midpointcircle(bubble[i].r * bubble[i].size, bubble[i].x, bubble[i].y)
        elif (bubble[i - 1].y < (330 - 2 * bubble[i].r - 2 * bubble[i - 1].r)) or (
                abs(bubble[i - 1].x - bubble[i].x) > (2 * bubble[i - 1].r + 2 * bubble[i].r + 10)):
            glColor3f(bubble[i].color[0], bubble[i].color[1], bubble[i].color[2])
            midpointcircle(bubble[i].r * bubble[i].size, bubble[i].x, bubble[i].y)

def draw_spaceship(centerX=0, centerY=-365):
    glPointSize(2)

    # Body (blue edges) - Increase size by scaling up
    glColor3f(0, 0, 1)
    # Left edge
    midpoint_line(centerX - 20, centerY - 20, centerX, centerY + 60)
    # Right edge
    midpoint_line(centerX, centerY + 60, centerX + 20, centerY - 20)
    # Base
    midpoint_line(centerX - 20, centerY - 20, centerX + 20, centerY - 20)

    # Rocket nose (white triangle) - Increase size by scaling up
    glColor3f(1, 1, 1)
    # Nose triangle
    midpoint_line(centerX, centerY + 80, centerX - 10, centerY + 60)  # Left edge
    midpoint_line(centerX - 10, centerY + 60, centerX + 10, centerY + 60)  # Base
    midpoint_line(centerX + 10, centerY + 60, centerX, centerY + 80)  # Right edge

    # Thrusters (red rectangles) - Increase size by scaling up
    glColor3f(1, 0, 0)
    # Left thruster
    midpoint_line(centerX - 15, centerY - 20, centerX - 5, centerY - 20)  # Top edge
    midpoint_line(centerX - 5, centerY - 20, centerX - 5, centerY - 40)  # Right edge
    midpoint_line(centerX - 5, centerY - 40, centerX - 15, centerY - 40)  # Bottom edge
    midpoint_line(centerX - 15, centerY - 40, centerX - 15, centerY - 20)  # Left edge

    # Right thruster
    midpoint_line(centerX + 15, centerY - 20, centerX + 5, centerY - 20)  # Top edge
    midpoint_line(centerX + 5, centerY - 20, centerX + 5, centerY - 40)  # Right edge
    midpoint_line(centerX + 5, centerY - 40, centerX + 15, centerY - 40)  # Bottom edge
    midpoint_line(centerX + 15, centerY - 40, centerX + 15, centerY - 20)  # Left edge

    # Balls (green circles) inside the body of the spaceship
    glColor3f(1, 1, 1)
    ball_radius = 4  # Increase the ball size
    # Draw two balls inside the spaceship, centered horizontally and positioned lower in the ship
    midpointcircle(ball_radius, centerX - 6, centerY + 20)  # Left ball
    midpointcircle(ball_radius, centerX + 6, centerY + 20)  # Right ball

def animate():
    current_time = time.time()
    delta_time = current_time - animate.start_time if hasattr(animate, 'start_time') else 0
    animate.start_time = current_time

    global freeze, bubble, catcher, gameover, score, bullet, misfires
    if not freeze and gameover < 3 and misfires < 3:
        # Update bubbles (move them down and apply blinking effect)
        for b in bubble:
            b.update()

        temp = []
        for i in range(len(bullet)):
            if bullet[i][1] < 400:
                bullet[i][1] += 10
            else:
                temp.append(i)
                misfires += 1
        try:
            for j in temp:
                del bullet[j]
        except:
            pass

        for i in range(len(bubble)):
            if i == 0:
                if bubble[i].y > -400:
                    bubble[i].y -= (10 + score * 5) * delta_time
                else:
                    gameover += 1
                    del bubble[i]
                    bubble.append(Bubble())
                    bubble.sort(key=lambda b: b.y)
            elif (bubble[i - 1].y < (330 - 2 * bubble[i].r - 2 * bubble[i - 1].r)) or (
                    abs(bubble[i - 1].x - bubble[i].x) > (2 * bubble[i - 1].r + 2 * bubble[i].r + 10)):
                if bubble[i].y > -400:
                    bubble[i].y -= (10 + score * 5) * delta_time
                else:
                    gameover += 1
                    del bubble[i]
                    bubble.append(Bubble())
                    bubble.sort(key=lambda b: b.y)
        try:
            for i in range(len(bubble)):
                if abs(bubble[i].y - -345) < (bubble[i].r) and abs(bubble[i].x - catcher.x) < (bubble[i].r + 20):
                    gameover += 3  
                for j in range(len(bullet)):
                    if abs(bubble[i].y - bullet[j][1]) < (bubble[i].r + 15) and abs(bubble[i].x - bullet[j][0]) < (
                            bubble[i].r + 20):
                        score += 1
                        print("Score:", score)
                        bubble[i].blinking = True  # Trigger blinking effect
                        del bullet[j]
                        bubble.append(Bubble())
        except:
            pass

    if (gameover >= 3 or misfires >= 3) and not freeze:
        print("Game Over! Score:", score)

        freeze = True
        bubble = [] 

    time.sleep(1 / 1000)
    glutPostRedisplay()

def key_pressed(*args):
    global bullet
    if args[0] == b' ':
        bullet.append([catcher.x, -355])

def main():
    global catcher, bullet
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE)
    glutInitWindowSize(W_Width, W_Height)
    glutCreateWindow(b"Bubble Shooter Game")
    glClearColor(0.1, 0.1, 0.1, 1)
    glOrtho(-250, 250, -400, 400, -1, 1)
    glutDisplayFunc(animate)
    glutKeyboardFunc(key_pressed)
    glutMainLoop()

if __name__ == "__main__":
    main()
