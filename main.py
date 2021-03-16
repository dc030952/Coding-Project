import pygame
import os
import math


#Constants
WIDTH = 800
HEIGHT = 600
FPS = 30
GROUND = HEIGHT - 30
SLOW = 3
FAST = 8
PLAYER_ACC = 0.9
PLAYER_FRICTION = -0.12
PLAYER_GRAV = 0.9
vec = pygame.math.Vector2

#Define Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
SKYBLUE = (135, 206, 235)

#Asset Folders
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'img')


#Initalize Variables
pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('The Platformer')



#Functions

#Draw Text Function
font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y):
	font = pygame.font.Font(font_name, size)
	text_surface = font.render(text, True, GREEN)
	text_rect = text_surface.get_rect()
	text_rect.midtop = (x, y)
	surf.blit(text_surface, text_rect)


def show_start_screen():
	screen.fill(BLACK)
	draw_text(screen, "Portal Escape", 64, WIDTH/2, HEIGHT/4)
	draw_text(screen, "WASD to move and space to shoot.", 22, WIDTH/2, HEIGHT/2)
	draw_text(screen, "Press any key to start", 18, WIDTH/2, HEIGHT * 3/4)
	pygame.display.flip()

	waiting = True
	while waiting:
		clock.tick(FPS)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
			if event.type == pygame.KEYUP:
				print("Key pressed to start game!")
				waiting = False

def show_gameover_screen():
	screen.fill(BLACK)
	draw_text(screen, "GAME OVER", 64, WIDTH/2, HEIGHT/4)
	draw_text(screen, "Press SPACE to restart the game.", 22, WIDTH/2, HEIGHT/2)
	pygame.display.flip()

	keystate = pygame.key.get_pressed()

	waiting = True
	while gameover:
		clock.tick(FPS)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
			if keystate [pygame.K_SPACE]:
				print("Key pressed to restart game!")
				show_start_screen()
				gameover = False


#Classes



#Player Class
class Player(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.imageload = pygame.image.load(os.path.join(img_folder,"scientist_right.png")).convert()
		self.imageload.set_colorkey(BLACK)
		self.image = pygame.transform.scale(self.imageload,(50,38))
		self.rect = self.image.get_rect()
		self.radius = 20
		self.rect.centerx = WIDTH / 2
		self.rect.bottom = HEIGHT - 10
		self.speedx = 0
		self.shoot_delay = 250
		self.last_shot = pygame.time.get_ticks()
		self.rect.center = (WIDTH/2, HEIGHT/2)
		self.y_speed = 5
		self.pos = vec(10, GROUND - 60)
		self.vel = vec(0, 0)
		self.acc = vec(0,0)
	def update(self):
		self.speedx = 0
		
		self.acc = vec(0, PLAYER_GRAV)

		keystate = pygame.key.get_pressed()

		if keystate [pygame.K_d]:
			self.acc.x += PLAYER_ACC	
		if keystate [pygame.K_a]:
			self.acc.x += -PLAYER_ACC
		if keystate [pygame.K_w]:
			self.rect.y += -5
		if keystate [pygame.K_s]:
			self.rect.y += 5
		#if keystate [pygame.K_SPACE]:
		#	self.shoot()
		if self.vel.y == 0 and keystate[pygame.K_UP]:
			self.vel.y = -20

		self.acc.x += self.vel.x * PLAYER_FRICTION

		self.vel += self.acc
		self.pos += self.vel + 0.5 * self.acc

		if keystate [pygame.K_k]:
			if gameover:
			show_gameover_screen()
			gameover = False

		if self.pos.x > WIDTH:
			self.pos.x = 0
		if self.pos.x < 0:
			self.pos.x = WIDTH

		if self.pos.y > GROUND:
			self.pos.y = GROUND + 1
			self.vel.y = 0

		self.rect.midbottom = self.pos

		mouseState = pygame.mouse.get_pressed()
		if mouseState[0] == 1:
			pos = pygame.mouse.get_pos()
			mouse_x = pos[0]
			mouse_y = pos[1]

			self.shoot(mouse_x, mouse_y) 
			all_sprites.add(laser)
			lasers.add(laser)

	def shoot(self, mouse_x, mouse_y):
			now = pygame.time.get_ticks()
			if now - self.last_shot > self.shoot_delay:
				self.last_shot = now


				bullet = Bullet(self.rect.right, 
					self.rect.centery, 
					mouse_x, 
					mouse_y)
				all_sprites.add(bullet)
				bullets.add(bullet)

class Bullet(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((5,10))
		self.image.fill(BLUE)
		self.image.set_colorkey(BLACK)
		'''
		self.rect = self.image.get_rect()
		self.rect.bottom = y
		self.rect.centerx = x
		self.speedx = + 100
		'''

		#Establish Rect
		self.rect = self.image.get_rect
		self.rect.left = start_x
		self.rect.bottom = start_y

		#Accurate Starting Point
		self.floating_point_x = start_x
		self.floating_point_y = start_y

		#Diff BTWN Start & Dest Points
		x_diff = dest_x - start_X
		y_diff = dest_y - start_y
		angle = math.atan2(y_diff, x_diff)

		#Velocity
		self.speedx = 20
		self.change_x = math.cos(angle) * self.speedx
		self.change_y = math.sin(angle) * self.speedx


	def update(self):
		#self.rect.x += self.speedx
		
		self.floating_point_y += self.change_y
		self.floating_point_x += self.change_x

		self.rect.y = int(self.floating_point_y)
		self.rect.x = int(self.floating_point_x)

		self.laser_count += 1
		if laser_count > 5:
			self.laser_count = 0		


		if self.rect.x < 0 or self.rect.x > WIDTH or self.rect.y < 0 or self.rect.y > HEIGHT:
			self.kill()

			
class CrossHairs(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)

		self.image = pygame.image.load(os.path.join(img_folder, "crosshair.png")).convert()
		self.image = pygame.transform.scale(self.image, (30,30))
		self.image.set_colorkey(BLACK)

		self.rect = self.image.get_rect()
		self.rect.x = 100
		self.rect.y = 100

		self.pos = vec(0,0)
		
		self.setCH = False

		self.old_x = 0
		self.old_y = 0

	def update(self):
		mouseState = pygame.mouse.get_pressed()
		pos = pygame.mouse.get_pos()

		self.rect.centerx = pos[0]
		self.rect.centery = pos[1]


clock = pygame.time.Clock()

#Sprite Groups
all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

crosshairs = CrossHairs()
all_sprites.add(crosshairs)


#Game Loop


#Process Events

start = True
gameover = True
running = True

while running:
	if start:
		show_start_screen()
		start = False

	clock.tick(FPS)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		
#Update
	all_sprites.update()

#Draw
	screen.fill(SKYBLUE)
	all_sprites.draw(screen)

#Flip
	pygame.display.flip()


pygame.quit()
