'''
CS5001: Mastermind Test
4/8/2022
Andrew Moy

test_mastermind_game.py: conducts two tests of the functions that return
    values in mastermind_game.py. 
'''

import unittest
from mastermind_game import Mastermind

class TestMastermind(unittest.TestCase):
    
    def test_check_code(self):
        self.game = Mastermind()
        # setting the answer key manually
        # since there's no method to set color_code, i do it manually
        self.game.color_code = ['red', 'green', 'purple', 'blue']

        guess1 = ['red', 'black', 'blue', 'green']
        guess2 = ['red', 'green', 'purple', 'blue']
        guess3 = ['yellow', 'purple', 'black', 'red']
        
        self.assertEqual(self.game.check_code(guess1), {'red': 2, 'black': 1})
        self.assertEqual(self.game.check_code(guess2), {'red': 0, 'black': 4})
        self.assertEqual(self.game.check_code(guess3), {'red': 2, 'black': 0})
        
    def test_import_leaderboard(self):
        '''
        function: tests the import_leaderboard function in mastermind.
        note: this function exports the leaderboard and then subsequently
        imports it so we can compare the returned values.
        '''
        self.game = Mastermind()
        self.game.leaderboard = [] # sets an empty leaderboard
        self.game.guesses, self.game.player_name = 10, 'andrew' # test score
        self.game.export_leaderboard() # writes the one line to leaderboard
        
        self.assertEqual(self.game.import_leaderboard(), [['10', 'andrew']])

        self.game.leaderboard = [] # resets to empty leaderboard
        self.game.guesses, self.game.player_name = 0, 'a;neirj;oiatj;ekjfds'
        self.game.export_leaderboard()

        self.assertEqual(self.game.import_leaderboard(),
                         [['0', 'a;neirj;oiatj;ekjfds']])

        self.game.guesses, self.game.player_name = 5, 'kite'
        self.game.export_leaderboard()

        self.assertEqual(self.game.import_leaderboard(),
                         [['0', 'a;neirj;oiatj;ekjfds'], ['5', 'kite']])
                    
        

def main():
    unittest.main(verbosity = 3)

if __name__ == '__main__':
    main()

