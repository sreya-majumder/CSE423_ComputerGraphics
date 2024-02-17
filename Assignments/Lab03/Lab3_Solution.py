#import 
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

#Window size 
W_Width, W_Height = 500, 500

#growth speed 
growth_speed = 0.2

#Point Class
class Point:
    #method to generate points
    def draw_points(self, x, y):
        glPointSize(3)
        glBegin(GL_POINTS)
        glVertex2f(x, y)
        glEnd()

#Circle Class
class Circle:
    #initialize circle
    def __init__(self, cen_x, cen_y):
        self.cen_x = cen_x
        self.cen_y = cen_y
        self.radius = 1  

    #Midpoint Circle Algorithm
    def draw_circle(self):
        x = 0
        y = self.radius
        d = 1 - self.radius
        point = Point()

        while x <= y:
            zone0 = (x, y)
            zone1 = (y, x)
            zone2 = (-x, y)
            zone3 = (-y, x)
            zone4 = (-x, -y)
            zone5 = (-y, -x)
            zone6 = (x, -y)
            zone7 = (y, -x)
            zone = [zone0, zone1, zone2, zone3, zone4, zone5, zone6, zone7]

            for i in range(len(zone)):
                point.draw_points(zone[i][0] + self.cen_x, zone[i][1] + self.cen_y)

            incrE = 2 * x + 3
            incrSE = 2 * (x - y) + 5

            if d <= 0:
                x += 1
                d = d + incrE
            else:
                x += 1
                y -= 1
                d = d + incrSE
                
    #Circle Size will increase
    def grow(self):
        self.radius += growth_speed

#Display
def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    glColor3f(1.0, 0.0, 0.0)

    #For every center, draw circle
    for circle in circles:
        circle.draw_circle()

    glutSwapBuffers()

#iterate
def iterate():
    glViewport(0, 0, 500, 500)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 500, 0.0, 500, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

#Coordinate convert
def convert_coordinate(x, y):
    a = x 
    b = (W_Height ) - y
    return a, b

circles = [] #Stores center of the circles by storing objects of Circle class

#Task - 1 (a)
#Clicking on a right button will generate new circle 
def mouseListener(button, state, x, y):
    global paused
    #Task - 1 (d)
    #If space button is clicked --> New circles won't be generated
    #Again clicking on space button --> New circles will be generated
    if not paused and button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        converted_coordinates = convert_coordinate(x, y)
        circle = Circle(converted_coordinates[0], converted_coordinates[1])
        circles.append(circle)
        glutPostRedisplay()

#Task - 1 (d)
#Pause False --> New Circle will be generated
#Pause True -->  New Circle won't be generated
paused = False
def keyboardListener(key, x, y):
    global paused , growth_speed
    if key == b' ':
        paused = not paused

#Task - 1 (e)
#Left Arrow --> Speed Increased
#Right Arrow --> Speed Decreased
def specialKeyListener(key,x,y):
    global growth_speed
    if key == GLUT_KEY_LEFT:
        growth_speed += 0.2 # Speed will be increased if left arrow is pressed
    if key == GLUT_KEY_RIGHT:
        growth_speed = max(0.2, growth_speed - 0.2) # Speed will be decreased if right arrow is pressed (min speed 0)

    glutPostRedisplay()


#idle function
def animate():
    global circles
    updated_circles = [] #Stores the centers of the circles after removing circles that have touched/crossed the boundary

    #boundary check 
    x_min = 0
    x_max = W_Width
    y_min = 0
    y_max = W_Height

    #Task - 1 (b)
    #Generated circles will grow overtime
    if paused == False:
        for circle in circles:
            circle.grow()
            #Task - 1 (c)
            #if circle does not fit in the screen that circle will be removed
            if (
                (circle.cen_x - circle.radius) > x_min
                and (circle.cen_x + circle.radius) < x_max
                and (circle.cen_y - circle.radius) > y_min
                and (circle.cen_y + circle.radius) < y_max
            ):
                updated_circles.append(circle)

        circles = updated_circles #Updating circle array
    glutPostRedisplay()

glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(500, 500)
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"Lab Assignment - 3")
glutDisplayFunc(showScreen)
glutIdleFunc(animate)
glutMouseFunc(mouseListener)
glutKeyboardFunc(keyboardListener)
glutSpecialFunc(specialKeyListener)
glutMainLoop()