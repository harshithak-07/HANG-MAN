import pygame
import random
def draw_window():
    global guessed
    global hangmanPics
    global status
    win.fill(WHITE)
    pic = hangmanPics[status]
    win.blit(pic, (winWidth/2 - pic.get_width()/2 + 20, 150))
    
    for i in range(len(buttons)):
        if buttons[i][4]:
            pygame.draw.circle(win, BLACK, (buttons[i][1], buttons[i][2]), buttons[i][3])
            pygame.draw.circle(win, buttons[i][0], (buttons[i][1], buttons[i][2]), buttons[i][3] - 2)
            label = btn_font.render(chr(buttons[i][5]), 1, BLACK)
            win.blit(label, (buttons[i][1] - (label.get_width() / 2), buttons[i][2] - (label.get_height() / 2)))
    spaced = emptyspaces(word, guessed)
    label1 = guess_font.render(spaced, 1, BLACK)
    rect = label1.get_rect()
    length = rect[2]
    win.blit(label1,(winWidth/2 - length/2, 400))
    pygame.display.update()


def randomWord():
    file = open('/home/user/Desktop/words.txt')
    f = file.readlines()
    i = random.randrange(0, len(f) - 1)

    return f[i][:-1]

def hang(guess):
    global word
    if guess.lower() not in word.lower():
        return True
    else:
        return False


def emptyspaces(word, guessed=[]):
    guessedLetters = guessed
    for x in range(len(word)):
        if word[x] != ' ':
            spacedWord += '_ '
            for i in range(len(guessedLetters)):
                if word[x].upper() == guessedLetters[i]:
                    spacedWord = spacedWord[:-2]
                    spacedWord += word[x].upper() + ' '
        elif word[x] == ' ':
            spacedWord += ' '
    return spacedWord

def buttonClick(x, y):
    for i in range(len(buttons)):
        if x < buttons[i][1] + 20 and x > buttons[i][1] - 20:
            if y < buttons[i][2] + 20 and y > buttons[i][2] - 20:
                return buttons[i][5]
    return None


def end(winner=False):
    global status
    lostTxt = 'BETTER LUCK NEXT TIME, press any key to play again...'
    winTxt = 'VICTORY! Press any key to play again...'
    draw_window()
    pygame.time.delay(1000)
    win.fill((238,121,159))

    if winner == True:
        label = end_font.render(winTxt, 1, BLACK)
    else:
        label = end_font.render(lostTxt, 1, BLACK)

    wordTxt = end_font.render(word.upper(), 1, BLACK)
    finalword = end_font.render('The word is: ', 1, BLACK)

    win.blit(wordTxt, (winWidth/2 - wordTxt.get_width()/2, 295))
    win.blit(finalword, (winWidth/2 - finalword.get_width()/2, 245))
    win.blit(label, (winWidth / 2 - label.get_width() / 2, 140))
    pygame.display.update()
    again = True
    while again:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                again = False
    reset()
def reset():
    global status
    global guessed
    global buttons
    global word
    for i in range(len(buttons)):
        buttons[i][4] = True
    status = 0
    guessed = []
    word = randomWord()


pygame.init()
winHeight = 480
winWidth = 850
win=pygame.display.set_mode((winWidth,winHeight))


BLACK = (0,0, 0)
WHITE = (255,255,255)
RED = (255,0, 0)
GREEN = (0,255,0)
BLUE = (0,0,255)
LIGHT_BLUE = (102,255,255)
CORN_SILK=(205,200,177)
CREAM=(255,253,208)
btn_font = pygame.font.SysFont("Fixedsys", 26)
guess_font = pygame.font.SysFont("monospace", 24)
end_font= pygame.font.SysFont('Fixedsys', 45)
word = ''
guessed = []
status = 0
buttons=[]

hangmanPics=[]
for i in range(7):
    hangmanPic= pygame.image.load('/home/user/Desktop/'+'hangman'+str(i)+'.png')
    hangmanPics.append(hangmanPic)


gap = round(winWidth / 13)
for i in range(26):
    if i < 13:
        y = 40
        x = 25 + (gap * i)
    else:
        x = 25 + (gap * (i - 13))
        y = 85
    buttons.append([CORN_SILK, x, y, 20, True, 65 + i])
    
word = randomWord()
start = True
while start:
    draw_window()
    pygame.time.delay(10)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            start = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                start = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            clickPos = pygame.mouse.get_pos()
            letter = buttonClick(clickPos[0], clickPos[1])
            if letter != None:
                guessed.append(chr(letter))
                buttons[letter - 65][4] = False
                if hang(chr(letter)):
                    if status != 5:
                        status += 1
                    else:
                        end()
                else:
                    print(emptyspaces(word, guessed))
                    if emptyspaces(word, guessed).count('_') == 0:
                        end(True)

pygame.quit()
            
