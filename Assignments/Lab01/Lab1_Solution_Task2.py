from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import time

W_Width, W_Height = 500, 500

movable_points = []
freeze_points = False 
blink = False
blink_duration = 1.0  

#Task -2(a)
#Generating random points that move diagonally
class Point:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.color = (random.random(), random.random(), random.random())
        self.speed = [random.uniform(-0.5, 0.5), random.uniform(-0.5, 0.5)]
        self.blinking = False
        self.last_blink_time = time.time()

def convert_coordinate(x, y):
    a = x - (W_Width / 2)
    b = (W_Height / 2) - y
    return a, b

def draw_points(x, y, s, color):
    glColor3f(color[0], color[1], color[2])
    glPointSize(s)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()

def generate_random_movable_point(x, y):
    point = Point()
    point.x, point.y = x, y
    movable_points.append(point)

#Mouse buttons
def mouseListener(button, state, x, y):
    global movable_points, freeze_points
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        if not freeze_points:
            c_x, c_y = convert_coordinate(x, y)
            generate_random_movable_point(c_x, c_y)
    elif button == GLUT_LEFT_BUTTON:
        toggle_blink()
    glutPostRedisplay()

#Task -2(b)
#Speed up and down
def specialKeyListener(key, x, y):
    global movable_points, freeze_points
    if not freeze_points:
        if key == GLUT_KEY_UP:
            for point in movable_points:
                point.speed = [s * 1.2 for s in point.speed]  # Increase speed
            print("Speed Increased")
        elif key == GLUT_KEY_DOWN:
            for point in movable_points:
                point.speed = [s * 0.8 for s in point.speed]  # Decrease speed
            print("Speed Decreased")
    glutPostRedisplay()



#Task -2(d)
#Space bar -Freeze and Unfreeze
def keyboardListener(key, x, y):
    global freeze_points, blink
    if key == b' ':  
        freeze_points = not freeze_points  
        if freeze_points:
            print("Points Freeze")
        else:
            print("Points Unfreeze")
    
    glutPostRedisplay()

#Task -2(c)
#Blinking
def toggle_blink():
    global blink
    blink = not blink

def animate():
    global movable_points, freeze_points, blink
    current_time = time.time()

    if freeze_points:
        blink = False 

    for point in movable_points:
        if not freeze_points:
            point.x += point.speed[0]
            point.y += point.speed[1]
            
            if point.x > W_Width / 2:
                point.x = -W_Width / 2
            if point.x < -W_Width / 2:
                point.x = W_Width / 2
            if point.y > W_Height / 2:
                point.y = -W_Height / 2
            if point.y < -W_Height / 2:
                point.y = W_Height / 2

            if blink:
                elapsed_time = current_time - point.last_blink_time
                if elapsed_time >= blink_duration:
                    point.blinking = not point.blinking
                    point.last_blink_time = current_time

    glutPostRedisplay()

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0, 0, 0, 0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0, 0, 200, 0, 0, 0, 0, 1, 0)
    glMatrixMode(GL_MODELVIEW)

    for point in movable_points:
        if not point.blinking or (point.blinking and int(time.time()) % 2 == 0):
            draw_points(point.x, point.y, 5, point.color)

    glutSwapBuffers()

def init():
    glClearColor(0, 0, 0, 0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(104, 1, 1, 1000.0)

glutInit()
glutInitWindowSize(W_Width, W_Height)
glutInitWindowPosition(0, 0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
wind = glutCreateWindow(b"Lab Assignment -1 Task -2")
init()
glutDisplayFunc(display)
glutIdleFunc(animate)
glutMouseFunc(mouseListener)
glutSpecialFunc(specialKeyListener)
glutKeyboardFunc(keyboardListener)
glutMainLoop()