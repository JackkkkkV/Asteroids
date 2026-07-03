import pygame
import constants

# Base class for game objects
class CircleShape(pygame.sprite.Sprite):
    containers: tuple[pygame.sprite.Group, ...]

    def __init__(self, x: float, y: float, radius: float) -> None:
        # we will be using this later
        if hasattr(self, "containers"):
            super().__init__(*self.containers)
        else:
            super().__init__()

        self.offset = pygame.Vector2(0, 0)
        self.position: pygame.Vector2 = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius

    @property
    def screenPosition(self):
        return self.position - self.offset + pygame.Vector2(constants.SCREEN_WIDTH / 2, constants.SCREEN_HEIGHT / 2)
        
    def draw(self, screen: pygame.Surface) -> None:
        # must override
        pass

    def update(self, dt: float) -> None:
        # must override
        pass
        
    def collides_with(self, other) -> bool: 

        if other.radius == constants.PLAYER_RADIUS:
             if ((self.radius + other.radius + 10) >= self.position.distance_to(other.position)):
                return True
             else:
                 return False
        else:
            if ((self.radius + other.radius - 20) >= self.position.distance_to(other.position)):
                 return True
            else:
                 return False
    
        