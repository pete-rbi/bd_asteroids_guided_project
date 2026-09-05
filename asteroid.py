# CH04 L01
import pygame,random
from constants import LINE_WIDTH, ASTEROID_MIN_RADIUS
from circleshape import CircleShape
from logger import log_event

class Asteroid(CircleShape):
    def __init__(self, x: float, y: float, radius: float) -> None:
        super().__init__(x, y, radius)

    def draw(self, screen:pygame.Surface):
        pygame.draw.circle(screen,"white",self.position, self.radius, LINE_WIDTH)

    def update(self, dt: float):
       self.position +=  self.velocity * dt
       
    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        log_event("asteroid_split")
        r_angle = random.uniform(20, 50)
        # print(f"random angle = {r_angle}")
        

        n_vec_1 = self.velocity.rotate(r_angle) # ch4l06 3.3
        n_vec_2 = self.velocity.rotate(-r_angle) # ch4l06 3.4
        # print(f"n_vec_1 = {n_vec_1}, {r_angle}")
        # print(f"n_vec_2 = {n_vec_2}")

        # n_radius = old_radius - ASTEROID_MIN_RADIUS ch4l06 3.5
        n_radius = self.radius - ASTEROID_MIN_RADIUS
        # print(f"n_radius = {n_radius}")

        n_aster_1 = Asteroid(self.position.x, self.position.y,n_radius) # ch4l06 3.6
        n_aster_2 = Asteroid(self.position.x, self.position.y,n_radius)
        
        n_aster_1.velocity = n_vec_1 * 1.2 # ch4106 3.7
        n_aster_2.velocity = n_vec_2 * 1.2 # ch4l06 3.8
        
        
        return # checked
