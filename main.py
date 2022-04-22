# Card Game program by Andrew Lichmanov
# Game: Birmingham Tavern
# Concept: Two players select avatars, known as Lads, who will proceed to compliment each other.
#           Lads will have different characteristics, that would be more susceptible to compliments.
#           Once a Lad's Flattered metre reaches maximum, they will accept the compliment, and respectfully
#           forfeit the game.
# Personality consultant: Carolinne

import random


class Lad:
    ladTypes = ['bus_', 'col_', 'bar_', 'sci_', 'art_']

    def __init__(self, name, kind):
        self.name = name
        self.kind = Lad.ladTypes[kind]
        self.fMeter = 0  # out of 100

        self.fileName = f"Characters\{self.kind}{random.randint(1, 3)}.txt"
        file = open(self.fileName, 'r')
        self.dataLines = file.readlines()
        for Line in range(len(self.dataLines)-1):
            self.dataLines[Line] = self.dataLines[Line][:-2]
        self.image = self.dataLines[0]
        self.Compliments = [' '.split(self.dataLines[1]), ' '.split(self.dataLines[2])]
        self.Lines = [self.dataLines[i] for i in range(3, 7)]
        file.close()

    def __str__(self):
        return str([self.fileName, self.Lines])

    def getCompliment(self,subject):
        if subject in self.Compliments[0]:
            self.fMeter += round(30 - 3.75*self.Compliments.index(subject))
            self.Compliments[0].remove(subject)
        elif subject in self.Compliments[1]:
            self.fMeter -= round(self.Compliments.index(subject)*3.75 - 30)
            if subject == self.Compliments[1][-1]:
                self.fMeter = -1
            self.Compliments[0].remove(subject)
        else:
            return False


A = Lad("Bobby", 1)