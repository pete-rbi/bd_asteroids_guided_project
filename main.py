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

# CH04 L03 FROM SOLUTION FILE
from shot import Shot
# FORFEITED XP -- prim. error player class

def main() -> None:
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    # CH03 L05
    updatable = pygame.sprite.Group() 
    drawable = pygame.sprite.Group()  
    Player.containers = (updatable, drawable)

    # CH04 L01
    asteroids = pygame.sprite.Group()
    # Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = updatable
    #roids = AsteroidField()
    asteroid_field = AsteroidField()
    
    # CH04 L03 - SOLUTION FILE XP FORFEITED
    shots = pygame.sprite.Group()
    Asteroid.containers = (asteroids, updatable, drawable)
    Shot.containers = (shots, updatable, drawable)

    # this line is a very very important line....
    
    # ch03 L02
    player = Player(x = SCREEN_WIDTH / 2, y = SCREEN_HEIGHT / 2)
    
    dt = 0.0
    # game loop
    while True:
        log_state()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        

        # ch03 L02
        # ship.update(dt)
        # ship.draw(screen)

        # CH03 L05 and CH04 L02
        updatable.update(dt)
        for a in asteroids: # sol. file used asteroid, not a
            #  sol. file wrong should be collide_with !
            if a.collide_with(player):
                log_event("player_hit")
                print("Game over!")
                sys.exit()
        screen.fill("black")        

        for p in drawable: # solution used obj, not p
            p.draw(screen)
        
        
        pygame.display.flip()

        # limit the framerate to 60 FPS -- from sol. file
        dt = clock.tick(60) / 1000
                
if __name__ == "__main__":
    main()
