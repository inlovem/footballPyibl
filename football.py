import random

import pyibl
import numpy as np
import pandas as pd
import matplotlib as plt


DEFAULT_UTILITY = 30
NOISE = 0.25
DECAY = 0.05
TEMPERATURE = 0
games = 160
plays = 60
f_down = False
down = 0
distance = 40
payoff = 0
ytd = 10

defaultout = "football_data.csv"
offense = pyibl.Agent("Offense Agent", ["direction", "pass", "short"], default_utility=DEFAULT_UTILITY, decay=DECAY, noise=NOISE)
#defense = pyibl.Agent("Defense Agent", [""])
left_play = {"direction": "left", "pass": False, "run" : False, "short": False}
right_play = {"direction": "right", "pass": False, "run" : False, "short": False} # least risky
middle_play = {"direction": "middle", "pass": False, "run" : False, "short": False}


def reset_agent(a, noise=NOISE, decay=DECAY):
    a.reset(False)
    a.noise = noise
    a.decay = decay



def run():
    time = 60
    yrdgain = 0


    for g in range(games):
        reset_agent(offense)
        offense.trace = True

        for t in range(1, time):# game start
            if t < 50: # low risk time in game
                if distance in range(30, 70): #low risk location
                    if down == 1 and ytd == 10: # most options to play
                        #risk = play_choice(down, ytd, time, distance) # some decimal indicating risk
                        #reward = success_payoff(risk, left_play, right_play, middle_play)
                        if random.randint(0, 1) < .5:
                            left_play["pass"] = True
                            right_play["pass"] = True
                            middle_play["pass"] = True
                        else
                            left_play["run"] = True
                            right_play["run"] = True
                            middle_play["run"] = True

                        play = offense.choose(left_play, middle_play, right_play)
                        if play["direction"] == "left":

                            payoff = random.randint(1, 10)
                            offense.respond(left_play)



                            payoff = random.randint(-5, 0)
                            offense.respond(left_play)


                        distance = distance + payoff
                        if play["direction"] == "middle":

                            payoff = random.randint(1, 10)
                            offense.respond(middle_play)



                            payoff = random.randint(-10, 0)
                            offense.respond(middle_play)

                        distance = distance + payoff
                        if play["direction"] == "right":

                            payoff = random.randint(1, 10)
                            offense.respond(right_play)



                            payoff = random.randint(-2, 0)
                            offense.respond(right_play)


                        distance = distance + payoff

                        down += 1





                    elif down == 2 and ytd in range(1, yrdgain):# no positive payoff and yard gain is none

                        down += 1
                    elif down == 3 and ytd in range(1, yrdgain): # postive payoff and yard gain is between 1 an


                        down += 1
                    elif down == 4 and ytd in range(1, yrdgain): # no payoff and yard gain exists
                        #success




                            down = 1
                            ytd = 10
                            distance = 10 - yrdgain

                        #failure


                        down = 1
                        ytd = 10
                        distance = random.randint(30, 60)
                        yrdgain and down restart

                # lower yards to touchdown but defense is not compact in space to cover
                elif distance in range(70, 90):

                    if down == 1 and ytd == 10:  # most options to play

                    elif down == 2 or down == 3 and ytd in range(1, 10)  # no positive payoff and yard gain is none

                    elif down == 2 or down == 3 and ytd in range(1, yrdgain)  # postive payoff and yard gain is between 1 an n

                    elif down == 4 and ytd in range in range(1, yrdgain)  # no payoff and yard gain exists


                # lower yards to touchdown but defense is compact and has lowest space to cover
                elif distance in range(90, 100):

                    if down == 1 and ytd in range(1, 10):  # most options to play

                    elif down == 2 or down == 3 and ytd in range(1, 10)  # no positive payoff and yard gain is none

                    elif down == 2 or down == 3 and ytd in range(1, yrdgain)  # postive payoff and yard gain is between 1 an n

                    elif down == 4 and ytd in range in range(1, yrdgain)  # no payoff and yard gain exists



            else: # higher risk time in game

                if distance in range(30, 70):  # low risk location

                    if down == 1 and ytd == 10:  # most options to play

                    elif down == 2 or down == 3 and ytd in range(1, 10)  # no positive payoff and yard gain is none

                    elif down == 2 or down == 3 and ytd in range(1,
                                                                 yrdgain)  # postive payoff and yard gain is between 1 an n

                    elif down == 4 and ytd in range in range(1, yrdgain)  # no payoff and yard gain exists

                # lower yards to touchdown but defense is not compact in space to cover
                elif distance in range(70, 90):

                    if down == 1 and ytd == 10:  # most options to play

                    elif down == 2 or down == 3 and ytd in range(1, 10)  # no positive payoff and yard gain is none

                    elif down == 2 or down == 3 and ytd in range(1, yrdgain)  # postive payoff and yard gain is between 1 an n

                    elif down == 4 and ytd in range in range(1, yrdgain)  # no payoff and yard gain exists

                # lower yards to touchdown but defense is compact and has lowest space to cover
                elif distance in range(90, 100):

                    if down == 1 and ytd in range(1, 10):  # most options to play

                    elif down == 2 or down == 3 and ytd in range(1, 10)  # no positive payoff and yard gain is none

                    elif down == 2 or down == 3 and ytd in range(1, yrdgain)  # postive payoff and yard gain is between 1 an n

                    elif down == 4 and ytd in range in range(1, yrdgain)  # no payoff and yard gain exists

            time-=.15


def play_choice(down, ytd, time, distance):
    return ((down * ytd * time)/ distance))


def success_payoff(risk, left_play, right_play, middle_play):


    return play_choice, reward
