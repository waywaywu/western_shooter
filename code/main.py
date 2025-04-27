import pygame,sys
from pygame import Vector2

from settings import *
from player import Player
from pytmx.util_pygame import load_pygame
from sprite import Sprite, Bullet
from monster import Coffin, Cactus
class AllSprites(pygame.sprite.Group):
	def __init__(self):
		super().__init__()
		self.offset = Vector2()
		self.display_surface = pygame.display.get_surface()
		self.bg = pygame.image.load('../graphics/other/bg.png').convert()

	def customize_draw(self,player):
		self.offset.x = player.rect.centerx - WINDOW_WIDTH / 2
		self.offset.y = player.rect.centery - WINDOW_HEIGHT / 4
		self.display_surface.blit(self.bg,-self.offset)
		for sprite in sorted(self.sprites(),key = lambda sprite:sprite.rect.centery):
			offset_rect = sprite.image.get_rect(center = sprite.rect.center)
			offset_rect.center -= self.offset
			self.display_surface.blit(sprite.image,offset_rect)


class Game:
	def __init__(self):
		pygame.init()
		self.display_surface = pygame.display.set_mode((WINDOW_HEIGHT,WINDOW_WIDTH))
		pygame.display.set_caption('Western shooter')
		self.clock = pygame.time.Clock()
		self.bullet_surf = pygame.image.load('../graphics/other/particle.png').convert_alpha()
		self.all_sprites = AllSprites()
		self.obstacle = pygame.sprite.Group()
		self.bullets = pygame.sprite.Group()
		self.monsters = pygame.sprite.Group()
		self.setup()
		self.music = pygame.mixer.Sound('../sound/music.mp3')
		self.music.play(loops=-1)

	def create_bullet(self,pos,direction):
		Bullet(pos,direction,self.bullet_surf,[self.all_sprites, self.bullets])
	def bullet_collision(self):
		for self.obstacles in self.obstacle.sprites():
			pygame.sprite.spritecollide(self.obstacles, self.bullets, True)
		for bullet in self.bullets.sprites():
			sprites = pygame.sprite.spritecollide(bullet, self.monsters, False)
			if sprites:
				bullet.kill()
				for sprite in sprites:
					sprite.damage()

		if pygame.sprite.spritecollide(self.player, self.bullets, True):
			self.player.damage()

	def setup(self):#coo banana
		tmx_map =  load_pygame('../data/map.tmx')
		for x,y,surf in tmx_map.get_layer_by_name('Fence').tiles():
			Sprite((x * 64,y * 64),surf,[self.all_sprites,self.obstacle])
		for obj in tmx_map.get_layer_by_name('Object'):
			Sprite((obj.x, obj.y),obj.image,[self.all_sprites,self.obstacle])
		for obj in tmx_map.get_layer_by_name('Entities'):
			if obj.name == 'Player':
				self.player = Player(
					pos = (obj.x, obj.y),
					groups = self.all_sprites,
					path = PATHS['player'],
					sprite_collision = self.obstacle,
					create_bullet = self.create_bullet)
			if obj.name == 'Coffin':
				Coffin((obj.x, obj.y),[self.all_sprites, self.monsters],PATHS['coffin'],self.obstacle,self.player)
			if obj.name == 'Cactus':
				Cactus((obj.x, obj.y),[self.all_sprites, self.monsters],PATHS['cactus'],self.obstacle,self.player, self.create_bullet)

	def run(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
			dt = self.clock.tick() / 1000
			self.all_sprites.update(dt)
			self.bullet_collision()
			self.display_surface.fill('black')
			self.all_sprites.customize_draw(self.player)
			pygame.display.update()

if __name__ == '__main__':
	game = Game()
	game.run()
