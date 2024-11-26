import pygame
import random
import numpy as np
import logging
import math

GRID_SIZE = 20 
GRID_WIDTH, GRID_HEIGHT = 40, 30
SCREEN_WIDTH, SCREEN_HEIGHT = GRID_WIDTH * GRID_SIZE, GRID_HEIGHT * GRID_SIZE
HUNGER_RATE = 0.1
FOOD_SPAWN_TIME = 2000

ACTIONS = [(0, -1), (0, 1), (-1, 0), (1, 0)]
ALPHA = 0.15
GAMMA = 0.9
EPSILON = 0.1

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Jogo de Tabuleiro Discreto com Q-Learning")
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

def direcao_vetor(x, y):
    angulo = math.degrees(math.atan2(y, x))

    angulo = angulo % 360

    if angulo < 22.5 or 337.5 <= angulo:
        return 0
    elif 22.5 <= angulo and angulo < 67.5:
        return 1
    elif 67.5 <= angulo and angulo < 112.5:
        return 2
    elif 112.5 <= angulo and angulo < 157.5:
        return 3
    elif 157.5 <= angulo and angulo < 202.5:
        return 4
    elif 202.5 <= angulo and angulo < 247.5:
        return 5
    elif 247.5 <= angulo and angulo < 292.5:
        return 6
    elif 292.5 <= angulo and angulo < 337.5:
        return 7

class AgentParticle:
    def __init__(self):
        self.x, self.y = GRID_WIDTH // 2, GRID_HEIGHT // 2
        self.hunger = 100
        self.q_table = {}

    def reset(self):
        self.x, self.y = GRID_WIDTH // 2, GRID_HEIGHT // 2
        self.hunger = 100

    def get_state(self, food):
        if not food:
            return (0, 0, self.hunger)

        nearest_food = min(food, key=lambda f: abs(self.x - f.x) + abs(self.y - f.y))
        dx, dy = nearest_food.x - self.x, nearest_food.y - self.y
        return (direcao_vetor(dx, dy), int(self.hunger) // 10)

    def choose_action(self, state, testing=False):
        if not testing and np.random.rand() < EPSILON:
            return random.choice(ACTIONS)
        return max(ACTIONS, key=lambda a: self.q_table.get((state, a), 0))

    def update_q_table(self, state, action, reward, next_state):
        max_future_q = max([self.q_table.get((next_state, a), 0) for a in ACTIONS])
        current_q = self.q_table.get((state, action), 0)
        new_q = (1 - ALPHA) * current_q + ALPHA * (reward + GAMMA * max_future_q)
        self.q_table[(state, action)] = new_q

    def move(self, action):
        dx, dy = action
        self.x = (self.x + dx) % GRID_WIDTH
        self.y = (self.y + dy) % GRID_HEIGHT

    def update_hunger(self):
        self.hunger -= HUNGER_RATE
        return self.hunger <= 0

    def eat_food(self):
        self.hunger = min(self.hunger + 10, 100)

class Food:
    def __init__(self):
        self.x = random.randint(0, GRID_WIDTH - 1)
        self.y = random.randint(0, GRID_HEIGHT - 1)

def main():
    agent = AgentParticle()
    training_episodes = 10000
    foods = [Food() for _ in range(5)]
    
    # ----------------------- TREINAMENTO -----------------------
    for episode in range(training_episodes):
        agent.reset()
        foods = [Food() for _ in range(5)]
        last_food_spawn = pygame.time.get_ticks()
        done = False

        while not done:
            state = agent.get_state(foods)
            action = agent.choose_action(state)
            agent.move(action)
            reward = -HUNGER_RATE
            
            if agent.update_hunger():
                done = True
                break

            for food in foods[:]:
                if agent.x == food.x and agent.y == food.y:
                    agent.eat_food()
                    reward += 10
                    foods.remove(food)

            if pygame.time.get_ticks() - last_food_spawn > FOOD_SPAWN_TIME:
                foods.append(Food())
                last_food_spawn = pygame.time.get_ticks()

            next_state = agent.get_state(foods)
            agent.update_q_table(state, action, reward, next_state)

    # ----------------------- TESTE -----------------------
    agent.reset()
    foods = [Food() for _ in range(5)]
    last_food_spawn = pygame.time.get_ticks()
    running = True

    while running:
        screen.fill(WHITE)
        state = agent.get_state(foods)
        action = agent.choose_action(state, testing=True)
        agent.move(action)

        if agent.update_hunger():
            print("Você morreu de fome!")
            break

        for food in foods[:]:
            if agent.x == food.x and agent.y == food.y:
                agent.eat_food()
                foods.remove(food)

        if pygame.time.get_ticks() - last_food_spawn > FOOD_SPAWN_TIME:
            foods.append(Food())
            last_food_spawn = pygame.time.get_ticks()

        for x in range(GRID_WIDTH):
            for y in range(GRID_HEIGHT):
                pygame.draw.rect(screen, WHITE, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)
        pygame.draw.rect(screen, BLUE, (agent.x * GRID_SIZE, agent.y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
        for food in foods:
            pygame.draw.rect(screen, GREEN, (food.x * GRID_SIZE, food.y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

        font = pygame.font.Font(None, 36)
        hunger_text = font.render(f"Hunger: {int(agent.hunger)}", True, RED)
        screen.blit(hunger_text, (10, 10))

        pygame.display.flip()
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()

if __name__ == "__main__":
    main()