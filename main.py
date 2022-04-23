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


class Lad:
    ladTypes = ['bus_', 'col_', 'bar_', 'sci_', 'art_']

    def __init__(self, name, kind):
        self.name = name
        self.kind = Lad.ladTypes[kind]
        self.fMeter = 0  # out of 100

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

    def Compliment(self, subject):
        if subject in self.Compliments[0]:
            self.fMeter += round(30 - 3.75 * self.Compliments[0].index(subject))
            self.Compliments[0].remove(subject)
        elif subject in self.Compliments[1]:
            if self.fMeter - round(self.Compliments[1].index(subject) * 3.75) > 0:
                self.fMeter -= round(self.Compliments[1].index(subject) * 3.75)
                if self.fMeter >= 100:
                    return [1,self.Lines[1]]
            else:
                self.fMeter = 0

            if subject == self.Compliments[1][-1]:
                self.fMeter = -1
                return [-1,self.Lines[3]]
            self.Compliments[1].remove(subject)
        else:
            return -2


All_Subjects = ['Looks', 'Craft', 'Lifestyle', 'Vibe', 'Mindset']
All_Compliments = {"Looks": ['Teeth', 'Hair', 'Eyes'], "Craft": ['Skill', 'Creativity'],
                   "Lifestyle": ['Wealth', 'Health', 'Life', 'Social'],
                   "Vibe": ['Personality', 'GenVibe'], "Mindset": ['Intel', 'Aspiration']}

A = Lad(input("Player 1: \nSelect Lad Name:\n"), int(input("Select Lad Type \n1: Business, 2: College Student, "
                                                           "3: Bartender, 4:Scientist, 5: Artist :\n")) - 1)

while True:
    print("Select complement subject")
    for i in range(5):
        print(f"{i+1}: {All_Subjects[i]}")
    compSubject = random.choice(All_Compliments[All_Subjects[int(input())-1]])
    print('subject: ', compSubject)
    resultA = A.Compliment(compSubject)
    print(A)
    try:
        print(resultA[1])
    except TypeError:
        print('nothing yet')