import pygame
import random
import os
import sys

# Screen dimensions - typically you'd set these to your display resolution for fullscreen
SCREEN_WIDTH = 1900
SCREEN_HEIGHT = 1200

# Define colors
RED = (255, 0, 0)
GOLD = (255, 215, 0)
GREEN = (0, 128, 0)

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Adinkra Screensaver")

ADINKRA_FOLDER = "adinkra_symbols"
ADINKRA_SYMBOLS = []

for filename in os.listdir(ADINKRA_FOLDER):
    if filename.endswith(".png"):
        try:
            symbol = pygame.image.load(os.path.join(ADINKRA_FOLDER, filename)).convert_alpha()
            ADINKRA_SYMBOLS.append(symbol)
        except pygame.error as e:
            print(f"Failed to load image {filename}: {e}")

if not ADINKRA_SYMBOLS:
    print("No symbols found in the directory.")
    pygame.quit()
    sys.exit()

class AdinkraSymbol:
    def __init__(self):
        self.image = random.choice(ADINKRA_SYMBOLS)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(-SCREEN_HEIGHT, 0)
        self.speed = random.randint(1, 3)

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > SCREEN_HEIGHT:
            self.rect.y = -self.rect.height
            self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)

def main():
    clock = pygame.time.Clock()
    symbols = [AdinkraSymbol() for _ in range(1000)]  # Create 800 Adinkra symbols
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False  # Exit on ESC

        screen.fill((0, 0, 0))  # Fill the screen with black before drawing symbols

        for symbol in symbols:
            symbol.update()
            screen.blit(symbol.image, symbol.rect)

        pygame.display.flip()  # Update the full display surface to the screen
        clock.tick(120)  # Limit to 60 frames per second

    pygame.quit()

if __name__ == "__main__":
    main()
