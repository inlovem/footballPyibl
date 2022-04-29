
import pyibl
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


DEFAULT_UTILITY = 30
NOISE = 0.25
DECAY = 0.5
PARTICIPANTS = 200
TRIALS = 500
attacker = pyibl.Agent(default_utility=DEFAULT_UTILITY, noise=NOISE, decay=.05)
defender = pyibl.Agent(default_utility=DEFAULT_UTILITY, noise=NOISE, decay= 5)


def run(trials, participants):
    attack_action = [0] * trials
    defend_action = [0] * trials

    for p in range(participants):
        attacker.reset()
        defender.reset()
        for t in range(trials):
            option1 = attacker.choose("attack", "not attack")
            option2 = defender.choose("defend", "not defend")
            if option1 == "attack":
                if option2 == "defend":
                    attack_action[t]+=1
                    defend_action[t]+=1
                    attacker.respond(-5)
                    defender.respond(5)
                else:
                    attack_action[t]+=1
                    attacker.respond(10)
                    defender.respond(-15)
            else:
                if option2 == "defend":
                    defend_action[t]+=1
                    attacker.respond(0)
                    defender.respond(-5)
                else:
                    attacker.respond(0)
                    defender.respond(0)
    plt.plot([n / participants for n in attack_action], label='attack')
    plt.plot([m / participants for m in defend_action], label='defend')
    plt.ylim([0, 1])
    plt.xlim([0, TRIALS + 1])
    plt.ylabel("probability of action")
    plt.xlabel("trials")
    plt.legend()
    plt.show()

def main():
    run(TRIALS, PARTICIPANTS)


if __name__ == '__main__':
    main()



