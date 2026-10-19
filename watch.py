import sys
import pygame
from agent import Agent
from snake import (
    CELL_SIZE, GRID_WIDTH, GRID_HEIGHT, BACKGROUND_COLOR,
    reset, step, state, action_to_direction,
    draw_grid, draw_positions, draw_food, draw_eyes,
)

MAX_STEPS_WITHOUT_FOOD = 100

def watch(path):
    a = Agent()
    a.load(path)
    a.epsilon = 0

    pygame.init()
    screen = pygame.display.set_mode((GRID_WIDTH * CELL_SIZE, GRID_HEIGHT * CELL_SIZE))
    clock = pygame.time.Clock()
    speed = 8

    positions, direction, fx, fy, score = reset()
    last_food = 0
    game = 1
    best = 0
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                # up or down arrows speed up or slow down
                elif event.key == pygame.K_UP:
                    speed = min(speed * 2, 128)
                elif event.key == pygame.K_DOWN:
                    speed = max(speed // 2, 1)

        current = state(positions, direction, (fx, fy))
        action = a.choose(current)
        direction = action_to_direction(action, direction)
        reward, fp, done = step(positions, direction, (fx, fy))
        fx, fy = fp

        if reward > 0:
            score += 1
            last_food = 0
        else:
            last_food += 1

        best = max(best, score)

        if done or last_food >= MAX_STEPS_WITHOUT_FOOD:
            positions, direction, fx, fy, score = reset()
            last_food = 0
            game += 1

        pygame.display.set_caption(f"game {game} | score {score} | best {best} | speed {speed}")
        screen.fill(BACKGROUND_COLOR)
        draw_positions(screen, positions)
        draw_food(screen, (fx, fy))
        draw_grid(screen)
        draw_eyes(screen, positions[0], direction, (fx, fy))
        pygame.display.flip()
        clock.tick(speed)

    pygame.quit()

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "q_table.json"
    watch(path)
