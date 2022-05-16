import random

import pygame
from pygame.math import Vector2
from boid import Boid, Behavior


WIDTH = 1280
HEIGHT = 720
BOID_COUNT = 15
ROAMING = False

def boid_factory(count=10):
    for _ in range(count):
        x = random.uniform(10, WIDTH-10)
        y = random.uniform(10, HEIGHT-10)
        color = (255,255,255)
        velocity = (random.uniform(-1,1), random.uniform(-1,1))
        boid = Boid((x, y), velocity=velocity, color=color)
        yield boid
    

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH,HEIGHT))

    all_sprites = pygame.sprite.Group()
    
    for boid in boid_factory(BOID_COUNT):
        all_sprites.add(boid)
    running = True
    clock = pygame.time.Clock()
    behavior = Behavior(height=HEIGHT, width=WIDTH, roam=ROAMING)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                print(event.pos)
                behavior.fav_point = Vector2(event.pos)
        behavior.change_state(all_sprites)

        screen.fill((0,0,0))
        all_sprites.update()
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(10)

    pygame.quit()

if __name__ == "__main__":
    main()
