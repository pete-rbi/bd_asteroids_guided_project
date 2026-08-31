import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from logger import log_state

# CH03 L02
from constants import PLAYER_RADIUS, LINE_WIDTH
from player import Player

def main():
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    clock = pygame.time.Clock()

    # ch03 L02
    ship = Player(x = SCREEN_WIDTH / 2, y = SCREEN_HEIGHT / 2)
    print(type(ship))
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
        ship.draw(screen)
        
        pygame.display.flip()
        dt = clock.tick(60) / 1000
        
        
if __name__ == "__main__":
    main()
