import random

class Agent:
    def __init__(self, alpha=0.1, gamma=0.9, epsilon=1, epsilon_decay=0.995, epsilon_min=0.01):
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = epsilon_min
        self.Q = {}
    
    def get_q(self, state):
        if self.Q.get(state) is None:
            self.Q[state] = [0, 0, 0]

        return self.Q[state]

    def decay_epsilon(self):
        self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)

    def choose(self, state):
        r = random.random()

        if r <= self.epsilon:
            action = random.randint(0, 2)
        else:
            best_val = float('-inf')
            indexes = []
            
            for i,v in enumerate(self.get_q(state)):
                if v > best_val:
                    indexes.clear()
                    indexes.append(i)
                    best_val = v
                elif v == best_val:
                    indexes.append(i)

            action = random.choice(indexes)

        return action


    def learn(self, state, action, reward, next_state, done):
        cur_guess = self.get_q(state)[action]
        if done:
            target = reward
        else:
            target = reward + self.gamma * max(self.get_q(next_state))

        self.Q[state][action] += self.alpha * (target - cur_guess)  
        