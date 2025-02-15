import pygame
import math
from circleshape import* 
from constants import*
from asteroid import*

def area(p1, p2, p3):
    return abs((p1.x * (p2.y - p3.y) + p2.x * (p3.y - p1.y) + p3.x * (p1.y - p2.y)) / 2.0)

def point_in_triangle(pt, v1, v2, v3):
    area_abc = area(v1, v2, v3)
    area_pab = area(pt, v1, v2)
    area_pbc = area(pt, v2, v3)
    area_pca = area(pt, v3, v1)
    return area_abc == area_pab + area_pbc + area_pca

# Distance function
def distance(p1, p2):
    return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)

# Get the closest point on a line segment to a point
def closest_point_on_line_segment(p, v1, v2):
    line_vec = v2 - v1
    p_vec = p - v1
    line_len = line_vec.length()
    if line_len == 0: return v1
    line_vec.normalize_ip()
    t = p_vec.dot(line_vec)
    t = max(0, min(t, line_len))
    return v1 + line_vec * t

# Circle-Triangle collision check
def circle_triangle_collision(circle_center, radius, v1, v2, v3):
    # Check if the circle's center is inside the triangle
    if point_in_triangle(circle_center, v1, v2, v3):
        return True
    
    # Check if the circle intersects any of the triangle's edges
    edges = [(v1, v2), (v2, v3), (v3, v1)]
    for edge_start, edge_end in edges:
        closest_point = closest_point_on_line_segment(circle_center, edge_start, edge_end)
        if distance(circle_center, closest_point) < radius:
            return True
    
    return False

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
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            if self.shoot_timer >0:
                return
            
            self.shoot_timer = PLAYER_SHOOT_COOLDOWN
            shot = Shot(self.position.x,self.position.y)
            shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED

