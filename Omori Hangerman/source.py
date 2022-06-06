# Amy
# Pygame Hangman

import pygame, random, sys

# Window and speed stuffs
screen = pygame.display.set_mode((1024, 768))
clock = pygame.time.Clock()
pygame.init()

pygame.display.set_caption('Omori Hangerman')

def text(message, x, y, fontsize, r, g, b):
	# Pre: Reads message, the coordinates, fontsize and colors through rgb values
	# Post: Displays text on the Pygame window according to the parameters above
	font = pygame.font.Font('assets\\misc\\OMORI_GAME2.ttf', int(fontsize))
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
		self.font = pygame.font.Font('assets\\misc\\OMORI_GAME2.ttf', int(h))

	def draw(self):
		# Pre: Reads created button size, position and text
		# Post: Draws the button on the Pygame screen, also deals with mouseover display to change color when hovered over
		if self.mouse == True:
			pygame.draw.rect(screen, (255, 255, 255), self.rect, 0, 15, 15)
			self.letter = self.font.render(self.text, True, (246,192,248))
			screen.blit(self.letter, (self.rect.x +4, self.rect.y-2))
		else:
			pygame.draw.rect(screen, (255,255,255), self.rect, 0, 15, 15)
			self.letter = self.font.render(self.text, True, (125, 41, 255))#(161,104,249))#(0, 0, 0))
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
		self.font = pygame.font.Font('assets\\misc\\OMORI_GAME2.ttf', int(50))
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
	for i in range(255, 0, -1):
		screen.fill((0,0,0))
		BG.set_alpha(i)
		screen.blit(BG, (0,-75))
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
	# Post: Displays sky background if theme is cute, and fills screen with black if it's spooky
	if Theme == 'cute':
		screen.blit(BG, (0,-75))
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

#~-~-#~-~-#~-~-#~-~-#~-~-#~-~-#~-~-Image Asset Config~-~-#~-~-#~-~-#~-~-#~-~-#~-~-#~-~-#~-~-#

# Default Hangingman assets config
hmScalex = 350
hmScaley = 350
hgman0 = pygame.transform.scale(pygame.image.load('assets\\images\\mari\\Empty.png'), (hmScalex, hmScaley))
hgman1 = pygame.transform.scale(pygame.image.load('assets\\images\\mari\\EmptyHead.png'), (hmScalex, hmScaley))
hgman2 = pygame.transform.scale(pygame.image.load('assets\\images\\mari\\OneEyeHead.png'), (hmScalex, hmScaley))
hgman3 = pygame.transform.scale(pygame.image.load('assets\\images\\mari\\BothEyesHead.png'), (hmScalex, hmScaley))
hgman4 = pygame.transform.scale(pygame.image.load('assets\\images\\mari\\HeadwithBody.png'), (hmScalex, hmScaley))
hgman5 = pygame.transform.scale(pygame.image.load('assets\\images\\mari\\OneArm.png'), (hmScalex, hmScaley))
hgman6 = pygame.transform.scale(pygame.image.load('assets\\images\\mari\\BothArms.png'), (hmScalex, hmScaley))
hgman7 = pygame.transform.scale(pygame.image.load('assets\\images\\mari\\OneLeg.png'), (hmScalex, hmScaley))
hgman8 = pygame.transform.scale(pygame.image.load('assets\\images\\mari\\cuteloss.png'), (hmScalex, hmScaley))

# Other Asset config
MouseCursor = pygame.transform.scale(pygame.image.load('assets\\images\\omorimouse.png').convert_alpha(), (30,30))
BG = pygame.image.load('assets\\images\\purplesky.jpg').convert()
Logo = pygame.transform.scale(pygame.image.load('assets\\images\\omorilogo.png').convert_alpha(), (350, 210))

# Tutorial asset config
AubreyN = pygame.transform.scale(pygame.image.load('assets\\images\\aubreyneutral.png').convert_alpha(), (176,235))
AubreyH = pygame.transform.scale(pygame.image.load('assets\\images\\aubreyhappy.png').convert_alpha(), (176,235))
AubreyS = pygame.transform.scale(pygame.image.load('assets\\images\\aubreysad.png').convert_alpha(), (176,235))
KeyboardDemo = pygame.image.load('assets\\images\\keyboarddemo.png').convert_alpha()
DialogueBox = pygame.transform.scale(pygame.image.load('assets\\images\\dialoguebox.png').convert_alpha(), (800,300))

# Win and losing asset config
spookywin = pygame.transform.scale(pygame.image.load('assets\\images\\mari\\savingmarispooky.png'), (400,360))
cutewin = pygame.transform.scale(pygame.image.load('assets\\images\\mari\\cutewin.png'), (350,350))

#~-~-#~-~-#~-~-#~-~-#~-~-#~-~-#~-~-Music and Sound Config~-~-#~-~-#~-~-#~-~-#~-~-#~-~-#~-~-#~-~-#

# Sound effects
startgamesound = pygame.mixer.Sound('assets\\audio\\sfx\\SE_load.ogg')
selectsound = pygame.mixer.Sound('assets\\audio\\sfx\\select.ogg')
wronglettercutesound = pygame.mixer.Sound('assets\\audio\\sfx\\cutewrong.ogg')
themeselectsound = pygame.mixer.Sound('assets\\audio\\sfx\\themeselect.ogg')
jssound = pygame.mixer.Sound('assets\\audio\\sfx\\somethingjs.ogg')
scaresound = pygame.mixer.Sound('assets\\audio\\sfx\\scare.ogg')

# Loading in default music
pygame.mixer.music.load('assets\\audio\\music\\titlemusic.mp3')

#~-~-#~-~-#~-~-#~-~-#~-~-#~-~-#~-~-Misc Config~-~-#~-~-#~-~-#~-~-#~-~-#~-~-#~-~-#~-~-#

# Animation config
TitleAnimation = animate('title', 520, 400, 15)
BunBunnyAnimation = animate('bunbunny', 200, 160, 15)
HellmariAnimation1 = animate('hell1', 400, 420, 5)
HellmariAnimation2 = animate('hell2', 400, 420, 5)

# Opening dictionary, converting all of it to uppercase, and generating a default word
words = open("assets\\misc\\Dictionary.txt").read().replace(' ', '').split("\n")
WordList = []
for word in words:
	word = word.upper()
	WordList.append(word)
sAnswer = hangmanword(random.choice(WordList))

# Setting variables before assets are drawn/created
alphabet = ['Q','W','E','R','T','Y','U','I','O','P','A','S','D','F','G','H','J','K','L','Z','X','C','V','B','N','M']
musicOptions = ['Sweetheart', 'Space BF', 'Humphrey', 'Mari', 'Mutantheart', 'Title']
playlist = []
keyboard = []
lTitleButtons = []
lDifficultyButtons = []
sReveal = ''
sLettersGuessed = ''
sWrongLetters = ''
correctletters = ''
sButtonInput = ''
UI = 'title'
Theme = 'cute'
iErrors = 0
bunnyy = 90
TutorialScreen = 0
keydelay = 0
anidelay = 0
startmusic = True
rungame = True
pygame.mouse.set_visible(False)

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


# Game Loop
while rungame:

	# Prevents the music from playing at the beginning every single tick and allows the music to be played fully through
	if startmusic == True:
		# The -1 allows it to loop after it's done playing
		pygame.mixer.music.play(-1)
		startmusic = False

	# Displays background, and updates mouse position so the mouse png can follow
	HangingMan=[hgman0,hgman1,hgman2,hgman3,hgman4,hgman5,hgman6,hgman7,hgman8]
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
		TitleAnimation.execute(250, 170)
		text('Developed by AmyKawa', 10, 700, 30, 255, 255, 255)
		text('Made with Pygame', 10, 730, 30, 255, 255, 255)

		list_buttondisplay(lTitleButtons)

		# Changes UI and allows for new assets to be shown on screen based on what button the user clicks
		if sButtonInput == 'Start':
			UI = 'difficulty'
		elif sButtonInput == 'How to Play':
			UI = 'instructions' 
		elif sButtonInput == 'Options':
			UI = 'options'

		text('Hangerman', 430, 70, 150, 255, 255, 255)

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
			screen.blit(HangingMan[8], (230,50))
		else:
			dialogue("My friends and I are very worried, please save her!", 'S', 738, 260, 100, 300)
			buttondisplay(sBackButton)

		if TutorialScreen < 5:
			text('Press enter to continue...', 280, 600, 60, 255, 255, 255)

		# Pygame key input is really sensitive, so this prevents one click of enter key to go through all the screens really quickly
		if keys[pygame.K_RETURN] and keydelay > 10:
			TutorialScreen += 1
			keydelay = 0

		if sButtonInput == 'Back':
			UI = 'title'
			TutorialScreen = 0

		keydelay += 1

	if UI == 'options':
		text('Options', 400, 70, 100, 255, 255, 255)
		text('Music', 150, 150, 100, 255, 255, 255)
		text('Theme', 650, 150, 100, 255, 255, 255)

		list_buttondisplay(playlist)
		buttondisplay(sBackButton)
		buttondisplay(sCuteButton)
		buttondisplay(sSpookyButton)

		# Credits
		text('Developed by AmyKawa', 10, 720, 30, 255, 255, 255)
		text('Made with Pygame', 10, 740, 30, 255, 255, 255)

		# Very efficient way (very efficient) of playing different music based on the button the user clicks on
		if Theme == 'cute':
			if sButtonInput == 'Sweetheart':
				loadsong('assets\\audio\\music\\sweetheartmusic.mp3')
				sButtonInput = ''
			elif sButtonInput == 'Space BF':
				loadsong('assets\\audio\\music\\spacebfmusic.mp3')
				sButtonInput = ''
			elif sButtonInput == 'Humphrey':
				loadsong('assets\\audio\\music\\humphreymusic.mp3')
				sButtonInput = ''
			elif sButtonInput == 'Mari':
				loadsong('assets\\audio\\music\\marimusic.mp3')
				sButtonInput = ''
			elif sButtonInput == 'Mutantheart':
				loadsong('assets\\audio\\music\\mutantheartmusic.mp3')
				sButtonInput = ''
			elif sButtonInput == 'Title':
				loadsong('assets\\audio\\music\\titlemusic.mp3')
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

		# Changing Hangingman to another model if the theme is changed, as well as changing default music
		if sButtonInput == 'Cute':
			Theme = 'cute'
			loadsong('assets\\audio\\music\\titlemusic.mp3')
			hmScalex = 350
			hmScaley = 350
			hgman0 = pygame.transform.scale(pygame.image.load('assets\\images\\mari\\Empty.png'), (hmScalex, hmScaley))
			hgman1 = pygame.transform.scale(pygame.image.load('assets\\images\\mari\\EmptyHead.png'), (hmScalex, hmScaley))
			hgman2 = pygame.transform.scale(pygame.image.load('assets\\images\\mari\\OneEyeHead.png'), (hmScalex, hmScaley))
			hgman3 = pygame.transform.scale(pygame.image.load('assets\\images\\mari\\BothEyesHead.png'), (hmScalex, hmScaley))
			hgman4 = pygame.transform.scale(pygame.image.load('assets\\images\\mari\\HeadwithBody.png'), (hmScalex, hmScaley))
			hgman5 = pygame.transform.scale(pygame.image.load('assets\\images\\mari\\OneArm.png'), (hmScalex, hmScaley))
			hgman6 = pygame.transform.scale(pygame.image.load('assets\\images\\mari\\BothArms.png'), (hmScalex, hmScaley))
			hgman7 = pygame.transform.scale(pygame.image.load('assets\\images\\mari\\OneLeg.png'), (hmScalex, hmScaley))
			hgman8 = pygame.transform.scale(pygame.image.load('assets\\images\\mari\\cuteloss.png'), (hmScalex, hmScaley))
			sButtonInput = ''
		if sButtonInput == 'Spooky':
			Theme = 'spooky'
			loadsong('assets\\audio\\music\\spookymusic.mp3')
			hmScalex = 400
			hmScaley = 360
			hgman0 = pygame.transform.scale(pygame.image.load('assets\\images\\mari\\HellmariEmpty.png'), (hmScalex, hmScaley))
			hgman1 = pygame.transform.scale(pygame.image.load('assets\\images\\mari\\HellmariRopeOnly.png'), (hmScalex, hmScaley))
			hgman2 = pygame.transform.scale(pygame.image.load('assets\\images\\mari\\HellmariHead.png'), (hmScalex, hmScaley))
			hgman3 = pygame.transform.scale(pygame.image.load('assets\\images\\mari\\HellmariTorso.png'), (hmScalex, hmScaley))
			hgman4 = pygame.transform.scale(pygame.image.load('assets\\images\\mari\\HellmariOneArm.png'), (hmScalex, hmScaley))
			hgman5 = pygame.transform.scale(pygame.image.load('assets\\images\\mari\\HellmariBothArms.png'), (hmScalex, hmScaley))
			hgman6 = pygame.transform.scale(pygame.image.load('assets\\images\\mari\\HellmariOneLeg.png'), (hmScalex, hmScaley))
			hgman7 = pygame.transform.scale(pygame.image.load('assets\\images\\mari\\HellmariFullBody.png'), (hmScalex, hmScaley))
			hgman8 = pygame.transform.scale(pygame.image.load('assets\\images\\mari\\HellmariSomething.png'), (hmScalex, hmScaley))
			sButtonInput = ''

	if UI == 'difficulty':

		text('Select a', 57, 266, 100, 255 ,255 ,255)
		text('difficulty', 57, 336, 100, 255, 255, 255)

		list_buttondisplay(lDifficultyButtons)
		buttondisplay(sBackButton)

		# Changes position of the bunny to follow the cursor when they mouse over a difficulty option, displays animation based on the position
		if cursorX <= 850 and cursorX >= 450:
			if cursorY <= 275 and cursorY >= 75:
				bunnyy = 90
			elif cursorY <= 474 and cursorY >= 275:
				bunnyy = 290
			elif cursorY <= 674 and cursorY >= 475:
				bunnyy = 490
		BunBunnyAnimation.execute(450, bunnyy)

		# Decorative rectangles
		pygame.draw.rect(screen, (255, 255, 255), (450, 75, 400, 180), 5)
		pygame.draw.rect(screen, (255, 255, 255), (450, 275, 400, 180), 5)
		pygame.draw.rect(screen, (255, 255, 255), (450, 475, 400, 180), 5)

		# Easy difficulty, the word has to be larger than 10. Plays the start game SFX, starts the game and fades the screen to black as a trasition
		if sButtonInput == "Easy": 
			while len(sAnswer)<10:
				sAnswer = hangmanword(random.choice(WordList))
			pygame.mixer.Sound.play(startgamesound)
			# Only loads the spooky music if it isn't playing, ignores if the song is already playing
			if Theme == 'spooky' and pygame.mixer.music.get_busy() == False:
				loadsong('assets\\audio\\music\\spookymusic.mp3')
			UI = 'game'
			fadein()

		# Medium difficulty, nothing is different except the word has to be at least 4 letters and less than 9 letters
		elif sButtonInput == "Medium":
			while len(sAnswer)<3 or len(sAnswer)>9:
				sAnswer = hangmanword(random.choice(WordList))
			pygame.mixer.Sound.play(startgamesound)
			if Theme == 'spooky' and pygame.mixer.music.get_busy() == False:
				loadsong('assets\\audio\\music\\spookymusic.mp3')
			UI = 'game'
			fadein()

		# Hard difficulty, nothing is different except the word has to be 3 letters or less
		elif sButtonInput == "Hard":
			while len(sAnswer)>3:
				sAnswer = hangmanword(random.choice(WordList))
			pygame.mixer.Sound.play(startgamesound)
			if Theme == 'spooky' and pygame.mixer.music.get_busy() == False:
				loadsong('assets\\audio\\music\\spookymusic.mp3')
			UI = 'game'
			fadein()

		elif sButtonInput == 'Back':
			UI = 'title'

		# Allows for the word to be displayed on console
		worddisplay = True

	if UI == 'game':

		# Resets BG to be fully visible since the alpha is at 0 after being faded out
		BG.set_alpha(2000)
		bgdisplay()
		# Prints word on Command prompt ONCE. It's printed infinitely if this while loop isn't implemented
		while worddisplay == True:
			print (sAnswer.getword())
			worddisplay = False

		# Displaying keyboard, hangingman and other assets on the scren
		screen.blit(HangingMan[iErrors], (375, 175))
		pygame.draw.rect(screen, (255, 255, 255), (45, 275, 180, 75), 5)

		list_buttondisplay(keyboard)

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
		
		if sAnswer.reveal(sLettersGuessed) == True:
			UI = 'fin'
			won = True
		elif sAnswer.reveal(sLettersGuessed) == False:
			# Starts slight jumpscare if the theme is on spooky and the person loses
			if Theme == 'spooky':
				pygame.mixer.Sound.play(scaresound)
				pygame.mixer.music.stop()
				pygame.mixer.Sound.play(jssound)
				UI = 'js1'
				anidelay = 0
			else:
				UI = 'fin'
				won = False
	
	# Really cheap way of displaying animations lmao, also a crappy workaround for me limiting all animations to 3 frames because I'm lazy
	if UI == 'js1':
		HellmariAnimation1.execute(340, 175)
		anidelay += 1
		if anidelay == 15:
			UI = 'js2'
			anidelay = 0
	if UI == 'js2':
		HellmariAnimation2.execute(340, 175)
		anidelay += 1
		if anidelay == 15:
			UI = 'fin'
			won = False

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
		if Theme == 'cute':
			if won == True:
				screen.blit(cutewin, (375, 175))
			else:
				screen.blit(HangingMan[8], (375, 175))
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
			sAnswer = hangmanword(random.choice(WordList))

	# Custom Mouse Cursor, displayed last so it's on the front layer and no assets cover it
	screen.blit(MouseCursor, (cursorX - 15, cursorY))

	pygame.display.update()
	clock.tick(60)
pygame.quit()
