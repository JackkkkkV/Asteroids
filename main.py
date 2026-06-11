import pygame
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from player import *
from logger import log_state
from asteroid import Asteroid
from asteroidfield import AsteroidField
def main():
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0.0

    

    #Groups
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()

    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
    #Player
    Player.containers = (updatable, drawable)
    player = Player((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2))
    asteroidField = AsteroidField()
    #game loop
    while True:
        dt = clock.tick(60)/ 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
             return
        
        updatable.update(dt)
        screen.fill("black")
        for item in drawable:
            item.draw(screen)
        log_state()
        pygame.display.flip()
       

if __name__ == "__main__":
    main()
