import pygame
from circleshape import* 
from constants import*
from asteroid import*

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)

        self.rotation = 0
        self.shoot_timer = 0
        self.velocity = pygame.Vector2(0,0)

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    
    def draw(self, screen):
        player_sprite = pygame.draw.polygon(screen, "white", self.triangle(),2)

    def rotate(self,dt):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.rotation += (PLAYER_TURN_SPEED* -dt)
        if keys[pygame.K_d]:
            self.rotation += (PLAYER_TURN_SPEED* dt)
    
    def screen_wrap(self):
            self.position.x %= SCREEN_WIDTH
            self.position.y %= SCREEN_HEIGHT

    def update(self, dt):
        self.shoot_timer -= dt
        keys = pygame.key.get_pressed()
        self.move(dt)
        self.rotate(dt)
        
        
        if keys[pygame.K_SPACE]:
            self.shoot()
        
        ## Screen Wrap ##
        self.position.x %= SCREEN_WIDTH
        self.position.y %= SCREEN_HEIGHT
        self.velocity *= FRICTION
    
    

    def move(self, dt):
        keys = pygame.key.get_pressed()
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        # Apply acceleration when moving forward
        if keys[pygame.K_w]:
            self.velocity += forward * ACCELERATION_RATE * dt
        if keys[pygame.K_s]:
            self.velocity -= forward * ACCELERATION_RATE * dt
        
        # Apply friction (slows down when no input)
        self.velocity *= FRICTION

        # Update position based on velocity
        self.position += self.velocity * dt

        if self.velocity.length() > PLAYER_SPEED:
            self.velocity = self.velocity.normalize() * PLAYER_SPEED




    def shoot(self):
        if self.shoot_timer >0:
            return
        
        self.shoot_timer = PLAYER_SHOOT_COOLDOWN
        shot = Shot(self.position.x,self.position.y)
        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
