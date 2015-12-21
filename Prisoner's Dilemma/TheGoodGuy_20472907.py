#!bin/usr/python
import random

class TheGoodGuy(PDBot):
    def __init__(self):
        self.init()

    def init(self):
        self.other_last_play="give 2"
        self.num_move = 1

    def get_play(self):
        breaking_bad_turn = 16
        if self.num_move >= breaking_bad_turn:
            return "take 1"
        else:
            return self.other_last_play
  
    def make_play(self,opponent_play):
        self.other_last_play = opponent_play
        self.num_move += 1