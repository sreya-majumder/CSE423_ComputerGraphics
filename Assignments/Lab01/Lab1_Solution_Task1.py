from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

W_Width, W_Height = 500, 500

raindrops = []

background_color = 0.0
rain_direction = 0

# Task -1(a)
#Drawing raindrops 
class Raindrop:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 5  

#Generating raindrops
def generate_raindrops():
    global raindrops
    gap = 15
    raindrops = []
    for y in range(250, -250, -gap):
        drop_pattern = [(-250 + i, y) for i in range(0, 501, gap)]
        raindrops += [Raindrop(start, y) for start, _ in drop_pattern]
    
#Raindrops motion
def update_raindrops():
    for raindrop in raindrops:
        raindrop.x += rain_direction * raindrop.speed

        if raindrop.x < -250:
            raindrop.x = 250
        elif raindrop.x > 250:
            raindrop.x = -250

        raindrop.y -= raindrop.speed

        if raindrop.y < -250:
            raindrop.y = 250

def convert_coordinate(x, y):
    global W_Width, W_Height
    a = x - (W_Width / 2)
    b = (W_Height / 2) - y
    return a, b

def draw_points(x, y, s):
    glPointSize(s)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()

def draw_lines(x1, y1, x2, y2, w):
    glLineWidth(w)
    glBegin(GL_LINES)
    glVertex2f(x1, y1)
    glVertex2f(x2, y2)
    glEnd()

def draw_triangles(x1, y1, x2, y2, x3, y3):
    glBegin(GL_TRIANGLES)
    glVertex2f(x1, y1)
    glVertex2f(x2, y2)
    glVertex2f(x3, y3)
    glEnd()

def draw_axes():
    glLineWidth(1)
    glBegin(GL_LINES)
    glColor3f(1.0, 0.0, 0.0)
    glVertex2f(250, 0)
    glVertex2f(-250, 0)
    glColor3f(0.0, 0.0, 1.0)
    glVertex2f(0, 250)
    glVertex2f(0, -250)
    glEnd()

#Task-1(c)
#Change background color (House and raindrops are considered)

def change_background_color(direction):
    global background_color
    background_color += direction
    if background_color < 0.0:
        background_color = 0.0
    elif background_color > 1.0:
        background_color = 1.0

def keyboardListener(key, x, y):
    if key == b'd':
        change_background_color(0.1)
        print("From dark to light simulating night to day")
        
    if key == b'n':
        change_background_color(-0.1)
        print("From light to dark simulating day to night")
    glutPostRedisplay()

#Task -1(b)
#Control the direction of rain
def specialKeyListener(key, x, y):
    global rain_direction
    if key == GLUT_KEY_LEFT:
        rain_direction -= 0.1 
        print("Bending Rain to the Left")
    elif key == GLUT_KEY_RIGHT:
        rain_direction += 0.1 
        print("Bending Rain to the Right")

    glutPostRedisplay()

#Finding the points that are inside the roof
def is_inside_triangle(x, y):
    v1 = (-150, 50)
    v2 = (150, 50)
    v3 = (0, 150)

    var = (v2[1] - v3[1]) * (v1[0] - v3[0]) + (v3[0] - v2[0]) * (v1[1] - v3[1])
    a = ((v2[1] - v3[1]) * (x - v3[0]) + (v3[0] - v2[0]) * (y - v3[1])) / var
    b  = ((v3[1] - v1[1]) * (x - v3[0]) + (v1[0] - v3[0]) * (y - v3[1])) / var
    c = 1 - a - b
    return 0 <= a <= 1 and 0 <= b <= 1 and 0 <= c <= 1

def display():
    glClearColor(background_color, background_color, background_color, 0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0, 0, 200, 0, 0, 0, 0, 1, 0)
    glMatrixMode(GL_MODELVIEW)
    
    #Raindrops will not be visible inside the house
    x_min, x_max = -140, 140
    y_min, y_max = -200, 50
    for raindrop in raindrops:
        if not is_inside_triangle(raindrop.x, raindrop.y)  and (raindrop.x < x_min or raindrop.x > x_max or raindrop.y < y_min or raindrop.y > y_max):
            glColor3f(0, 0, 1.0) #rain color
            draw_points(raindrop.x, raindrop.y, 2)
    
    #Task -1(a)
    #Designing the house

    # Interior point of the house - yellow 
    glColor3f(1.0, 1.0, 0.0)
    glBegin(GL_POINTS)
    for x in range(-140, 140):
        for y in range(-200, 50):
            glVertex2f(x, y)
    glEnd()

    # Roof of the house - red
    glColor3f(1.0, 0.0, 0.0)  
    glBegin(GL_POINTS)
    for x in range(-149, 150):
        for y in range(51, 150):
           if is_inside_triangle(x,y):
                glVertex2f(x, y)

    glEnd()
    
    #Lines of house - green color

    glColor3f(0.0, 1.0, 0.0)  
    draw_lines(-150, 50, 150, 50, 10)
    draw_lines(-150, 50, 0, 150, 10)
    draw_lines(150, 50, 0, 150, 10)
    draw_triangles(-160, 45, -150, 45, -150, 55)
    draw_triangles(150, 45, 160, 45, 150, 55)
    draw_lines(-140, 50, -140, -200, 10)
    draw_lines(140, 50, 140, -200, 10)
    draw_lines(-140, -200, 140, -200, 10)

    draw_lines(-100, -200, -100, -50, 2)
    draw_lines(-100, -50, -30, -50, 2)
    draw_lines(-30, -50, -30, -200, 2)
    glColor3f(0, 1, 0)
    draw_points(-40, -125, 5)

    draw_lines(50, -50, 100, -50, 2)
    draw_lines(50, -80, 50, -20, 2)
    draw_lines(50, -80, 100, -80, 2)
    draw_lines(100, -80, 100, -20, 2)
    draw_lines(50, -20, 100, -20, 2)
    draw_lines(50, -80, 100, -80, 2)
    draw_lines(75, -80, 75, -20, 2)
    draw_points(-143, -202, 5)
    draw_points(143, -202, 5)

    
    glutSwapBuffers()

def animate():
    update_raindrops()
    glutPostRedisplay()

def init():
    glClearColor(0, 0, 0, 0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(104, 1, 1, 1000.0)

    generate_raindrops()

glutInit()
glutInitWindowSize(W_Width, W_Height)
glutInitWindowPosition(0, 0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
wind = glutCreateWindow(b"Lab Assignment 1- Task 1")
init()
glutDisplayFunc(display)
glutIdleFunc(animate)
glutKeyboardFunc(keyboardListener)
glutSpecialFunc(specialKeyListener)
glutMainLoop()