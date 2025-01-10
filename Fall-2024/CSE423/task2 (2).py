from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import math

# Screen dimensions
WIDTH, HEIGHT = 500, 500

# Game variables
player_x, player_y = WIDTH // 2, HEIGHT // 2
player_radius = 10
player_color = (0, 1, 0)  # Green
lives = 3  # Number of lives
score = 0
enemies = []

item_x, item_y = random.randint(50, 450), random.randint(50, 450)
item_radius = 5
item_color = (1, 1, 0)  # Yellow

def draw_circle(xc, yc, r, color):
    glColor3f(*color)
    x, y = 0, r
    d = 1 - r

    def plot_circle_points(xc, yc, x, y):
        glVertex2f(xc + x, yc + y)
        glVertex2f(xc - x, yc + y)
        glVertex2f(xc + x, yc - y)
        glVertex2f(xc - x, yc - y)
        glVertex2f(xc + y, yc + x)
        glVertex2f(xc - y, yc + x)
        glVertex2f(xc + y, yc - x)
        glVertex2f(xc - y, yc - x)

    glBegin(GL_POINTS)
    plot_circle_points(xc, yc, x, y)
    while x < y:
        x += 1
        if d < 0:
            d += 2 * x + 1
        else:
            y -= 1
            d += 2 * (x - y) + 1
        plot_circle_points(xc, yc, x, y)
    glEnd()

def draw_line(x1, y1, x2, y2, color):
    glColor3f(*color)
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx - dy

    glBegin(GL_POINTS)
    while True:
        glVertex2f(x1, y1)
        if x1 == x2 and y1 == y2:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x1 += sx
        if e2 < dx:
            err += dx
            y1 += sy
    glEnd()

def init():
    glClearColor(0, 0, 0, 1)
    gluOrtho2D(0, WIDTH, 0, HEIGHT)

def display():
    global player_x, player_y, item_x, item_y, score, enemies, lives

    glClear(GL_COLOR_BUFFER_BIT)

    # Draw player
    draw_circle(player_x, player_y, player_radius, player_color)

    # Draw item
    draw_circle(item_x, item_y, item_radius, item_color)

    # Draw enemies
    for ex, ey in enemies:
        draw_circle(ex, ey, 8, (1, 0, 0))  # Red

    # Draw remaining lives
    glColor3f(1, 1, 1)  # White
    glRasterPos2f(10, HEIGHT - 20)
    for c in f"Lives: {lives}":
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(c))

    # Draw score
    glRasterPos2f(10, HEIGHT - 40)
    for c in f"Score: {score}":
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(c))

    # Swap buffers
    glutSwapBuffers()

def update(value):
    global item_x, item_y, score, enemies, lives, player_x, player_y  # Add player_x and player_y here

    # Check collision with item
    if math.hypot(player_x - item_x, player_y - item_y) < player_radius + item_radius:
        score += 1
        item_x, item_y = random.randint(50, 450), random.randint(50, 450)

    # Move enemies
    for i in range(len(enemies)):
        ex, ey = enemies[i]
        if ex < player_x:
            ex += 1
        else:
            ex -= 1
        if ey < player_y:
            ey += 1
        else:
            ey -= 1
        enemies[i] = (ex, ey)

        # Check collision with player
        if math.hypot(player_x - ex, player_y - ey) < player_radius + 8:
            lives -= 1  # Decrease life when hit by enemy
            if lives <= 0:
                print(f"Game Over! Your score: {score}")
                glutLeaveMainLoop()  # Exit the game loop
            else:
                # Reset player position after collision
                player_x, player_y = WIDTH // 2, HEIGHT // 2

    # Spawn new enemies over time
    if random.random() < 0.01:  # 1% chance per frame
        enemies.append((random.randint(0, WIDTH), random.randint(0, HEIGHT)))

    glutPostRedisplay()
    glutTimerFunc(16, update, 0)

def keyboard(key, x, y):
    global player_x, player_y

    if key == b'w' and player_y + player_radius < HEIGHT:
        player_y += 10
    elif key == b's' and player_y - player_radius > 0:
        player_y -= 10
    elif key == b'a' and player_x - player_radius > 0:
        player_x -= 10
    elif key == b'd' and player_x + player_radius < WIDTH:
        player_x += 10

if __name__ == "__main__":
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(WIDTH, HEIGHT)
    glutCreateWindow(b"Space Explorer")
    glutDisplayFunc(display)
    glutKeyboardFunc(keyboard)
    glutTimerFunc(16, update, 0)
    init()
    glutMainLoop()
