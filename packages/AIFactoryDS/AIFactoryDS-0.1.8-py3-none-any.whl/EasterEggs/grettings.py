import random


def how_are_you():
    status = random.random()
    if status < 0.3:
        print("Good :)")
    elif status < 0.6:
        print("I'm alright")
    else:
        print("Let... let me go home...")