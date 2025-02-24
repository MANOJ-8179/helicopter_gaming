import os
import pygame
import random
from flask import Flask, render_template

# Initialize Flask app
app = Flask(__name__)

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Game settings
HELICOPTER_WIDTH = 120
HELICOPTER_HEIGHT = 100
OBSTACLE_WIDTH = 70
OBSTACLE_HEIGHT = 300
OBSTACLE_GAP = 200
OBSTACLE_SPEED = 5

# Load helicopter image
image_path = os.path.join("static", "helicopter.png")  # Ensure the correct path
if not os.path.exists(image_path):
    raise FileNotFoundError("Error: 'helicopter.png' not found. Please place it in the 'static' folder.")

helicopter_image = pygame.image.load(image_path)
helicopter_image = pygame.transform.scale(helicopter_image, (HELICOPTER_WIDTH, HELICOPTER_HEIGHT))

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Helicopter Game")

# Clock for controlling frame rate
clock = pygame.time.Clock()

def draw_helicopter(x, y):
    screen.blit(helicopter_image, (x, y))

def draw_obstacle(x, y, width, height):
    pygame.draw.rect(screen, GREEN, [x, y, width, height])
    pygame.draw.rect(screen, GREEN, [x, y + height + OBSTACLE_GAP, width, SCREEN_HEIGHT - (y + height + OBSTACLE_GAP)])

def show_message(message, color, size, position):
    font = pygame.font.SysFont(None, size)
    text = font.render(message, True, color)
    screen.blit(text, position)

def game_loop():
    # Game variables
    x = 100
    y = 300
    y_change = 0
    obstacle_x = SCREEN_WIDTH
    obstacle_y = random.randint(-150, 150)
    game_over = False
    score = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    y_change = -5
                if event.key == pygame.K_DOWN:
                    y_change = 5
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    y_change = 0

        if not game_over:
            y += y_change
            screen.fill(BLACK)

            # Draw the helicopter
            draw_helicopter(x, y)

            # Draw the obstacles
            draw_obstacle(obstacle_x, obstacle_y, OBSTACLE_WIDTH, OBSTACLE_HEIGHT)

            # Move the obstacles
            obstacle_x -= OBSTACLE_SPEED

            if obstacle_x < -OBSTACLE_WIDTH:
                obstacle_x = SCREEN_WIDTH
                obstacle_y = random.randint(-150, 150)
                score += 1

            # Check for collisions
            if y > SCREEN_HEIGHT - HELICOPTER_HEIGHT or y < 0:
                game_over = True
            if (x + HELICOPTER_WIDTH > obstacle_x and x < obstacle_x + OBSTACLE_WIDTH) and (y < obstacle_y + OBSTACLE_HEIGHT or y + HELICOPTER_HEIGHT > obstacle_y + OBSTACLE_HEIGHT + OBSTACLE_GAP):
                game_over = True

            # Display the score
            show_message(f"Score: {score}", WHITE, 35, (10, 10))

            pygame.display.update()
            clock.tick(60)
        else:
            screen.fill(BLACK)
            show_message("Game Over", RED, 75, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50))
            show_message(f"Final Score: {score}", WHITE, 50, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2))
            show_message("Press R to Restart or Q to Quit", WHITE, 30, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 + 50))
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        game_loop()
                        return
                    if event.key == pygame.K_q:
                        pygame.quit()
                        return

@app.route("/")
def index():
    return render_template("index.html")  # Renders the front-end (if needed)

if __name__ == "__main__":
    game_loop()  # Run locally
