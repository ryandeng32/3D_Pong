####################################
# Game name: 3D Pong               #
# File name: usedFunc.py           #
# Author: Ryan Deng                #
# Last Edited: 09/04/2019          #                      
####################################
# this file contains all the function used in main.py 

# futures, this imports python3 division
# division in python3 results in a double instead of an int in python2
from __future__ import division

# other libraries
from visual import *
from math import sqrt, atan, cos, sin, pi
import random

# files included
from settings import *
############################################################################################################################################################

# add_score adds score to the player who scored a point, and change that player's score's display's colour to yellow 
def add_score(scoredP, otherP):
    scoredP.score += 1
    scoredP.scored = True
    scoredP.scoreDisplay.color = color.yellow
    otherP.scoreDisplay.color = color.white


# goTowards makes AI go towards the invisible_ball at a slight angle
# the speed of AI is based on difficulty
def goTowards(ball, p, difficulty):
    # roomY and roomZ is for the AI to hit the ball at an angle
    roomY = random.randint(0,round(P_Y/3))
    roomZ = random.randint(0,round(P_Z/3))
    
    if difficulty == 1:
        divisor = 120
    elif difficulty == 2:
        divisor = 100
    elif difficulty == 3:
        divisor = 70
    # set the default divisor to be 140 
    else:
        divisor = 100
    if ball.pos.y + roomY > p.pos.y:
        p.pos.y += PSPEED/divisor
    if ball.pos.y + roomY< p.pos.y:
        p.pos.y -= PSPEED/divisor
    if ball.pos.z + roomZ > p.pos.z:
        p.pos.z += PSPEED/divisor
    if ball.pos.z + roomZ < p.pos.z:
        p.pos.z -= PSPEED/divisor


# this function moves invisible_ball's position to match ball's
# and it makes the invisible_ball travels faster based on invisibleBallMultiple
def invisibleBall(invisible_ball, ball):
    invisible_ball.pos = ball.pos
    invisible_ball.velocity = invisibleBallMultiple * ball.velocity

    
# this function uses Pythagorean Theorem to make sure the speed of ball stays the same with different y and z components of the velocity
def constantSpeed(ballSpeed, VY, VZ):
    return sqrt(abs(ballSpeed)**2 - abs(VY)**2 - abs(VZ)**2)


# limit player's position so they don't move outside of the walls 
def limitPosition(p):
    if p.pos.y - P_Y / 2 < -WALL_Y + 0.5:
        p.pos.y = -WALL_Y + 0.5 + P_Y / 2
    if p.pos.y + P_Y / 2 > WALL_Y - 0.5:
        p.pos.y = WALL_Y - 0.5 - P_Y / 2
    if p.pos.z + P_Z / 2 > WALL_Y - 0.5:
        p.pos.z = WALL_Y - 0.5 - P_Z / 2
    if p.pos.z - P_Z / 2 < -WALL_Y + 0.5:
        p.pos.z = -WALL_Y + 0.5 + P_Z / 2


# this function checks and executes collision with the players
# a, b, c, d in the arguments are operators, they makes the function usable for both players 
def collisionPlayer(ball, p, ballSpeed,a,b,c,d):
    room = 0.1# used for collision, to make the collision looks more realistic
    if((eval("(ball.pos.x {} ball.radius {} p.pos.x {} P_X/2.0)".format(a,b,c)))  and (ball.pos.y - ball.radius + room <= p.pos.y + P_Y/2.0 and ball.pos.y + ball.radius - room >= p.pos.y-P_Y/2.0) and (ball.pos.z -ball.radius + room <= p.pos.z+ P_Z/2.0 and ball.pos.z + ball.radius - room >= p.pos.z-P_Z/2.0)):

        # this part is checking where the ball hits player's pad
        # the ball is then reflected based on the variable DEVIATION 
        dist1 = p.pos.y - ball.pos.y
        ball.velocity.y = dist1 * DEVIATION
        dist2 = p.pos.z - ball.pos.z
        ball.velocity.z = dist2 * DEVIATION
        ball.velocity.x = d * constantSpeed(ballSpeed,ball.velocity.y, ball.velocity.z)

        # return True when a collision with player does happen
        return True


# this function checks and executes collision with the goaltenders
# a, b, c in the arguments are operators, they makes the function usable for both goaltenders 
def collisionGoalTender(ball, goalTender, a, b, c):
    room = 2 * BALLR / 6 # used for collision
    if (eval("(ball.pos.x {} ball.radius {} goalTender.pos.x {} 0.5)".format(a,b,c)) and (ball.pos.y - ball.radius + room <= goalTender.pos.y + GT_Y_SIZE/2.0 and ball.pos.y + ball.radius - room >= goalTender.pos.y-GT_Y_SIZE/2.0) and (ball.pos.z - ball.radius + room <= goalTender.pos.z +GT_Z_SIZE/2.0 and ball.pos.z + ball.radius - room >= goalTender.pos.z -GT_Z_SIZE/2.0)):
        ball.velocity.x = -ball.velocity.x

        # return True when a collision with goaltender does happen
        return True


# this function checks and executes collision with the walls
def collisionWall(ball, wallU, wallD, wallF, wallB):
    if (ball.pos.y + ball.radius >= wallU.pos.y - WALL_THICK/2.0) or (ball.pos.y - ball.radius <= wallD.pos.y + WALL_THICK/2.0):
        ball.velocity.y = -ball.velocity.y
    if (ball.pos.z + ball.radius >= wallF.pos.z - WALL_THICK/2.0) or (ball.pos.z - ball.radius <= wallB.pos.z + WALL_THICK/2.0):
        ball.velocity.z = -ball.velocity.z


# this function checks and executes collision with the pyramid obstacles 
def collisionPyra(ball):

    # this part caculates the angle of collision between the ball's velocity vector and the obstacle
    # this angle is denoted as the variable "theta"
    # then the angle used to calculate new vector is denoted as the variable "angle"
    beta = atan(10/20)
    if ball.velocity.x == 0:
        alpha = pi/2 - beta
    elif ball.velocity.y == 0:
        alpha = 0
    else: 
        alpha = atan(abs(ball.velocity.y)/abs(ball.velocity.x)) # angle of alpha in radian
    # direction is 2 when ball go towards p1 
    if ball.velocity.x <= 0:
        direction = 2
        theta = abs(alpha - beta)
    # direction is 1 when ball go towards p2 
    else:
        direction = 1
        theta = alpha + beta
    angle = theta + beta

    # calculate the new velocity vector after collision based on the magnitude of the original vector and the angle calculated 
    lengthVector = abs(sqrt(ball.velocity.x ** 2 + ball.velocity.y ** 2))
    newX = lengthVector * cos(angle)
    newY = lengthVector * sin(angle)

    # hit keeps track of whether the collision happens 
    hit = False 
    # section keeps track of the section being collided with, -1 is when no collision happens
    section = -1
    # ballZY makes referencing ball.pos.z and ball.pos.y easier 
    ballZY = []
    if ball.pos.x >= -20 and ball.pos.x <= 20: 
        ballZY = [ball.pos.z, ball.pos.y]


        # logic for getting the value of section
        # this is achieved using the shoelace theorem (to calculate area based on coordinates)
        if (ballZY[0] == 0 and ballZY[1] == 0):
            section = 0
        elif (abs(100-10*ballZY[1]) + abs(5*ballZY[0]+5*ballZY[1]) + abs(5*ballZY[1]-5*ballZY[0])) == 100:
            section = 1
        elif (abs(100-10*ballZY[0]) + abs(5*ballZY[0]-5*ballZY[1]) + abs(5*ballZY[1]+5*ballZY[0])) == 100:
            section = 2
        elif (abs(-100-10*ballZY[1]) + abs(5*ballZY[1]-5*ballZY[0]) + abs(-5*ballZY[0]-5*ballZY[1])) == 100:
            section = 3
        elif (abs(-100-10*ballZY[0]) + abs(5*ballZY[1]-5*ballZY[0]) + abs(5*ballZY[0]+5*ballZY[1])) == 100:
            section = 4

        # logic for detecting collision with the section 
        if section == 0:
            ball.velocity.x = -ball.velocity.x
            return True
        elif section == 1:
            if direction == 1:
                if ball.pos.y - ball.radius <= 0.5 * ball.pos.x + 10:
                    hit = True
            elif direction == 2:
                if ball.pos.y - ball.radius <= -0.5 * ball.pos.x + 10 :
                    hit = True
        elif section == 2:
            if direction == 1:
                if ball.pos.z - ball.radius <= 0.5 * ball.pos.x + 10 :
                    hit = True
            elif direction == 2:
                if ball.pos.z - ball.radius <= -0.5 * ball.pos.x + 10 :
                    hit =  True
        elif section == 3:
            if direction == 1:
                if ball.pos.y + ball.radius >= -0.5 * ball.pos.x - 10 :
                    hit =  True
            elif direction == 2:
                if ball.pos.y + ball.radius >= 0.5 * ball.pos.x - 10 :
                    hit =  True
        elif section == 4:
            if direction == 1:
                if ball.pos.z + ball.radius >= -0.5 * ball.pos.x - 10 :
                    hit = True

            elif direction == 2: 
                if ball.pos.z + ball.radius >= 0.5 * ball.pos.x - 10 :
                    hit = True

        # if the section is collided, 
        if hit:
            # printing out the angles and lengthVector for testing purpose
            # print("alpha = {}, beta = {}, theta = {}, angle = {}".format(alpha, beta, theta, angle))
            # print(lengthVector)

            # logic for assigning values for the new velocity vector 
            if ball.velocity.x < 0: 
                ball.velocity.x = -1 * newX
            else:
                ball.velocity.x = newX
            if section == 1:
                ball.velocity.y = newY
            elif section == 2:
                ball.velocity.z = newY
            elif section == 3:
                ball.velocity.y = -1 * newY
            elif section == 4:
                ball.velocity.z = -1 * newY

            # slightly move the ball's position away from the obstacles to avoid multiple collision detected 
            if direction == 1:
                ball.pos.x -= 2
            else:
                ball.pos.x += 2
            if section == 1:
                ball.pos.y += 2
            elif section == 3:
                ball.pos.y -= 2
            elif section == 2:
                ball.pos.z += 2
            elif section == 4:
                ball.pos.z -= 2

            # return True because there is a collision 
            return True
############################################################################################################################################################
                                
# openScene will display when the game starts
# this displays menu and allows players to select game difficulty and game mode
def openScene():
    speed = 0
    difficulty = 0
    mode = 0
    infoScene = display(title='Game Start', x=0, y=0, width=1400, height=800, centre=(0, 0, 0), background=(1,1,1))
    infoScene.visible = True

    # display menu
    line1 = text(text="Press 1,2,3 for difficulty", pos=(0,5,0), align = 'center' ,depth = 0.5, color=color.black)
    line2 = text(text="The higher the difficulty, the faster the speed", pos=(0,3,0), align = 'center' ,depth = 0.5, color=color.red)
    line3 = text(text="The difficulty also affect how the AI behave", pos=(0,1,0), align = 'center' ,depth = 0.5, color=color.red)
    line4 = text(text="", pos=(0,-1,0), align = 'center' ,depth = 0.5, color=color.red)
    line5 = text(text="", pos=(0,-3,0), align = 'center' ,depth = 0.5, color=color.red)

    # wait for players to choose a difficulty
    while True:
        rate(RATE)
        if infoScene.kb.keys:
            key = infoScene.kb.getkey()
            if key == '1':
                speed = 0.1
                difficulty = 1
            elif key == '2':
                speed = 0.12
                difficulty = 2
            elif key == '3':
                speed = 0.15
                difficulty = 3
            elif key == '4':  # speed fast for testing purpose
                speed = 0.2
                difficulty = 4
            elif key == '5':  # speed slow for testing purpose
                speed = 0.03
                difficulty = 5
            # default speed is 0.07
            else:
                speed = 0.1
                difficulty = 1 
            break

    # change the menu for game mode selection 
    line1.text = "Press 1,2,3,4 to select game mode"
    line2.text = "Mode_1 -  Practice with just a wall, no scoring, with obstacles"
    line3.text = "Mode_2 -  Practice with an AI, with fixed goaltenders and scoring, with obsacles"
    line4.text = "Mode_3 -  2 players with fixed goaltenders and scoring" 
    line5.text = "Mode_4 -  4 players, 2 players controls pads, 2 players control goaltenders, with obstacles"

    # wait for the players to choose a game mode 
    while True:
        rate(RATE)
        if infoScene.kb.keys:
            key = infoScene.kb.getkey()
            if key == '1':
                mode = 1
            elif key == '2':
                mode = 2
            elif key == '3':
                mode = 3
            elif key == '4':
                mode = 4
            # default mode is 1 
            else:
                mode = 1
            break

    # display controls for the players based on game mode selected     
    line1.text = ""
    line2.text = ""
    line3.text = ""
    line4.text = ""
    line5.text = ""
    
    line2.text = "Use arrow keys to move red player"
    if mode == 3 or mode == 4:
        line3.text = "Use 'E', 'A', 'C', and 'Z' to move blue player up, left, down, and right"
    line1.text = "Press any key to continue..."

    # press any key to continue 
    while True:
        rate(RATE)
        if infoScene.kb.keys:
            infoScene.visible = False
            break

    # return speed, difficulty, and mode as a tuple for main.py to unpack,
    return (speed, difficulty, mode)


# endScene will display when the game loop ends
def endScene(winner):
    infoScene = display(title='Game Over', x=0, y=0, width=1400, height=800, centre=(0, 0, 0), background=(1,1,1))
    infoScene.visible = True
    info1 = text(pos = (0,1,0), text="Game Over", align="center", depth=0.1, color=color.black)

    # change the display based on who won
    if winner != "":
        if winner == "Red Wins!":
            infoScene.background = (1,0,0)
        elif winner == "Blue Wins!":
            infoScene.background = (0,0,1)
        else:
            infoScene.background = (1,1,1)
        info2 = text(pos = (0,-1,0), text=winner, align="center", depth=0.1, color=color.black)


