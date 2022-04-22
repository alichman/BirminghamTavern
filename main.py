# Card Game program by Andrew Lichmanov
# Game: Birmingham Tavern
# Concept: Two players select avatars, known as Lads, who will proceed to compliment each other.
#           Lads will have different characteristics, that would be more susceptible to compliments.
#           Once a Lad's Flattered metre reaches maximum, they will accept the compliment, and respectfully
#           forfeit the game.
# Personality consultant: Carolinne

import random

class Lad:
    def __init__(self,name,kind):
        self.name = name
        self.kind = kind
        self.fMeter = 0 #out of 100
    def get_compliments(self):
