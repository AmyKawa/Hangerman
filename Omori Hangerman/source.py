# Block 5
# Amy Lee
# Final Project 2 - Pygame Hangman

import pygame, random, sys, time

# Window and speed stuffs
screen = pygame.display.set_mode((1024, 768))
clock = pygame.time.Clock()
pygame.init()
# This is needed because theme is referenced very early in the code
Theme = 'cute'

pygame.display.set_caption('Omori Hangerman')

def textfont():
	# Pre: Checks appearance theme the user is on
	# Post: Updates the font for all text and buttons in the game based on the theme
	if Theme == 'cute' or Theme == 'pride':
		font = 'assets\\misc\\OMORI_GAME2.ttf'
	else:
		font = 'assets\\misc\\OMORI_GAME.ttf'
	return font

def text(message, x, y, fontsize, r, g, b):
	# Pre: Reads message, the coordinates, fontsize and colors through rgb values
	# Post: Displays text on the Pygame window according to the parameters above
	font = pygame.font.Font(textfont(), int(fontsize))
	string = font.render(message, False, (r,g,b))
	screen.blit(string, (x, y))

class button:
	def __init__(self, text, x, y, w, h, size):
		# Pre: Reads the values that it's given in brackets
		# Post: Creates a button of those given values (position, size, text)
		self.rect = pygame.Rect(x, y, w, h)
		self.text = text
		self.size = size
		self.mouse = False
		self.clicked = False
		self.font = pygame.font.Font(textfont(), int(h))

	def draw(self):
		# Pre: Reads created button size, position and text
		# Post: Draws the button on the Pygame screen, also deals with mouseover display to change color when hovered over
		if self.mouse == True:
			if Theme == 'cute' or Theme == 'pride':
				self.letter = self.font.render(self.text, True, (246,192,248))
			else:
				self.letter = self.font.render(self.text, True, (255,0,0))
			pygame.draw.rect(screen, (255, 255, 255), self.rect, 0, 15, 15)
			screen.blit(self.letter, (self.rect.x +4, self.rect.y-2))
		else:
			if Theme == 'cute' or Theme == 'pride':
				self.letter = self.font.render(self.text, True, (125, 41, 255))
			else:
				self.letter = self.font.render(self.text, True, (0, 0, 0))
			pygame.draw.rect(screen, (255,255,255), self.rect, 0, 15, 15)
			screen.blit(self.letter, (self.rect.x +4, self.rect.y-2))

	def mouseover(self):
		# Pre: Gets the x and y coordinates of the mouse cursor
		# Post: If the mouse is on a coordinate where a button is, tells the code that the button has been moused over
		x , y = pygame.mouse.get_pos()
		if x >= self.rect.x and x < self.rect.x + self.size and y > self.rect.y and y < self.rect.y + self.size:
			self.mouse = True
		else:
			self.mouse = False
	
	def buttonclicked(self):
		# Pre: Determines if the mouse button is down and if it's over a button
		# Post: Adds the letter/word value it clicked on to the list of either guessed letters or another variable to detect word
		global sLettersGuessed
		global sButtonInput
		pos = pygame.mouse.get_pos()
		letterclicked = 'placeholder'
		if self.rect.collidepoint(pos):
			self.mouse = True
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				self.clicked = True
				letterclicked = self.text
			if pygame.mouse.get_pressed()[0] == 0:
				self.clicked = False
		else:
			self.mouse = False
		if len(letterclicked) == 1:
			sLettersGuessed += letterclicked
			pygame.mixer.Sound.play(selectsound)
		elif len(letterclicked) > 1 and letterclicked != 'placeholder':
			sButtonInput = letterclicked
			pygame.mixer.Sound.play(selectsound)

class hangmanword:
	def __init__(self, word):
		# Pre: Reads the word it's given (from the random choice from the words in the dictionary)
		# Post: Gives x and y coordinates to where the reveal should start, reads length of word and setting font of letters and width of underscore
		self.word = word
		self.length = len(self.word)
		self.x = 535
		for x in range(self.length):
			self.x -= 20
		self.y = 80
		self.width = 40
		self.font = pygame.font.Font(textfont(), int(50))
		self.result = 'playing'

	def reveal(self, sLettersGuessed):
		# Pre: Gets all the letters in the variable sLettersGuessed
		# Post: Draws reveal based on how many letters in sLettersGuessed match with the letters in the answer, also returns true or false if the win or lose condition is met
		global iErrors
		sReveal = ''
		for char in self.word:
			if char in sLettersGuessed:
				sReveal += char
			else:
				sReveal += "_"
		text(sReveal, self.x, self.y, 100, 255, 255, 255)
		if sReveal == self.word and iErrors != 8:
			return True
		elif iErrors == 8:
			return False

	def __contains__(self, substr):
		# Pre: Deals with in statements, reads substring
		# Post: If that substring is in the chosen word/answer, returns True. Allows for in statement to be used with this class
		if substr in self.word:
			return True
		else:
			return False
	
	def __len__(self):
		# Pre: Deals with len function
		# Post: Returns the length of the hangman word and allows for len() function to be used with this class
		return self.length
	
	def getword(self):
		# Pre: Deals with the hangman word
		# Post: Returns the word that is being used for the current hangman round
		return self.word

class hangingman:
	def __init__(self, x, y):
		# Pre: Makes a hangingman based on theme player chose
		# Post: Creates a list that contains all converted pngs of the hangingman
		self.x = x #375
		self.y = y #175
		self.image = []
		for x in range(0, 9):
			if Theme == 'cute' or Theme == 'pride':
				self.image.append(pygame.transform.scale(pygame.image.load('assets\\images\\mari\\mari' + str(x) + '.png').convert_alpha(), (350, 350)))
			else:
				self.image.append(pygame.transform.scale(pygame.image.load('assets\\images\\mari\\spooky\\hellmari' + str(x) + '.png').convert_alpha(), (400, 360)))

	def draw(self, errors):
		# Pre: Reads the number of errors the player has mae
		# Post: Displays the index in the hangingman list that matches the errors of the player at the right coordinates
		screen.blit(self.image[errors], (self.x, self.y))

class animate:
	def __init__(self, basename, scalex, scaley, framemult):
		# Pre: Reads parameters entered by user
		# Post: Creates an animation with the correct images and frames
		pngs = ['assets\\images\\frames\\'+ basename + 'frame1.png', 'assets\\images\\frames\\' + basename + 'frame2.png', 'assets\\images\\frames\\' + basename + 'frame3.png']
		self.animation = []
		self.frame = 0
		for frame in pngs:
			for x in range(framemult):
				self.animation.append(pygame.transform.scale(pygame.image.load(frame).convert_alpha(), (scalex, scaley)))

	def execute(self, x, y):
		# Pre: Takes information from the __init__ function
		# Post: Displays the animation at the correct x and y coordinates with that information (such as images)
		screen.blit(self.animation[self.frame],(x, y))
		self.frame += 1
		if self.frame == len(self.animation):
			self.frame = 0

def fadein():
	# Pre: Deals with fade-in effect
	# Post: Slowly fades the screen to black
	# It will fade the background corresponding to the theme
	for i in range(255, 0, -1):
		screen.fill((0,0,0))
		if Theme == 'cute':
			BG.set_alpha(i)
			screen.blit(BG, (0, -75))
		elif Theme == 'pride':
			pridebg.set_alpha(i)
			screen.blit(pridebg, (0, -150))
		else:
			Spookybg.set_alpha(i)
			screen.blit(Spookybg, (0, 0))
		pygame.display.flip()
		clock.tick(200)

def dialogue(message, emotion, x, y, boxx, boxy):
	# Pre: Deals with How to Play interaction and creating dialogue boxes
	# Post: Displays character message, emotion portrait and dialogue box in the correct coordinates
	if emotion == 'H':
		aubrey = AubreyH
	elif emotion == 'N':
		aubrey = AubreyN
	else:
		aubrey = AubreyS
	screen.blit(DialogueBox, (boxx,boxy))
	text(message, 126, 470, 40, 255, 255, 255)
	text('AUBREY', 110, 405, 30, 255, 255, 255)
	screen.blit(aubrey, (x, y))

def loadsong(song):
	# Pre: Dealing with background music to allow players to change music
	# Post: Unloads current song playing, loads the new song and starts the music
	global startmusic
	pygame.mixer.music.unload()
	pygame.mixer.music.load(song)
	startmusic = True

def bgdisplay():
	# Pre: Deals with background display
	# Post: Displays sky background if theme is cute, pride flag if theme is pride, and fills screen with black if it's spooky
	if Theme == 'cute':
		screen.blit(BG, (0,-75))
	elif Theme == 'pride':
		screen.blit(pridebg, (0, -150))
	else:
		screen.fill((0,0,0))

def buttondisplay(button):
	# Pre: Reads button that user entered
	# Post: Draws the button on screen and adds its mouseover and buttonclicked properties
	button.draw()
	button.mouseover()
	button.buttonclicked()

def list_buttondisplay(buttonlist):
	# Pre: Reads list that user entered
	# Post: Draws all buttons in the list on screen and adds its mouseover and buttonclicked properties
	for button in range(len(buttonlist)):
		buttonlist[button].draw()
		buttonlist[button].mouseover()
		buttonlist[button].buttonclicked()

def create_buttons():
	# Pre: Used for button creation
	# Post: Creates every button so it can be drawn, I threw this into a function because they need to be re-referenced and recreated for font changes
	# Really the only change that this makes after the initial creation is update the font of the buttons when the player chooses a new theme

	# Some glitches with these buttons for some reason so just globalized all of them to avoid confusion
	global sBackButton, sSpookyButton, sCuteButtons, sPrideButton

	# Keyboard creation
	x = 210
	y = 546
	for char in alphabet:
		currkey = (button(char, x, y, 50, 50, 50))
		keyboard.append(currkey)
		x += 60
		if char == "P":
			x = 240
			y += 60
		if char == "L":
			x = 300
			y += 60

	# Title Screen button creation
	sStartButton = (button('Start', 132 , 587, 160, 80, 160)) # size = w
	sInstructionsButton = (button('How to Play', 370, 587, 320, 80, 320))
	sOptionsButton = (button('Options', 750 , 587, 200, 80, 200))
	lTitleButtons.append(sStartButton)
	lTitleButtons.append(sInstructionsButton)
	lTitleButtons.append(sOptionsButton)

	# How to Play screen button creation
	sBackButton = (button('Back', 455, 680, 150, 60, 150))

	# Difficulty button creation
	sEasyButton = (button('Easy', 667, 140 , 150, 60, 150))
	sMediumButton = (button('Medium', 667, 340 , 150, 60, 150))
	sHardButton = (button('Hard', 667, 540 , 150, 60, 150))
	lDifficultyButtons.append(sEasyButton)
	lDifficultyButtons.append(sMediumButton)
	lDifficultyButtons.append(sHardButton)

	# Options menu creation
	songx = 150
	songy = 275
	for song in musicOptions:
		currsong = (button(song, 150, songy, 220, 50, 220))
		playlist.append(currsong)
		songy += 75
	sCuteButton = (button('Cute', 667, 340 , 150, 60, 150))
	sSpookyButton = (button('Spooky', 667, 440 , 150, 60, 150))
	sPrideButton = (button('Pride', 667, 540, 150, 60, 150))
	lThemes.append(sCuteButton)
	lThemes.append(sSpookyButton)
	lThemes.append(sPrideButton)

def shuffle(string):
	# Pre: Reads string entered by user
	# Post: Returns the string randomly shuffled
	stringlist = list(string)
	random.shuffle(stringlist)
	result = ''.join(stringlist)
	return result

def secret_jumpscare():
	# Pre: Only triggers of the variable 'secret' is == 3 which means the secret jumpscare will occur
	# Post: Runs the secret jumpscare, plays animation and shows the shuffled text every tick, creating a glitched text effect
	SecretAnimation1.execute(230,90)
	gtextr, gtextg, gtextb = random.randint(0,255), random.randint(0,255), random.randint(0,255),
	text(shuffle("You couldn't save Mari in time..."), 80, 520, 85, gtextr, gtextg, gtextb)

#~-~-#~-~-#~-~-#~-~-#~-~-#~-~-#~-~-Image Asset Config~-~-#~-~-#~-~-#~-~-#~-~-#~-~-#~-~-#~-~-#

# Other Asset config
MouseCursor = pygame.transform.scale(pygame.image.load('assets\\images\\omorimouse.png').convert_alpha(), (30,30))
BG = pygame.image.load('assets\\images\\cute_bg.jpg').convert()
pridebg = pygame.transform.scale(pygame.image.load('assets\\images\\pride_bg.png').convert(), (1200,1100))
Spookybg = pygame.transform.scale(pygame.image.load('assets\\images\\spooky_bg.jpg').convert(), (1200,1100))
Logo = pygame.transform.scale(pygame.image.load('assets\\images\\omorilogo.png').convert_alpha(), (350, 210))

# Tutorial asset config
AubreyN = pygame.transform.scale(pygame.image.load('assets\\images\\aubreyneutral.png').convert_alpha(), (176,235))
AubreyH = pygame.transform.scale(pygame.image.load('assets\\images\\aubreyhappy.png').convert_alpha(), (176,235))
AubreyS = pygame.transform.scale(pygame.image.load('assets\\images\\aubreysad.png').convert_alpha(), (176,235))
KeyboardDemo = pygame.image.load('assets\\images\\keyboarddemo.png').convert_alpha()
DialogueBox = pygame.transform.scale(pygame.image.load('assets\\images\\dialoguebox.png').convert_alpha(), (800,300))

# Win and losing asset config
spookywin = pygame.transform.scale(pygame.image.load('assets\\images\\mari\\spooky\\savingmarispooky.png'), (400,360))
cutewin = pygame.transform.scale(pygame.image.load('assets\\images\\mari\\cutewin.png'), (350,350))

#~-~-#~-~-#~-~-#~-~-#~-~-#~-~-#~-~-Music and Sound Config~-~-#~-~-#~-~-#~-~-#~-~-#~-~-#~-~-#~-~-#

# Sound effects
startgamesound = pygame.mixer.Sound('assets\\audio\\sfx\\SE_load.ogg')
selectsound = pygame.mixer.Sound('assets\\audio\\sfx\\select.ogg')
wronglettercutesound = pygame.mixer.Sound('assets\\audio\\sfx\\cutewrong.ogg')
themeselectsound = pygame.mixer.Sound('assets\\audio\\sfx\\themeselect.ogg')
jssound = pygame.mixer.Sound('assets\\audio\\sfx\\somethingjs.ogg')
scaresound = pygame.mixer.Sound('assets\\audio\\sfx\\scare.ogg')
secretscaresound = pygame.mixer.Sound('assets\\audio\\sfx\\secretjssound.mp3')

# Loading in default music
pygame.mixer.music.load('assets\\audio\\music\\Titlemusic.mp3')

#~-~-#~-~-#~-~-#~-~-#~-~-#~-~-#~-~-Misc Config~-~-#~-~-#~-~-#~-~-#~-~-#~-~-#~-~-#~-~-#

# Animation config
TitleAnimation = animate('title', 520, 400, 15)
BunBunnyAnimation = animate('bunbunny', 200, 160, 15)
HellmariAnimation1 = animate('hell1', 400, 420, 5)
HellmariAnimation2 = animate('hell2', 400, 420, 5)
YassifyAnimation = animate('yassify', 520, 400, 15)
SecretAnimation1 = animate('secret', 600, 630, 5)

# Opening both dictionaries, converting all of it to uppercase, and generating a default word
regularwords = open("assets\\misc\\Dictionary.txt").read().replace(' ', '').split("\n")
WordList = []
for word in regularwords:
	word = word.upper()
	WordList.append(word)
sAnswer = hangmanword(random.choice(WordList))

# Setting variables before assets are drawn/created
alphabet = ['Q','W','E','R','T','Y','U','I','O','P','A','S','D','F','G','H','J','K','L','Z','X','C','V','B','N','M']
musicOptions = {'Sweetheart', 'Space BF', 'Humphrey', 'Mari', 'Mutantheart', 'Title'}
playlist = []
keyboard = []
lTitleButtons = []
lDifficultyButtons = []
lThemes = []
sReveal = ''
sLettersGuessed = ''
sWrongLetters = ''
correctletters = ''
sButtonInput = ''
sBackButton = ''
sSpookyButton = ''
sCuteButton = ''
sPrideButton = ''
UI = 'title'
iErrors = 0
bunnyy = 90
TutorialScreen = 0
keydelay = 0
anidelay = 0
startmusic = True
rungame = True
initialize_round = False
pygame.mouse.set_visible(False)
# Hangingman class default config
Mari = hangingman(375, 175)
tutorial_mari = hangingman(230,50)
# Creates buttons by default
create_buttons()

# Game Loop
while rungame:

	# Prevents the music from playing at the beginning every single tick and allows the music to be played fully through, also allows for music changes
	if startmusic == True:
		# The -1 allows it to loop after it's done playing
		pygame.mixer.music.play(-1)
		startmusic = False

	# Displays background, gets X and y of mouse, and key input detection
	cursorX, cursorY = pygame.mouse.get_pos()
	bgdisplay()
	keys = pygame.key.get_pressed()

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			rungame = False


	# Only draws assets and runs code based on UI variable which controls what is seen and playable on the screen at one time
	if UI == 'title':

		# Decorative assets
		screen.blit(Logo, (90, 50))
		pygame.draw.line(screen, (0,0,0), (270 , 0), (270, 70), 2)
		if Theme == 'cute' or Theme == 'spooky':
			TitleAnimation.execute(250, 170)
		else:
			YassifyAnimation.execute(250,170)
		text('Developed by AmyKawa', 10, 700, 30, 255, 255, 255)
		text('Made with Pygame', 10, 730, 30, 255, 255, 255)
		text('Hangerman', 430, 70, 150, 255, 255, 255)

		# Button assets
		list_buttondisplay(lTitleButtons)

		# Changes UI and allows for new assets to be shown on screen based on what button the user clicks
		if sButtonInput == 'Start':
			UI = 'difficulty'
		elif sButtonInput == 'How to Play':
			UI = 'instructions' 
		elif sButtonInput == 'Options':
			UI = 'options'


	if UI == 'instructions':

		# Tutorial dialogue, variable TutorialScreen controls what can be shown on screen
		if TutorialScreen == 0:
			dialogue("Thank goodness you're here!", 'N', 738, 260, 100, 300)
		elif TutorialScreen == 1:
			dialogue("Mari needs our help, she's stuck in a tree and it's scary...", 'S', 738, 260, 100, 300)
		elif TutorialScreen == 2:
			dialogue('You have the power to save her!', 'H', 738, 260, 100, 300)
		elif TutorialScreen == 3:
			dialogue('Click keys on the virtual keyboard to guess the word.', 'N', 738, 260, 100, 300)
			screen.blit(KeyboardDemo, (100, 150))
		elif TutorialScreen == 4:
			dialogue("Save Mari before it's too late! 8 wrong guesses will end", 'S', 738, 260, 100, 300)
			text('the game.', 126, 512, 40, 255, 255, 255)
			tutorial_mari.draw(8)
		else:
			dialogue("My friends and I are very worried, please save her!", 'S', 738, 260, 100, 300)
			buttondisplay(sBackButton)

		if TutorialScreen < 5:
			text('Press enter to continue...', 280, 600, 60, 255, 255, 255)

		# Pygame key input is really sensitive, so this prevents one click of enter key to go through all the screens really quickly
		if keys[pygame.K_RETURN] and keydelay > 10:
			TutorialScreen += 1
			keydelay = 0
		keydelay += 1

		# Button assets
		if sButtonInput == 'Back':
			UI = 'title'
			TutorialScreen = 0

	if UI == 'options':

		# Decorative assets
		text('Options', 400, 70, 100, 255, 255, 255)
		text('Music', 150, 150, 100, 255, 255, 255)
		text('Theme', 650, 150, 100, 255, 255, 255)
		text('Developed by AmyKawa', 10, 700, 30, 255, 255, 255)
		text('Made with Pygame', 10, 730, 30, 255, 255, 255)

		# Button display
		list_buttondisplay(playlist)
		list_buttondisplay(lThemes)
		buttondisplay(sBackButton)

		# Music selection
		if Theme == 'cute' or Theme == 'pride':
			if sButtonInput in musicOptions:
				loadsong('assets\\audio\\music\\' + sButtonInput + 'music.mp3')
				sButtonInput = ''
		# Locks the songs from being played during spooky theme because the songs are too happy and ruins the theme
		elif Theme == 'spooky':
			if sButtonInput in {'Sweetheart', 'Space BF', 'Humphrey', 'Mari', 'Mutantheart', 'Title'}:
				pygame.mixer.Sound.play(wronglettercutesound)
				sButtonInput = ''

		if sButtonInput == 'Next':
			TutorialScreen += 1

		if sButtonInput == 'Back':
			UI = 'title'

		# Changing Hangingman to another model if the theme is changed, as well as changing font and default music
		# Active list is changed if pride theme is chosen, reverted back to the dictionary.txt if changed to cute or spooky theme
		if sButtonInput == 'Cute' or sButtonInput == 'Pride':
			if sButtonInput == 'Cute':
				Theme = 'cute'
			else:
				Theme = 'pride'
			loadsong('assets\\audio\\music\\Titlemusic.mp3')
			sAnswer = hangmanword(random.choice(WordList))
			Mari = hangingman(375, 175)
			tutorial_mari = hangingman(230,50)
			create_buttons()
			sButtonInput = ''

		if sButtonInput == 'Spooky':
			Theme = 'spooky'
			loadsong('assets\\audio\\music\\Spookymusic.mp3')
			Mari = hangingman(375, 175)
			tutorial_mari = hangingman(230,50)
			sAnswer = hangmanword(random.choice(WordList))
			create_buttons()
			sButtonInput = ''

	if UI == 'difficulty':

		# Decorative assets
		text('Select a', 57, 266, 100, 255 ,255 ,255)
		text('difficulty', 57, 336, 100, 255, 255, 255)
		pygame.draw.rect(screen, (255, 255, 255), (450, 75, 400, 180), 5)
		pygame.draw.rect(screen, (255, 255, 255), (450, 275, 400, 180), 5)
		pygame.draw.rect(screen, (255, 255, 255), (450, 475, 400, 180), 5)

		# Changes position of the bunny to follow the cursor when they mouse over a difficulty option, displays animation based on the position
		if cursorX <= 850 and cursorX >= 450:
			if cursorY <= 275 and cursorY >= 75:
				bunnyy = 90
			elif cursorY <= 474 and cursorY >= 275:
				bunnyy = 290
			elif cursorY <= 674 and cursorY >= 475:
				bunnyy = 490
		BunBunnyAnimation.execute(450, bunnyy)

		# Button display
		list_buttondisplay(lDifficultyButtons)
		buttondisplay(sBackButton)

		# Easy difficulty, the word has to be larger than 10
		if sButtonInput == "Easy": 
			while len(sAnswer)<10:
				sAnswer = hangmanword(random.choice(WordList))
			initialize_round = True

		# Medium difficulty, the word has to be at least 4 letters and less than 9 letters
		elif sButtonInput == "Medium":
			while len(sAnswer)<3 or len(sAnswer)>9:
				sAnswer = hangmanword(random.choice(WordList))
			initialize_round = True

		# Hard difficulty, the word has to be 3 letters or less
		elif sButtonInput == "Hard":
			while len(sAnswer)>3:
				sAnswer = hangmanword(random.choice(WordList))
			initialize_round = True

		elif sButtonInput == 'Back':
			UI = 'title'

		# Plays the start game SFX, starts the game and fades the screen to black as a transition
		if initialize_round == True:
			pygame.mixer.Sound.play(startgamesound)
			if Theme == 'spooky' and pygame.mixer.music.get_busy() == False:
				loadsong('assets\\audio\\music\\spookymusic.mp3')
			UI = 'game'
			fadein()
			print (sAnswer.getword())
			# Generates a number from 1 to 5, if it lands on 3, losing the hangman game will trigger a secret jumpscare. This number changes every round
			secret = 3#random.randint(1,5)
			print (secret)

	if UI == 'game':

		# Resets BGs to be fully visible since the alpha is at 0 after being faded out
		BG.set_alpha(2000)
		pridebg.set_alpha(2000)
		bgdisplay()

		# Displaying keyboard and hangingman
		Mari.draw(iErrors)
		list_buttondisplay(keyboard)

		# Checking if the letter the user guessed is in the word or not, adds errors if it's wrong, updates reveal if it's right, also plays sounds
		for char in sLettersGuessed:
			if char not in sAnswer:
				if char not in sWrongLetters:
					iErrors += 1
					sWrongLetters += char
					sLettersGuessed = sLettersGuessed.replace(char, '')
					pygame.mixer.Sound.play(wronglettercutesound)
			else:
				if char not in correctletters:
					correctletters += char
					pygame.mixer.Sound.play(selectsound)

		# Displaying wrong letters, reveal and errors
		sAnswer.reveal(sLettersGuessed)
		text(sWrongLetters, 50, 275, 40, 255, 0, 0)
		text("Errors:", 50, 300, 40, 255, 0, 0)
		text(str(iErrors), 150, 300, 40, 255, 0, 0)
		pygame.draw.rect(screen, (255, 255, 255), (45, 275, 180, 75), 5)

		# Goes to end screen and does specific actions whether the user won or loss
		if sAnswer.reveal(sLettersGuessed) == True:
			UI = 'fin'
			won = True
		elif sAnswer.reveal(sLettersGuessed) == False:
			# Starts slight jumpscare if the theme is on spooky and the person loses
			# There is a 1 in 5 chance to trigger the secret jumpscare, configures assets based on that (triggers if == 3)
			# If theme isn't spooky, jumps to losing page immediately
			if Theme == 'spooky':
				if secret == 3:
					pygame.mixer.Sound.play(secretscaresound)
				else:
					pygame.mixer.Sound.play(scaresound)
				pygame.mixer.music.stop()
				pygame.mixer.Sound.play(jssound)
				UI = 'jumpscare'
				jsphase = 1
				anidelay = 0
			else:
				UI = 'fin'
				won = False

	# Really cheap way of displaying end jumpscare, also a crappy workaround for me limiting all animations to 3 frames because I'm lazy
	# Displays alternate animation if they get the secret jumpscare
	if UI == 'jumpscare':
		if jsphase == 1:
			if secret == 3:
				secret_jumpscare()
			else:
				HellmariAnimation1.execute(340, 175)
			if anidelay == 15:
				jsphase = 2
				anidelay = 0
		else:
			if secret == 3:
				secret_jumpscare()
			else:
				HellmariAnimation2.execute(340, 175)
			if anidelay == 15:
				UI = 'fin'
				won = False
		# Allows for animation to play for a certain amount of ticks (prevents it from all happening at once and not being visible to human eye)
		anidelay += 1

	if UI == 'fin':

		# Displaying text and assets on screen based on if the player loses or wins
		if won == True:
			text('You saved Mari!', 280, 520, 100, 255, 252, 0)
		elif won == False:
			text("You couldn't save Mari in time...", 80, 520, 85, 255, 255, 255)
			text('The word was', 340, 620, 50, 255, 255, 255)
			text(sAnswer.getword(), 586, 620, 50, 255, 252, 0)
		sAnswer.reveal(sLettersGuessed)

		buttondisplay(sBackButton)

		# Displaying assets on screen based on the theme the player chose
		if Theme == 'cute' or Theme == 'pride':
			if won == True:
				screen.blit(cutewin, (375, 175))
			else:
				Mari.draw(iErrors)
		else:
			if won == True:
				screen.blit(spookywin, (375, 175))

		# Showing wrong letters, reveal and error count
		pygame.draw.rect(screen, (255, 255, 255), (45, 275, 180, 75), 5)
		text(sWrongLetters, 50, 275, 40, 255, 0, 0)
		text("Errors:", 50, 300, 40, 255, 0, 0)
		text(str(iErrors), 150, 300, 40, 255, 0, 0)

		if sButtonInput == 'Back':
			# Resets variables to allow for a new round of hangman
			UI = 'title'
			sReveal = ''
			sLettersGuessed = ''
			sWrongLetters = ''
			correctletters = ''
			iErrors = 0
			initialize_round = False
			sAnswer = hangmanword(random.choice(WordList))

	# Custom Mouse Cursor, displayed last so it's on the front layer and no assets cover it
	screen.blit(MouseCursor, (cursorX - 15, cursorY))

	pygame.display.update()
	clock.tick(60)
pygame.quit()
