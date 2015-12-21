from pdbot import PDBot

class BeatYoBot(PDBot):
    def __init__(self):
        self.init()

    def init(self):
        pass

    def get_play(self):
        return "take 1"

    def make_play(self,opponent_play):
        return