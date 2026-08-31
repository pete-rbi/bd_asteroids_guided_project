# CH03 L02
# do I need to import pygame ?
import pygame
from circleshape import CircleShape
from constants import PLAYER_RADIUS, LINE_WIDTH


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

    def draw(self, screen: pygame.Surface) -> None:
        return pygame.draw.polygon(screen,"white",self.triangle(), LINE_WIDTH)

    
