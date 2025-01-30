import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Game settings
WIDTH, HEIGHT = 800, 600
PLAYER_SPEED = 5
ENEMY_SPEED = 2  # Initial enemy speed
ENEMY_ACCELERATION = 0.2  # Speed increase per score
NEW_ENEMY_THRESHOLD = 5  # Add a new enemy every 5 points

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
COLORS = {
    "blue": (0, 0, 200),
    "red": (200, 0, 0),
    "green": (0, 200, 0),
    "yellow": (200, 200, 0),
    "purple": (150, 0, 150),
    "orange": (255, 165, 0),
    "pink": (255, 192, 203),
    "cyan": (0, 255, 255),
    "brown": (165, 42, 42),
    "gray": (128, 128, 128)
}
SHAPES = ["rectangle", "circle", "triangle", "star", "hexagon"]

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame - Choose Shape & Color")

# Font setup
pygame.font.init()
font = pygame.font.Font(None, 48)
title_font = pygame.font.Font(None, 64)  # Larger font for titles

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Load sounds
pygame.mixer.init()
collision_sound = pygame.mixer.Sound("mixkit-player-losing-or-failing-2042.wav")  # Replace with your sound file
score_sound = pygame.mixer.Sound("mixkit-winning-a-coin-video-game-2069.wav")  # Replace with your sound file
menu_music = pygame.mixer.Sound("The Adventure Begins 8-bit remix.wav")  # Replace with your menu music file
game_music = pygame.mixer.Sound("06. Spring (The Valley Comes Alive).wav")  # Replace with your game music file

# Play menu music
menu_music.play(-1)  # Loop indefinitely


def draw_text(text, size, x, y, color=BLACK, font_type=None):
    """Function to draw text on the screen."""
    if font_type is None:
        font_type = pygame.font.Font(None, size)
    text_surface = font_type.render(text, True, color)
    screen.blit(text_surface, (x, y))


def draw_button(text, x, y, width, height, color, hover_color, action=None):
    """Function to draw a button with hover effect."""
    mouse_pos = pygame.mouse.get_pos()
    clicked = pygame.mouse.get_pressed()

    # Smooth hover effect
    if x + width > mouse_pos[0] > x and y + height > mouse_pos[1] > y:
        pygame.draw.rect(screen, hover_color, (x, y, width, height), border_radius=10)
        if clicked[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(screen, color, (x, y, width, height), border_radius=10)

    draw_text(text, 36, x + 10, y + 10, WHITE)


def draw_shape(shape, color, rect):
    """Function to draw different shapes."""
    if shape == "rectangle":
        pygame.draw.rect(screen, color, rect, border_radius=10)
    elif shape == "circle":
        pygame.draw.ellipse(screen, color, rect)
    elif shape == "triangle":
        pygame.draw.polygon(
            screen,
            color,
            [(rect.x + rect.width // 2, rect.y),  # Top
             (rect.x, rect.y + rect.height),  # Bottom left
             (rect.x + rect.width, rect.y + rect.height)]  # Bottom right
        )
    elif shape == "star":
        pygame.draw.polygon(
            screen,
            color,
            [(rect.x + rect.width // 2, rect.y),  # Top
             (rect.x + rect.width * 0.4, rect.y + rect.height * 0.4),  # Left middle
             (rect.x, rect.y + rect.height * 0.4),  # Left top
             (rect.x + rect.width * 0.3, rect.y + rect.height * 0.6),  # Left bottom
             (rect.x + rect.width * 0.2, rect.y + rect.height),  # Bottom left
             (rect.x + rect.width // 2, rect.y + rect.height * 0.7),  # Bottom middle
             (rect.x + rect.width * 0.8, rect.y + rect.height),  # Bottom right
             (rect.x + rect.width * 0.7, rect.y + rect.height * 0.6),  # Right bottom
             (rect.x + rect.width, rect.y + rect.height * 0.4),  # Right top
             (rect.x + rect.width * 0.6, rect.y + rect.height * 0.4)]  # Right middle
        )
    elif shape == "hexagon":
        pygame.draw.polygon(
            screen,
            color,
            [(rect.x + rect.width * 0.25, rect.y),  # Top left
             (rect.x + rect.width * 0.75, rect.y),  # Top right
             (rect.x + rect.width, rect.y + rect.height * 0.5),  # Right middle
             (rect.x + rect.width * 0.75, rect.y + rect.height),  # Bottom right
             (rect.x + rect.width * 0.25, rect.y + rect.height),  # Bottom left
             (rect.x, rect.y + rect.height * 0.5)]  # Left middle
        )


def fade_in():
    """Fade-in effect for transitions."""
    fade_surface = pygame.Surface((WIDTH, HEIGHT))
    fade_surface.fill(BLACK)
    for alpha in range(0, 255, 5):
        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0, 0))
        pygame.display.flip()
        pygame.time.delay(30)


def fade_out():
    """Fade-out effect for transitions."""
    fade_surface = pygame.Surface((WIDTH, HEIGHT))
    fade_surface.fill(BLACK)
    for alpha in range(255, 0, -5):
        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0, 0))
        pygame.display.flip()
        pygame.time.delay(30)


def pause_menu():
    """Pause menu where player can resume, restart, or quit."""
    paused = True
    game_music.stop()  # Stop game music when paused
    while paused:
        screen.fill(WHITE)
        draw_text("Game Paused", 64, WIDTH // 3, HEIGHT // 4, BLACK, title_font)

        def resume():
            nonlocal paused
            paused = False
            game_music.play(-1)  # Resume game music

        def restart():
            nonlocal paused
            paused = False
            game_music.stop()  # Stop game music when restarting
            return "restart"

        def quit_game():
            pygame.quit()
            sys.exit()

        draw_button("Resume", WIDTH // 3, HEIGHT // 3, 200, 50, (0, 200, 0), (0, 255, 0), resume)
        draw_button("Restart", WIDTH // 3, HEIGHT // 2, 200, 50, (200, 200, 0), (255, 255, 0), restart)
        draw_button("Quit", WIDTH // 3, HEIGHT // 1.5, 200, 50, (200, 0, 0), (255, 0, 0), quit_game)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


def main_menu():
    """Function for the main menu where player chooses color and shape."""
    selected_shape = 0  # 0: rectangle, 1: circle, 2: triangle, 3: star, 4: hexagon
    selected_color = "blue"  # Default color

    waiting = True
    while waiting:
        screen.fill(WHITE)
        draw_text("Choose Shape (← →)", 40, WIDTH // 3, HEIGHT // 4)
        draw_text("Choose Color (1-0)", 40, WIDTH // 3, HEIGHT // 3)

        # Show shape preview
        shape_rect = pygame.Rect(WIDTH // 2 - 25, HEIGHT // 3 + 50, 50, 50)
        draw_shape(SHAPES[selected_shape], COLORS[selected_color], shape_rect)

        # Show color choices
        color_keys = list(COLORS.keys())
        for i, color in enumerate(color_keys):
            pygame.draw.rect(screen, COLORS[color], (WIDTH // 3 + i * 60, HEIGHT // 3 + 120, 50, 50), border_radius=10)
            if color == selected_color:
                pygame.draw.rect(screen, BLACK, (WIDTH // 3 + i * 60, HEIGHT // 3 + 120, 50, 50), 3, border_radius=10)

        # Show start text
        draw_text("Press SPACE to Start", 40, WIDTH // 3, HEIGHT // 2)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    selected_shape = (selected_shape - 1) % len(SHAPES)
                if event.key == pygame.K_RIGHT:
                    selected_shape = (selected_shape + 1) % len(SHAPES)
                if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9, pygame.K_0]:
                    selected_color = color_keys[event.key - pygame.K_1]
                if event.key == pygame.K_SPACE:
                    menu_music.stop()  # Stop menu music when game starts
                    waiting = False  # Exit menu and start game

    return SHAPES[selected_shape], COLORS[selected_color]  # Return chosen shape & color


def game_loop(player_shape, player_color):
    """Main game loop."""
    global ENEMY_SPEED

    # Reset variables
    player = pygame.Rect(WIDTH // 2, HEIGHT - 100, 50, 50)
    enemies = [
        {"rect": pygame.Rect(random.randint(0, WIDTH - 50), 0, 50, 50), "shape": random.choice(SHAPES)}
    ]
    score = 0
    ENEMY_SPEED = 2  # Reset enemy speed
    game_over = False

    # Play game music
    game_music.play(-1)  # Loop indefinitely

    running = True
    while running:
        screen.fill(WHITE)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:  # Pause the game
                    action = pause_menu()
                    if action == "restart":
                        game_music.stop()  # Stop game music when restarting
                        return  # Restart game

        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x > 0:
            player.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT] and player.x < WIDTH - 50:
            player.x += PLAYER_SPEED

        # Enemy movement
        for enemy in enemies[:]:  # Iterate over a copy to modify safely
            enemy["rect"].y += ENEMY_SPEED

            # Reset enemy when reaching bottom
            if enemy["rect"].y > HEIGHT:
                score += 1  # Increase score
                score_sound.play()  # Play score sound
                enemy["rect"].x = random.randint(0, WIDTH - 50)  # Reset position
                enemy["rect"].y = 0  
                enemy["shape"] = random.choice(SHAPES)  # Change shape
                ENEMY_SPEED += ENEMY_ACCELERATION  # Increase enemy speed

                # Add new enemies over time
                if score % NEW_ENEMY_THRESHOLD == 0:
                    new_enemy = {"rect": pygame.Rect(random.randint(0, WIDTH - 50), 0, 50, 50), "shape": random.choice(SHAPES)}
                    enemies.append(new_enemy)

            # Collision detection
            if player.colliderect(enemy["rect"]):
                collision_sound.play()  # Play collision sound
                game_music.stop()  # Stop game music when losing
                game_over = True
                running = False

        # Draw player
        draw_shape(player_shape, player_color, player)

        # Draw enemies
        for enemy in enemies:
            draw_shape(enemy["shape"], (200, 0, 0), enemy["rect"])

        # Draw score
        draw_text(f"Score: {score}", 36, 10, 10)

        # Update the display
        pygame.display.flip()
        clock.tick(30)

    if game_over:
        game_over_screen(score)  # Show game over screen after losing


def game_over_screen(score):
    """Display game over screen with score."""
    screen.fill(WHITE)
    draw_text("Game Over", 50, WIDTH // 3, HEIGHT // 4)
    draw_text(f"Final Score: {score}", 40, WIDTH // 3, HEIGHT // 3)

    def restart():
        game_music.stop()  # Stop game music when restarting
        main_menu()  # Return to main menu

    def quit_game():
        pygame.quit()
        sys.exit()

    draw_button("Restart", WIDTH // 3, HEIGHT // 2, 200, 50, (0, 200, 0), (0, 255, 0), restart)
    draw_button("Quit", WIDTH // 3, HEIGHT // 1.5, 200, 50, (200, 0, 0), (255, 0, 0), quit_game)

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


def main():
    """Main function to run the game."""
    while True:
        chosen_shape, chosen_color = main_menu()  # Let player choose shape & color
        game_loop(chosen_shape, chosen_color)


if __name__ == "__main__":
    main()