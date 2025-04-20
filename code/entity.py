import pygame
from pygame import Vector2
from os import walk
import math

class Entity(pygame.sprite.Sprite):
    def __init__(self,pos,groups,path,sprite_collision):
        super().__init__(groups)
        self.import_assets(path)
        self.frame_index = 0
        self.status = 'down_idle'
        self.image = self.animation[self.status][self.frame_index]
        self.rect = self.image.get_rect(center=pos)
        self.pos = Vector2(self.rect.center)
        self.direction = Vector2()
        self.speed = 200
        self.hitbox = self.rect.inflate(-self.rect.width * 0.5, -self.rect.height / 2)
        self.sprite_collision = sprite_collision
        self.attacking = False
        self.health = 3
        self.is_vulnerble = True
        self.hit_time = None
    def damage(self):
        if self.is_vulnerble:
            self.health -= 1
            self.is_vulnerble = False
            self.hit_time =  pygame.time.get_ticks()
    def vulnerbility_timer(self):
        if not self.is_vulnerble:
            current_time = pygame.time.get_ticks()
            if current_time - self.hit_time > 400:
                self.is_vulnerble = True


    def import_assets(self,path):
        self.animation = {}
        for index,folder in enumerate(walk(path)):
            print(index, folder)
            if index == 0:
                for name in folder[1]:
                    self.animation[name] = []
            else:
                for file_name in sorted(folder[2], key = lambda string: int(string.split('.')[0])):
                    path = folder[0] + '/' + file_name
                    surf = pygame.image.load(path).convert_alpha()
                    key = folder[0].split('/')[4]
                    self.animation[key].append(surf)

    def move(self, dt):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
            self.pos.x += self.direction.x * self.speed * dt
            self.hitbox.centerx = round(self.pos.x)
            self.rect.centerx = self.hitbox.centerx
            self.collision('horizontal')

            self.pos.y += self.direction.y * self.speed * dt
            self.hitbox.centery = round(self.pos.y)
            self.rect.centery = self.hitbox.centery
            self.collision('vertical')
    def collision(self,direction):
        for sprite in self.sprite_collision.sprites():
           if sprite.hitbox.colliderect(self.hitbox):
               if direction == 'horizontal':
                   if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                        self.rect.centerx = self.hitbox.centerx
                        self.pos.x = self.hitbox.centerx
                   if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right
                        self.rect.centerx = self.hitbox.centerx
                        self.pos.x = self.hitbox.centerx
               else:
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                        self.rect.centery = self.hitbox.centery
                        self.pos.y = self.hitbox.centery
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom
                        self.rect.centery = self.hitbox.centery
                        self.pos.y = self.hitbox.centery
