'''
CS5001: Mastermind
4/14/2022
Andrew Moy

mastermind_constants.py: holds all the constants needed for the game
'''
# window size
WINDOW = (500, 500)

# board rectangle coordinates
GUESSING_BOARD_START = (-245, 245)
GUESSING_BOARD_DIMENSIONS = [300, 400, 300, 400]

LEADERBOARD_START = (90, 245)
LEADERBOARD_DIMENSIONS = [140, 400, 140, 400]

GUESSING_SPACE_START = (-245, -164)
GUESSING_SPACE_DIMENSIONS = [475, 73, 475, 73]

# guessing board coordinates
INITIAL_EMPTY_MARBLE = (-200, 200)
BOARD_X_ADDITION = 35
BOARD_Y_DOWN = 37

# drawing the pegs
INITIAL_PEG = (-9, 214)
PEG_ON_RIGHT = 10
PEG_DOWN = 13
SET_LEFT = 10
SET_DOWN = 23.75

PEG_SET_DOWN = 36.75

# drawing the leaderboard
LEADERBOARD_TURTLE_START = (100, 210)
LEADERBOARD_SCORES_START = (100, 175)
LEADERBOARD_SCORES_DOWN = 30

# gif placement positions
XBUTTON_COORDS = (75, -202)
CHECKBUTTON_COORDS = (32, -200)
QUITBUTTON_COORDS = (195, -200)
POGCHAMP_COORDS = (-55, 214)

# gif beginning and ending coordinates on x and y
CHECKBUTTON_X = (12, 52)
CHECKBUTTON_Y = (-220, -180)

XBUTTON_X = (55, 95)
XBUTTON_Y = (-222, -182)

QUITBUTTON_X = (170, 220)
QUITBUTTON_Y = (-214, -186)

# marble object positions
MARBLE_OBJECT_Y = -215

RED_X = -210
BLUE_X = -175
GREEN_X = -140
YELLOW_X = -105
PURPLE_X = -70
BLACK_X = -35

FULL_GUESS = 4
