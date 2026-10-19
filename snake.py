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

# these are just some names for the directions so that its less confusing. note that its in clockwise order
# so you can use modular arithmetic to rotate around
RIGHT, DOWN, LEFT, UP = 0, 1, 2, 3

# directional offsets in the same order as our enums
DIRECTION_OFFSETS = [(1, 0), (0, 1), (-1, 0), (0, -1)]

direction = RIGHT
last_direction = RIGHT

def reset():
    p = starting_snake()
    d = RIGHT

    fx, fy = spawn_food(p)
    return p, d, fx, fy, 0

def spawn_food(positions):
    fx = random.randint(0, GRID_WIDTH - 1)
    fy = random.randint(0, GRID_HEIGHT - 1)   

    while (fx, fy) in positions:
        fx = random.randint(0, GRID_WIDTH - 1)
        fy = random.randint(0, GRID_HEIGHT - 1)   

    return (fx, fy)

fx, fy = spawn_food(positions)

def dead(positions, nx, ny):
    hit_wall = nx < 0 or nx >= GRID_WIDTH or ny < 0 or ny >= GRID_HEIGHT
    hit_self = (nx, ny) in positions

    return hit_wall or hit_self

def step(positions, direction, fp):
    fx, fy = fp
    hx, hy = positions[0]
    dx, dy = DIRECTION_OFFSETS[direction]
    nx = hx + dx
    ny = hy + dy

    ate = False
    if (nx, ny) != (fx, fy):
        del positions[-1]
    else:
        fx, fy = spawn_food(positions)
        ate = True

    if dead(positions, nx, ny):
        return (-10, fp, True)
        
    positions.insert(0, (nx, ny))

    if ate:
        return (10, (fx, fy), False)
    else:
        return (0, fp, False)

def state(positions, direction, fp):
    fx, fy = fp 
    hx, hy = positions[0]

    # first 3 bits are danger: straight right left 
    # next 4 bits are current direction: right down left up
    # next 4 bits are food position: left right up down
    #        0  1  2  3  4  5  6  7  8  9  10
    #        1  2  3  1  2  3  4  1  2  3  4
    bits = []

    bits[3+direction] = 1

    if dead(positions, hx+DIRECTION_OFFSETS[direction][0], hy+DIRECTION_OFFSETS[direction][1]):
        bits[0] = 1
    if dead(positions, hx+DIRECTION_OFFSETS[(direction+1)%4][0], hy+DIRECTION_OFFSETS[(direction+1)%4][1]):
        bits[1] = 1
    if dead(positions, hx+DIRECTION_OFFSETS[(direction-1)%4][0], hy+DIRECTION_OFFSETS[(direction-1)%4][1]):
        bits[2] = 1
    
    if hy > fy:
        bits[9] = 1
    elif hy < fy:
        bits[10] = 1
    if hx > fx:
        bits[7] = 1
    elif hx < fx:
        bits[8] = 1

    return tuple(bits)

score = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_w and last_direction != DOWN:
                direction = UP
            elif event.key == pygame.K_s and last_direction != UP:
                direction = DOWN
            elif event.key == pygame.K_a and last_direction != RIGHT:
                direction = LEFT
            elif event.key == pygame.K_d and last_direction != LEFT:
                direction = RIGHT

    last_direction = direction
    
    reward, fp, gameover = step(positions, direction, (fx, fy))
    score += reward

    fx, fy = fp

    if gameover:
        positions, direction, fx, fy, score = reset()
        last_direction = direction

    screen.fill(BACKGROUND_COLOR)
    draw_positions(screen, positions)
    draw_food(screen, (fx, fy))
    draw_grid(screen)
    pygame.display.flip()
    clock.tick(3)

pygame.quit()
sys.exit()