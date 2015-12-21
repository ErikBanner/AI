from pdbot import PDBot
import random

class BeatYoBot(PDBot):
    def __init__(self):
        self.init()

    def init(self):
        self.other_last_play="give 2"

    def get_play(self):
        if random.random() < 0.9:
            myplay = self.other_last_play
        else:
            if random.random() > 0.5:
                myplay =  "give 2"
            else:
                myplay =  "take 1"
        self.my_last_play = myplay

        return myplay

    def make_play(self,opponent_play):
        self.other_last_play = opponent_play
        return