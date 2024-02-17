from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

#Catcher Bowl Class
class Catcher:

    #Initializing catcher's width,height,x,y Coordinates
    def __init__(self):
        self.width = 100
        self.height = 20
        self.x = 200
        self.y = 5
        self.speed = 10

    #catcher bowl moving to left
    def move_left(self):
        if self.x - self.width // 5 > 0:
            self.x -= self.speed

    #catcher bowl moving to right
    def move_right(self):
        if self.x + self.width + self.width // 5 < 500:
            self.x += self.speed

    #drawing catcher bowl using MPL algorithm
    def draw_catcher(self):
        x1 = self.x
        x2 = self.x + self.width
        y1 = self.y
        y2 = self.y + self.height
        if diamond.y>=0:
           glColor3f(1.0, 1.0, 1.0)  #catcher color white(usual)
        else:
           glColor3f(1.0, 0.0, 0.0)  #catcher color red (if game over)
           
        findZone(x1, y1, x2, y1) #bottom line
        findZone(x1, y1, x1 - self.width // 5, y2) #left line
        findZone(x1 - self.width // 5, y2, x2 + self.width // 5, y2) #top line
        findZone(x2, y1, x2 + self.width // 5, y2)#Right line

#Diamond Class
class Diamond:

    #Initializing diamond width,height,x,y,color,acceleration,maximum speed
    def __init__(self):
        self.width = 10
        self.height = 10
        self.x = random.randint(10, 490)
        self.y = 500
        self.speed = 1
        self.color = (random.uniform(0.7, 1.0), random.uniform(0.7, 1.0), random.uniform(0.7, 1.0))
        self.acceleration = .05
        self.max_speed = 5

    # Diamond fall vertically, if catched score increased and reset diamond
    def move(self):
        global score
        self.y -= self.speed
        if collide():
            score+=1
            print("Score:",score)
            self.reset_position()
            self.randomize_color()
        
    #Reset diamond position,speed when new diamond is created
    def reset_position(self):
        self.x = random.randint(10, 490)
        self.y = 500
        self.speed += self.acceleration #speed adjustment according to difficulty
        self.speed = min(self.speed, self.max_speed) # speed should not be greater than the maximum speed

    #Random Diamond Color
    def randomize_color(self):
        self.color = (random.uniform(0.7, 1.0), random.uniform(0.7, 1.0), random.uniform(0.7, 1.0))

    #Draw Diamond    
    def draw_diamond(self):
        glColor3f(*self.color)
        findZone(self.x, self.y, self.x + self.width, self.y + self.height)
        findZone(self.x, self.y, self.x - self.width, self.y + self.height)
        findZone(self.x - self.width, self.y + self.height, self.x, self.y + 2 * self.height)
        findZone(self.x, self.y + 2 * self.height, self.x + self.width, self.y + self.height)
        
#Creating object of Catcher and Diamond Class
catcher = Catcher()
diamond = Diamond()

#Counting Score
score = 0
def create_catcher():
    catcher.draw_catcher()

def create_diamond():
    diamond.draw_diamond()

# Drawing Points
def draw_points(x, y):
    glPointSize(1)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()

# Midpoint Line Algorithm
def draw_lines(x1, y1, x2, y2, z):
    dx = x2 - x1
    dy = y2 - y1
    d = (2 * dy) - dx
    incrE = 2 * dy
    incrNE = (2 * dy) - (2 * dx)
    x = x1
    y = y1
    if z == 0:
        draw_points(x, y)
    else:
        backConvertZone(x, y, z)

    while (x < x2):
        if d <= 0:
            x = x + 1
            d = d + incrE
        else:
            x = x + 1
            y = y + 1
            d = d + incrNE
        if z == 0:
            draw_points(x, y)
        else:
            backConvertZone(x, y, z)

# Find Zone of the points
def findZone(x1, y1, x2, y2):
    if y1 > y2:
        x1, y1, x2, y2 = x2, y2, x1, y1
    dx = x2 - x1
    dy = y2 - y1
    zone = 0
    if (abs(dx) >= abs(dy) and dx >= 0 and dy >= 0):
        zone = 0
    elif (abs(dy) > abs(dx) and dx >= 0 and dy >= 0):
        zone = 1
    elif (abs(dy) > abs(dx) and dx <= 0 and dy >= 0):
        zone = 2
    elif (abs(dy) <= abs(dx) and dx <= 0 and dy >= 0):
        zone = 3
    elif (abs(dx) <= abs(dy) and dx <= 0 and dy <= 0):
        zone = 4
    elif (abs(dy) > abs(dx) and dx <= 0 and dy <= 0):
        zone = 5
    elif (abs(dy) >= abs(dx) and dx >= 0 and dy <= 0):
        zone = 6
    elif (abs(dx) >= abs(dy) and dx >= 0 and dy <= 0):
        zone = 7

    if zone != 0:
        forConvertZone(x1, y1, x2, y2, zone)
    else:
        draw_lines(x1, y1, x2, y2, zone)

# Other Zones --> Zone 0
def forConvertZone(x1, y1, x2, y2, z):
    if z == 1:
        draw_lines(y1, x1, y2, x2, z)
    elif z == 2:
        draw_lines(-y1, x1, -y2, x2, z)
    elif z == 3:
        draw_lines(-x1, y1, -x2, y2, z)
    elif z == 4:
        draw_lines(-x1, -y1, -x2, -y2, z)
    elif z == 5:
        draw_lines(-y1, -x1, -y2, -x2, z)
    elif z == 6:
        draw_lines(y1, -x1, y2, -x2, z)
    elif z == 7:
        draw_lines(x1, -y1, x2, -y2, z)

# Zone 0 --> Other zones
def backConvertZone(x, y, z):
    if z == 1:
        draw_points(y, x)
    elif z == 2:
        draw_points(y, -x)
    elif z == 3:
        draw_points(-x, y)
    elif z == 4:
        draw_points(-x, -y)
    elif z == 5:
        draw_points(-y, -x)
    elif z == 6:
        draw_points(-y, x)
    elif z == 7:
        draw_points(x, -y)

#Iterate
def iterate():
    glViewport(0, 0, 500, 500)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 500, 0.0, 500, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

is_game_paused = False #If false then game will resume  
game_over = False #If false game is not over

#ShowScreen Function For Display
def showScreen():
    global is_game_paused,game_over,score
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    glColor3f(1.0, 1.0, 0.0)

    create_catcher() # create catcher bowl

    create_diamond() #create diamond

    # If game is paused (is_game_paused==True) then play button
    if is_game_paused:
        draw_play_button()

    #If game is not paused (is_game_paused == False) then pause button
    else:
        draw_pause_button()
        # Diamond position will be updated if gaome is not paused
        if not is_game_paused:  
            diamond.move()

    draw_left_arrow_button() #Restart Button

    draw_exit_button() #Exit Button

    glutSwapBuffers()

    if diamond.y < 0 and not game_over:
        game_over = True
        print("Game Over! Score: ",score)
        create_catcher()
        
#Collide Function For tracking Diamond is "catched" or not
def collide():
    return ((catcher.x  < diamond.x + diamond.width) and (catcher.x + catcher.width + 20 > diamond.x)  and (catcher.y < diamond.y + diamond.height) and (catcher.y + catcher.height > diamond.y))  

#Restarting Game 
def restart_game():
    global score, catcher, diamond, game_over
    print("Starting Over!")
    score = 0
    catcher = Catcher()
    diamond = Diamond()
    game_over = False

#Restart Button(Left Arrow Button)
def draw_left_arrow_button():
    glColor3f(0.0, 1.0, 1.0)
    findZone(20, 460, 60, 460)
    findZone(20, 460, 40, 440)
    findZone(20, 460, 40, 480)

#Play Button
def draw_play_button():
    glColor3f(1.0, 0.75, 0.0)
    findZone(245, 440, 245, 480)
    findZone(245, 440, 275, 460)
    findZone(245, 480, 275, 460)

#Pause Button
def draw_pause_button():
    glColor3f(1.0, 0.75, 0.0)
    findZone(245, 440, 245, 480)
    findZone(255, 440, 255, 480)

#Cross Button (Red Cross Button)
def draw_exit_button():
    glColor3f(1.0, 0.0, 0.0)
    findZone(440, 440, 480, 480)
    findZone(440, 480, 480, 440)

wind = None   
#Functionalities if Mouse is clicked 
def mouse_callback(button, state, x, y):
    global score, catcher, diamond, is_game_paused,wind 

    # Convert Y coordinate
    y = 500 - y
    
    #if 3 buttons are clicked
    if button == GLUT_LEFT_BUTTON and state == GLUT_UP:
        if not is_game_paused:
            # Check if the click is within the pause button area
            if 245 <= x <= 255 and 440 <= y <= 480:
                is_game_paused = True  # Pause the game
            # Check if the click is within the left arrow area
            elif 20 <= x <= 60 and 440 <= y <= 480:
                restart_game()
            # Check if the click is within the exit button area
            elif 440 <= x <= 480 and 440 <= y <= 480:
                print("Goodbye! Score:", score)
                glutDestroyWindow(wind)
                #glutLeaveMainLoop()
        else:
            # Check if the click is within the play button area
            if 245 <= x <= 275 and 440 <= y <= 480:
                is_game_paused = False # Resume the game

#When Left and Right Arrow is clicked, then catcher will be shifted to left and right 
def specialKeyListener(key,x,y):
    global is_game_paused
    if not is_game_paused:
        if key == GLUT_KEY_LEFT:
            catcher.move_left()
        elif key == GLUT_KEY_RIGHT:
            catcher.move_right()

    glutPostRedisplay()

def animate(_):
    # codes for any changes in Models, Camera
    glutPostRedisplay()
    glutTimerFunc(16, animate, 0) 

glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(500, 500)
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"Lab Assignment -2")
glutDisplayFunc(showScreen)
glutMouseFunc(mouse_callback)

glutSpecialFunc(specialKeyListener)
glutTimerFunc(0, animate, 0) 
glutMainLoop()