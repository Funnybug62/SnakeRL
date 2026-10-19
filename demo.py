import pygame
import random
import sys

CELL_SIZE = 80
GRID_WIDTH = 10
GRID_HEIGHT = 10

# these are colors. obviously
BACKGROUND_COLOR = (170, 215, 80)
GRID_COLOR = (150, 195, 65)
SNAKE_COLOR = (50, 100, 220)
FOOD_COLOR = (231, 71, 29)

pygame.init()
screen = pygame.display.set_mode(((GRID_WIDTH * CELL_SIZE, GRID_HEIGHT * CELL_SIZE)))
pygame.display.set_caption("snake? i barely know her")
clock = pygame.time.Clock()
running = True

def starting_snake():
    cx = GRID_WIDTH // 2
    cy = GRID_HEIGHT // 2

    return [(cx, cy), (cx - 1, cy), (cx - 2, cy)]

# this is a list of tuples. feel free to ask if you have questions about it!
# the front of the list (0 indexed) is going to be the head
positions = starting_snake()

# for this project we will be using numbers for the orthogonal directions for simpolicity sake
# they go clockwise: 0 => right; 1 => down; 2 => left; 3 => up
direction = 0
last_direction = 0

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

while running:
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    
    screen.fill(BACKGROUND_COLOR)
    draw_positions(screen, positions)
    draw_food(screen, (fx, fy))
    draw_grid(screen)
    pygame.display.flip()
    clock.tick(3)