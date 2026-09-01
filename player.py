# CH03 L02
# do I need to import pygame ?
import pygame
from circleshape import CircleShape
from constants import PLAYER_RADIUS, LINE_WIDTH
# CH03 L03
from constants import PLAYER_TURN_SPEED
# CH04 LO4
from constants import PLAYER_SPEED

class Player(CircleShape):
    def __init__(self, x:float, y:float):
        super().__init__(x, y, radius = PLAYER_RADIUS )
        rotation = 0
        self.rotation = rotation
    # in the Player class
    def triangle(self) -> list[pygame.Vector2]:
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen: pygame.Surface):
        # CH03 L04 removed 'return' from begining of bottom line , now jq == True
        pygame.draw.polygon(screen,"white",self.triangle(), LINE_WIDTH)

    # CH03 L03
    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt 
        

    def update(self, dt: float) -> None:
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)

        # CH03 L04
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)

    # CH03 L04
    def move(self, dt):
        unit_vector = pygame.Vector2(0, 1)
        rotated_vector = unit_vector.rotate(self.rotation)
        rotated_with_speed_vector = rotated_vector * PLAYER_SPEED * dt
        self.position += rotated_with_speed_vector
        

