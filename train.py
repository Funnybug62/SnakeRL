from snake import state, reset, step, action_to_direction
from agent import Agent
from tqdm import tqdm

def train(episodes, a):
    scores = []

    progress = tqdm(range(episodes), desc="Training", unit="game")

    for episode in progress:
        positions, direction, fx, fy, score = reset()
        last_food = 0
        running = True
        score = 0
        
        while running:
            current = state(positions, direction, (fx, fy))
            action = a.choose(current)
            direction = action_to_direction(action, direction)
            reward, fp, done = step(positions, direction, (fx, fy))
            fx, fy = fp

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
                running = False

        scores.append(score)
        a.decay_epsilon()

        recent = scores[-50:]
        progress.set_postfix(avg=f"{sum(recent) / len(recent):.1f}", best=max(scores), eps=f"{a.epsilon:.3f}", states=len(a.Q))

    return scores

def main():
    a = Agent()
    train(1000, a)
    a.save("q_table.json")

if __name__ == "__main__":
    main()