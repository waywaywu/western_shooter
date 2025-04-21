import pygame
from entity import Entity
from pygame.math import Vector2
class Monster:
    def walk_to_player(self):
        enemy_pos = Vector2(self.rect.center)
        player_pos = Vector2(self.player.rect.center)
        distance = (player_pos - enemy_pos).magnitude()
        if distance != 0:
            direction = (player_pos - enemy_pos).normalize()
        else:
            direction = Vector2()
        return (distance, direction)

    def face_player(self):
        distance, direction = self.get_player_distance_direction()
        if distance < self.notice_radius:
            if -0.5 < direction.y < 0.5:
                if direction.x < 0:
                    self.status = 'left_idle'
                elif direction.x > 0:
                    self.status = 'right_idle'
            else:
                if direction.y < 0:
                    self.status = 'up_idle'
                elif direction.y > 0:
                    self.status = 'down_idle'
        distance, direction = self.get_player_distance_direction()
        if self.attack_radius < distance < self.walk_radius:
            self.direction = direction
            self.status = self.status.split('_')[0]
        else:
            self.direction = Vector2()
    def get_player_distance_direction(self):
        enemy_pos = Vector2(self.rect.center)
        player_pos = Vector2(self.player.rect.center)
        distance = (player_pos - enemy_pos).magnitude()
        if distance != 0:
            direction = (player_pos - enemy_pos).normalize()
        else:
            direction = Vector2()
        return (distance, direction)
class Coffin(Entity, Monster):
    def __init__(self,pos,groups,path,sprite_collision,player):
        super().__init__(pos,groups,path,sprite_collision)

        self.player = player
        self.notice_radius = 550
        self.walk_radius = 400
        self.attack_radius = 50
        self.speed = 150
    def attack(self):
        distance = self.get_player_distance_direction()[0]
        if distance < self.attack_radius and not self.attacking:
            self.attacking = True
            self.frame_index = 0
        if self.attacking:
            self.status = self.status.split('_')[0] + '_attack'

    def animate(self,dt):

        current_animation = self.animation[self.status]
        if int(self.frame_index) == 4 and self.attacking:
            if self.get_player_distance_direction()[0] < self.attack_radius:
                self.player.damage()
        self.frame_index += 7 * dt
        if self.frame_index >= len(current_animation):
            self.frame_index = 0
            if self.attacking:
                self.attacking = False
        self.image = current_animation[int(self.frame_index)]



    def walk_to_player(self):
        distance, direction = self.get_player_distance_direction()
        if self.attack_radius < distance < self.walk_radius:
            self.direction = direction
            self.status = self.status.split('_')[0]
        else:
            self.direction = Vector2()
    def update(self, dt):
        self.walk_to_player()
        self.move(dt)
        self.check_death()
        self.attack()
        self.animate(dt)
        self.face_player()
        self.vulnerbility_timer()


class Cactus(Entity, Monster):
    def __init__(self, pos, groups, path, sprite_collision,player,create_bullet):
        super().__init__(pos, groups, path, sprite_collision)
        self.player = player
        self.notice_radius = 600
        self.walk_radius = 500
        self.attack_radius = 350
        self.speed = 90
        self.create_bullet = create_bullet
        self.bullet_shot = False
    def attack(self):
        distance = self.get_player_distance_direction()[0]
        if distance < self.attack_radius and not self.attacking:
            self.attacking = True
            self.frame_index = 0
            self.bullet_shot = False
        if self.attacking:
            self.status = self.status.split('_')[0] + '_attack'

    def animate(self, dt):
        current_animation = self.animation[self.status]
        if int(self.frame_index) == 6 and self.attacking and not self.bullet_shot:
            direction = self.get_player_distance_direction()[1]
            pos = self.rect.center + direction * 150
            self.create_bullet(pos, direction)
            self.bullet_shot = True
        self.frame_index += 7 * dt
        if self.frame_index >= len(current_animation):
            self.frame_index = 0
            if self.attacking:
                self.attacking = False
        self.image = current_animation[int(self.frame_index)]
    def update(self, dt):
        self.face_player()
        self.move(dt)
        self.check_death()
        self.attack()
        self.walk_to_player()
        self.animate(dt)
        self.vulnerbility_timer()