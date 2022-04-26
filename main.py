# Card Game program by Andrew Lichmanov
# Game: Birmingham Tavern
# Concept: Two players select avatars, known as Lads, who will proceed to compliment each other.
#           Lads will have different characteristics, that would be more susceptible to compliments.
#           Once a Lad's Flattered metre reaches maximum, they will accept the compliment, and respectfully
#           forfeit the game.
# Mechanics: Each Lad has weak and strong compliments, as well as a Lose-Condition game-ending compliment.
#            Selecting the Lose-Condition makes the complimenting lad to lose the game.
#            For all other compliments, the Lad will be flattered based on the compliment's ranking
#            in the Lad's text file
# Personality consultant: Carolinne

import random
from tkinter import *
from PIL import Image, ImageTk


class Lad:
    ladTypes = ['bus_', 'col_', 'bar_', 'sci_', 'art_']

    def __init__(self, name, kind):
        self.name = name
        self.kind = Lad.ladTypes[kind]
        self.fMeter = 0  # out of 100

        self.All_Compliments = {"Looks": ['Teeth', 'Hair', 'Eyes'],
                                "Craft": ['Skill', 'Creativity'],
                                "Lifestyle": ['Wealth', 'Health', 'Life', 'Social'],
                                "Vibe": ['Personality', 'GenVibe'],
                                "Mindset": ['Intel', 'Aspiration']}

        self.fileName = f"Characters\{self.kind}{random.randint(1, 3)}.txt"
        file = open(self.fileName, 'r')
        self.dataLines = file.readlines()
        for Line in range(len(self.dataLines) - 1):
            self.dataLines[Line] = self.dataLines[Line].strip()
        self.image = self.dataLines[0]
        self.Compliments = [self.dataLines[1].split(), self.dataLines[2].split()]
        self.Lines = [self.dataLines[i] for i in range(3, 7)]
        file.close()

    def __str__(self):
        return f'File: {self.fileName}, Flatter: {self.fMeter}, \nCompliments: {self.Compliments}'

    def getKind(self):
        typeNames = ['Businessperson', 'College Student', 'Bartender', 'Scientist', 'Artist']
        return typeNames[Lad.ladTypes.index(self.kind)]

    def getOptions(self):
        toDel = []
        for sect in self.All_Compliments.keys():
            if not self.All_Compliments[sect]:
                toDel.append(sect)
        for item in toDel:
            self.All_Compliments.pop(item, None)
        return list(self.All_Compliments.keys())

    def Compliment(self):
        All_Subjects = A.getOptions()
        print("Select complement subject")
        for i, j in enumerate(All_Subjects):
            print(f"{i + 1}: {j}")
        subject = random.choice(self.All_Compliments[All_Subjects[int(input()) - 1]])
        print('subject: ', subject)

        if subject in self.Compliments[0]:
            self.fMeter += round(30 - 3.75 * self.Compliments[0].index(subject))

            if self.fMeter >= 100:
                return [1, self.Lines[2]]
            else:
                result = [0, None]

            self.Compliments[0].remove(subject)
        else:
            self.fMeter -= round(self.Compliments[1].index(subject) * 6)
            if self.fMeter < 0:
                self.fMeter = 0

            if subject == self.Compliments[1][-1]:
                self.fMeter = -1
                result = [-1, self.Lines[3]]
            else:
                result = [0, None]

            self.Compliments[1].remove(subject)

        for sect in list(self.All_Compliments.keys()):
            print(sect)
            if subject in self.All_Compliments[sect]:
                print("+++++ IN HERE")
                print(self.All_Compliments[sect])
                self.All_Compliments[sect].remove(subject)
                print(self.All_Compliments[sect])
                print('DONE')
                break
        return result


window = Tk()

A = Lad(input("Player 1: \nSelect Lad Name:\n"), int(input("Select Lad Type \n1: Business, 2: College Student, "
                                                           "3: Bartender, 4:Scientist, 5: Artist :\n")) - 1)

while True:
    print(A)
    resultA = A.Compliment()
    if resultA[0] == 1:
        print(A.fMeter, '\n')
        print(resultA[1])
        break
    elif resultA[0] == -1:
        print(A.fMeter, '\n')
        print(resultA[1])
        break
window.mainloop()
