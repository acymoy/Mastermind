'''
CS5001: Mastermind
4/4/2022
Andrew Moy

mastermind_game.py: creates and handles the game mastermind, mainly using
    turtle. 
'''

from turtle import Turtle, Screen
from Marble import Marble
from Point import Point
from mastermind_constants import *
import copy
import random
import time
import logging

COLORS = ['red', 'blue', 'green', 'yellow', 'purple', 'black']

class Mastermind:
    def __init__(self):
        logging.basicConfig(filename='mastermind_errors.err',
                            encoding='utf8',
                            level=logging.DEBUG,
                            format='%(asctime)s %(message)s')
        logging.info('init game...')
        
        self.init_game()
        self.init_marbles()
        self.init_gameplay()
        self.get_name()
        self.wn.onclick(self.on_click) # screen 'wn' listening for clicks
        self.wn.mainloop()
        
    def on_click(self, x, y):
        '''
        function: passes when a click occurs on screen. checks if marbles were
            clicked first, then within the separate clickable spaces.
        params: x, y as the coordinates that were clicked
        returns: none
        '''
        # tests if a marble was clicked
        for marble in self.marble_list:
            if marble.clicked_in_region(x, y) and marble.is_empty == False:
                 self.update_guess(marble)
        # tests if checkbutton (located at 32, -200)
        if x >= CHECKBUTTON_X[0] and x <= CHECKBUTTON_X[1] \
           and y >= CHECKBUTTON_Y[0] and y <= CHECKBUTTON_Y[1]:
            self.confirm_guess()
        
        # tests if xbutton (located at 75, -202)
        if x >= XBUTTON_X[0] and x <= XBUTTON_X[1] \
           and y >= XBUTTON_Y[0] and y <= XBUTTON_Y[1]:
            self.cancel_guess()
        
        # tests if quitbutton (located at 195, -200)
        if x >= QUITBUTTON_X[0] and x <= QUITBUTTON_X[1] \
           and y >= QUITBUTTON_Y[0] and y <= QUITBUTTON_Y[1]:
            self.quit_game()

    def init_game(self):
        '''
        function: initializes the screen and the turtle drawing the hud boxes.
        '''
        # initializing the turtle objects
        self.wn = Screen()
        self.wn.setup(500, 500)
        self.wn.title('CS5001: Mastermind')
        self.hud = Turtle()
        self.hud.speed(0)
        self.hud.ht()
        # loading the buttons and draws everything
        self.register_shapes()
        self.draw_hud()
        self.draw_board()
        self.draw_pegs()
        self.draw_leaderboard()
        self.load_gifs()

    def get_name(self):
        '''
        function: gets the player name with a pop-up. if no name is supplied
            or cancel is pressed, it sets it to anon
        '''
        self.player_name = self.wn.textinput('Mastermind',
                                             'Enter Player Name: ')
        if self.player_name == None:
            logging.info('player did not enter name')
            self.player_name = 'Anon'
        
    def draw_hud(self):
        # drawing the guessing board
        self.rectangle(GUESSING_BOARD_START, GUESSING_BOARD_DIMENSIONS)
        # drawing the leaderboard
        self.rectangle(LEADERBOARD_START, LEADERBOARD_DIMENSIONS)
        # drawing the guessing space
        self.rectangle(GUESSING_SPACE_START, GUESSING_SPACE_DIMENSIONS)

    def rectangle(self, start_xy, dimensions):
        '''
        function: draws a rectangle starting from top right
        params: start_xy as a tuple with the starting coordinates of turtle,
            dimensions as a list/tuple containing the length/width/length/width
            of the rectangle
        returns: none
        '''
        self.hud.up()
        self.hud.setposition(start_xy)
        self.hud.down()
        self.hud.pensize(5)
        self.hud.setheading(0)
        for turns in range(4):
            self.hud.forward(dimensions[turns])
            self.hud.right(90)

    def draw_board(self):
        '''
        function: draws the empty marbles in the board to display while making
            guesses (located in left of left box)
        '''
        self.board = Turtle()
        self.board.speed(0)
        self.board.ht()
        self.board.up()
        self.board.setpos(INITIAL_EMPTY_MARBLE)
        for row in range(10):
            self.board.down()
            self.board.circle(13)
            for column in range(3):
                x, y = self.board.pos()
                self.board.up()
                self.board.setpos(x + BOARD_X_ADDITION, y)
                self.board.down()
                self.board.circle(13)
            self.board.up()
            x, y = self.board.pos()
            # moves the turtle back 3 spaces to draw a new row of marbles
            self.board.setpos(x - (BOARD_X_ADDITION * 3), y - BOARD_Y_DOWN)

    def draw_pegs(self):
        '''
        function: draws the empty pegs in the board space (located right in
            the left box)
        params: none
        returns: none
        '''
        self.pegs = Turtle()
        self.pegs.speed(0)
        self.pegs.ht()
        self.pegs.up()
        self.pegs.setpos(INITIAL_PEG)
        for row in range(10):
            self.pegs.down()
            self.pegs.circle(4)
            for set in range(3): # draws 3 more pegs to form a set
                x, y = self.pegs.pos()
                self.pegs.up()
                if set % 2 == 0: # if even, move it 10 to the right
                    self.pegs.setpos(x + PEG_ON_RIGHT, y)
                elif set % 2 == 1: #if odd, move it back 10 and down 13
                    self.pegs.setpos(x - PEG_ON_RIGHT, y - PEG_DOWN)
                self.pegs.down()
                self.pegs.circle(4)
            self.pegs.up()
            x, y = self.pegs.pos()
            # moves it down for the next set of pegs
            self.pegs.setpos(x - SET_LEFT, y - SET_DOWN)

    def draw_leaderboard(self):
        '''
        function: imports the leaderboard scores and displays them on screen
        params: none
        returns: none
        '''
        self.leaderboard = self.import_leaderboard()
        self.leaders = Turtle()
        self.leaders.up()
        self.leaders.speed(0)
        self.leaders.ht()
        self.leaders.setpos(LEADERBOARD_TURTLE_START)
        self.leaders.down()
        leaderboard_title_font = ('Arial', 15, 'bold')
        # writing leaderboard title
        self.leaders.write('High Scores:', font=leaderboard_title_font)
        self.leaders.up()
        # writing leaderboard scores
        self.leaders.setpos(LEADERBOARD_SCORES_START)
        leaders_font = ('Arial', 12, 'bold')
        for i in range(len(self.leaderboard)):
            self.leaders.down()
            self.leaders.write(f'{self.leaderboard[i][1]} : '
                               f'{self.leaderboard[i][0]}', font=leaders_font)
            self.leaders.up()
            x, y = self.leaders.pos()
            self.leaders.setpos(x, y - LEADERBOARD_SCORES_DOWN)
            if i >= 10: # limit 11 scores listed on scoreboard
                break
            
    def register_shapes(self):
        '''
        function: adds the required gifs/imgs to the screen object to add
            later.
        params: none
        returns: none
        '''
        try:
            self.wn.register_shape('xbutton.gif')
            self.wn.register_shape('checkbutton.gif')
            self.wn.register_shape('leaderboard_error.gif')
            self.wn.register_shape('Lose.gif')
            self.wn.register_shape('quitbutton.gif')
            self.wn.register_shape('quitmsg.gif')
            self.wn.register_shape('winner.gif')
            self.wn.register_shape('pogchamp.gif')
        except:
            logging.error('failed to register gif image')

    def load_gifs(self):
        '''
        function: loads the buttons and stuff for the game
        params: none
        returns: none
        other notes:
            coordinates:
            - xbutton (40x40)
            - checkbutton (40x40)
            - quitbutton at 170, -185 to 220, -215
        '''
        try:
            self.xbutton = Turtle(shape='xbutton.gif')
            self.xbutton.up()
            self.xbutton.setposition(XBUTTON_COORDS)
            self.checkbutton = Turtle(shape='checkbutton.gif')
            self.checkbutton.up()
            self.checkbutton.setpos(CHECKBUTTON_COORDS)
            self.quit = Turtle(shape='quitbutton.gif')
            self.quit.up()
            self.quit.setpos(QUITBUTTON_COORDS)
            self.pog = Turtle(shape='pogchamp.gif')
            self.pog.up()
            self.pog.setpos(POGCHAMP_COORDS)
        except:
            logging.error('gif image failed to load')

    def init_marbles(self):
        '''
        function: initializes the six guessing marbles
        params: none
        returns: none
        notes: default marble radius is 15
        '''
        self.red = Marble(Point(RED_X, MARBLE_OBJECT_Y), 'red')
        self.red.draw()
        self.blue = Marble(Point(BLUE_X, MARBLE_OBJECT_Y), 'blue')
        self.blue.draw()
        self.green = Marble(Point(GREEN_X, MARBLE_OBJECT_Y), 'green')
        self.green.draw()
        self.yellow = Marble(Point(YELLOW_X, MARBLE_OBJECT_Y), 'yellow')
        self.yellow.draw()
        self.purple = Marble(Point(PURPLE_X, MARBLE_OBJECT_Y), 'purple')
        self.purple.draw()
        self.black = Marble(Point(BLACK_X, MARBLE_OBJECT_Y), 'black')
        self.black.draw()
        
        self.marble_list = [self.red, self.blue, self.green, self.yellow,
                            self.purple, self.black]

    def init_gameplay(self):
        '''
        function: initializes a lot of the gameplay elements. generates the
            color code, initializes the guess and player_guess variables.
        params: none
        returns: none
        '''
        self.color_copy = copy.deepcopy(COLORS)
        random.shuffle(self.color_copy)
        self.color_code = self.color_copy[0:4] # generates correct code
        self.guesses = 0
        self.player_guess = []
        self.game_over = False # removes functionality if True

    def check_code(self, player_guess):
        '''
        function: checks the list player_guess compared to the generated
            correct color code. passes the amount of black first, then red
            into a dictionary for later retrieval when updating pegs.
        params: list player_guess containing the player's full guess (len 4)
        returns: returns dictionary pegs, which contains the amount of
            red/black pegs from the player_guess.
        '''
        pegs = {'red': 0, 'black': 0}
        for i in range(len(player_guess)):
            if player_guess[i] == self.color_code[i]:
                pegs['black'] += 1
            elif player_guess[i] in self.color_code:
                pegs['red'] += 1
        return pegs

    def update_guess(self, marble):
        '''
        function: appends list player_guess to add color, empties given marble,
            and then updates the board to show selection
        params: marble object that was clicked
        returns: none
        '''
        if (len(self.player_guess) < 4) and \
           (marble.get_color() not in self.player_guess):
            self.player_guess.append(marble.get_color())
            marble.draw_empty()
            self.draw_guess()

    def draw_guess(self):
        '''
        function: draws the marble object that was just clicked as part of
            a guess. bases where to start drawing with how many guesses are
            already in the player_guess list.
        params: none
        returns: none
        '''
        starting_y = INITIAL_EMPTY_MARBLE[1] - (self.guesses * BOARD_Y_DOWN)
        starting_x = INITIAL_EMPTY_MARBLE[0] + \
                     ((len(self.player_guess) - 1) * BOARD_X_ADDITION)
        self.board.up()
        self.board.setpos(starting_x, starting_y)
        self.board.color(self.player_guess[-1])
        self.board.begin_fill()
        self.board.pencolor('black')
        self.board.circle(13)
        self.board.end_fill()

    def draw_pegs_guess(self, pegs):
        '''
        function: re-draws (or appears to fill in) the pegs in the board space.
            does red pegs first, then black pegs.
        params: pegs, which is a dictionary resulting from check_code(). it
            has however many red or black pegs the player got from guessing.
        returns: none
        '''
        starting_y = INITIAL_PEG[1] - (self.guesses * PEG_SET_DOWN)
        coordinates = [(INITIAL_PEG[0], starting_y), (1, starting_y),
                       (INITIAL_PEG[0], starting_y - PEG_DOWN),
                       (1, starting_y - PEG_DOWN)]
        peg_count = 0
        for i in range(pegs['red']):
            self.pegs.up()
            self.pegs.setpos(coordinates[peg_count])
            self.pegs.color('red')
            self.pegs.begin_fill()
            self.pegs.pencolor('black')
            self.pegs.circle(4)
            self.pegs.end_fill()
            peg_count += 1
        for i in range(pegs['black']):
            self.pegs.up()
            self.pegs.setpos(coordinates[peg_count])
            self.pegs.color('black')
            self.pegs.begin_fill()
            self.pegs.pencolor('black')
            self.pegs.circle(4)
            self.pegs.end_fill()
            peg_count += 1

    def reset_guessing(self):
        '''
        function: resets the guessing space marble objects and the
            player_guess, used when either the X button is hit (triggering
            cancel_guess()) or the check button is hit (triggering
            confirm_guess()).
        params: none
        returns: none
        '''
        self.red.draw()
        self.blue.draw()
        self.green.draw()
        self.yellow.draw()
        self.purple.draw()
        self.black.draw()
        
        self.player_guess = []

    def confirm_guess(self):
        '''
        function: if list player_guess length is 4 (a full guess), checks
            the code, adds one to the guess if in valid, moves the to-be-drawn
            line down one on the board, and then resets the guess to zero
        params: none
        returns: none
        '''
        if len(self.player_guess) == FULL_GUESS and not self.game_over:
            # print(self.color_code) # for testing
            pegs = self.check_code(self.player_guess)
            self.draw_pegs_guess(pegs)
            self.guesses += 1
            # checking win/lose conditions, if not then increment down a guess
            if pegs['black'] == 4: # if all pegs are black, that means u won
                self.win()
            elif self.guesses == 10: # 10 guesses until u lose
                self.create_popup('lose')
                self.game_over = True # to remove functionality
                time.sleep(3)
                self.popup.ht()
            else: # if neither, increment down one guess space on the board
                pogx, pogy = self.pog.pos()
                self.pog.setpos(pogx, pogy - BOARD_Y_DOWN)
                self.reset_guessing()

    def cancel_guess(self):
        '''
        function: functionality for the X button. resets the player's guess,
            fills in the current guessing space with white so it's blank. then
            calls reset_guessing() which resets the marble objects in the
            selection space.
        params: none
        returns: none
        '''
        if not self.game_over:
            self.player_guess = []
            for i in range(4):
                self.player_guess.append('white')
                self.draw_guess()
            self.reset_guessing()
        
    def quit_game(self):
        '''
        function: functionality for the quit button. creates the quit popup,
            waits for 3 seconds, and then exits the program.
        params: none
        returns: none
        '''
        self.create_popup('quit')
        time.sleep(3)
        self.wn.bye()

    def win(self):
        '''
        function: functionality for when the player wins. creates the win
            popup, and then exports your score to the leaderboard doc.
        params: none
        returns: none
        '''
        self.create_popup('win')
        time.sleep(3)
        self.popup.ht()
        self.game_over = True
        self.export_leaderboard()

    def import_leaderboard(self):
        '''
        function: attempts to open leaderboard.txt and sort the scores by
            least to greatest value. sort first, and then split afterwards so
            the order is already established.
            should be formatted as [[SCORE, NAME]]
        params:
        returns: leaderboard nested list as [[SCORE, NAME],[SCORE2, NAME2],etc]
        '''
        leaderboard = []
        num_scores = []
        raw_scores = []
        try:
            with open('leaderboard.txt', mode='r', encoding='utf8') \
                 as scores:
                for line in scores:
                    raw_scores.append(line)
            for score in raw_scores: # cleaning the data
                score = score.replace('\n', '')
                split_score = score.split('@')
                leaderboard.append(split_score)
            # sorts by int version of first term in leaderboard
            leaderboard.sort(key = lambda x: int(x[0])) 
        except Exception:
            self.create_popup('leaderboard_error')
            time.sleep(2)
            self.popup.ht()
            logging.error('FileNotFoundError: '
                          'leaderboard.txt failed to load.')
        return leaderboard
                    
    def export_leaderboard(self):
        '''
        function: appends the new score/name to the leaderboard list, then
            combines the nested lists so it's non-nested strings, then formats
            and exports to leaderboard.txt as 'SCORE@NAME' format. don't need
            to sort because leaderboard.txt is sorted when next imported.
        params:
        returns:
        '''
        joined_scores = []
        self.leaderboard.append([self.guesses, self.player_name])
        for score in self.leaderboard:
            joined_scores.append(f'{score[0]}@{score[1]}')
        try:
            with open('leaderboard.txt', mode='w', encoding='utf8') as end:
                for score in joined_scores:
                    end.write(f'{score}\n')
        except Exception:
            self.create_popup('leaderboard_error')
            time.sleep(2)
            self.popup.ht()
            logging.error('Error: failed to write to '
                               'leaderboard.txt')
        
    def create_popup(self, condition: str):
        '''
        function: depending on condition passed in, sets the image to a certain
            registered shape and then creates a popup for it.
        params: condition as string indicating which popup to make
        returns: none, just creates a new turtle with the popup
        '''
        try:
            if condition == 'win':
                image = 'winner.gif'
            elif condition == 'lose':
                image = 'Lose.gif'
            elif condition == 'quit':
                image = 'quitmsg.gif'
            elif condition == 'leaderboard_error':
                image = 'leaderboard_error.gif'
            elif condition == 'file_error':
                image = 'file_error.gif'
            self.popup = Turtle(shape=image)
            self.popup.setpos(0, 0) # popup is at center of screen
        except:
            logging.error('failed to load image gif')

    def __str__(self):
        return 'Mastermind Game'
            
def main():
    mm = Mastermind()
    
if __name__ == '__main__':
    main()
