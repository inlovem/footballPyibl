import pyibl
import numpy as np
import pandas as pd
import matplotlib as plt


DEFAULT_UTILITY = 30
NOISE = 0.25
DECAY = 0.5
TEMPERATURE = 0
games = 160
plays = 60
time = 60
time_to_end = time - p

defaultout = "football_data.csv"
offense = pyibl.Agent("Offense Agent", ["direction", "pass", "short"], default_utility=DEFAULT_UTILITY, decay=DECAY, noise=NOISE)
#defense = pyibl.Agent("Defense Agent", [""])
left_play = {"direction": "left", "pass": False, "short": False}
right_play = {"direction": "right", "pass": False, "short": False}
middle_play = {"direction": "middle", "pass": False, "short": False}


def reset_agent(a, noise=NOISE, decay = DECAY):
    a.reset(False)
    a.noise = noise
    a.decay = decay



def run():


    for g in range(games):
        reset_agent(offense)
        #reset_agent(defense)
        offense.trace = True
        #defense.trace = True

        for p in range(plays):
            offense_play = offense.choose()
            #defense_play = defense.choose("")

