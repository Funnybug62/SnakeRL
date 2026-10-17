import pygame
import random
import sys

CELL_SIZE = 80
GRID_WIDTH = 10
GRID_HEIGHT = 10

BACKGROUND_COLOR = (170, 215, 80)
GRID_COLOR = (150, 195, 65)
SNAKE_COLOR = (50, 100, 220)
FOOD_COLOR = (231, 71, 29)

pygame.init()
screen = pygame.display.set_mode((GRID_WIDTH * CELL_SIZE, GRID_HEIGHT * CELL_SIZE))
pygame.display.set_caption("testotesto")
clock = pygame.time.Clock()
running = True

def draw_grid(surface):
    for x in range(0, GRID_WIDTH * CELL_SIZE, CELL_SIZE):
        pygame.draw.line(surface, GRID_COLOR, (x, 0), (x, GRID_HEIGHT * CELL_SIZE))
    for y in range(0, GRID_HEIGHT * CELL_SIZE, CELL_SIZE):
        pygame.draw.line(surface, GRID_COLOR, (0, y), (GRID_WIDTH * CELL_SIZE, y))


def draw_positions(surface, positions):
    for x, y in positions:
        rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(surface, SNAKE_COLOR, rect)

def draw_food(surface, fp): 
    fx, fy = fp

    rect = pygame.Rect(fx * CELL_SIZE, fy * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(surface, FOOD_COLOR, rect)

def starting_snake():
    cx = GRID_WIDTH // 2
    cy = GRID_HEIGHT // 2

    return [(cx, cy), (cx - 1, cy), (cx - 2, cy)]

# this is a list of tuples. feel free to ask if you have questions about it!
# the front of the list (0 indexed) is going to be the head
positions = starting_snake()
positions = starting_snake()

# for this project we will be using numbers for the orthogonal directions for simpolicity sake
# more specifically, -1 => left; 1 => right; -2 => up; 2 => down
direction = 1
last_direction = 1

def reset():
    p = starting_snake()
    p = starting_snake()
    d = 1

    fx, fy = spawn_food(p)
    return p, d, fx, fy

def spawn_food(positions):
    fx = random.randint(0, GRID_WIDTH - 1)
    fy = random.randint(0, GRID_HEIGHT - 1)   

    while (fx, fy) in positions:
        fx = random.randint(0, GRID_WIDTH - 1)
        fy = random.randint(0, GRID_HEIGHT - 1)   

    return (fx, fy)

fx, fy = spawn_food(positions)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_w and last_direction != 2:
                direction = -2
            elif event.key == pygame.K_s and last_direction != -2:
                direction = 2
            elif event.key == pygame.K_a and last_direction != 1:
                direction = -1
            elif event.key == pygame.K_d and last_direction != -1:
                direction = 1

    last_direction = direction
    
    if (direction == 1):
        hx, hy = positions[0]
        nx = hx+1
        ny = hy
    if (direction == -1):
        hx, hy = positions[0]
        nx = hx-1
        ny = hy
    if (direction == 2):
        hx, hy = positions[0]
        nx = hx
        ny = hy+1
    if (direction == -2):
        hx, hy = positions[0]
        nx = hx
        ny = hy-1
    positions.insert(0, (nx, ny))
    if (nx, ny) != (fx, fy):
        del positions[-1]
    else:
        fx, fy = spawn_food(positions)

    hit_wall = nx < 0 or nx >= GRID_WIDTH or ny < 0 or ny >= GRID_HEIGHT
    hit_self = positions.count((nx, ny)) > 1

    if hit_wall or hit_self:
        positions, direction, fx, fy = reset()
        last_direction = direction
    

    screen.fill(BACKGROUND_COLOR)
    draw_positions(screen, positions)
    draw_food(screen, (fx, fy))
    draw_grid(screen)
    pygame.display.flip()
    clock.tick(3)

pygame.quit()
sys.exit()