import constants
from circleshape import CircleShape
import pygame
from shot import Shot

class Player(CircleShape):

    def __init__(self, x, y):
        super().__init__(x, y, constants.PLAYER_RADIUS)
        self.rotation = 0
        self.type = "Player"
        self.rot = 0
        self.cooldown = 0
        self.shotgun = False
        self.sprite = pygame.image.load("ship.png").convert_alpha()
        self.sprite_scaled = pygame.transform.scale(self.sprite, (250, 200))
        self.rocket_sound_cooldown = 0
        self.speed = 0
        
    def triangle(self) -> list[pygame.Vector2]:
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.screenPosition + forward * self.radius
        b = self.screenPosition - forward * self.radius - right
        c = self.screenPosition - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen: pygame.Surface):
        #pygame.draw.polygon(screen, "white", self.triangle(), constants.LINE_WIDTH)

        rotated_scaled_sprite = pygame.transform.rotate(self.sprite_scaled, -self.rotation - 180)
        self.sprite_rect = rotated_scaled_sprite.get_rect(center= (self.screenPosition))
        screen.blit(rotated_scaled_sprite, self.sprite_rect)

    def rotate(self, dt):
        self.rot += (constants.PLAYER_TURN_SPEED * dt)
        self.rotation = self.rot

    def update(self, dt: float) -> None:
        
        self.cooldown -= dt
        self.cooldown = max(self.cooldown, 0)
        self.rocket_sound_cooldown -= dt
        self.rocket_sound_cooldown = max(self.rocket_sound_cooldown, 0)
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt)
            if self.rocket_sound_cooldown > 0:
                pass
            else:
                pygame.mixer.Sound("rocket_sound.mp3").set_volume(0.5)
                pygame.mixer.Sound("rocket_sound.mp3").play()
                self.rocket_sound_cooldown = constants.ROCKET_SOUND_COOLDOWN_SECONDS
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_SPACE]:
            self.shoot()
        if keys[pygame.K_LSHIFT]:
            constants.PLAYER_SPEED = 400


        #Deceleration
        elif keys == False:
            if self.speed (0.001 < 0):
                self.speed = 0
            else:
                self.speed *= constants.FRICTION


        #Acceleration effect    
        else:
           if not keys[pygame.K_w] and not keys[pygame.K_s]:
               constants.PLAYER_SPEED = 0
           elif constants.PLAYER_SPEED < 200:
                constants.PLAYER_SPEED += 5
           elif constants.PLAYER_SPEED >= 200:
                
                constants.PLAYER_SPEED = 200
                
    def move(self, dt):
        unit_vector = pygame.Vector2(0, 1)
        rotated_vector = unit_vector.rotate(self.rotation)
        rotated_with_speed_vector = rotated_vector * constants.PLAYER_SPEED * dt
        self.speed = rotated_with_speed_vector
        self.position += self.speed
        # if self.position.y < 0:
        #     self.position.y = constants.SCREEN_HEIGHT
        # elif self.position.y > constants.SCREEN_HEIGHT:
        #     self.position.y = 0
        # if self.position.x < 0:
        #     self.position.x = constants.SCREEN_WIDTH
        # elif self.position.x > constants.SCREEN_WIDTH:
        #     self.position.x = 0
    def shoot(self):
        

        if self.cooldown > 0:
            return
        else:
            pygame.mixer.Sound("shot_sound.mp3").play()
            
            
            shot = Shot(self.position, constants.SHOT_RADIUS)
       
            shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * constants.PLAYER_SHOOT_SPEED
            self.cooldown = constants.PLAYER_SHOOT_COOLDOWN_SECONDS
            if self.shotgun:
                shotL = Shot(self.position, constants.SHOT_RADIUS)
       
                shotL.velocity = pygame.Vector2(0, 1).rotate(self.rotation - 10) * constants.PLAYER_SHOOT_SPEED

                shotR = Shot(self.position, constants.SHOT_RADIUS)
       
                shotR.velocity = pygame.Vector2(0, 1).rotate(self.rotation + 10) * constants.PLAYER_SHOOT_SPEED




    