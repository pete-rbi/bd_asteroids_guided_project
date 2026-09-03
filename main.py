import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from logger import log_state

# CH03 L02
from constants import PLAYER_RADIUS, LINE_WIDTH
from player import Player

# CH04 L01
from asteroidfield import AsteroidField
from asteroid import Asteroid

# CH04 L02
from logger import log_event
import sys

def main():
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    pygame.init()
    
    # CH03 L05
    updatable = pygame.sprite.Group() 
    drawable = pygame.sprite.Group()  
    Player.containers = (updatable, drawable)

    # CH04 L01
    asteroids = pygame.sprite.Group()
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
    roids = AsteroidField()
    
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    clock = pygame.time.Clock()

    # ch03 L02
    ship = Player(x = SCREEN_WIDTH / 2, y = SCREEN_HEIGHT / 2)
    
    dt = 0.0
    # game loop
    while True:
        # 1. Check for player inputs
        # 2. Update the game world
        # 3. Draw the game to the screen
        log_state()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        screen.fill("black")

        # ch03 L02
        # ship.update(dt)
        # ship.draw(screen)

        # CH03 L05 and CH04 L02
        updatable.update(dt)
        for a in asteroids:
            if a.collide_with(ship):
                log_event("player_hit")
                print("Game over!")
                sys.exit()
                
        for p in drawable:
            p.draw(screen)
        
        
        pygame.display.flip()
        dt = clock.tick(60) / 1000
        
        
if __name__ == "__main__":
    main()
