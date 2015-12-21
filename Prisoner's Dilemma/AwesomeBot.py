#import the base class
from pdbot import PDBot

#add whatever libraries you need here from the standard library set
import random

class AwesomeBot(PDBot):
    #can add a constructor to set up any state you need
    #this will be called once at the start of all the games your bot will play
    def __init__(self):
        self.init()

    def init(self):
        #initialise
        #awesomebot always starts with cooperation
        self.other_last_play="give 2"

    #get_play is a function that takes no arguments
    #and returns one of the two strings "give 2" or "take 1" 
    #denoting the next play your agent will take in the game
    def get_play(self):
        #almost-tit-for-tat
        if random.random() < 0.9:
            #tit-for-tat 90% of the time
            myplay = self.other_last_play
        else:
            #random 10% of the time
            if random.random() > 0.5:
                myplay =  "give 2"
            else:
                myplay =  "take 1"
        #you may also want to store myplay here, although awesomebot doesn't need this
        self.my_last_play = myplay

        return myplay

    #make_play is a function that takes a single string argument
    #that is either "give 2" or "take 1" denoting the opponent's
    #last play in the game    
    def make_play(self,opponent_play):
        #store for next round
        self.other_last_play = opponent_play
        return
class TheGoodGuy(PDBot):
    def __init__(self):
        self.init()

    def init(self):
        self.other_last_play="give 2"
        self.num_move = 1

    def get_play(self):
        breaking_bad_turn = 17
        if self.num_move >= breaking_bad_turn:
            return "take 1"
        else:
            return self.other_last_play
  
    def make_play(self,opponent_play):
        self.other_last_play = opponent_play
        self.num_move += 1
class BeatYoBot(PDBot):
    def __init__(self):
        self.init()

    def init(self):
        self.other_last_play="give 2"

    def get_play(self):
        # #almost-tit-for-tat
        # if random.random() < 0.9:
        #     #tit-for-tat 90% of the time
        #     myplay = self.other_last_play
        # else:
        #     #random 10% of the time
        #     if random.random() > 0.5:
        #         myplay =  "give 2"
        #     else:
        #         myplay =  "take 1"
        # #you may also want to store myplay here, although awesomebot doesn't need this
        # self.my_last_play = myplay

        return self.other_last_play

    def make_play(self,opponent_play):
        self.other_last_play = opponent_play
        return
class AlwaysDefeatBot(PDBot):
    def __init__(self):
        self.init()

    def init(self):
        pass

    def get_play(self):
        return "take 1"

    def make_play(self,opponent_play):
        return
class RunningDeadBot(PDBot):
    def __init__(self):
        self.init()

    def init(self):
        # starts with cooperation
        self.other_last_play= "give 2"
        # turns counter
        self.iteration = 1

    def get_play(self):
        if self.iteration >= 17:
            return "take 1"
        else: # tit-for-tat
            return self.other_last_play

    def make_play(self,opponent_play):
        # store for next round
        self.other_last_play = opponent_play
        self.iteration += 1
        return
class WalkingDeadBot(PDBot):
    def __init__(self):
        self.init()

    def init(self):
        # starts with cooperation
        self.other_last_play= "give 2"
        # turns counter
        self.iteration = 1

    def get_play(self):
        if self.iteration >= 16:
            return "take 1"
        else: # tit-for-tat
            return self.other_last_play

    def make_play(self,opponent_play):
        # store for next round
        self.other_last_play = opponent_play
        self.iteration += 1
        return
        
if __name__ == "__main__":
    bots_score = [0,0,0,0,0,0]
    for y in xrange(15):
        for i in xrange(6-1):
            for j in xrange(i+1, 6):
                bot1 = AwesomeBot()
                bot2 = TheGoodGuy()
                bot3 = BeatYoBot()
                bot4 = AlwaysDefeatBot()
                bot5 = RunningDeadBot()
                bot6 = WalkingDeadBot()
                bots = [bot1, bot2, bot3, bot4, bot5, bot6]
                botA = bots[i]
                botB = bots[j]
                done = False            
                botA_score = bots_score[i]
                botB_score = bots_score[j]
                for x in xrange(5):
                    botA.init()
                    botB.init()
                    iteration = 1
                    maxiterations = 15 + random.randint(-3,3)
                    while iteration < maxiterations and not done:
                        botA_action = botA.get_play()
                        botB_action = botB.get_play()
                        botA.make_play(botB_action)
                        botB.make_play(botA_action)

                        if botB_action == "give 2":
                            bots_score[i] += 2
                        if botA_action == "give 2":
                            bots_score[j] += 2
                        if botA_action == "take 1":
                            bots_score[i] += 1
                        if botB_action == "take 1":
                            bots_score[j] += 1
                        
                        iteration += 1
    for y in xrange(len(bots_score)):
        bots_score[y] = int(bots_score[y] / 20)

    print bots_score