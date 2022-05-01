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
# Graphics consultants: Carolinne, Lauren

import random
from pygame import *


class Lad:
    ladTypes = ['bus_', 'col_', 'bar_', 'sci_', 'art_']

    def __init__(self, name, kind, side):
        self.name = name
        self.kind = Lad.ladTypes[kind]
        self.fMeter = 0  # out of 100
        self.side = 0

        self.All_Compliments = {"Looks": ['Teeth', 'Hair', 'Eyes'],
                                "Craft": ['Skill', 'Creativity'],
                                "Lifestyle": ['Wealth', 'Health', 'Life', 'Social'],
                                "Vibe": ['Personality', 'GenVibe'],
                                "Mindset": ['Intel', 'Aspiration']}

        self.fileName = f"Characters/{self.kind}{random.randint(1, 3)}.txt"
        file = open(self.fileName, 'r')
        self.dataLines = file.readlines()
        for Line in range(len(self.dataLines) - 1):
            self.dataLines[Line] = self.dataLines[Line].strip()
        self.image = image.load("images/" + self.dataLines[0])
        self.Compliments = [self.dataLines[1].split(), self.dataLines[2].split()]
        self.Lines = [self.dataLines[i].split('~') for i in range(3, 7)]
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

    def drawCharacter(self):
        win.blit(self.image, (320, -5))

    def drawOptions(self):
        for i, j in enumerate(self.getOptions()):
            win.blit(btn, (30 + i * 80, 270))
            win.blit(text.render(j, True, (0, 0, 0)), (35 + i * 80 + (10 - len(j)) * 2, 277))

    def checkClick(self, mPos):
        if 270 <= mPos[1] <= 292:
            for i in range(len(self.getOptions())):
                if 30 + i * 80 <= mPos[0] <= 105 + i * 80:
                    return i
            return None

    def drawBar(self):
        win.blit(bar, (5, 30))
        BARPOS = int(234 * self.fMeter / 100)
        draw.rect(win, (240, 194, 96), Rect(11, 269 - BARPOS, 7, BARPOS))

    def Compliment(self, Sub):
        All_Subjects = self.getOptions()
        subject = random.choice(self.All_Compliments[All_Subjects[Sub]])
        print('subject: ', subject)

        if subject in self.Compliments[0]:
            self.fMeter += round(30 - 3.75 * self.Compliments[0].index(subject))

            if self.fMeter >= 100:
                return [1, self.Lines[2]]
            else:
                status = [0, None]

            self.Compliments[0].remove(subject)
        else:
            self.fMeter -= round(self.Compliments[1].index(subject) * 6)
            if self.fMeter < 0:
                self.fMeter = 0

            if subject == self.Compliments[1][-1]:
                self.fMeter = -1
                status = [-1, self.Lines[3]]
            else:
                status = [0, None]

            self.Compliments[1].remove(subject)

        for sect in list(self.All_Compliments.keys()):
            if subject in self.All_Compliments[sect]:
                print("+++++ IN HERE")
                print(self.All_Compliments[sect])
                self.All_Compliments[sect].remove(subject)
                print(self.All_Compliments[sect])
                print('flatter: ', self.fMeter)
                print('DONE')
                break
        return status


class BG:
    def __init__(self):
        self.frame = 0
        self.images = [image.load(f'BG/{i}.png') for i in range(12)]

    def draw(self):
        win.blit(self.images[self.frame // 2], (0, 0))
        self.frame += 1
        if self.frame == 24:
            self.frame = 0


def writeSpeech(Text, Iter, speak, Coord=(210,260)):
    win.blit(text.render(speak + ' :', True, (0, 0, 0)), (210, 240))

    cX, cY = Coord
    if Iter is None:
        win.blit(text.render(Text[0], True, (0, 0, 0)), (cX, cY))
        win.blit(text.render(Text[1], True, (0, 0, 0)), (cX, cY + 10))
        win.blit(text.render(Text[2], True, (0, 0, 0)), (cX, cY + 20))
        return None

    if Iter < len(Text[0]):
        win.blit(text.render(Text[0][0:Iter], True, (0, 0, 0)), (cX, cY))
    elif Iter < len(Text[1]+Text[0]):
        win.blit(text.render(Text[0], True, (0, 0, 0)), (cX, cY))
        win.blit(text.render(Text[1][0:Iter-len(Text[0])], True, (0, 0, 0)), (cX, cY+10))
    elif Iter < len(Text[0]+Text[1]+Text[2]):
        win.blit(text.render(Text[0], True, (0, 0, 0)), (cX, cY))
        win.blit(text.render(Text[1], True, (0, 0, 0)), (cX, cY+10))
        win.blit(text.render(Text[2][0:Iter - len(Text[0]+Text[1])], True, (0, 0, 0)), (cX, cY + 20))

    elif Iter >= len(Text[0]+Text[1]+Text[2]):
        return None
    return Iter + 1


P = [Lad(input("Player 1: \nSelect Lad Name:\n"),
         int(input("Select Lad Type \n1: Business, "
                   "2: College Student, "
                   "3: Bartender, "
                   "4:Scientist, "
                   "5: Artist :\n")) - 1, 0) for i in range(1)]

cP = 0
waitFrame = 0

init()
win = display.set_mode((640, 314))
btn = image.load('images/btn.png')
bar = image.load('images/bar.png')
text = font.Font("FONT.ttf", 6)
box = image.load('images/tBox.png')
Clock = time.Clock()
bg = BG()

f = open('genLines/good.txt', 'r')
Good_Lines = [i for i in f.readlines()]
f.close()

f = open('genLines/bad.txt', 'r')
Bad_Lines = [i for i in f.readlines()]
f.close()

# INTRODUCTION PHASE
step = 0
while True:
    if step is None:
        waitFrame += 1
        if waitFrame == 24:
            break
    bg.draw()
    P[cP].drawCharacter()
    win.blit(box, (190, 230))
    step = writeSpeech(P[cP].Lines[0], step, P[cP].name)

    for Event in event.get():
        if Event.type == QUIT:
            quit()

    display.update()
    Clock.tick(12)




# GAME PHASE
while True:
    bg.draw()
    P[cP].drawCharacter()
    P[cP].drawOptions()
    P[cP].drawBar()
    for Event in event.get():
        if Event.type == QUIT:
            quit()
        elif Event.type == MOUSEBUTTONUP:
            sub = P[cP].checkClick(mouse.get_pos())
            if sub is not None:
                result = P[cP].Compliment(sub)

    display.update()
    Clock.tick(12)

