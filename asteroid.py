import constants
import pygame
from circleshape import CircleShape
import math
#from random import random, randint
from logger import log_event
import random


class Asteroid(CircleShape):

    def __init__(self, x: float, y: float, radius: float) -> None:
        super().__init__(x, y, radius)
        self.radius = radius
        self.points = []
        d = random.randint(6, 14)
        for t in range(d):
            r = radius * (0.5 + random.random() / 2)
            self.points.append(pygame.Vector2(r*math.sin(t/d * 2 * math.pi), r*math.cos(t/d * 2 * math.pi)))



    def draw(self, screen):
        # pygame.draw.circle(screen, "white", self.position, self.radius, constants.LINE_WIDTH)
        points = list(map(lambda p: p + self.screenPosition, self.points))

        pygame.draw.polygon(screen, (112, 85, 59), points)

    def update(self, dt):
        self.position += self.velocity * dt

    def split(self):
       
        self.kill()
        if self.radius <= constants.ASTEROID_MIN_RADIUS:
            return
        log_event("asteroid_split")

        angle = random.uniform(20, 50)
        v1 =  self.velocity.rotate(angle)
        v2 = self.velocity.rotate(-angle)


        radius = self.radius / 1.4 # constants.ASTEROID_MIN_RADIUS
        a1 = Asteroid(self.position.x, self.position.y, radius)
       
        a1.velocity = v1 * 1.2
            
        a2 = Asteroid(self.position.x, self.position.y, radius)
       
        a2.velocity = v2 * 1.2