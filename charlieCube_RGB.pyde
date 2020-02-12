#Conection for CharlieCube RGB 


add_library('serial')
from java.lang import System
System.loadLibrary("jSSC-2.8") #the native library we need


"""
UP:    color++
DOWN:  color--
RIGHT: ->
LEFT:  <-
SHIFT: random
ALT:   animation1

MOUSE_DRAG: rotation (X,Y)
"""


"""
0: off
1: red
2: green
3: blue
4: yellow
5: magenta
6: cyan
7: white
"""

colorRGB = [0 for k in xrange(8)]
colorRGB[0] = color(0)
colorRGB[1] = color(255,0,0)
colorRGB[2] = color(0,255,0)
colorRGB[3] = color(0,0,255)
colorRGB[4] = color(255,255,0)
colorRGB[5] = color(255,0,255)
colorRGB[6] = color(0,255,255)
colorRGB[7] = color(255)


# cubes
size_gral = 360  #180 360 540 720 etc.
box_size = size_gral/18
desplazamiento = box_size*3

# 3D matrix for colors
n = 4
color_led = [[[0 for k in xrange(n)] for j in xrange(n)] for i in xrange(n)]

#rotation with mouse  https://processing.org/examples/rgbcube.html
xmag = 0 
ymag = 0
newXmag = .40 * TWO_PI # para la vista inicial
newYmag = .60 * TWO_PI # para la vista inicial


cont_colorled = 0
index_x = 0
flag_dir = 0

# forum.processing.org/two/discussion/1725/millis-and-timer
WAIT_TIME = int (0.01 * 1000) # 3.5 seconds   0.001 = 10 ms
startTime = 0
flag_animation1 = -1
cont_animation1 = 0

flag_random = 0
 
def setup():
    global arduino
    global startTime
    println(Serial.list())
    arduino = Serial(this, "COM3", 57600)
    
    size(size_gral*2, size_gral, P3D) 
    noStroke()
    fill(255)
    
    color_all(7)
    startTime = millis();
 
def draw():
    global newXmag
    global newYmag
    global startTime
    global cont_animation1
    global flag_random
    
    background(25)
    lights()
    fov = PI/3.0
    cameraZ = (height/2.0) / tan(fov/2.0);
    perspective(fov, float(width)/float(height), cameraZ/10.0, cameraZ*10.0)
    
    if timer1() and flag_animation1 == 1:
        z = int(cont_animation1 / 16)
        y = int((cont_animation1 - z*16) / 4)
        x = cont_animation1 - z*16 - y*4
        if color_led[x][y][z] == 6:
            if flag_random == 0:
                color_one(x, y, z , 1)
        else:
            color_one(x, y, z, color_led[x][y][z] + 1)
        send_colorString()
        cont_animation1 += 1
        if cont_animation1 > 63:
            cont_animation1 = 0
        startTime = millis();
    
    # world
    pushMatrix() 
    
    translate(width/2, height/2, -30) 
    if mousePressed:
        newXmag = mouseX/float(width) * TWO_PI
        newYmag = mouseY/float(height) * TWO_PI
          
    world_rotation()
    drawLeds()
    drawWorld()
    drawAxes()

    popMatrix()
    # world

 
def timer1():
    global startTime
    global WAIT_TIME
    return millis() - startTime > WAIT_TIME;


def keyPressed():
    global cont_colorled
    global index_x
    global flag_dir
    global flag_animation1
    global cont_animation1
    global flag_random
    
    flag_random = 0
    if key == CODED:
        if keyCode == UP:                          # color++()
            cont_colorled +=1
            if cont_colorled > 6 :
                cont_colorled = 1
            color_all(cont_colorled)
        elif keyCode == DOWN:                      # color--()
            cont_colorled -=1
            if cont_colorled < 1 :
                cont_colorled = 6
            color_all(cont_colorled)
        elif keyCode == RIGHT:                     # 
            for j in range(4):
                for k in range(4):
                    if flag_dir == -1:
                        color_one(index_x, j, k, color_led[index_x][j][k])
                    elif color_led[index_x][j][k] == 6 :
                        color_one(index_x, j, k, 1)    
                    else: 
                        color_one(index_x, j, k, color_led[index_x][j][k] + 1)
            index_x += 1
            flag_dir = 1
            if index_x > 3:
                index_x = 0
            send_colorString()
        elif keyCode == LEFT:                      # 
            if index_x == 0 and flag_dir == 0:
                index_x = 3
            for j in range(4):
                for k in range(4):
                    if flag_dir == 1:
                        color_one(index_x, j, k, color_led[index_x][j][k])
                    elif color_led[index_x][j][k] == 1 :
                        color_one(index_x, j, k, 6)    
                    else:
                        color_one(index_x, j, k, color_led[index_x][j][k] - 1)
            index_x -= 1
            flag_dir = -1
            if index_x < 0:
                index_x = 3
            send_colorString()
        elif keyCode == SHIFT:                     # random
           for i in range(4):
               for j in range(4):
                   for k in range(4):
                       color_one(i, j, k, int(random(1,6)))
           send_colorString()
           flag_random = 1

        elif keyCode == ALT:                       # animation1
            flag_animation1 = - flag_animation1
            if flag_animation1 == -1:
                cont_animation1 = 0
   #    elif keyCode == CONTROL:                   # 




def send_colorString():
    stringColor =""
    for i in range(4):
        for j in range(4):
            for k in range(4):
                stringColor += str(color_led[k][j][i])        # [i][j][k] cambio de cables
    stringColor+= "\n"
    #println(stringColor)
    arduino.write(stringColor)
    delay(15)

                
def color_all(color_aux):
    global index_x
    global flag_dir
    for i in range(4):
        for j in range(4):
            for k in range(4):
                color_led[i][j][k] = color_aux
    send_colorString()
    index_x = 0
    flag_dir = 0
    
def color_one(i, j, k, color_aux):
    color_led[i][j][k] = color_aux
    
def drawLeds():
    for i in range(4):
        for j in range(4):
                for k in range(4):
                    drawLed(i, j, k)

def drawLed(i, j, k):
    global box_size
    global desplazamiento
    global color_led
    global flag_lines
    global colorRGB
    
    noStroke()
    fill(colorRGB[color_led[i][j][k]])
    
    
    pushMatrix()
    translate(-box_size*4.5 + i*desplazamiento, box_size*4.5 - j*desplazamiento, box_size*4.5 - k*desplazamiento)  
    sphere(box_size)
    
    #lines led
    noFill()
    stroke(200)
    box(box_size*1.8)
    
    popMatrix()
    
# box external
def drawWorld():
    stroke(128)
    noFill()
    box(box_size*10)
    
def drawAxes():
    global box_size
    global size_gral
    
    pushMatrix()
    translate(-box_size*4.5, box_size*4.5, box_size*4.5)  
    # line(x1, y1, z1, x2, y2, z2)
    stroke("#FF0000")
    line(-50, 0, 0, size_gral+50, 0, 0)   #red x
    stroke("#00FF00")
    line(0,-size_gral-50,0, 0, 50, 0)   #green y
    stroke("#0000FF")
    line(0,0,-size_gral-50, 0, 0, 50)   #blue z
    
    popMatrix()

# https://processing.org/examples/rgbcube.html
def world_rotation():
    global xmag
    global ymag
    global newXmag
    global newYmag
    global diff
    
    diff = xmag-newXmag
    if abs(diff) >  0.01: 
        xmag -= diff/4.0 
  
    diff = ymag-newYmag
    if abs(diff) >  0.01: 
        ymag -= diff/4.0
  
    rotateX(-ymag)
    rotateY(-xmag) 
    
    # cambio de vista
    rotateZ(PI) 
