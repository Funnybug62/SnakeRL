from snake import state, reset, step, action_to_direction
from agent import Agent

def train(episodes, a):
    positions, direction, fx, fy, score = reset()
    last_food = 0

    scores = []

    for episode in enumerate(episodes):
        running = True
        while running:
            score = 0
            current = state(positions, direction, (fx, fy))
            action = a.choose(current)
            direction = action_to_direction(action, direction)
            reward, fp, done = step(positions, direction, (fx, fy))

            if done:
                next_s = current
            else:
                next_s = state(positions, direction, fp)

            a.learn(current, action, reward, next_s, done)

            if done:
                running = False

            if reward > 0:
                last_food = 0
                score += 1
            else:
                last_food += 1

            if last_food >= 100:
                a.learn(current, action, -10, current, True)
                
        scores.append(score)
        a.decay_epsilon()

def main():
    a = Agent()
    train(500, a=a)

if __name__ == "__main__":
    main()