import random

import pyibl
import numpy as np
import pandas as pd
import matplotlib as plt


DEFAULT_UTILITY = 30
NOISE = 0.25
DECAY = 0.5
TEMPERATURE = 0
GAMES = 6
plays = 6
DOWN = 1
DISTANCE = 40
payoff = 0
YTD = 10
TIME = 60


DefaultOut = "football_data.csv"

left_play = {"direction": "left", "pass_forward": False, "run_forward": False, "short": False}
right_play = {"direction": "right", "pass_forward": False, "run_forward": False, "short": False}  # least risky
middle_play = {"direction": "middle", "pass_forward": False, "run_forward": False, "short": False}
offense = pyibl.Agent("Offense Agent", ["direction", "pass_forward", "short"], default_utility=DEFAULT_UTILITY,
                      decay=DECAY, noise=NOISE)

def reset_agent(a, noise=NOISE, decay=DECAY):
    a.reset(False)
    a.noise = noise
    a.decay = decay



def run_play(distance = DISTANCE, down = DOWN, ytd = YTD, time = TIME, f_down_bool = False, output_file = DefaultOut):




   # with open(output_file, "w") as f:
        #print("Games,Time,Selected,Warning,Covered,Action,Outcome,Cumulative", file=f)

        for g in range(GAMES):
            reset_agent(offense)


            f_down = [0] * GAMES
            #offense.trace = True
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
                                ytd = 10
                                break
                    # lower yards to touchdown but defense is compact and has lowest space to cover
                    elif distance in range(90, 100):
                        for down in range(4):
                            down_plays(f_down, t, distance, down, ytd, f_down_bool)

                            if f_down_bool == True:
                                ytd = 10
                                break

                    elif distance > 100:
                            distance = DISTANCE

                else: # higher risk time in game
                    if distance in range(30, 70):  # low risk location
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
                                ytd = 10
                                break
                    elif distance in range(90, 100):
                        for down in range(4):
                            down_plays(f_down, t, distance, down, ytd, f_down_bool)
                            if f_down_bool == True:
                                ytd = 10
                                break
                    elif distance > 100:
                            distance = DISTANCE
        
        

        #plt.plot([n / participants for n in attack_action], label='attack')
        #plt.plot([m / participants for m in defend_action], label='defend')
        #plt.ylim([0, 1])
        #plt.xlim([0, TRIALS + 1])
        #plt.ylabel("probability of action")
        #plt.xlabel("trials")
        #plt.legend()
        #plt.show()

                    #print(f"{g + 1},{t + 1},{selected},{int(warned)}, {int(covered)},{int(attack)}, {payoff}, {total}",file=f)

   # return {"covered": (covered_attack / (GAMES * TIME)), "uncovered":(uncovered_attack / (GAMES * TIME)), "withdraw": (withdraw / (GAMES * TIME))}







def down_plays(f_down, t, distance, down, ytd, f_down_bool = False):
    # figure out likelihoods of pass to run in time and distance
    if random.randint(0, 1) < .6:
        left_play["pass_forward"] = True
        right_play["pass_forward"] = True
        middle_play["pass_forward"] = True
        if random.randint(0, ytd) < .7:
            left_play["short"] = True
            right_play["short"] = True
            middle_play["short"] = True
    else:
        left_play["run_forward"] = True
        right_play["run_forward"] = True
        middle_play["run_forward"] = True
    play = offense.choose(left_play, middle_play, right_play)
    # start of all left plays




    if play["direction"] == "left":
        # start of left pass plays
        if play["pass_forward"] == True:
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
        # start of middle pass plays
        if play["pass_forward"] == True:
            if play["short"] == True:  # short left  pass
                payoff = random.randint(-10, 10)  # moderate risk payoff
                offense.respond(payoff * t)
                if payoff > 0:  # forward movement
                    ytd = ytd - payoff
                    distance = distance + payoff
                    if ytd > 0:
                        return f_down, distance, down, ytd, f_down_bool
                    else:  # first down achieved
                        f_down[down] += 1
                        f_down_bool = True
                        return f_down, distance, down, ytd, f_down_bool
                else:  # negative forward movement
                    ytd = ytd + abs(
                        payoff)  # if the first down has not occurred, the payoff is taken from the yards to first down
                    distance = distance + payoff  # distance on the field
                    return f_down, distance, down, ytd, f_down_bool

            else:  # long middle pass
                payoff = random.randint(-25, 10)  # higher risk payoff
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
                    ytd = ytd + abs(
                        payoff)  # if the first down has not occurred, the payoff is taken from the yards to first down
                    distance = distance + payoff  # distance on the field
                    return f_down, distance, down, ytd

        # start of middle side rush plays
        else:
            payoff = random.randint(-2, 4)  # lower risk payoff
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
                ytd = ytd + abs(
                    payoff)  # if the first down has not occurred, the payoff is taken from the yards to first down
                distance = distance + payoff  # distance on the field
                return f_down, distance, down, ytd



    # start of all right plays

    if play["direction"] == "right":
        # start of right pass plays
        if play["pass_forward"] == True:
            if play["short"] == True:  # short left  pass
                payoff = random.randint(-2, 10)  # moderate risk payoff
                offense.respond(payoff * t)
                if payoff > 0:  # forward movement
                    ytd = ytd - payoff
                    distance = distance + payoff
                    if ytd > 0:
                        return f_down, distance, down, ytd, f_down_bool
                    else:  # first down achieved
                        f_down[down] += 1
                        f_down_bool = True
                        return f_down, distance, down, ytd, f_down_bool
                else:  # negative forward movement
                    ytd = ytd + abs(
                        payoff)  # if the first down has not occurred, the payoff is taken from the yards to first down
                    distance = distance + payoff  # distance on the field
                    return f_down, distance, down, ytd, f_down_bool

            else:  # long right  pass
                payoff = random.randint(-15, 15)  # higher risk payoff
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
                    ytd = ytd + abs(
                        payoff)  # if the first down has not occurred, the payoff is taken from the yards to first down
                    distance = distance + payoff  # distance on the field
                    return f_down, distance, down, ytd

        # start of right side rush plays
        else:
            payoff = random.randint(-2, 10)  # lower risk payoff
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
                ytd = ytd + abs(
                    payoff)  # if the first down has not occurred, the payoff is taken from the yards to first down
                distance = distance + payoff  # distance on the field
                return f_down, distance, down, ytd




print(run_play())
    #df = pd.read_csv("football_data.csv")
    #print(df)
    #print(data)
    #action = list(data.keys())
    #values = list(data.values())
    #fig = plt.figure(figsize=(100, 100))  # may need to reset based on output size
    #plt.bar(action, values, width=0.2, color=['red', 'green', 'blue', 'yellow'])
    #plt.ylim([0.0, 100])
    #plt.ylable('unknown')
    #plt.xlable('unknown')
    #plt.legend()
    #plt.show()

