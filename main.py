import pygame	# 2D Graphics Library
import os		



# SETTINGS
WIDTH, HEIGHT = 1280, 720
FPS = 60
VEL = 5
BULLET_VEL = 10
MAX_BULLETS = 3
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

WIN = pygame.display.set_mode((WIDTH, HEIGHT))


# COLORS
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)

# DIVIDER
BORDER_WIDTH = 10
BORDER = pygame.Rect((WIDTH//2)-(BORDER_WIDTH//2), 0, BORDER_WIDTH, HEIGHT)


# SOUNDFX
pygame.mixer.init()
BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Grenade+1.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Gun+Silencer.mp3'))

# FONTS
pygame.font.init()
HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

# EVENT CONTROLLER
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2


# YELLOW SPACESHIP
YELLOW_SPACESHIP_IMAGE = pygame.image.load(
	os.path.join('Assets','spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

# RED SPACESHIP
RED_SPACESHIP_IMAGE = pygame.image.load(
	os.path.join('Assets','spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

# BACKGROUND
SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')), (WIDTH,HEIGHT))


# GAME VIEW
def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
		WIN.blit(SPACE, (0,0)) # BACKGROUND
		pygame.draw.rect(WIN, BLACK, BORDER) # CENTER BORDER
		red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, WHITE) # RED HEALTH METER
		yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, WHITE) # YELLOW HEALTH METER
		WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
		WIN.blit(yellow_health_text, (10,10))
		WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y)) # UPDATING SHIP POS ON SCREEN
		WIN.blit(RED_SPACESHIP, (red.x, red.y))

		# BULLET "ANIMATION"
		for bullet in red_bullets:
			pygame.draw.rect(WIN, RED, bullet)
		for bullet in yellow_bullets:
			pygame.draw.rect(WIN, YELLOW, bullet)

		# UPDATE CHANGES TO DISPLAY
		pygame.display.update()


# YELLOW MOVEMENT
def yellow_handle_movement(keys_pressed, yellow):
		if keys_pressed[pygame.K_a] and yellow.x - VEL > 0: # LEFT
			yellow.x -= VEL
		if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x: # RIGHT
			yellow.x += VEL
		if keys_pressed[pygame.K_w] and yellow.y - VEL > 0: # UP
			yellow.y -= VEL
		if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT - 15: # DOWN
			yellow.y += VEL

# RED MOVEMENT
def red_handle_movement(keys_pressed, red):
		if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width: # LEFT
			red.x -= VEL
		if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH: # RIGHT
			red.x += VEL
		if keys_pressed[pygame.K_UP] and red.y - VEL > 0: # UP
			red.y -= VEL
		if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT - 15: # DOWN
			red.y += VEL

# BULLET LOGIC
def handle_bullets(yellow_bullets, red_bullets, yellow, red):
	for bullet in yellow_bullets:
		bullet.x += BULLET_VEL # SHOOTING TO THE RIGHT (+ ON X AXIS)
		if red.colliderect(bullet):
			pygame.event.post(pygame.event.Event(RED_HIT))
			yellow_bullets.remove(bullet)
		elif bullet.x > WIDTH: # CONDITIONAL/KEEP ALL BULLETS ON SCREEN
			yellow_bullets.remove(bullet)

	for bullet in red_bullets:
		bullet.x -= BULLET_VEL # SHOOTING TO THE LEFT (- ON X-AXIS)
		if yellow.colliderect(bullet):
			pygame.event.post(pygame.event.Event(YELLOW_HIT))
			red_bullets.remove(bullet)
		elif bullet.x < 0: # CONDITIONAL/KEEP ALL BULLETS ON SCREEN
			red_bullets.remove(bullet)

# GAME WIN SEQUENCE
def draw_winner(text):
	draw_text = WINNER_FONT.render(text, 1, WHITE)
	WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width()//2, HEIGHT//2 - draw_text.get_height()//2))
	pygame.display.update()
	pygame.time.delay(5000) # RESET DELAY (ms)

def main():

	# SHIP STARTING POSITION
	yellow = pygame.Rect(WIDTH//2 - WIDTH//4, HEIGHT//2, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
	red = pygame.Rect(WIDTH//2 + WIDTH//4, HEIGHT//2, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

	# NEW GAME/NO BULLETS IN GAME SPACE
	red_bullets = []
	yellow_bullets = []

	# INITIAL PLAYER HEALTH
	red_health = 3
	yellow_health = 3


	clock = pygame.time.Clock()
	run = True

	# GAME RUNNING CONDITIONAL
	while run:
		clock.tick(FPS) # REFRESH/FRAME RATE
		for event in pygame.event.get():
			if event.type == pygame.QUIT: # CHECK IF GAME CLOSED
				run = False
				pygame.quit()

			if event.type == pygame.KEYDOWN: # SHOOT
				if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS: # MAX BULLET LIMITER
					bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 -2, 10, 5)
					yellow_bullets.append(bullet)
					BULLET_FIRE_SOUND.play()
				if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS: # MAX BULLET LIMITER
					bullet = pygame.Rect(red.x, red.y + red.height//2 -2, 10, 5)
					red_bullets.append(bullet)
					BULLET_FIRE_SOUND.play()

			if event.type == RED_HIT:
				red_health -= 1
				BULLET_HIT_SOUND.play()

			if event.type == YELLOW_HIT:
				yellow_health -= 1
				BULLET_HIT_SOUND.play()

		winner_text = ""

		if red_health <= 0:
			winner_text = "YELLOW WINS!"
		if yellow_health <= 0:
			winner_text = "RED WINS!"

		if winner_text != "":
			draw_winner(winner_text)
			break

		print(red_bullets, yellow_bullets) # PRINT POSITION OF BULLETS TO CONSOLE
		keys_pressed = pygame.key.get_pressed() # CHECK FOR KEY PRESSES

		yellow_handle_movement(keys_pressed, yellow) # YELLOW MOVEMENT FUNCTION
		red_handle_movement(keys_pressed,red) # RED MOVEMENT FUNCTION
		handle_bullets(yellow_bullets, red_bullets, yellow, red) # BULLET HANDLING FUNCTION

		draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health) # UPDATE ABOVE ASSESSMENT OF GAMESPACE TO SCREEN



	main() # KEEP RUNNING UNTIL CLOSED

if __name__ == "__main__":
	main()