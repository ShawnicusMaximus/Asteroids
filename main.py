import sys
import pygame
from constants import*
from player import*
from circleshape import*
from asteroid import*
from asteroidfield import *


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("ASTEROIDS")
    clock = pygame.time.Clock()
    dt = 0

    updatable = pygame.sprite.Group() 
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    Shot.containers = (shots, updatable, drawable)
    
    AsteroidField.containers = (updatable,)

    asteroid_field = AsteroidField()

    Player.containers = (updatable, drawable)

    player = Player((SCREEN_WIDTH/2), (SCREEN_HEIGHT/2))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return


        updatable.update(dt)
        for asteroid in asteroids:
            if circle_triangle_collision(asteroid.position, asteroid.radius, *player.triangle()):
                print("Game Over!")
                sys.exit()
        
            for shot in shots:
                if asteroid.collision(shot):
                    shot.kill() 
                    asteroid.split()
            
        screen.fill("black")

        for obj in drawable:
            obj.draw(screen)
        
        pygame.display.flip()

        # limit the framerate to 60 FPS
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()

