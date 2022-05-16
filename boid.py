import random
import math
import pygame
from pygame.math import Vector2
MIN_DIST = 100


class Boid(pygame.sprite.Sprite):
    def __init__(self, center, color=(0,0,255), velocity=(5,5)):
        super().__init__()
        self.pos = Vector2(center)
        self.color = color
        self.image = pygame.Surface([25, 20])
        self.image.set_colorkey((0,0,0))
        x, y = center
        self.velocity = Vector2(velocity)
        points = [
            (0, 0),
            (5, 20),
            (10, 0),
        ]
        pygame.draw.polygon(self.image, self.color, points, 0)
        self.orig_image = self.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.new_v = self.velocity

    def update(self):
        
        self.velocity = self.new_v
        new_pos = self.pos + self.velocity
        angle = Vector2().angle_to(self.pos-new_pos)
        n_angle = (180 - (angle - 90)) % 360
        self.pos = self.pos.rotate(angle)
        self.pos = new_pos
        self.image = pygame.transform.rotate(self.orig_image, n_angle)

        self.rect.center = self.pos


class Behavior:
    def __init__(self,
            min_distance=20,
            center_factor=25,
            match_factor=16,
            width=1280, 
            height=720,
            speed_limit=50,
            roam=False,
            ):
        self.min_distance = min_distance
        self.center_factor = center_factor
        self.match_factor = match_factor
        self.height = height
        self.width = width
        self.speed_limit = speed_limit
        self.roam=roam
        self.fav_point = Vector2((self.width/2, self.height/2))


    def change_state(self, boids):
        for boid in boids:
            set_d = self.set_distance(boid, boids)
            go_c = self.go_center(boid, boids)
            match_v = self.match_velocity(boid, boids)
            edge_v = self.avoid_edge(boid)
            fav_v = self.fav_place(boid,self.roam)
            boid.new_v += go_c
            boid.new_v += set_d
            boid.new_v += match_v
            boid.new_v += edge_v
            boid.new_v += fav_v
            
            boid.new_v = self.limit_velocity(boid.new_v)

    def set_distance(self, boid, boids):
        c = Vector2()
        for target in boids:
            if boid == target:
                continue
            distance = boid.pos.distance_to(target.pos)
            if distance < self.min_distance:
                c = c - (boid.pos - target.pos)
        return c

    def go_center(self, boid, boids):
        count = 0
        center = Vector2()
        for target in boids:
            if target == boid:
                continue
            center += target.pos
            count += 1
        center = center / count
        
        return (center - boid.pos) / self.center_factor
            
    def match_velocity(self, boid, boids):
        count = 0
        av = Vector2()
        for target in boids:
            if target != boid:
                continue
            av += target.velocity
            count += 1
        av = av / count
        return (av - boid.velocity) / self.match_factor

    def avoid_edge(self, boid):
        new_v = Vector2()
        if boid.pos.y <= 5:
            new_v.y = 2
        if boid.pos.y >= self.height - 5:
            new_v.y = -2
        if boid.pos.x <= 5:
            new_v.x = 2
        if boid.pos.x >= self.width - 5:
            new_v.x = -2
        return new_v

    def limit_velocity(self, new_v):
        if new_v.magnitude() > self.speed_limit:
            return (new_v / new_v.magnitude()) * self.speed_limit
        return new_v


    def fav_place(self, boid, roam=False):
        if roam:
            x = random.uniform(0, self.width-5)
            y = random.uniform(0, self.height-5)
            corner = [
                (20, 20),
                (1260, 20),
                (20, 700),
                (1260, 700),
            ]
            point = Vector2(random.choice(corner))
        else:
            point = self.fav_point
        return (point - boid.pos) / 10

