from __future__ import division
from visual import *
from settings import *
from math import sqrt
import random

def viewConfig(p1, p2, goalTender2, wallL, wallR, scorePos,mode):
    if mode == -1:
        wallL.opacity = 1
        wallR.opacity = 0
        p1.scoreDisplay.pos=(-(SCOREPOSX-1),SCOREPOSY, mode*scorePos)
        p2.scoreDisplay.pos=(-(SCOREPOSX-1),SCOREPOSY,-1 * mode * scorePos + 10)
    else:
        wallL.opacity = 0
        wallR.opacity = 1
        p1.scoreDisplay.pos=(SCOREPOSX-1,SCOREPOSY, -1 * mode * (scorePos + 10))
        p2.scoreDisplay.pos=(SCOREPOSX-1,SCOREPOSY,mode)
    p1.scoreDisplay.axis=(0,0,mode)
    p2.scoreDisplay.axis=(0,0,mode)
    p1.scoreDisplay.pos=(SCOREPOSX-1,SCOREPOSY, -210)
    p2.scoreDisplay.pos=(SCOREPOSX-1,SCOREPOSY,200)


    
def add_score(scoredP, otherP):
    scoredP.score += 1
    scoredP.scored = True
    scoredP.scoreDisplay.color = color.yellow
    otherP.scoreDisplay.color = color.white
    
def goTowards(ball, p):
    roomY = random.randint(0,P_Y/2)
    roomZ = random.randint(0,P_Z/2)
    if ball.pos.y + roomY > p.pos.y:
        p.pos.y += PSPEED/130
    if ball.pos.y + roomY< p.pos.y:
        p.pos.y -= PSPEED/130
    if ball.pos.z + roomZ > p.pos.z:
        p.pos.z += PSPEED/130
    if ball.pos.z + roomZ < p.pos.z:
        p.pos.z -= PSPEED/130

    
def invisibleBall(invisible_ball, ball):
    invisible_ball.pos = ball.pos
    invisible_ball.velocity = invisibleBallMultiple * ball.velocity
    
 
def constantSpeed(ballSpeed, VY, VZ):
    return sqrt(abs(ballSpeed)**2 - abs(VY)**2 - abs(VZ)**2)


def limitPosition(p):
    if p.pos.y - P_Y / 2 < -WALL_Y + 0.5:
        p.pos.y = -WALL_Y + 0.5 + P_Y / 2
    if p.pos.y + P_Y / 2 > WALL_Y - 0.5:
        p.pos.y = WALL_Y - 0.5 - P_Y / 2
    if p.pos.z + P_Z / 2 > WALL_Y - 0.5:
        p.pos.z = WALL_Y - 0.5 - P_Z / 2
    if p.pos.z - P_Z / 2 < -WALL_Y + 0.5:
        p.pos.z = -WALL_Y + 0.5 + P_Z / 2

def collisionPlayer(ball, p, ballSpeed,a,b,c,d):
    room = 0.1# used for collision
    if ((eval("(ball.pos.x {} ball.radius {} p.pos.x {} P_X/2.0)".format(a,b,c)))  and (ball.pos.y - ball.radius + room <= p.pos.y + P_Y/2.0 and ball.pos.y + ball.radius - room >= p.pos.y-P_Y/2.0) and (ball.pos.z -ball.radius + room <= p.pos.z+ P_Z/2.0 and ball.pos.z + ball.radius - room >= p.pos.z-P_Z/2.0)):
        dist1 = p.pos.y - ball.pos.y
        ball.velocity.y = dist1 * DEVIATION

        dist2 = p.pos.z - ball.pos.z
        ball.velocity.z = dist2 * DEVIATION
        ball.velocity.x = d * constantSpeed(ballSpeed,ball.velocity.y, ball.velocity.z)
        return True

def collisionGoalTender(ball, goalTender, a, b, c):
    room = 2 * BALLR / 6.0 # used for collision
    if (eval("(ball.pos.x {} ball.radius {} goalTender.pos.x {} 0.5)".format(a,b,c)) and (ball.pos.y - ball.radius + room <= goalTender.pos.y + GT_Y_SIZE/2.0 and ball.pos.y + ball.radius - room >= goalTender.pos.y-GT_Y_SIZE/2.0) and (ball.pos.z - ball.radius + room <= goalTender.pos.z +GT_Z_SIZE/2.0 and ball.pos.z + ball.radius - room >= goalTender.pos.z -GT_Z_SIZE/2.0)):
        ball.velocity.x = -ball.velocity.x
        return True

def collisionWall(ball, wallU, wallD, wallF, wallB):
    if (ball.pos.y + ball.radius >= wallU.pos.y - WALL_THICK/2.0) or (ball.pos.y - ball.radius <= wallD.pos.y + WALL_THICK/2.0):
        ball.velocity.y = -ball.velocity.y
    if (ball.pos.z + ball.radius >= wallF.pos.z - WALL_THICK/2.0) or (ball.pos.z - ball.radius <= wallB.pos.z + WALL_THICK/2.0):
        ball.velocity.z = -ball.velocity.z
    
def openScene():
    speed = 0
    mode = 0
    infoScene = display(title='Game Start', x=0, y=0, width=1400, height=800, centre=(0, 0, 0), background=(1,1,1))
    infoScene.visible = True
    
    line1 = text(text="Press 1,2,3 for difficulty", pos=(0,5,0), align = 'center' ,depth = 0.5, color=color.black)
    line2 = text(text="The higher the difficulty, the faster the speed", pos=(0,3,0), align = 'center' ,depth = 0.5, color=color.red)
    line3 = text(text="The difficulty also affect how the AI behave", pos=(0,1,0), align = 'center' ,depth = 0.5, color=color.red)
    line4 = text(text="", pos=(0,-1,0), align = 'center' ,depth = 0.5, color=color.red)
    line5 = text(text="", pos=(0,-3,0), align = 'center' ,depth = 0.5, color=color.red)

    while True:
        rate(60)
        if infoScene.kb.keys:
            key = infoScene.kb.getkey()
            if key == '1':
                speed = 0.07 / dT
            elif key == '2':
                speed = 0.1 / dT
            elif key == '3':
                speed = 0.12 / dT
            elif key == '4':  # test speed fast
                speed = 0.15 / dT
            elif key == '5':  # test speed extreme
                speed = 0.5 / dT
            break
        
    line1.text = "Press 1,2,3,4 to select game mode"
    line2.text = "Mode_1 -  Practice with just a wall, no scoring"
    line3.text = "Mode_2 -  Practice with an AI, with fixed goaltenders and scoring"
    line4.text = "Mode_3 -  2 players with fixed goaltenders and scoring" 
    line5.text = "Mode_4 -  4 players, 2 players controls pads, 2 players control goaltenders"
    
    while True:
        rate(60)
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
            infoScene.visible = False
            break
    return (speed, mode)


def endScene():
    infoScene = display(title='Game Over', x=0, y=0, width=500, height=300, centre=(0, 0, 0), background=(1, 0, 0))
    infoScene.visible = True
    info = text(text="Game Over", align="center", depth=3, color=color.magenta)
