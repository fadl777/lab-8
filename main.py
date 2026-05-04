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
        "life": random.uniform(30, 180),
        "max_speed": max_speed,

        # --- Exercise 7 ---
        "trail": []
    }

# --- Exercise 4: collision function ---
def check_collision(a, b) -> bool:
    dx = a["x"] - b["x"]
    dy = a["y"] - b["y"]
    distance = math.hypot(dx, dy)
    return distance < (a["size"] + b["size"])


# --- Init squares (Exercise 1) ---
squares = []

for _ in range(5):
    sq = create_square()
    sq["size"] = 25
    squares.append(sq)

for _ in range(10):
    sq = create_square()
    sq["size"] = 10
    squares.append(sq)

for _ in range(30):
    sq = create_square()
    sq["size"] = 4
    squares.append(sq)

# --- Main loop ---
running = True
while running:
    dt = clock.tick(60) / 1000

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- Update ---
    for square in squares[:]:  # safe iteration copy

        # Exercise 2
        square["life"] -= dt
        if square["life"] <= 0:
            size = square["size"]

            squares.remove(square)

            new_sq = create_square()
            new_sq["size"] = size

            squares.append(new_sq)
            continue

        # Random jitter
        square["vx"] += random.uniform(-20, 20) * dt
        square["vy"] += random.uniform(-20, 20) * dt

        # Interaction (Exercise 4)
        for other in squares:
            if other is square:
                continue

            if check_collision(square, other):
                dx = other["x"] - square["x"]
                dy = other["y"] - square["y"]

                if square["size"] < other["size"]:
                    square["vx"] -= dx * 2 * dt
                    square["vy"] -= dy * 2 * dt
                elif square["size"] > other["size"]:
                    square["vx"] += dx * dt
                    square["vy"] += dy * dt

        # --- Exercise 5 + 6 ---
        for other in squares[:]:
            if other is square:
                continue

            if check_collision(square, other):

                # Exercise 5
                if square["size"] > other["size"]:
                    if other in squares:
                        squares.remove(other)
                        squares.append(create_square())

                # Exercise 6
                if square["size"] > other["size"]:
                    square["size"] += other["size"] * 0.2

                    if other in squares:
                        squares.remove(other)

                        new_sq = create_square()
                        new_sq["size"] = other["size"]
                        squares.append(new_sq)

        # Limit speed
        speed = math.hypot(square["vx"], square["vy"])
        if speed > square["max_speed"]:
            scale = square["max_speed"] / speed
            square["vx"] *= scale
            square["vy"] *= scale

        # Move
        square["x"] += square["vx"] * dt
        square["y"] += square["vy"] * dt

        # --- Exercise 7: Trails ---
        square["trail"].append((square["x"], square["y"]))
        if len(square["trail"]) > 30:
            square["trail"].pop(0)

        # Exercise 3
        if square["x"] < 0:
            square["x"] = WIDTH
        elif square["x"] > WIDTH:
            square["x"] = 0

        if square["y"] < 0:
            square["y"] = HEIGHT
        elif square["y"] > HEIGHT:
            square["y"] = 0

    # --- Draw ---
    screen.fill((0, 0, 0))

    for square in squares:

        # draw trail (Exercise 7)
        for i in range(len(square["trail"]) - 1):
            pygame.draw.line(
                screen,
                square["color"],
                square["trail"][i],
                square["trail"][i + 1],
                2
            )

        pygame.draw.rect(
            screen,
            square["color"],
            (square["x"], square["y"], square["size"], square["size"]),
        )

    fps_text = font.render(f"FPS: {clock.get_fps():.1f}", True, (255, 255, 255))
    screen.blit(fps_text, (10, 10))

    pygame.display.flip()

pygame.quit()