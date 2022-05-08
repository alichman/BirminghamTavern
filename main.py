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
# Personality consultants: Carolinne, Iza, Danell, Olivia
# Graphics consultants: Carolinne, Lauren

import random
from pygame import *


class Lad:
    ladTypes = ['bus_', 'col_', 'bar_', 'sci_', 'art_']

    def __init__(self, name, kind, side):
        self.name = name
        self.kind = Lad.ladTypes[kind]
        self.fMeter = 0  # out of 100
        self.side = side  # 0 is R, 1 is L

        self.All_Compliments = {"Looks": ['Teeth', 'Hair', 'Eyes'],
                                "Craft": ['Skill', 'Creativity'],
                                "Lifestyle": ['Wealth', 'Health', 'Social'],
                                "Vibe": ['Personality', 'GenVibe'],
                                "Mindset": ['Intel', 'Aspiration']}
        if self.kind == 'art_' and self.name == 'Karen':
            self.fileName = f"Characters/art_1.txt"
        else:
            self.fileName = f"Characters/{self.kind}{random.randint(1, 3)}.txt"

        file = open(self.fileName, 'r')
        self.dataLines = file.readlines()

        for Line in range(len(self.dataLines) - 1):
            self.dataLines[Line] = self.dataLines[Line].strip()

        firstVals = self.dataLines[0].split()
        self.image = image.load("images/" + firstVals[0])
        self.sound = firstVals[1]
        if self.side:
            self.image = transform.flip(self.image, True, False)
        self.Compliments = [self.dataLines[1].split(), self.dataLines[2].split()]
        self.Lines = [self.dataLines[i] for i in range(3, 7)]
        file.close()

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
        if not self.side:
            win.blit(self.image, (320, -5))
        else:
            win.blit(self.image, (0, -5))

    def drawOptions(self):
        offset = 30 + self.side * 180
        for i, j in enumerate(self.getOptions()):
            win.blit(btn, (offset + i * 80, 270))
            win.blit(text.render(j, True, (0, 0, 0)), (offset + 5 + i * 80 + (10 - len(j)) * 2, 277))

    def checkClick(self, mPos):
        offset = 30 + self.side * 180
        if 270 <= mPos[1] <= 292:
            for i in range(len(self.getOptions())):
                if offset + i * 80 <= mPos[0] <= offset + 75 + i * 80:
                    return i
            return None

    def drawBar(self):
        if self.side:
            x = 620
        else:
            x = 5
        BARPOS = int(234 * self.fMeter / 100)
        win.blit(bar, (x, 30))
        draw.rect(win, (240, 194, 96), Rect(x + 6, 269 - BARPOS, 7, BARPOS))

    def sayLine(self, line, side=None):
        if side is None:
            side = self.side

        if type(line) == int:
            if line >= 0:
                Line = self.Lines[line]
            else:
                Line = [random.choice(Good_Lines), random.choice(Bad_Lines)][line]
        else:
            f = open(f"genLines/{line}.txt")
            Line = random.choice(f.readlines())
            f.close()

        step = 0
        waitFrame = 0
        while True:
            if step is None:
                waitFrame += 1
                if waitFrame == 24:
                    break
            bg.draw()
            P[cP].drawBar()
            P[cP].drawCharacter()
            if side:
                Coord = (265, 260)
            else:
                Coord = (100, 260)
            step = writeSpeech(Line, step, self.name, Coord, self.sound)

            for Event in event.get():
                if Event.type == QUIT:
                    quit()
                if Event.type == MOUSEBUTTONUP:
                    if step is None:
                        waitFrame = 23
                    else:
                        step = None

            display.update()
            Clock.tick(12)

    def Compliment(self, Sub):
        All_Subjects = self.getOptions()
        subject = random.choice(self.All_Compliments[All_Subjects[Sub]])
        print('subject: ', subject)
        P[1 - cP].sayLine(subject, self.side)

        if subject in self.Compliments[0]:
            self.fMeter += round(30 - 3.75 * self.Compliments[0].index(subject))

            if self.fMeter >= 100:
                status = [2, self.Lines[2]]
            else:
                status = [1, None]

            self.Compliments[0].remove(subject)
        else:
            self.fMeter -= round(self.Compliments[1].index(subject) * 6)
            if self.fMeter < 0:
                self.fMeter = 0

            if subject == self.Compliments[1][-1]:
                self.fMeter = -1
                status = [-2, self.Lines[3]]
            else:
                status = [-1, None]

            self.Compliments[1].remove(subject)

        for sect in list(self.All_Compliments.keys()):
            if subject in self.All_Compliments[sect]:
                self.All_Compliments[sect].remove(subject)
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


def writeSpeech(Text, Iter, Speak, Coord, Sound):
    cX, cY = Coord
    win.blit(box, (cX - 20, cY - 30))
    win.blit(text.render(Speak + ' :', True, (0, 0, 0)), (cX, cY - 20))
    Text = Text.split('~')

    if Iter is None:
        win.blit(text.render(Text[0], True, (0, 0, 0)), (cX, cY))
        win.blit(text.render(Text[1], True, (0, 0, 0)), (cX, cY + 10))
        win.blit(text.render(Text[2], True, (0, 0, 0)), (cX, cY + 20))
        return None

    if Iter < len(Text[0]):
        win.blit(text.render(Text[0][0:Iter], True, (0, 0, 0)), (cX, cY))
    elif Iter < len(Text[1] + Text[0]):
        win.blit(text.render(Text[0], True, (0, 0, 0)), (cX, cY))
        win.blit(text.render(Text[1][0:Iter - len(Text[0])], True, (0, 0, 0)), (cX, cY + 10))
    elif Iter < len(Text[0] + Text[1] + Text[2]):
        win.blit(text.render(Text[0], True, (0, 0, 0)), (cX, cY))
        win.blit(text.render(Text[1], True, (0, 0, 0)), (cX, cY + 10))
        win.blit(text.render(Text[2][0:Iter - len(Text[0] + Text[1])], True, (0, 0, 0)), (cX, cY + 20))

    elif Iter >= len(Text[0] + Text[1] + Text[2]):
        return None
    return Iter + 1


P = [Lad(input(f"Player {1 + i}: \nSelect Lad Name:\n"),
         int(input("Select Lad Type \n1: Business, "
                   "2: College Student, "
                   "3: Bartender, "
                   "4:Scientist, "
                   "5: Artist :\n")) - 1, i) for i in range(2)]

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
cP = 0
P[0].sayLine(0)
cP = 1
P[1].sayLine(0)

# GAME PHASE
GAME = True
while GAME:
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
                if result[0] == 1:
                    P[cP].sayLine(-2)
                elif result[0] == 2:
                    P[cP].sayLine(2)
                    cP = 1 - cP
                    P[cP].sayLine(1)
                    GAME = False
                elif result[0] == -1:
                    P[cP].sayLine(-1)
                elif result[0] == -2:
                    P[cP].sayLine(3)
                    GAME = False
                cP = 1 - cP

    display.update()
    Clock.tick(12)
