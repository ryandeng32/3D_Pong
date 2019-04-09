####################################
# Game name: 3D Pong               #
# File name: settings.py           #
# Author: Ryan Deng                #
# Last Edited: 9/04/2019           #                      
####################################
# this file contains variables responsible for the configuration of the game

# configs the x, y, z position of walls 
WALL_X = 150  
WALL_Y = 50  
WALL_Z = 50
# configs the thickness of the walls
WALL_THICK = 1

# the size of goaltenders, they are related to the size of walls
GT_Y_SIZE = (2 * WALL_Y) / 4.0
GT_Z_SIZE = (2 * WALL_Y) / 4.0

# configs the radius of ball/ pong 
BALLR = 3

# configs how much faster the invisible ball is 
invisibleBallMultiple = 1.5

# DEVIATION determines how sensitive the angle of deflection is
DEVIATION = 0.005

# RATE determines how fast the game loop is 
RATE = 1000

# controls how close the players are to the walls 
PPOS = WALL_X - 5

# configs the x, y, z sizes of the score boards
SCOREPOSX = WALL_X + 2
SCOREPOSY = WALL_Y - 60
SCOREPOSZ = 180

# configs the x, y, z sizes of players' pads 
P_X = 0.3
P_Y = 8
P_Z = 8

# configs the speed of players' pads
PSPEED = 2.5

# game ends when one player reaches this score 
gamePoints = 10




