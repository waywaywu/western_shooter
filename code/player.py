import pygame
import math

from pygame import Vector2
from os import walk
from entity import Entity

class Player(Entity):
    def __init__(self,pos,groups,path,sprite_collision,create_bullet):
        super().__init__(pos,groups,path,sprite_collision)
        self.create_bullet = create_bullet
        self.bullet_shot = False
    def get_status(self):
        if self.direction.x == 0 and self.direction.y == 0:
            self.status = self.status.split('_')[0] + '_idle'
        if self.attacking:
            self.status = self.status.split('_')[0] + '_attack'
    def import_assets(self,path):
        self.animation = {}
        for index,folder in enumerate(walk(path)):
            if index == 0:
                for name in folder[1]:
                    self.animation[name] = []
            else:
                for file_name in sorted(folder[2], key = lambda string: int(string.split('.')[0])):
                    path = folder[0] + '/' + file_name
                    surf = pygame.image.load(path).convert_alpha()
                    key = folder[0].split('/')[3]
                    self.animation[key].append(surf)






    def input(self):
        keys = pygame.key.get_pressed()
        if not self.attacking:
            if keys[pygame.K_RIGHT]:
                self.direction.x = 1
                self.status =  'right'
            elif keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.status = 'left'
            else:
                self.direction.x = 0
            if keys[pygame.K_UP]:
                self.direction.y = -1
                self.status = 'up'
            elif keys[pygame.K_DOWN]:
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0
            if keys[pygame.K_SPACE]:
                self.attacking = True
                self.direction = Vector2()
                self.frame_index = 0
                self.bullet_shot = False
                match self.status.split('_')[0]:
                    case 'left':self.bullet_direction = Vector2(-1,0)
                    case 'right':self.bullet_direction = Vector2(1, 0)
                    case 'up':self.bullet_direction = Vector2(0, -1)
                    case 'down':self.bullet_direction = Vector2(0, 1)

    def animate(self,dt):
        current_animation = self.animation[self.status]
        self.frame_index += 7 * dt
        if int(self.frame_index) == 2 and self.attacking and not self.bullet_shot:
            self.bullet_start_pos = self.rect.center + self.bullet_direction * 80
            self.create_bullet(self.bullet_start_pos,self.bullet_direction)
            self.bullet_shot = True
        if self.frame_index >= len(current_animation):
            self.frame_index = 0
            if self.attacking:
                self.attacking = False
        self.image = current_animation[int(self.frame_index)]

    def update(self,dt):
        self.input()
        self.move(dt)
        self.animate(dt)
        self.get_status()
        self.vulnerbility_timer()
