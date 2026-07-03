import constants
import pygame
from circleshape import CircleShape
import random
from player import Player

class Powerup(CircleShape):

    def __init__(self, x: float, y: float, radius: float) -> None:
        super().__init__(x, y, radius)
        
        
    def draw(self, screen):
       

        pygame.draw.circle(screen, "Green", self.screenPosition, 15)

    def update(self, dt):
        
        pass






    