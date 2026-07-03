import pygame
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from player import *
from logger import log_state, log_event
from asteroid import Asteroid
from asteroidfield import AsteroidField
import sys
from shot import Shot
from powerup import Powerup
import random
import constants
import time




def main():
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0.0
    
    pygame.mixer.music.load("music.mp3")
    pygame.mixer.music.play(loops=-1)
    pygame.mixer.music.set_volume(0.5)


    #background
    bg_image = pygame.image.load("background.jpg").convert()
    bg_image = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))  

    #Groups
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    powerups = pygame.sprite.Group()

    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
    Powerup.containers = (powerups, updatable, drawable)
    #Player
    Player.containers = (updatable, drawable)
    Shot.containers = (shots, updatable, drawable)
    
    player = Player((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2))
    asteroidField = AsteroidField()

    #scoreboard
    invincibility = 0
    score_value = 0
    lives_value = 3
    font = pygame.font.Font('freesansbold.ttf', 24)
    
    def rendscore():
        
        score = font.render("Score: " + str(score_value), True, (255, 255, 255))
        screen.blit(score, (54, 25))

        lives = font.render("Lives: " + str(lives_value), True, (255, 255, 255))
        screen.blit(lives, (54, 50))
        return


    #upgrades
    
    powerup_count = 20
    powerup_duration = 0
    
    
        
    #game loop
    while True:
        dt = clock.tick(60)/1000
        asteroidField.offset = player.position -  pygame.Vector2(constants.SCREEN_WIDTH / 2, constants.SCREEN_HEIGHT / 2)
        invincibility -= 1
        invincibility = max(invincibility, 0)
        if powerup_count <= 0:
            randomX = random.randint(0, constants.SCREEN_WIDTH)
            randomY = random.randint(0, constants.SCREEN_HEIGHT)

            powerup = Powerup(randomX, randomY, 15)
            powerup.draw(screen)
            powerup_count = 20

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
             return
        
        updatable.update(dt)

        
        if powerup_duration <= 0:
            constants.PLAYER_SHOOT_COOLDOWN_SECONDS = 0.3
            player.shotgun = False
        for item in asteroids:
            
            if item.position.distance_to(player.position) > constants.SCREEN_WIDTH * 2:
                item.kill()
                

            if item.collides_with(player):

                if (lives_value > 0) and (invincibility <= 0):
                    lives_value -= 1
                    invincibility = 120
                    
                        
                if lives_value == 0:
                    log_event("player_hit")
                    print("Game over!")
                    print(f"Score: {score_value}")
                    sys.exit()
            
            for shot in shots:
                if item.collides_with(shot):
                    log_event("asteroid_shot")
                    item.split()
                    shot.kill()
                    score_value += 1
                    powerup_count -= 1
                    powerup_duration -= 1
        for item in powerups:
            if item.collides_with(player):
                constants.PLAYER_SHOOT_SPEED += 50
                powerup_duration = 30
                if powerup_duration > 0:
                    constants.PLAYER_SHOOT_COOLDOWN_SECONDS -= 0.2
                    player.shotgun = True
                score_value += 50
                
                item.kill()
        screen.blit(bg_image, (0, 0))
       # screen.fill("black")
        for item in drawable:
            item.offset = player.position
            item.draw(screen)
        rendscore()

        log_state()
        pygame.display.flip()
       

if __name__ == "__main__":
    main()
