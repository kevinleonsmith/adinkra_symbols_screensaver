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
    def __init__(self, has_trail):
        self.image = random.choice(ADINKRA_SYMBOLS)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(-SCREEN_HEIGHT, 0)
        self.speed = random.randint(1, 11)
        self.has_trail = has_trail
        self.trail = []  # To store previous positions for the vapor trail

    def update(self):
        if self.has_trail:
            self.trail.append((self.rect.x, self.rect.y))
            if len(self.trail) > 10:  # Limit trail length
                self.trail.pop(0)
        self.rect.y += self.speed
        if self.rect.y > SCREEN_HEIGHT:
            self.rect.y = -self.rect.height
            self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
            if self.has_trail:
                self.trail.clear()  # Clear trail on reset

    def draw(self, surface):
        if self.has_trail:
            for i, pos in enumerate(self.trail):
                alpha = int(255 * (i / len(self.trail)))  # Calculate alpha value
                trail_image = self.image.copy()
                trail_image.fill((255, 255, 255, alpha), special_flags=pygame.BLEND_RGBA_MULT)
                surface.blit(trail_image, pos)
        surface.blit(self.image, self.rect.topleft)

def main():
    clock = pygame.time.Clock()
    symbols = [AdinkraSymbol(has_trail=random.random() < 0.13) for _ in range(2000)]  # 33% have trails
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
            symbol.draw(screen)

        pygame.display.flip()  # Update the full display surface to the screen
        clock.tick(120)  # Limit to 120 frames per second

    pygame.quit()

if __name__ == "__main__":
    main()
