import math
import random

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# Screen dimensions
WIDTH, HEIGHT = 500, 500


# Game variables
player_x, player_y = WIDTH // 2, HEIGHT // 2
player_radius = 10
player_color = (0, 1, 0)  
lives = 3  
score = 0
level = 1
enemies = []
projectiles = [] 
game_paused = False


item_x, item_y = random.randint(50, 450), random.randint(50, 450)
item_radius = 5
item_color = (1, 1, 0) 

# Power-up variables
power_up_x, power_up_y = random.randint(50, 450), random.randint(50, 450)
power_up_radius = 6
power_up_color = (0, 0, 1)  
power_up_active = False
power_up_timer = 0


# Shooting variables
projectile_radius = 2
projectile_speed = 5


def draw_projectiles():
    glColor3f(1, 0, 0)  
    for px, py in projectiles:
        draw_circle(px, py, projectile_radius, (1, 0, 1))


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

# Define star positions
stars = [(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(100)]  
def draw_stars():
    glBegin(GL_POINTS)
    glColor3f(1, 1, 1)  
    for star in stars:
        glVertex2f(star[0], star[1])
    glEnd()

def display():
    global player_x, player_y, item_x, item_y, score, enemies, lives, level

    glClear(GL_COLOR_BUFFER_BIT)

    draw_stars()

    # Draw player
    draw_circle(player_x, player_y, player_radius, player_color)

    # Draw item
    draw_circle(item_x, item_y, item_radius, item_color)
    
    # Draw power-up
    if not power_up_active:
        draw_circle(power_up_x, power_up_y, power_up_radius, power_up_color)

    # Draw enemies
    for ex, ey, etype in enemies:
        draw_circle(ex, ey, 8, (1, 0, 0))  # Red

    draw_projectiles()  
  
    # Draw remaining lives
    glColor3f(1, 1, 1) 
    glRasterPos2f(10, HEIGHT - 20)
    for c in f"Lives: {lives}":
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(c))


    # Draw score
    glRasterPos2f(10, HEIGHT - 40)
    for c in f"Score: {score}":
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(c))


    # Draw level
    glRasterPos2f(10, HEIGHT - 60)
    for c in f"Level: {level}":
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(c))
    
    # Swap buffers
    glutSwapBuffers()


def update(value):
    global item_x, item_y, score, enemies, lives, player_x, player_y
    global power_up_active, power_up_timer, level, enemy_spawn_rate, player_radius
    global power_up_x, power_up_y
    global etype
    global projectiles, game_paused

    if game_paused:
        glutTimerFunc(16, update, 0)
        return  # Skip updating if the game is paused

    # Update projectiles
    projectiles = [(px, py + projectile_speed) for px, py in projectiles if py < HEIGHT]



     # Check for projectile collisions with enemies
    for i, (px, py) in enumerate(projectiles):
        for j, (ex, ey, etype) in enumerate(enemies):
            if math.hypot(px - ex, py - ey) < player_radius + 8: 
                projectiles.pop(i)  
                enemies.pop(j) 
                score += 5  
                break  

    # Check collision with item
    if math.hypot(player_x - item_x, player_y - item_y) < player_radius + item_radius:
        score += 1
        item_x, item_y = random.randint(50, 450), random.randint(50, 450)

    # Check collision with power-up
    if not power_up_active and math.hypot(player_x - power_up_x, player_y - power_up_y) < player_radius + power_up_radius:
        power_up_active = True
        power_up_timer = 100  
        power_up_x, power_up_y = random.randint(50, 450), random.randint(50, 450)
        score += 3

    # Apply power-up effect
    if power_up_active:
        player_radius = 25 
        power_up_timer -= 1
        if power_up_timer <= 0:
            power_up_active = False
            player_radius = 15

    # Move enemies
    for i in range(len(enemies)):
        ex, ey, etype = enemies[i]  

        ex = max(0, min(WIDTH, ex))
        ey = max(0, min(HEIGHT, ey))

       ''' if etype == "slow":
            ex += 0.5 if ex < player_x else -0.5  
            ey += 0.5 if ey < player_y else -0.5
        elif etype == "fast":
            ex += 1 if ex < player_x else -1  
            ey += 1 if ey < player_y else -1
        elif etype == "zigzag":
            ex += random.choice([-0.5, 0.5])  
            ey += random.choice([-0.5, 0.5])'''

            
        enemies[i] = (ex, ey, etype)  # Update the enemy's position and type

        # Check collision with player
        enemy_radius =8
        if math.hypot(player_x - ex, player_y - ey) < player_radius + enemy_radius:
            lives -= 1  # Decrease life when hit by enemy
            if lives <= 0:
                print(f"Game Over! Your score: {score}")
                glutLeaveMainLoop()  
            else:
                player_x, player_y = WIDTH // 2, HEIGHT // 2

    # Spawn new enemies over time
    enemy_spawn_rate = 0.004 
    if random.random() < enemy_spawn_rate:
        etype = random.choice(['slow', 'fast', 'zigzag'])  
        enemies.append((random.randint(0, WIDTH), random.randint(0, HEIGHT), etype))

    # Level up based on score
    if score > level * 10:  
        level += 1
        enemy_spawn_rate = max(0.03, enemy_spawn_rate + 0.002)

    glutPostRedisplay()
    glutTimerFunc(16, update, 0)

def keyboard(key, x, y):
    global player_x, player_y,projectiles,game_paused


    if key == b'w' and player_y + player_radius < HEIGHT:
        player_y += 10
    elif key == b's' and player_y - player_radius > 0:
        player_y -= 10
    elif key == b'a' and player_x - player_radius > 0:
        player_x -= 10
    elif key == b'd' and player_x + player_radius < WIDTH:
        player_x += 10
    if key == b'p':  
        game_paused = not game_paused
        if not game_paused:
            glutTimerFunc(16, update, 0)

    if key == b' ':  
        projectiles.append((player_x, player_y + player_radius)) 

    glutPostRedisplay()


glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(WIDTH, HEIGHT)
glutCreateWindow(b"Pacman Space Explorer")
glutDisplayFunc(display)
glutKeyboardFunc(keyboard)
glutTimerFunc(16, update, 0)
init()
glutMainLoop()