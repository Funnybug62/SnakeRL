import pygame
import random

CELL_SIZE = 40
GRID_WIDTH = 15
GRID_HEIGHT = 15

BACKGROUND_COLOR = (170, 215, 80)
GRID_COLOR = (150, 195, 65)
SNAKE_COLOR = (50, 100, 220)
FOOD_COLOR = (231, 71, 29)

# these are just some names for the directions so that its less confusing. note that its in clockwise order
# so you can use modular arithmetic to rotate around
RIGHT, DOWN, LEFT, UP = 0, 1, 2, 3

# directional offsets in the same order as our enums
DIRECTION_OFFSETS = [(1, 0), (0, 1), (-1, 0), (0, -1)]

# 1
def draw_grid(surface):
    for x in range(0, GRID_WIDTH * CELL_SIZE, CELL_SIZE):
        pygame.draw.line(surface, GRID_COLOR, (x, 0), (x, GRID_HEIGHT * CELL_SIZE))
    for y in range(0, GRID_HEIGHT * CELL_SIZE, CELL_SIZE):
        pygame.draw.line(surface, GRID_COLOR, (0, y), (GRID_WIDTH * CELL_SIZE, y))

# 2
def draw_positions(surface, positions):
    for x, y in positions:
        rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(surface, SNAKE_COLOR, rect)

# googy eyes (i lwk googled how to make these so dont ask me)
def draw_eyes(surface, head, direction, fp):
    hx, hy = head
    fx, fy = fp
    dx, dy = DIRECTION_OFFSETS[direction]
    sx, sy = -dy, dx

    center_x = hx * CELL_SIZE + CELL_SIZE / 2
    center_y = hy * CELL_SIZE + CELL_SIZE / 2
    food_x = fx * CELL_SIZE + CELL_SIZE / 2
    food_y = fy * CELL_SIZE + CELL_SIZE / 2

    eye_radius = CELL_SIZE * 0.2
    pupil_radius = CELL_SIZE * 0.09

    for side in (-1, 1):
        ex = center_x + dx * CELL_SIZE * 0.15 + sx * side * CELL_SIZE * 0.22
        ey = center_y + dy * CELL_SIZE * 0.15 + sy * side * CELL_SIZE * 0.22

        pygame.draw.circle(surface, (255, 255, 255), (ex, ey), eye_radius)
        pygame.draw.circle(surface, (0, 0, 0), (ex, ey), eye_radius, 2)

        lx = food_x - ex + random.uniform(-15, 15)
        ly = food_y - ey + random.uniform(-15, 15)
        length = max((lx ** 2 + ly ** 2) ** 0.5, 1)
        reach = eye_radius - pupil_radius - 1
        px = ex + lx / length * reach
        py = ey + ly / length * reach

        pygame.draw.circle(surface, (0, 0, 0), (px, py), pupil_radius)

# 3
def draw_food(surface, fp):
    fx, fy = fp

    rect = pygame.Rect(fx * CELL_SIZE, fy * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(surface, FOOD_COLOR, rect)

# 4
def starting_snake():
    cx = GRID_WIDTH // 2
    cy = GRID_HEIGHT // 2

    return [(cx, cy), (cx - 1, cy), (cx - 2, cy)]

# 5
def action_to_direction(action, direction):
    if action == 1:
        return (direction + 1) % 4
    if action == 2:
        return (direction - 1) % 4

    return direction

# 6
def reset():
    p = starting_snake()
    d = RIGHT

    fx, fy = spawn_food(p)
    return p, d, fx, fy, 0

# 7
def spawn_food(positions):
    fx = random.randint(0, GRID_WIDTH - 1)
    fy = random.randint(0, GRID_HEIGHT - 1)   

    while (fx, fy) in positions:
        fx = random.randint(0, GRID_WIDTH - 1)
        fy = random.randint(0, GRID_HEIGHT - 1)   

    return (fx, fy)

# 8
def dead(positions, nx, ny):
    hit_wall = nx < 0 or nx >= GRID_WIDTH or ny < 0 or ny >= GRID_HEIGHT
    hit_self = (nx, ny) in positions

    return hit_wall or hit_self

# 9
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
        ate = True

    if dead(positions, nx, ny):
        return (-10, fp, True)

    positions.insert(0, (nx, ny))
        
    if ate:
        fx, fy = spawn_food(positions)
        return (10, (fx, fy), False)
    else:
        return (0, fp, False)

def dfs(positions, sp): 
    hx, hy = sp
    tx, ty = positions[-1] 
    visited = set() 
    stack = [(hx, hy)] 
    
    while stack: 
        cur = stack.pop() 
        if cur not in visited: 
            visited.add(cur)
            cx, cy = cur 
            
            for D in range(4):
                nx = cx+DIRECTION_OFFSETS[D][0]
                ny = cy+DIRECTION_OFFSETS[D][1]

                if nx >= 0 and nx < GRID_WIDTH and ny >= 0 and ny < GRID_HEIGHT:
                    if nx == tx and ny == ty:
                        return True
                    elif (nx, ny) not in positions:
                        stack.append((nx, ny))
    return False

# 10
def state(positions, direction, fp):
    fx, fy = fp 
    hx, hy = positions[0]

    # first 3 bits are danger: straight right left 
    # next 4 bits are current direction: right down left up
    # next 4 bits are food position: left right up down
    #        0  1  2  3  4  5  6  7  8  9  10 11 12 13
    #        1  2  3  1  2  3  4  1  2  3  4  1  2  3
    bits = [0]*14

    bits[3+direction] = 1

    sx, sy = (hx+DIRECTION_OFFSETS[direction][0], hy+DIRECTION_OFFSETS[direction][1])
    rx, ry = (hx+DIRECTION_OFFSETS[(direction+1)%4][0], hy+DIRECTION_OFFSETS[(direction+1)%4][1])
    lx, ly = (hx+DIRECTION_OFFSETS[(direction-1)%4][0], hy+DIRECTION_OFFSETS[(direction-1)%4][1])

    straight = right = left = True

    if dead(positions, sx, sy):
        bits[0] = 1
        straight = False
    if dead(positions, rx, ry):
        bits[1] = 1
        right = False
    if dead(positions, lx, ly):
        bits[2] = 1
        left = False


    if straight:
        copy = positions[:]
        copy.insert(0, (sx, sy))
        if (sx, sy) != fp:
            del copy[-1]

        if dfs(copy, copy[0]):
            bits[11] = 1
    if right:
        copy = positions[:]
        copy.insert(0, (rx, ry))
        if (rx, ry) != fp:
            del copy[-1]

        if dfs(copy, copy[0]):
            bits[12] = 1
    if left:
        copy = positions[:]
        copy.insert(0, (lx, ly))
        if (lx, ly) != fp:
            del copy[-1]

        if dfs(copy, copy[0]):
            bits[13] = 1
        
    
    
    if hx > fx:
        bits[7] = 1
    elif hx < fx:
        bits[8] = 1
    if hy > fy:
        bits[9] = 1
    elif hy < fy:
        bits[10] = 1
    

    return tuple(bits)

def main():
    pygame.init()
    screen = pygame.display.set_mode((GRID_WIDTH * CELL_SIZE, GRID_HEIGHT * CELL_SIZE))
    pygame.display.set_caption("testio")
    clock = pygame.time.Clock()
    # this is a list of tuples. feel free to ask if you have questions about it!
    # the front of the list (0 indexed) is going to be the head
    positions = starting_snake()

    direction = RIGHT
    last_direction = RIGHT
    running = True
    score = 0
    fx, fy = spawn_food(positions)

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
        draw_eyes(screen, positions[0], direction, (fx, fy))
        pygame.display.flip()
        clock.tick(3)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()