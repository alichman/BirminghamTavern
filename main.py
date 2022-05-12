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
# Personality consultants: Carolinne, Iza, Danell, Olivia, Levente, Holly
# Graphics consultants: Carolinne, Lauren, Levente

import random
from pygame import *


# Class that contains the majority of code in it. Instantiated for each player.
class Lad:
    # class var for file names.
    ladTypes = ['bus_', 'col_', 'bar_', 'sci_', 'art_']

    # Initializes all the values for each lad
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

        # FILE READING SECTION - extracts character data from designated file
        # Cheat code (Easter egg) to guarantee Artist_1 character
        if self.kind == 'art_' and self.name == 'Karen':
            self.fileName = f"Characters/art_1.txt"
        else:
            # Selects random character from 3 in each category
            self.fileName = f"Characters/{self.kind}{random.randint(1, 3)}.txt"

        file = open(self.fileName, 'r')
        self.dataLines = file.readlines()

        # Makes data more usable
        for Line in range(len(self.dataLines) - 1):
            self.dataLines[Line] = self.dataLines[Line].strip()

        # Unnecessary split, intended for later use with custom voices
        firstVals = self.dataLines[0].split()
        self.image = image.load("images/" + firstVals[0])
        # self.sound = firstVals[1] - will be added later
        # Flips image if needed
        if self.side:
            self.image = transform.flip(self.image, True, False)
        self.Compliments = [self.dataLines[1].split(), self.dataLines[2].split()]
        self.Lines = [self.dataLines[i] for i in range(3, 7)]
        file.close()

    # Clears empty dictionary keys, returns list of remaining keys
    def getOptions(self):
        toDel = []
        for sect in self.All_Compliments.keys():
            if not self.All_Compliments[sect]:
                toDel.append(sect)
        for item in toDel:
            self.All_Compliments.pop(item, None)
        return list(self.All_Compliments.keys())

    # Draws character image, considering its side
    def drawCharacter(self):
        if not self.side:
            win.blit(self.image, (320, -5))
        else:
            win.blit(self.image, (0, -5))

    # Draws buttons for each available category of compliment
    def drawOptions(self):
        offset = 30 + self.side * 180
        for i, j in enumerate(self.getOptions()):
            win.blit(btn, (offset + i * 80, 270))
            win.blit(text.render(j, True, (0, 0, 0)), (offset + 5 + i * 80 + (10 - len(j)) * 2, 277))

    # Receives position of mouse on clicks, returns what button was pressed, if any
    def checkClick(self, mPos):
        offset = 30 + self.side * 180
        if 270 <= mPos[1] <= 292:
            for i in range(len(self.getOptions())):
                if offset + i * 80 <= mPos[0] <= offset + 75 + i * 80:
                    return i
            return None

    # Draws flatter bar shell and flatter bar
    def drawBar(self):
        if self.side:
            x = 620
        else:
            x = 5
        BARPOS = int(234 * self.fMeter / 100)
        win.blit(bar, (x, 30))
        draw.rect(win, (240, 194, 96), Rect(x + 6, 269 - BARPOS, 7, BARPOS))

    # Line can be str or int. Receives code for line to say, and side to display the message. Default is self.side
    def sayLine(self, line, side=None):
        if side is None:
            side = self.side
    # Line is encoded as follows:
        # If line is an int, positive lines are included in the txt file, and negatives are default responses
        # If line is a str, all possible lines are in the designated file in genLines
        if type(line) == int:
            if line >= 0:
                Line = self.Lines[line]
            else:
                Line = [random.choice(Good_Lines), random.choice(Bad_Lines)][line]
        else:
            f = open(f"genLines/{line}.txt")
            Line = random.choice(f.readlines())
            f.close()

        # Begin Text Phase
        step = 0
        waitFrame = 0
        while True:
            # Waiting after text is finished
            if step is None:
                waitFrame += 1
                if waitFrame == 24:
                    break
            # Draw everything
            bg.draw()
            P[cP].drawBar()
            P[cP].drawCharacter()

            # Call writeSpeech
            if side:
                Coord = (265, 260)
            else:
                Coord = (100, 260)
            step = writeSpeech(Line, step, self.name, Coord, None)

            # Standard quit even and Dialog Skip
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

    # Receives category for compliment, chooses random subject and evals score gained. Returns status code and response.
    def Compliment(self, Sub):
        All_Subjects = self.getOptions()
        subject = random.choice(self.All_Compliments[All_Subjects[Sub]])
        print('subject: ', subject)
        P[1 - cP].sayLine(subject, self.side)

        # If sub is a good compliment, gain score based on how recent it is in the list
        if subject in self.Compliments[0]:
            self.fMeter += round(30 - 3.75 * self.Compliments[0].index(subject))

            # If win conditions are met, return win code
            if self.fMeter >= 100:
                status = 2
            else:
                status = 1
            # Prevents repetition by removing used subjects
            self.Compliments[0].remove(subject)
        # If sub is a bad compliment, lose score based on how recent it is in the list
        else:
            self.fMeter -= round(self.Compliments[1].index(subject) * 6)
            if self.fMeter < 0:
                self.fMeter = 0
            # If lose condition is selected, return lose code
            if subject == self.Compliments[1][-1]:
                self.fMeter = -1
                status = -2
            else:
                status = -1
            # Prevents repetition by removing used subjects
            self.Compliments[1].remove(subject)
        # Removes subject from main dictionary
        for sect in list(self.All_Compliments.keys()):
            if subject in self.All_Compliments[sect]:
                self.All_Compliments[sect].remove(subject)
                break
        return status


# Class BackGround - simplifies animating the GIF and keeps track of the frames
class BG:
    def __init__(self, folder):
        self.frame = 0
        self.images = [image.load(f'{folder}/{i}.png') for i in range(12)]

    def draw(self):
        win.blit(self.images[self.frame // 2], (0, 0))
        self.frame += 1
        if self.frame == 24:
            self.frame = 0


# Global function for writing speech bubbles, mostly used for objects but initially made global
# Takes in text, iteration of text, speaker and coordinates (Sound is none for now)
# Function draws speech bubble, and iterates through text.
# Note: Due to iteration, manual enters must be made. The function supports exactly 3 lines.
def writeSpeech(Text, Iter, Speak, Coord, Sound):
    cX, cY = Coord
    win.blit(box, (cX - 20, cY - 30))
    win.blit(text.render(Speak + ' :', True, (0, 0, 0)), (cX, cY - 20))
    Text = Text.split('~')  # ~ is used as \n

    # If iteration is done, write all text.
    if Iter is None:
        win.blit(text.render(Text[0], True, (0, 0, 0)), (cX, cY))
        win.blit(text.render(Text[1], True, (0, 0, 0)), (cX, cY + 10))
        win.blit(text.render(Text[2], True, (0, 0, 0)), (cX, cY + 20))
        return None

    # Write lines
    if Iter < len(Text[0]):
        if Text[0][Iter].isalpha():
            speak.play()
        win.blit(text.render(Text[0][0:Iter], True, (0, 0, 0)), (cX, cY))
    elif Iter < len(Text[1] + Text[0]):
        if Text[1][Iter - len(Text[0])].isalpha():
            speak.play()
        win.blit(text.render(Text[0], True, (0, 0, 0)), (cX, cY))
        win.blit(text.render(Text[1][0:Iter - len(Text[0])], True, (0, 0, 0)), (cX, cY + 10))
    elif Iter < len(Text[0] + Text[1] + Text[2]):
        if Text[2][Iter - len(Text[1]) - len(Text[0])].isalpha():
            speak.play()
        win.blit(text.render(Text[0], True, (0, 0, 0)), (cX, cY))
        win.blit(text.render(Text[1], True, (0, 0, 0)), (cX, cY + 10))
        win.blit(text.render(Text[2][0:Iter - len(Text[0] + Text[1])], True, (0, 0, 0)), (cX, cY + 20))

    # If iteration is past the length of text, end iteration. Else, add 1
    elif Iter >= len(Text[0] + Text[1] + Text[2]):
        return None
    return Iter + 1


# Function to draw player indicator
def drawPlayer(p):
    x = 320 - 200 * p
    win.blit(pBox, (x, 10))
    win.blit(text.render(f'Your turn, Player {p + 1}', True, (0, 0, 0)), (x + 10, 15))


# Initialize all pygame values, and load images.
init()
win = display.set_mode((640, 314))
display.set_caption('Birmingham Tavern')
btn = image.load('images/btn.png')
bar = image.load('images/bar.png')
text = font.Font("FONT.ttf", 6)
box = image.load('images/tBox.png')
pBox = image.load('images/pBox.png')

# Create clock, sound and BG
speak = mixer.Sound('speak.wav')
Clock = time.Clock()
bg = BG('BG')
mn = BG('Menu')

# Prepare all good and bad responses
f = open('genLines/good.txt', 'r')
Good_Lines = [i for i in f.readlines()]
f.close()

f = open('genLines/bad.txt', 'r')
Bad_Lines = [i for i in f.readlines()]
f.close()

# MAIN MENU


MENU = True
while MENU:
    mn.draw()

    for Event in event.get():
        # Standard quit loop
        if Event.type == QUIT:
            quit()
        elif Event.type == MOUSEBUTTONUP:
            mouseX, mouseY = mouse.get_pos()
            if 400<mouseX<590 and 115<mouseY<310:
                MENU = False
    display.update()
    Clock.tick(12)

for i in range(24):
    win.fill((0,0,0))
    for Event in event.get():
        # Standard quit loop
        if Event.type == QUIT:
            quit()
    display.update()
    Clock.tick(12)

# CHAR SELECT PHASE

# Lad creating section (user input)
# Section ensures that lad_type is an int between 1 and 5
sil = image.load('images/sil.png')
P = []
for i in range(2):
    while True:
        bg.draw()
        win.blit(sil, (320*(1-i), -5))
        for i, j in enumerate(Lad.ladTypes):
            win.blit


cP = 0
P[0].sayLine(0)
cP = 1
P[1].sayLine(0)

# GAME PHASE
GAME = True
RESULT = None
while GAME:
    # Draw all relevant assets
    bg.draw()
    P[cP].drawCharacter()
    P[cP].drawOptions()
    P[cP].drawBar()
    drawPlayer(1 - cP)

    for Event in event.get():
        # Standard quit loop
        if Event.type == QUIT:
            quit()

        # Detects click, sends data to Lad objects, and acts on result.
        # Result data is encoded as follows:
            # -1 and 1 are standard bad and good results, causing a standard bad or good response;
            # -2 and 2 are losing and winning results, breaking the loop and moving on to next phase.
        elif Event.type == MOUSEBUTTONUP:
            sub = P[cP].checkClick(mouse.get_pos())
            if sub is not None:
                result = P[cP].Compliment(sub)
                if result == 1:
                    P[cP].sayLine(-2)
                elif result == -1:
                    P[cP].sayLine(-1)

                elif result == 2:
                    P[cP].sayLine(2)
                    cP = 1 - cP
                    P[cP].sayLine(1)
                    RESULT = (cP + 1, 1)
                    GAME = False
                elif result == -2:
                    P[cP].sayLine(3)
                    RESULT = (cP + 1, 2)
                    GAME = False
                cP = 1 - cP
    display.update()
    Clock.tick(12)

# Conclusion section
# load images based on result
msg = image.load(f'images/win{RESULT[0]}.png')
res = image.load(f'images/result{RESULT[1]}.png')
# Draws relevant assets, and closes on click
while True:
    bg.draw()
    win.blit(msg, (0, 0))
    win.blit(res, (0, 0))

    for Event in event.get():
        if Event.type == QUIT:
            quit()
        if Event.type == MOUSEBUTTONUP:
            quit()
    display.update()
    Clock.tick(12)
