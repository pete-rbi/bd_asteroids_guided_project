import pygame
# You need to have pygame installed.
import sys
import random
from collections.abc import Callable

# from constants.py
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
PLAYER_RADIUS = 20
LINE_WIDTH = 2
PLAYER_TURN_SPEED = 300
PLAYER_SPEED = 200
ASTEROID_MIN_RADIUS = 20
ASTEROID_KINDS = 3
ASTEROID_SPAWN_RATE_SECONDS = 0.8
ASTEROID_MAX_RADIUS = ASTEROID_MIN_RADIUS * ASTEROID_KINDS
SHOT_RADIUS = 5
PLAYER_SHOOT_SPEED = 500
PLAYER_SHOOT_COOLDOWN_SECONDS = 0.3


# circlespace.py
# Base class for game objects
class CircleShape(pygame.sprite.Sprite):
    containers: tuple[pygame.sprite.Group, ...]

    def __init__(self, x: float, y: float, radius: float) -> None:
        # we will be using this later
        if hasattr(self, "containers"):
            super().__init__(*self.containers)
        else:
            super().__init__()

        self.position: pygame.Vector2 = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius

    def draw(self, screen: pygame.Surface) -> None:
        # must override
        pass

    def update(self, dt: float) -> None:
        # must override
        pass

    # CH04 L02
    def collides_with(self, other):
        sum_r = self.radius + other.radius
        dist = pygame.math.Vector2.distance_to(self.position, other.position)
        return dist <= sum_r


# player.py

class Player(CircleShape):
    def __init__(self, x:float, y:float) -> None:
        super().__init__(x, y, radius = PLAYER_RADIUS)
        self.rotation = 0.0
        self.cooldown = 0.0 
        
    # in the Player class
    def triangle(self) -> list[pygame.Vector2]:
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen: pygame.Surface):
        pygame.draw.polygon(screen,"white",self.triangle(), LINE_WIDTH)

    # CH03 L03
    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt 
        

    def update(self, dt: float) -> None:
        self.cooldown -= dt 
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_SPACE]: 
            if self.cooldown > 0: 
                pass
            else:
                self.shoot()
                self.cooldown = PLAYER_SHOOT_COOLDOWN_SECONDS

    def shoot(self) -> None:
        shot = Shot(self.position.x, self.position.y)
        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
    
    
    def move(self, dt: float) -> None:
        unit_vector = pygame.Vector2(0, 1)
        rotated_vector = unit_vector.rotate(self.rotation)
        rotated_with_speed_vector = rotated_vector * PLAYER_SPEED * dt
        self.position += rotated_with_speed_vector


# asteroid.py

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
        
        r_angle = random.uniform(20, 50)
        
        

        n_vec_1 = self.velocity.rotate(r_angle)
        n_vec_2 = self.velocity.rotate(-r_angle) 
        

        
        n_radius = self.radius - ASTEROID_MIN_RADIUS
        

        n_aster_1 = Asteroid(self.position.x, self.position.y,n_radius) # ch4l06 3.6
        n_aster_2 = Asteroid(self.position.x, self.position.y,n_radius)
        
        n_aster_1.velocity = n_vec_1 * 1.2 # ch4106 3.7
        n_aster_2.velocity = n_vec_2 * 1.2 # ch4l06 3.8
        return

# asteroidfield.py

# moved into class AsteroidField
# Edge = tuple[pygame.Vector2, Callable[[float], pygame.Vector2]]


class AsteroidField(pygame.sprite.Sprite):
    containers: pygame.sprite.Group

    Edge = tuple[pygame.Vector2, Callable[[float], pygame.Vector2]]
    
    edges: list[Edge] = [
        (
            pygame.Vector2(1, 0),
            lambda y: pygame.Vector2(-ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT),
        ),
        (
            pygame.Vector2(-1, 0),
            lambda y: pygame.Vector2(
                SCREEN_WIDTH + ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT
            ),
        ),
        (
            pygame.Vector2(0, 1),
            lambda x: pygame.Vector2(x * SCREEN_WIDTH, -ASTEROID_MAX_RADIUS),
        ),
        (
            pygame.Vector2(0, -1),
            lambda x: pygame.Vector2(
                x * SCREEN_WIDTH, SCREEN_HEIGHT + ASTEROID_MAX_RADIUS
            ),
        ),
    ]

    def __init__(self) -> None:
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.spawn_timer = 0.0

    def spawn(
        self, radius: float, position: pygame.Vector2, velocity: pygame.Vector2
    ) -> None:
        asteroid = Asteroid(position.x, position.y, radius)
        asteroid.velocity = velocity

    def update(self, dt: float) -> None:
        self.spawn_timer += dt
        if self.spawn_timer > ASTEROID_SPAWN_RATE_SECONDS:
            self.spawn_timer = 0

            # spawn a new asteroid at a random edge
            edge = random.choice(self.edges)
            speed = random.randint(40, 100)
            velocity = edge[0] * speed
            velocity = velocity.rotate(random.randint(-30, 30))
            position = edge[1](random.uniform(0, 1))
            kind = random.randint(1, ASTEROID_KINDS)
            self.spawn(ASTEROID_MIN_RADIUS * kind, position, velocity)


# shot.py

class Shot(CircleShape):
    def __init__(self, x: float, y: float) -> None:
        super().__init__(x, y, SHOT_RADIUS)

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)

    def update(self, dt: float) -> None:
        self.position += self.velocity * dt


# main.py

def main() -> None:
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    print("Code from:")
    print("boot.dev 'Asteroid Guided Project' course")
    print("pete-rbi edited it down to one file *main.py*")    
    print()
    print("#########################")
    print("Keyboard Button Control")
    print("Press 'w' to go forward")
    print("Press 's' to go backwards")
    print("Press 'a' to rotate left")
    print("Press 'd' to rotate right")
    print("Press 'spacebar' to fire")
    print("##########################")
    
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    
    updatable = pygame.sprite.Group() 
    drawable = pygame.sprite.Group()  
    Player.containers = (updatable, drawable)

    
    asteroids = pygame.sprite.Group()
    
    AsteroidField.containers = updatable
    
    asteroid_field = AsteroidField()
    
    
    shots = pygame.sprite.Group()
    Asteroid.containers = (asteroids, updatable, drawable)
    Shot.containers = (shots, updatable, drawable)

    # this line is a very very important line....
    
    
    player = Player(x = SCREEN_WIDTH / 2, y = SCREEN_HEIGHT / 2)
    
    dt = 0.0
    running = True
    # game loop
    while running:
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Game quit!")
                running = False
        

        

        
        updatable.update(dt)
        for asteroid in asteroids: 
            
            if asteroid.collides_with(player):
                
                print("Game over!")
                running = False
                # sys.exit()

        for asteroid in asteroids: 
            for shot in shots:
                if shot.collides_with(asteroid):
                    
                    shot.kill()
                    # asteroid.kill()
                    asteroid.split() 
                    

        screen.fill("black")        

        for p in drawable: 
            p.draw(screen)
        
        
        pygame.display.flip()

        
        dt = clock.tick(60) / 1000
                
if __name__ == "__main__":
    main()
    pygame.quit()
    # sys.exit()
 
