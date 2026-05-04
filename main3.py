import pygame
import random
import math

# --- Setup ---
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)

# --- Constants ---
NUM_SQUARES = 20
MIN_SIZE = 10
MAX_SIZE = 40
MAX_SPEED = 120  # pixels per second

# --- Create one square ---
def create_square():
    size = random.randint(MIN_SIZE, MAX_SIZE)

    # bigger = slower
    max_speed = MAX_SPEED * (MAX_SIZE / size)

    return {
        "x": random.uniform(0, WIDTH),
        "y": random.uniform(0, HEIGHT),
        "vx": random.uniform(-1, 1) * max_speed,
        "vy": random.uniform(-1, 1) * max_speed,
        "size": size,
        "color": (
            random.randint(50, 255),
            random.randint(50, 255),
            random.randint(50, 255),
        ),
        "life": random.uniform(30, 180),  # seconds
        "max_speed": max_speed,
    }

# --- Init squares ---
squares = [create_square() for _ in range(NUM_SQUARES)]

# --- Main loop ---
running = True
while running:
    dt = clock.tick(60) / 1000  # delta time in seconds

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- Update ---
    for square in squares:
        # Life system
        square["life"] -= dt
        if square["life"] <= 0:
            squares.remove(square)
            squares.append(create_square())
            continue

        # Random jitter (small randomness)
        square["vx"] += random.uniform(-20, 20) * dt
        square["vy"] += random.uniform(-20, 20) * dt

        # Interaction with others
        for other in squares:
            if other is square:
                continue

            dx = other["x"] - square["x"]
            dy = other["y"] - square["y"]
            distance = math.hypot(dx, dy)

            if distance < 100:
                # FLEE (small runs away from big)
                if square["size"] < other["size"]:
                    square["vx"] -= dx * 2 * dt
                    square["vy"] -= dy * 2 * dt

                # CHASE (big goes toward small)
                elif square["size"] > other["size"]:
                    square["vx"] += dx * dt
                    square["vy"] += dy * dt

        # Limit speed
        speed = math.hypot(square["vx"], square["vy"])
        if speed > square["max_speed"]:
            scale = square["max_speed"] / speed
            square["vx"] *= scale
            square["vy"] *= scale

        # Move (time-based)
        square["x"] += square["vx"] * dt
        square["y"] += square["vy"] * dt

        # Bounce on walls
        if square["x"] <= 0 or square["x"] >= WIDTH:
            square["vx"] *= -1
        if square["y"] <= 0 or square["y"] >= HEIGHT:
            square["vy"] *= -1

    # --- Draw ---
    screen.fill((0, 0, 0))

    for square in squares:
        pygame.draw.rect(
            screen,
            square["color"],
            (square["x"], square["y"], square["size"], square["size"]),
        )

    # FPS display
    fps_text = font.render(f"FPS: {clock.get_fps():.1f}", True, (255, 255, 255))
    screen.blit(fps_text, (10, 10))

    pygame.display.flip()

pygame.quit()