from visual import *
# subprocess module is for adding sound
import subprocess
import random
# these are files that I included for a cleaner code layout
from settings import *
from scenes import *


# setting the speed of the ball, and setting the game mode
ballSpeed, mode = openScene()
ballSpeed2 = 1.5 * ballSpeed


# add invisible ball to create imperfect AI

# GAME MODE
# 1 - 1 player in practice mode, fixed goaltenders
# 2 - 1 player against a computer, fixed goaltenders
# 3 - 2 players, fixed goaltenders
# 4 - 4 players, 2 players control pads, 2 players control goaltenders
# 5 - watch mode, same as 3, but robot controls both pads, and obstacle
scene = display(width=1400, height=800, range = 145, background=color.black)

shadow = cylinder(pos=vector(0,-WALL_Y+WALL_THICK/2.0,0), color = color.black, axis=vector(0,0.1,0), radius=3)
ballBox1 = box(pos = (0,1,0),size =(0.01,2*WALL_Y-1,2*WALL_Z), color = color.black,opacity = 0.1)

# creating walls - up, down, left, right, front, back
wallU = box(pos=(0,WALL_Y,0),size=(2*WALL_X,WALL_THICK,2*WALL_Z),color = color.green,opacity =1)
wallD = box(pos=(0,-WALL_Y,0),size=(2*WALL_X,WALL_THICK,2*WALL_Z),color = color.green,opacity =1)
wallL = box(pos=(-WALL_X,0,0),size=(WALL_THICK,2*WALL_Y,2*WALL_Z),color = color.green,opacity =1)
wallR = box(pos=(WALL_X,0,0),size=(WALL_THICK,2*WALL_Y,2*WALL_Z),color = color.green,opacity =1)
wallF = box(pos=(0,0,WALL_Z),size=(2*WALL_X,2*WALL_Y,WALL_THICK),color = color.green,opacity=1)
wallB = box(pos=(0,0,-WALL_Z),size=(2*WALL_X,2*WALL_Y,WALL_THICK),color = color.green,opacity=1)
# score boards
scoreBoard1red = box(pos=(SCOREPOSX,SCOREPOSY,-SCOREPOSZ),size=(1,110,2*SCOREPOSZ), color = color.red)
scoreBoard1blue = box(pos=(SCOREPOSX,SCOREPOSY,SCOREPOSZ),size=(1,110,2*SCOREPOSZ), color = color.blue)
scoreBoard2red = box(pos=(-SCOREPOSX,SCOREPOSY,-SCOREPOSZ),size=(1,110,2*SCOREPOSZ), color = color.red)
scoreBoard2blue = box(pos=(-SCOREPOSX,SCOREPOSY,SCOREPOSZ),size=(1,110,2*SCOREPOSZ), color = color.blue)

# hide score board in mode 1
if mode == 1:
    scoreBoard1red.opacity = 0
    scoreBoard1blue.opacity = 0
    scoreBoard2red.opacity = 0
    scoreBoard2blue.opacity = 0
    
goalTender1 = box(pos=(-(WALL_X-4),0,0),size=(1,GT_Y_SIZE,GT_Z_SIZE),material = materials.wood,opacity =0.3)
# only create goalTender2 when game mode is not 1 
if mode != 1:
    goalTender2 = box(pos=(WALL_X-4,0,0),size=(1,GT_Y_SIZE,GT_Z_SIZE),material = materials.wood,opacity =1)

# obstacles under construction
if mode == 5:
    ball = sphere(pos=(-5,7,20), radius=4, material = materials.wood )

# player 1 
p1 = box(pos=(-PPOS,0,0), size =(P_X,P_Y,P_Z), color = color.red)
p1.velocity = (0,0,0)
p1.score = 0
p1.scored = False
if mode != 1:
    # player 2 
    p2 = box(pos=(PPOS,0,0), size =(P_X,P_Y,P_Z), color = color.blue)
    p2.velocity = (0,0,0)
    p2.score = 0
    p2.scored = False
    
# scores display
if mode != 1:
    p1Display1 = text (font = "Times",text=str(p1.score), height = 20, width = 15, depth=0.5, axis=(0,0,1),color=color.white)
    p2Display1 = text (font = "Times",text=str(p2.score), height = 20, width = 15, depth=0.5, axis=(0,0,1),color=color.white)

ball = sphere(pos=(0,0,0), radius=BALLR, color=color.cyan,make_trail = True, interval=10,retain=100 )
ball.velocity = vector(-1 * ballSpeed,0,0)

invisible_ball = sphere(pos=(0,0,0), radius=BALLR, color=color.red)
invisible_ball.velocity = vector(-1 * ballSpeed2, 0, 0)


# once one player scores, restart will be set to true, this is to implement pauses during gameplay
restart = False
# control is a variable used for player movement, stores a key when a key is pressed
control = ""
done = False

while not done:
    rate(RATE1)
    if scene.kb.keys:
        key = scene.kb.getkey()
        control = key
    else:
        control = ""
    if control == 'up':
        p1.velocity = (0,PSPEED,0)
    elif control == 'down':
        p1.velocity = (0,-PSPEED,0)
    elif control == 'left':
        p1.velocity = (0,0,-PSPEED)
    elif control == 'right':
        p1.velocity = (0,0,PSPEED)
    else:
        p1.velocity = (0,0,0)
    p1.pos += p1.velocity
    if mode != 1:
        if control == 'e':
            p2.velocity = (0,PSPEED,0)
        elif control == 'c':
            p2.velocity = (0,-PSPEED,0)
        elif control == 'a':
            p2.velocity = (0,0,PSPEED)
        elif control == 'z':
            p2.velocity = (0,0,-PSPEED)
        else:
            p2.velocity = (0,0,0)
        p2.pos += p2.velocity



    # ball collision with p2
    if mode != 1:
        #possibly add error trap to make sure sqrt function does not take a negative number as argument
        collisionPlayer(ball,p2, ballSpeed,'+' , '>=', '-',-1)
        collisionPlayer(invisible_ball, p2, ballSpeed2, '+', '>=', '-', -1)

    # ball collision with p1
        collisionPlayer(ball,p1, ballSpeed,'-', '<=', '+', 1)
        collisionPlayer(invisible_ball, p1, ballSpeed2, '-', '<=', '+', 1)

    if mode != 1:
        # ball collision with goalTender2
        collisionGoalTender(ball, goalTender2, "+", ">=", "-")
        collisionGoalTender(invisible_ball, goalTender2, '+', '>=', '-')
    # ball collision with goalTender1
    collisionGoalTender(ball, goalTender1, "-", "<=", "+")
    collisionGoalTender(invisible_ball, goalTender1, '+', '>=', '-')


    # ball collision with wall u,d,f,b
    collisionWall(ball, wallU, wallD, wallF, wallB)
    collisionWall(invisible_ball, wallU, wallD, wallF, wallB)
    
    ball.pos += ball.velocity
    invisible_ball.pos += ball.velocity


 
    if mode == 2 or mode == 5:
        p2.pos.y = ball.pos.y 
        p2.pos.z = ball.pos.z

    # scoring logic 
    if (ball.pos.x + ball.radius >= wallR.pos.x-WALL_THICK/2.0):
        if mode == 1:
            ball.velocity.x = -ball.velocity.x
        else:
            p1.score += 1
            p1.scored = True
            p1Display1.color = color.yellow
            p2Display1.color = color.white
            restart = True
            subprocess.call(["afplay", "hit1.wav"])
    if (ball.pos.x - ball.radius  <=  wallL.pos.x + WALL_THICK/2.0):
        if mode != 1:
            p2.score += 1
            p2.scored = True
            p1Display1.color = color.white
            p2Display1.color = color.yellow
        restart = True
        subprocess.call(["afplay", "hit2.wav"])


    # ballboxes and shadow
    ballBox1.pos.x = ball.pos.x
    shadow.pos.z = ball.pos.z
    shadow.pos.x = ball.pos.x
    shadow.radius = 5-((ball.pos.y - wallD.pos.y)/(2*WALL_Y))*4+0.5
    shadow.opacity = 1-((ball.pos.y - wallD.pos.y)/(2*WALL_Y))+0.1


    if mode != 1:
        p1Display1.text = str(p1.score)
        p2Display1.text = str(p2.score)

    if restart:
        p1.pos=(-PPOS,0,0)
        if mode != 1:
            p2.pos=(PPOS,0,0)

        while True:
            rate(100)
            if scene.kb.keys:
                key = scene.kb.getkey()
                if key == 'p':
                    break

        randY = random.uniform(-WALL_Y+7, WALL_Y-7)
        randZ = random.uniform(-WALL_Z+7, WALL_Z-7)
        # this needs to be fixed
        if p1.scored == True:
            ballPOSX = p2.pos.x - 3
            ballVX = -1
            p1.scored = False
        elif p2.scored == True:
            ballPOSX = p1.pos.x + 3
            ballVX = 1
            p2.scored = False
        ball.pos = (ballPOSX,randY, randZ)
        randVX = random.choice([-1,1])
        randVY = random.uniform(-0.01,0.01)
        randVZ = random.uniform(-0.01,0.01)
        ball.velocity = vector(ballVX * constantSpeed(ballSpeed,randVY, randVZ), randVY, randVZ)

        restart = False



    limitPosition(p1)
    if mode != 1:
        limitPosition(p2)




    if ball.velocity.x >= 0:
        if mode != 1 and mode != 2:
            ballBox1.opacity =((ball.pos.x-wallL.pos.x)/(2*WALL_X))*0.3
            scene.forward=vector(-3,-0.3,0)
            wallF.opacity=1
            wallL.opacity=1
            wallB.opacity=1
            wallR.opacity=0
            scoreBoard1red.opacity = 0
            scoreBoard1blue.opacity = 0
            scoreBoard2red.opacity = 1
            scoreBoard2blue.opacity = 1
            goalTender2.opacity = 0.3
            goalTender1.opacity =1
            p1Display1.axis=(0,0,-1)
            p1Display1.pos=(-(SCOREPOSX-1),SCOREPOSY,-140)
            p2Display1.axis=(0,0,-1)
            p2Display1.pos=(-(SCOREPOSX-1),SCOREPOSY,150)

    else:
        ballBox1.opacity =0.3-((ball.pos.x-wallL.pos.x)/(2*WALL_X))*0.3
        scene.forward=vector(3,-0.3,0)
        wallF.opacity= 1
        wallL.opacity=0
        wallB.opacity=1
        wallR.opacity=1
        goalTender1.opacity = 0.3

        if mode != 1:
            goalTender2.opacity =1
            scoreBoard1red.opacity = 1
            scoreBoard1blue.opacity = 1
            scoreBoard2red.opacity = 0
            scoreBoard2blue.opacity = 0
            p1Display1.axis=(0,0,1)
            p1Display1.pos=(SCOREPOSX-1,SCOREPOSY,-150)
            p2Display1.axis=(0,0,1)
            p2Display1.pos=(SCOREPOSX-1,SCOREPOSY,140)

    if mode != 1:
        if p1.score == 10 or p2.score == 10:
            done = True
scene.visible = False
endScene()

