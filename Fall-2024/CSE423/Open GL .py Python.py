
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import random


widthofscreen, heightofscreen = 1500, 1000

catch1 = widthofscreen // 8
catch2 = 280  # Adjusted position of the catcher
lane2 = 280
bullets = []
gravels = []
pause = False
bullet_speed = 5
bird_shifting = 0
shifting_magnitude = 0
score1 = 0
obstacle1 = 260  # Random initial position along the height
obstacle2 = widthofscreen  # Initial position along the width
obstacle_size = random.randint(15, 30)
obstacle_speed = 2
diamond_color = [1, 0, 0]
shooter_x = widthofscreen // 2
shooter_y = 90
shooter_r = 15
game_over = False
is_day = True
pause = False
# Fixed color for the diamond (red)
score = 0
balls = []
rotation_angle = 0
color = [random.random(), random.random(), random.random()]
stars = []
jump_height = 200
jump_speed = 5
jump_count = 0
sun_x = widthofscreen // 4
sun_y = heightofscreen - 120


def creatediamond():
    global diamond_color, obstacle_size, obstacle2, obstacle1, balls
    x = random.randint(1500, 1800)
    y = obstacle1
    r = obstacle_size
    balls.append((x, y, r))


def go_diamond():
    global balls
    if pause == False:
        new_balls = []

        for i in balls[0:4]:
            x, y, r = i
            for j in balls:
                if (j[0] < x + r and j[1] < y + r) or (j[0] > x - r and j[1] > y - r) or (
                        j[0] > x - r and j[1] < y + r) or (j[0] < x + r and j[1] > y - r):
                    balls.pop(balls.index(j))
            x -= 5
            if x > 0:
                new_balls.append((x, y, r))

        balls = new_balls


def draw_balls():
    global color, balls
    for i in balls:
        circle(i[0], i[1], i[2], color)


def generate_stars():
    global widthofscreen, heightofscreen, stars
    stars = [(random.randint(0, widthofscreen), random.randint(0, heightofscreen)) for _ in range(50)]


def draw_bullet():
    for b in bullets:
        bx, by, bz = b
        circle(bx, by, bz, [1, 0, 0])


def shoot_bullet():
    global bullets

    if pause == False:
        new_bullets = []

        for b in bullets:
            x, y, r = b
            x += 30
            if x < widthofscreen:
                new_bullets.append((x, y, r))
        bullets = new_bullets


def clouds():
    global shifting_magnitude


    glEnable(GL_POINT_SMOOTH)
    if is_day:
        glColor3f(1, 1, 1)
    else:
        glColor3f(.5, .5, .5)
    glPointSize(30)
    glBegin(GL_POINTS)
    # first phase
    glVertex2f(100 + shifting_magnitude, 900)
    glVertex2f(120 + shifting_magnitude, 900)
    glVertex2f(140 + shifting_magnitude, 900)
    glVertex2f(110 + shifting_magnitude, 920)
    glVertex2f(130 + shifting_magnitude, 920)
    # second phase
    glVertex2f(100 + 200 + shifting_magnitude, 900 - 40)
    glVertex2f(120 + 200 + shifting_magnitude, 900 - 40)
    glVertex2f(140 + 200 + shifting_magnitude, 900 - 40)
    glVertex2f(110 + 200 + shifting_magnitude, 920 - 40)
    glVertex2f(130 + 200 + shifting_magnitude, 920 - 40)
    # third phase
    glVertex2f(100 + 400 + shifting_magnitude, 900 - 120)
    glVertex2f(120 + 400 + shifting_magnitude, 900 - 120)
    glVertex2f(140 + 400 + shifting_magnitude, 900 - 120)
    glVertex2f(110 + 400 + shifting_magnitude, 920 - 120)
    glVertex2f(130 + 400 + shifting_magnitude, 920 - 120)
    glEnd()

    glBegin(GL_POINTS)
    # first phase
    glVertex2f(400 + shifting_magnitude, 900)
    glVertex2f(420 + shifting_magnitude, 900)
    glVertex2f(440 + shifting_magnitude, 900)
    glVertex2f(410 + shifting_magnitude, 920)
    glVertex2f(430 + shifting_magnitude, 920)
    # second phase
    glVertex2f(400 + 200 + shifting_magnitude, 900 - 40)
    glVertex2f(420 + 200 + shifting_magnitude, 900 - 40)
    glVertex2f(440 + 200 + shifting_magnitude, 900 - 40)
    glVertex2f(410 + 200 + shifting_magnitude, 920 - 40)
    glVertex2f(140 + 200 + shifting_magnitude, 920 - 40)
    # third phase
    glVertex2f(400 + 400 + shifting_magnitude, 900 - 120)
    glVertex2f(420 + 400 + shifting_magnitude, 900 - 120)
    glVertex2f(440 + 400 + shifting_magnitude, 900 - 120)
    glVertex2f(410 + 400 + shifting_magnitude, 920 - 120)
    glVertex2f(430 + 400 + shifting_magnitude, 920 - 120)
    glEnd()

    glBegin(GL_POINTS)
    # first phase
    glVertex2f(800 + shifting_magnitude, 900)
    glVertex2f(820 + shifting_magnitude, 900)
    glVertex2f(840 + shifting_magnitude, 900)
    glVertex2f(810 + shifting_magnitude, 920)
    glVertex2f(830 + shifting_magnitude, 920)
    # second phase
    glVertex2f(800 + 200 + shifting_magnitude, 900 - 40)
    glVertex2f(820 + 200 + shifting_magnitude, 900 - 40)
    glVertex2f(840 + 200 + shifting_magnitude, 900 - 40)
    glVertex2f(810 + 200 + shifting_magnitude, 920 - 40)
    glVertex2f(840 + 200 + shifting_magnitude, 920 - 40)
    # third phase
    glVertex2f(800 + 400 + shifting_magnitude, 900 - 120)
    glVertex2f(820 + 400 + shifting_magnitude, 900 - 120)
    glVertex2f(840 + 400 + shifting_magnitude, 900 - 120)
    glVertex2f(810 + 400 + shifting_magnitude, 920 - 120)
    glVertex2f(830 + 400 + shifting_magnitude, 920 - 120)
    glEnd()


def createrestartbutton():
    Midpoint(10, heightofscreen - 30, 60, heightofscreen - 30, [0, 0, 0])
    Midpoint(10, heightofscreen - 30, 20, heightofscreen - 20, [0, 0, 0])
    Midpoint(10, heightofscreen - 30, 20, heightofscreen - 40, [0, 0, 0])


def createpausebutton():
    bright_yellow = [1.0, 1.0, 0.0]  # Bright yellow color
    if pause:
        Midpoint(widthofscreen // 2 - 5, heightofscreen - 20, widthofscreen // 2 - 5, heightofscreen - 40,
                 bright_yellow)
        Midpoint(widthofscreen // 2 - 5, heightofscreen - 40, widthofscreen // 2 + 20, heightofscreen - 30,
                 bright_yellow)
        Midpoint(widthofscreen // 2 - 5, heightofscreen - 20, widthofscreen // 2 + 20, heightofscreen - 30,
                 bright_yellow)
    else:
        Midpoint(widthofscreen // 2 - 5, heightofscreen - 20, widthofscreen // 2 - 5, heightofscreen - 40,
                 bright_yellow)
        Midpoint(widthofscreen // 2 + 5, heightofscreen - 20, widthofscreen // 2 + 5, heightofscreen - 40,
                 bright_yellow)


def createexitbutton():
    Midpoint(widthofscreen - 30, heightofscreen - 20, widthofscreen - 10, heightofscreen - 40, [1, 0, 0])
    Midpoint(widthofscreen - 30, heightofscreen - 40, widthofscreen - 10, heightofscreen - 20, [1, 0, 0])


def Midpoint(x1, y1, x2, y2, color):
    glColor3f(*color)
    glPointSize(5)
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    steep = abs(dy) > abs(dx)

    if steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2
        dx, dy = dy, dx

    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1

    d = 2 * dy - dx
    y = y1

    for x in range(int(x1), int(x2) + 1):
        if steep:
            glBegin(GL_POINTS)
            glVertex2f(int(y), int(x))
            glEnd()
        else:
            glBegin(GL_POINTS)
            glVertex2f(int(x), int(y))
            glEnd()

        if d > 0:
            y += 1 if y1 < y2 else -1
            d -= 2 * dx
        d += 2 * dy


def circle(a, b, r, color):
    glColor3f(*color)
    glPointSize(5)
    d = 1 - r
    x = 0
    y = r
    while x <= y:
        if d < 0:
            d = d + 2 * x + 3
            x += 1
        else:
            d = d + 2 * x - 2 * y + 5
            x += 1
            y -= 1
        glBegin(GL_POINTS)
        glVertex2f(x + a, y + b)
        glVertex2f(x + a, -y + b)
        glVertex2f(-x + a, -y + b)
        glVertex2f(-x + a, y + b)
        glVertex2f(y + a, x + b)
        glVertex2f(y + a, -x + b)
        glVertex2f(-y + a, -x + b)
        glVertex2f(-y + a, x + b)
        glEnd()


def draw_sun():
    global widthofscreen, heightofscreen, is_day, sun_x, sun_y



    glColor3f(1, 1, 0)  # Yellow color for the shooter
    if not is_day:
        glColor3f(1, 1, 1)
    glPointSize(400)
    glBegin(GL_POINTS)
    glVertex2f(sun_x, sun_y)

    glEnd()


def createcatch(x, y):
    global catch1, catch2, game_over, rotation_angle, car_x, car_y, car_r
    color = [0.5, 0, 0.5]  # Default color for the tank
    if game_over:
        color = [1, 0, 0]  # Change color if the game is over

    # Draw tank base
    Midpoint(x - 100, y, x + 100, y, color)  # Top side of the base
    Midpoint(x - 100, y - 40, x + 100, y - 40, color)  # Bottom side of the base
    Midpoint(x - 100, y, x - 100, y - 40, color)  # Left side of the base
    Midpoint(x + 100, y, x + 100, y - 40, color)  # Right side of the base

    # Draw tank treads
    Midpoint(x - 110, y - 10, x - 100, y - 40, color)  # Left tread slant
    Midpoint(x + 110, y - 10, x + 100, y - 40, color)  # Right tread slant
    Midpoint(x - 110, y - 10, x + 110, y - 10, color)  # Top of the treads
    Midpoint(x - 110, y - 40, x - 100, y - 40, color)  # Bottom of left tread
    Midpoint(x + 110, y - 40, x + 100, y - 40, color)  # Bottom of right tread

    # Draw tank turret
    Midpoint(x - 40, y, x + 40, y, color)  # Bottom side of the turret
    Midpoint(x - 40, y, x - 40, y + 30, color)  # Left side of the turret
    Midpoint(x + 40, y, x + 40, y + 30, color)  # Right side of the turret
    Midpoint(x - 40, y + 30, x + 40, y + 30, color)  # Top side of the turret

    # Draw tank cannon
    Midpoint(x, y + 30, x, y + 70, color)  # Cannon extending from the turret

    # Draw tank circles (treads)
    circle(x - 90, y - 25, 15, color)  # Left tread circle
    circle(x + 90, y - 25, 15, color)  # Right tread circle


def change(value):
    global obstacle2, obstacle1, score, obstacle_size, obstacle_speed, game_over, diamond_color, catch1, catch2, bullets, shifting_magnitude, bird_shifting

    if not pause and not game_over:  # Only update game elements if game is not over
        shifting_magnitude += 0.1
        bird_shifting -= 0.1
        if obstacle2 < 0:
            obstacle2 = widthofscreen
            obstacle1 = catch2
            obstacle_speed += 20
            score += 1
            print("Score:", score)

        for ball in balls:
            ball_x, ball_y, ball_r = ball
            distance = ((ball_x - catch1) ** 2 + (ball_y - catch2) ** 2) ** 0.5
            if (distance <= 80):
                game_over = True  # Set game over state
                print("Game Over. Obstacles collided with the car.")
                print("Total Score:", score)

        new_bullets = []
        for b in bullets:
            b_x, b_y, b_r = b
            hit = False
            for ball in balls:
                ball_x, ball_y, ball_r = ball
                dist = ((ball_x - b_x) ** 2 + (ball_y - b_y) ** 2) ** 0.5
                if (dist <= b_r + ball_r):
                    hit = True
                    obstacle2 = widthofscreen
                    obstacle1 = 250
                    obstacle_speed += 0.1
                    score += 1
                    print("Score:", score)
                    bullets.remove(b)
                    balls.remove(ball)

    glutPostRedisplay()

    if not game_over:  # Call itself again only if game is not over
        glutTimerFunc(16, change, 0)


# Call itself again for next frame
# Call itself again for next frame

def bird():
    global bird_shifting
    glColor3f(0.447, 1.0, 0.973)
    glPointSize(1)

    # Bird head
    Midpoint(610+bird_shifting, 760, 640+bird_shifting, 760, (0.447, 1, 0.973))
    Midpoint(610+bird_shifting, 760, 636+bird_shifting, 776, (0.447, 1, 0.973))
    Midpoint(610+bird_shifting, 776, 620+bird_shifting, 760, (0.447, 1, 0.973))

    # Body
    Midpoint(620+bird_shifting, 760, 620+bird_shifting, 740, (0.447, 1, 0.973))
    Midpoint(620+bird_shifting, 740, 610+bird_shifting, 760, (0.447, 1, 0.973))

    # Tail
    Midpoint(636+bird_shifting, 760, 640+bird_shifting, 750, (0.447, 1, 0.973))
    Midpoint(640+bird_shifting, 750, 650+bird_shifting, 770, (0.447, 1, 0.973))
    Midpoint(636+bird_shifting, 760, 650+bird_shifting, 770, (0.447, 1, 0.973))

    # Additional details for the head
    Midpoint(628+bird_shifting, 770, 632+bird_shifting, 770, (0.447, 1, 0.973))  # Eye
    Midpoint(632+bird_shifting, 770, 635+bird_shifting, 773, (0.447, 1, 0.973))  # Beak
    Midpoint(632+bird_shifting, 770, 635+bird_shifting, 767, (0.447, 1, 0.973))  # Beak

    # Additional details for the body
    Midpoint(615+bird_shifting, 750, 618+bird_shifting, 745, (0.447, 1, 0.973))  # Wing
    Midpoint(618+bird_shifting, 745, 615+bird_shifting, 740, (0.447, 1, 0.973))  # Wing


def another_bird():
    global bird_shifting
    glColor3f(0.447, 1.0, 0.973)
    glPointSize(1)

    # Bird head
    Midpoint(810+bird_shifting, 760, 840+bird_shifting, 760, (0.447, 1, 0.973))
    Midpoint(810+bird_shifting, 760, 836+bird_shifting, 776, (0.447, 1, 0.973))
    Midpoint(810+bird_shifting, 776, 820+bird_shifting, 760, (0.447, 1, 0.973))

    # Body
    Midpoint(820+bird_shifting, 760, 820+bird_shifting, 740, (0.447, 1, 0.973))
    Midpoint(820+bird_shifting, 740, 810+bird_shifting, 760, (0.447, 1, 0.973))

    # Tail
    Midpoint(836+bird_shifting, 760, 840+bird_shifting, 750, (0.447, 1, 0.973))
    Midpoint(840+bird_shifting, 750, 850+bird_shifting, 770, (0.447, 1, 0.973))
    Midpoint(836+bird_shifting, 760, 850+bird_shifting, 770, (0.447, 1, 0.973))

    # Additional details for the head
    Midpoint(828+bird_shifting, 770, 832+bird_shifting, 770, (0.447, 1, 0.973))  # Eye
    Midpoint(832+bird_shifting, 770, 835+bird_shifting, 773, (0.447, 1, 0.973))  # Beak
    Midpoint(832+bird_shifting, 770, 835+bird_shifting, 767, (0.447, 1, 0.973))  # Beak

    # Additional details for the body
    Midpoint(815+bird_shifting, 750, 818+bird_shifting, 745, (0.447, 1, 0.973))  # Wing
    Midpoint(818+bird_shifting, 745, 815+bird_shifting, 740, (0.447, 1, 0.973))



    Midpoint(1110 + bird_shifting, 760, 1140 + bird_shifting, 760, (0.447, 1, 0.973))
    Midpoint(1110 + bird_shifting, 760, 1136 + bird_shifting, 776, (0.447, 1, 0.973))
    Midpoint(1110 + bird_shifting, 776, 1120 + bird_shifting, 760, (0.447, 1, 0.973))

    # Body
    Midpoint(1120 + bird_shifting, 760, 1120 + bird_shifting, 740, (0.447, 1, 0.973))
    Midpoint(1120 + bird_shifting, 740, 1110 + bird_shifting, 760, (0.447, 1, 0.973))

    # Tail
    Midpoint(1136 + bird_shifting, 760, 1140 + bird_shifting, 750, (0.447, 1, 0.973))
    Midpoint(1140 + bird_shifting, 750, 1150 + bird_shifting, 770, (0.447, 1, 0.973))
    Midpoint(1136 + bird_shifting, 760, 1150 + bird_shifting, 770, (0.447, 1, 0.973))

    # Additional details for the head
    Midpoint(1128 + bird_shifting, 770, 1132 + bird_shifting, 770, (0.447, 1, 0.973))  # Eye
    Midpoint(1132 + bird_shifting, 770, 1135 + bird_shifting, 773, (0.447, 1, 0.973))  # Beak
    Midpoint(1132 + bird_shifting, 770, 1135 + bird_shifting, 767, (0.447, 1, 0.973))  # Beak

    # Additional details for the body
    Midpoint(1115 + bird_shifting, 750, 1118 + bird_shifting, 745, (0.447, 1, 0.973))  # Wing
    Midpoint(1118 + bird_shifting, 745, 1115 + bird_shifting, 740, (0.447, 1, 0.973))


def display():
    global is_day, game_over

    glClear(GL_COLOR_BUFFER_BIT)
    if is_day:
        glClearColor(0, 0.8, 0.76, 0.2)
    else:
        glClearColor(0, 0, 0.2, 1)
    createrestartbutton()
    createpausebutton()
    createexitbutton()
    draw_bullet()
    shoot_bullet()
    clouds()
    another_bird()
    bird()
    creatediamond()
    draw_balls()
    go_diamond()
    generate_stars()
    draw_sun()
    glColor3f(1.0, 0.0, 0.0)
    if game_over:
        glRasterPos2f(widthofscreen // 2 - 100, heightofscreen // 2)
        glutBitmapString(GLUT_BITMAP_TIMES_ROMAN_24, b"Game Over")

    if not is_day:
        glColor3f(1, 1, 1)  # White color for stars
        glPointSize(2)  # Adjust the size of the stars as needed
        glBegin(GL_POINTS)
        for star in stars:
            glVertex2f(*star)
        glEnd()

    # Draw lane-like road
    glPointSize(50)
    glColor3f(0.2, 0.2, 0.2)  # Dark gray color for the lane
    for a in range(0, widthofscreen + 1, 30):
        for b in range(0, 235, 30):
            glBegin(GL_POINTS)
            glVertex2f(a, b)
            glEnd()

    # Draw white strip-like lines within the lane
    glColor3f(1.0, 1.0, 1.0)  # White color for the strips
    strip_width = 10  # Width of the white strip
    strip_gap = 50  # Gap between the strips
    if not pause:
        strip_x = widthofscreen - (glutGet(GLUT_ELAPSED_TIME) // 5 % strip_gap)  # Subtract time-based calculation to move backward
    else:
        strip_x = widthofscreen - (glutGet(GLUT_ELAPSED_TIME) // 10000000 % strip_gap)

    while strip_x > 0:  # Iterate while strip_x is greater than 0
        # Draw the strip
        glPointSize(20)
        glBegin(GL_POINTS)
        glVertex2f(strip_x, lane2 - 80 + 10)
        glVertex2f(strip_x + 10, lane2 - 80 + 10)
        glVertex2f(strip_x + 20, lane2 - 80 + 10)
        glEnd()
        strip_x -= strip_gap  # Move strip_x backward by subtracting strip_gap

    createcatch(catch1, catch2)
    glutSwapBuffers()


# mouse listener
def mouse_click(button, state, x, y):
    global game_over, score, obstacle_speed, obstacle2, obstacle1, catch1, catch2, bullets, pause, balls

    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        y = heightofscreen - y
        if widthofscreen - 50 <= x <= widthofscreen - 10 and heightofscreen - 50 <= y <= heightofscreen - 10:
            print(f"Goodbye. Final Score: {score}")
            glutLeaveMainLoop()
        elif widthofscreen // 2 - 20 <= x <= widthofscreen // 2 + 20 and heightofscreen - 50 <= y <= heightofscreen - 10:
            if not game_over:
                pause = not pause
        elif 10 <= x <= 60 and heightofscreen - 50 <= y <= heightofscreen - 10:  # restart button
            print("Restarting Game")
            game_over = False
            score = 0
            catch1 = widthofscreen // 8
            catch2 = 280
            bullets = []
            balls = []  # Clear bullets
            pause = False


def special_keys(key, x, y):
    global catch1, catch2
    if not pause:
        step = 10
        if not game_over:
            if key == GLUT_KEY_LEFT:
                catch1 = max(catch1 - step, 70)
            elif key == GLUT_KEY_RIGHT:
                catch1 = min(catch1 + step, widthofscreen - 70)


def keyboard(key, x, y):
    global is_day, catch1, catch2, jump_count, jump_height, jump_speed, game_over, bullets

    if key == b'i':
        is_day = not is_day
        glutPostRedisplay()
    elif key == b'f':
        global bullet_x, bullet_y, bullet_r
        bullet_x = catch1
        bullet_y = catch2
        bullet_r = 5
        bullets.append((bullet_x, bullet_y, bullet_r))
    elif key == b' ':
        if not pause and not game_over:
            if jump_count == 0:  # Ensure the car is not already jumping
                jump_count = 1
                glutTimerFunc(16, jump_callback, 0)


def jump_callback(value):
    global jump_count, catch2
    if jump_count < jump_height:
        catch2 += jump_speed
        jump_count += jump_speed
        glutTimerFunc(16, jump_callback, 0)
    else:
        # Reached the peak of the jump, start returning to original position
        jump_count = -jump_height  # Set jump_count to negative to start the fall
        glutTimerFunc(16, fall_callback, 0)


def fall_callback(value):
    global jump_count, catch2
    if jump_count < 0:
        catch2 -= jump_speed
        jump_count += jump_speed
        glutTimerFunc(16, fall_callback, 0)
    else:
        # Return to original position completed
        jump_count = 0  # Reset jump_count


glutInit()
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE)
glutInitWindowSize(widthofscreen, heightofscreen)
glutCreateWindow(b"Obstacle Crusher")
glOrtho(0, widthofscreen, 0, heightofscreen, -1, 1)
glClearColor(0, 1, 1, 1)  # Cyan background

glutDisplayFunc(display)
glutSpecialFunc(special_keys)  # Register special keys function
glutMouseFunc(mouse_click)
glutKeyboardFunc(keyboard)
glutTimerFunc(0, change, 0)  # Start animation loop immediately

glutMainLoop()
