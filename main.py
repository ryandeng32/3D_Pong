####################################
# File name: 3D Pong               #
# Author: Ryan Deng                #
# Last Edited: 24/03/2019          #                      
####################################
# futures
from __future__ import division

# other libraries
from visual import *
# subprocess module is for adding sound
import subprocess
import random

# these are files that I included for a cleaner code layout
from settings import *
from scenes import *
######################################################################

# set test to true to enter test mode
test = False

# setting the speed of the ball by selecting difficulty, and setting the game mode
# if game mode is 2, difficulty also affects difficulty of the computer opponent(will be refered as AI but it's just a fake AI)
ballSpeed, mode = openScene()

# GAME MODE
# 1 - 1 player in practice mode, fixed goaltenders
# 2 - 1 player against a computer, fixed goaltenders
# 3 - 2 players, fixed goaltenders
# 4 - 4 players, 2 players control pads, 2 players control goaltenders
scene = display(width=1400, height=800, range = 190, background=color.black)

# shadow and ballBox is used to indicate the position of the ball better for player
shadow = cylinder(pos=vector(0,-WALL_Y+WALL_THICK/2.0,0), color = color.black, axis=vector(0,0.1,0), radius=3)
ballBox = box(pos = (0,1,0),size =(0.01,2*WALL_Y-1,2*WALL_Z), color = color.black,opacity = 0.1)

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
    p1.scoreDisplay = text (font = "Times",text=str(p1.score), height = 20, width = 15, depth=0.5, axis=(0,0,1),color=color.white)
    p2.scoreDisplay = text (font = "Times",text=str(p2.score), height = 20, width = 15, depth=0.5, axis=(0,0,1),color=color.white)

ball = sphere(pos=(0,0,0), radius=BALLR, color=color.cyan)# enable trail code: make_trail = True, interval=10,retain=100 
ball.velocity = vector(-1 * ballSpeed,0,0)


# add invisible ball to create imperfect AI
# the concept of using a invisible ball is taken from https://gamedev.stackexchange.com/questions/57352/imperfect-pong-ai
if mode == 2: 
    invisible_ball = sphere(pos=(0,0,0), radius=BALLR, color=color.red)
    invisible_ball.velocity = vector(0,0,0)
    if not test:
        invisible_ball.opacity = 0


# during game mode 2, go is true when the ball is going towards AI, go activates invisible ball
if mode == 2: 
    go = False
# once one player scores, restart will be set to true, this is to implement pauses during gameplay
restart = False
# done controls the game loop, when done is True, the game loop finishes
done = False
# control is a variable used for player movement, stores a key when a key is pressed
control = ""

while not done:
    rate(RATE)

    # configuring control for player 1(arrow keys)  
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
        # configuring control for player 2(e - up, c - down, a - left, z - right)
        # these keys are used because they are compatible for my keyboard
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
    if mode == 4:
        if control == '1':
            pass
            

    # make sure players don't move out of the field
    limitPosition(p1)
    if mode != 1:
        limitPosition(p2)



    # ball collision with p2
    if mode != 1:
        #possibly add error trap to make sure sqrt function does not take a negative number as argument
        collisionPlayer(ball,p2, ballSpeed,'+' , '>=', '-',-1)

    # ball collision with p1
    if collisionPlayer(ball,p1, ballSpeed,'-', '<=', '+', 1):
        if mode == 2:
            go = True
            invisibleBall(invisible_ball,ball)
        else:
            pass

    if mode != 1:
        # ball collision with goalTender2
        collisionGoalTender(ball, goalTender2, "+", ">=", "-")
    # ball collision with goalTender1
    if collisionGoalTender(ball, goalTender1, "-", "<=", "+"):
        if mode == 2:
            go = True
            invisibleBall(invisible_ball,ball)
        else:
            pass

    # ball collision with wall u,d,f,b
    collisionWall(ball, wallU, wallD, wallF, wallB)
    if mode == 2: 
        collisionWall(invisible_ball, wallU, wallD, wallF, wallB)

    ball.pos += ball.velocity
    if mode == 2: 
        invisible_ball.pos += invisible_ball.velocity
        if invisible_ball.pos.x > p2.pos.x-5:
            invisible_ball.velocity = vector(0,0,0)
    
    # make AI move towards invisible ball when condition is met
    if (mode == 2):
        if go: 
            goTowards(invisible_ball, p2)
        # when p2's position is the same as the invisible ball, stop going towards it
        if p2.pos.x == invisible_ball.pos.x and p2.pos.y == invisible_ball.pos.y and p2.pos.z == invisible_ball.pos.z:
            go = False


    # scoring logic 
    if (ball.pos.x + ball.radius >= wallR.pos.x-WALL_THICK/2.0):
        if mode == 1:
            ball.velocity.x = -ball.velocity.x
        else:
            add_score(p1,p2)
            restart = True
            subprocess.call(["afplay", "hit1.wav"])
    if (ball.pos.x - ball.radius  <=  wallL.pos.x + WALL_THICK/2.0):
        if mode != 1:
            add_score(p2,p1)
        restart = True
        subprocess.call(["afplay", "hit2.wav"])


    # ballboxes and shadow
    ballBox.pos.x = ball.pos.x
    shadow.pos.z = ball.pos.z
    shadow.pos.x = ball.pos.x
    shadow.radius = 5-((ball.pos.y - wallD.pos.y)/(2*WALL_Y))*4+0.5
    shadow.opacity = 1-((ball.pos.y - wallD.pos.y)/(2*WALL_Y))+0.1

    # update score display
    if mode != 1:
        p1.scoreDisplay.text = str(p1.score)
        p2.scoreDisplay.text = str(p2.score)

    
    if restart:
        # pause the game until p is pressed 
        p1.pos=(-PPOS,0,0)
        if mode != 1:
            p2.pos=(PPOS,0,0)
        while True:
            rate(RATE)
            if scene.kb.keys:
                key = scene.kb.getkey()
                if key == 'p':
                    break
        # respawn ball at random location on y and z axis
        randY = random.uniform(-WALL_Y+7, WALL_Y-7)
        randZ = random.uniform(-WALL_Z+7, WALL_Z-7)
        if p1.scored == True or mode == 1:
            ballPOSX = PPOS - 3
            ballVX = -1
            p1.scored = False
        elif p2.scored == True:
            ballPOSX = -PPOS + 3
            ballVX = 1
            p2.scored = False
        ball.pos = (ballPOSX,randY, randZ)

        # respawn ball with random speed
        randVX = random.choice([-1,1])
        randVY = random.uniform(-0.01,0.01)
        randVZ = random.uniform(-0.01,0.01)
        ball.velocity = vector(ballVX * constantSpeed(ballSpeed,randVY, randVZ), randVY, randVZ)
        if mode == 2: 
            go = True
            invisibleBall(invisible_ball,ball)
        restart = False
        
    # when ball is going towards p2
    if ball.velocity.x >= 0:
        if mode != 1 and mode != 2:
            ballBox.opacity =((ball.pos.x-wallL.pos.x)/(2*WALL_X))*0.3
            if not test:
                scene.forward=vector(-3,-0.3,0)
            goalTender1.opacity =1
            viewConfig(p1,p2,goalTender2, wallL, wallR, 200,-1)
            scoreBoard1red.opacity = 0
            scoreBoard1blue.opacity = 0
            scoreBoard2red.opacity = 1
            scoreBoard2blue.opacity = 1
            goalTender2.opacity = 0.3
        else:
            wallL.opacity = 0
            wallR.opacity = 1

    # when ball is going towards p1
    else:
        ballBox.opacity =0.3-((ball.pos.x-wallL.pos.x)/(2*WALL_X))*0.3
        if not test:
            scene.forward=vector(3,-0.3,0)
        goalTender1.opacity = 0.3
        if mode != 1:
            viewConfig(p1,p2,goalTender2, wallL, wallR, 200,1)
            scoreBoard1red.opacity = 1
            scoreBoard1blue.opacity = 1
            scoreBoard2red.opacity = 0
            scoreBoard2blue.opacity = 0
            goalTender2.opacity =1
        else:
            wallL.opacity = 0
            wallR.opacity = 1
            

    # game over when one player reaches 10 points
    if mode != 1:
        if p1.score == 10 or p2.score == 10:
            done = True

# display endgame screen
scene.visible = False
endScene()

