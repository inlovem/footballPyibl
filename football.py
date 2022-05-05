import random

import pyibl
import numpy as np
import pandas as pd
import matplotlib as plt


DEFAULT_UTILITY = 30
NOISE = 0.25
DECAY = 0.05
TEMPERATURE = 0
games = 600
plays = 60
DOWN = 1
DISTANCE = 40
payoff = 0
YTD = 10
TIME = 60


defaultout = "football_data.csv"
offense = pyibl.Agent("Offense Agent", ["direction", "pass", "short"], default_utility=DEFAULT_UTILITY, decay=DECAY, noise=NOISE)
left_play = {"direction": "left", "pass": False, "run" : False, "short": False}
right_play = {"direction": "right", "pass": False, "run" : False, "short": False} # least risky
middle_play = {"direction": "middle", "pass": False, "run" : False, "short": False}


def reset_agent(a, noise=NOISE, decay=DECAY):
    a.reset(False)
    a.noise = noise
    a.decay = decay



def run(distance = DISTANCE, down = DOWN, ytd = YTD, time = TIME, f_down_bool = False):
    for g in range(games):
        reset_agent(offense)
        offense.trace = True
        f_down = [0] * games
        for t in range(1, time):# game start
            if t < 50: # low risk time in game
                if distance in range(30, 70): #low risk location
                    for down in range(4):
                        down_plays(f_down, t, distance, down, ytd, f_down_bool)
                        if f_down_bool == True:
                            ytd = 10
                            break

                # lower yards to touchdown but defense is not compact in space to cover
                elif distance in range(70, 90):
                    for down in range(4):
                        down_plays(f_down, t, distance, down, ytd, f_down_bool)
                        if f_down_bool == True:
                            break
                # lower yards to touchdown but defense is compact and has lowest space to cover
                elif distance in range(90, 100):
                    for down in range(4):
                        down_plays(f_down, t, distance, down, ytd, f_down_bool)

                        if f_down_bool == True:
                            break

                elif distance > 100:
                        distance = DISTANCE

            else: # higher risk time in game
                if distance in range(30, 70):  # low risk location
                    for down in range(4):
                        down_plays(f_down, t, distance, down, ytd, f_down_bool)
                        if f_down_bool == True:
                            break
                # lower yards to touchdown but defense is not compact in space to cover
                elif distance in range(70, 90):
                    for down in range(4):
                        down_plays(f_down, t, distance, down, ytd, f_down_bool)
                        if f_down_bool == True:
                            break
                elif distance in range(90, 100):
                    for down in range(4):
                        down_plays(f_down, t, distance, down, ytd, f_down_bool)
                        if f_down_bool == True:
                            break
                elif distance > 100:
                        distance = DISTANCE


def down_plays(f_down, t, distance, down, ytd, f_down_bool = False):
    # figure out lieklihoods of pass to run in time and distance
    if random.randint(0, 1) < .5:
        left_play["pass"] = True
        right_play["pass"] = True
        middle_play["pass"] = True
        if random.randint(0, ytd) < .6:
            left_play["short"] = True
            right_play["short"] = True
            middle_play["short"] = True
    else:
        left_play["run"] = True
        right_play["run"] = True
        middle_play["run"] = True
    play = offense.choose(left_play, middle_play, right_play)
    # start of all left plays




    if play["direction"] == "left":
        # start of left pass plays
        if play["pass"] == True:
            if play["short"] == True:  # short left  pass
                payoff = random.randint(-5, 10)  # moderate risk payoff
                offense.respond(payoff * t)
                if payoff > 0:  # forward movement
                    ytd = ytd - payoff
                    distance = distance + payoff
                    if ytd > 0:
                        return f_down, distance, down, ytd, f_down_bool
                    else: # first down achieved
                        f_down[down] += 1
                        f_down_bool = True
                        return f_down, distance, down, ytd, f_down_bool
                else:   # negative forward movement
                    ytd = ytd + abs(payoff)  # if the first down has not occurred, the payoff is taken from the yards to first down
                    distance = distance + payoff  # distance on the field
                    return f_down, distance, down, ytd, f_down_bool

            else:  # long left  pass
                payoff = random.randint(-15, 10)  # higher risk payoff
                offense.respond(payoff * t)
                distance = distance + payoff
                if payoff > 0:
                    ytd = ytd - payoff
                    distance = distance + payoff
                    if ytd > 0:
                        return f_down, distance, down, ytd
                    else:
                        f_down[down] += 1
                        f_down_bool = True
                        return f_down, distance, down, ytd, f_down_bool
                else:
                    ytd = ytd + abs(payoff)  # if the first down has not occurred, the payoff is taken from the yards to first down
                    distance = distance + payoff  # distance on the field
                    return f_down, distance, down, ytd

        # start of left side rush plays
        else:
            payoff = random.randint(-2, 7)  # lower risk payoff
            offense.respond(payoff + t)
            if payoff > 0:
                ytd = ytd - payoff
                distance = distance + payoff
                if ytd > 0:
                    return f_down, distance, down, ytd
                else:
                    f_down[down] += 1
                    f_down_bool = True
                    return f_down, distance, down, ytd, f_down_bool
            else:
                ytd = ytd + abs(payoff)  # if the first down has not occurred, the payoff is taken from the yards to first down
                distance = distance + payoff  # distance on the field
                return f_down, distance, down, ytd
    # start of all right plays




    if play["direction"] == "middle":
        # start of middle  pass plays
        if play["pass"] == True:
            if play["short"] == True:  # short left  pass
                payoff = random.randint(-5, 10)  # moderate risk payoff
                offense.respond(payoff * t)
                if payoff > 0:
                    ytd = ytd - payoff
                    distance = distance + payoff
                    if ytd != 0:
                        return f_down, distance, down, ytd
                    else:
                        f_down[down] += 1
                        f_down_bool = True
                        return f_down, distance, down, ytd, f_down_bool
                else:
                    ytd = ytd + abs(payoff)  # if the first down has not occurred, the payoff is taken from the yards to first down
                    distance = distance + payoff  # distance on the field
                    return f_down, distance, down, ytd
            else:  # long left  pass
                payoff = random.randint(-15, 10)  # higher risk payoff
                offense.respond(payoff * t)
                distance = distance + payoff
                if payoff > 0:
                    ytd = ytd - payoff
                    distance = distance + payoff
                    if ytd != 0:
                        return f_down, distance, down, ytd
                    else:
                        f_down[down] += 1
                        f_down_bool = True
                        return f_down, distance, down, ytd, f_down_bool
                else:
                    ytd = ytd + abs(payoff)  # if the first down has not occurred, the payoff is taken from the yards to first down
                    distance = distance + payoff  # distance on the field
                    return f_down, distance, down, ytd
        # start of middle rush plays
        else:
            payoff = random.randint(-2, 7)  # lower risk payoff
            offense.respond(payoff * t)
            if payoff > 0:
                ytd = ytd - payoff
                distance = distance + payoff
                if ytd != 0:
                    return f_down, distance, down, ytd
                else:
                    f_down[down] += 1
                    f_down_bool = True
                    return f_down, distance, down, ytd, f_down_bool
            else:
                ytd = ytd + abs(payoff) # if the first down has not occurred, the payoff is taken from the yards to first down
                distance = distance + payoff  # distance on the field
                return f_down, distance, down, ytd






    if play["direction"] == "right":
        # start of left pass plays
        if play["pass"] == True:
            if play["short"] == True:  # short left  pass
                payoff = random.randint(-5, 10)  # moderate risk payoff
                offense.respond(payoff * t)
                if payoff > 0:
                    ytd = ytd - payoff
                    distance = distance + payoff
                    if ytd != 0:
                        return f_down, distance, down, ytd
                    else:
                        f_down[down] += 1
                        f_down_bool = True
                        return f_down, distance, down, ytd, f_down_bool
                else:
                    ytd = ytd + abs(payoff)  # if the first down has not occurred, the payoff is taken from the yards to first down
                    distance = distance + payoff  # distance on the field
                    down += 1
                    return f_down, distance, down, ytd
            else:  # long left  pass
                payoff = random.randint(-15, 10)  # higher risk payoff
                offense.respond(payoff * t)
                distance = distance + payoff
                if payoff > 0:
                    ytd = ytd - payoff
                    distance = distance + payoff
                    if ytd != 0:
                        return f_down, distance, down, ytd
                    else:
                        f_down[down] += 1
                        f_down_bool = True
                        return f_down, distance, down, ytd, f_down_bool
                else:
                    ytd = ytd + abs(payoff)  # if the first down has not occurred, the payoff is taken from the yards to first down
                    distance = distance + payoff  # distance on the field
                    down += 1
                    return f_down, distance, down, ytd
        # start of left side rush plays
        else:
            payoff = random.randint(-2, 7)  # lower risk payoff
            offense.respond(payoff * t)
            if payoff > 0:
                ytd = ytd - payoff
                distance = distance + payoff
                if ytd != 0:
                    return f_down, distance, down, ytd
                else:
                    f_down[down] += 1
                    f_down_bool = True
                    return f_down, distance, down, ytd, f_down_bool
            else:
                ytd = ytd + abs(payoff)  # if the first down has not occurred, the payoff is taken from the yards to first down
                distance = distance + payoff  # distance on the field
                down += 1
                return f_down, distance, down, ytd

