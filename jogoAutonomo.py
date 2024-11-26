import pygame
import random
import numpy as np
import logging
import time

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
PARTICLE_RADIUS = 10
FOOD_RADIUS = 5
HUNGER_RATE = 0.1
FOOD_SPAWN_TIME = 2000

ACTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]
ALPHA = 0.5
GAMMA = 0.9
EPSILON = 0.1

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Jogo de Partícula com Aprendizado por Reforço")
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

class AgentParticle:
    def __init__(self):
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2
        self.hunger = 100
        self.q_table = {}

    def reset(self):
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2
        self.hunger = 100

    def get_state(self, food):
        if not food:
            return (0, 0, self.hunger)
    
        nearest_food = min(food, key=lambda f: (self.x - f.x) ** 2 + (self.y - f.y) ** 2)
        dx = nearest_food.x - self.x
        dy = nearest_food.y - self.y
        return (dx, dy, int(self.hunger))

    def choose_action(self, state, testing=False):
        if not testing and np.random.rand() < EPSILON:
            action = random.choice(ACTIONS)
            return action
        action = max(ACTIONS, key=lambda action: self.q_table.get((state, action), 0))
        return action

    def update_q_table(self, state, action, reward, next_state):
        max_future_q = max([self.q_table.get((next_state, a), 0) for a in ACTIONS])
        current_q = self.q_table.get((state, action), 0)
        new_q = (1 - ALPHA) * current_q + ALPHA * (reward + GAMMA * max_future_q)
        self.q_table[(state, action)] = new_q

    def move(self, action):
        dx, dy = action
        self.x = (self.x + dx * 5) % SCREEN_WIDTH
        self.y = (self.y + dy * 5) % SCREEN_HEIGHT

    def update_hunger(self):
        self.hunger -= HUNGER_RATE
        if self.hunger <= 0:
            return True
        return False

    def eat_food(self):
        self.hunger = min(self.hunger + 20, 100)

class Food:
    def __init__(self):
        self.x = random.randint(0, SCREEN_WIDTH)
        self.y = random.randint(0, SCREEN_HEIGHT)

def main():
    agent = AgentParticle()
    training_episodes = 10000 
    testing_episode = 1
    foods = [Food() for _ in range(5)]
    
    # ----------------------- TREINAMENTO -----------------------
    for episode in range(training_episodes):
        logging.info("Início do episódio de treinamento %d", episode + 1)
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
                if (agent.x - food.x) ** 2 + (agent.y - food.y) ** 2 < (PARTICLE_RADIUS + FOOD_RADIUS) ** 2:
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
    start_time = time.time()
    while running:
        screen.fill(WHITE)
        
        state = agent.get_state(foods)
        action = agent.choose_action(state, testing=True)
        agent.move(action)

        if agent.update_hunger():
            print("Você morreu de fome!")
            break

        for food in foods[:]:
            if (agent.x - food.x) ** 2 + (agent.y - food.y) ** 2 < (PARTICLE_RADIUS + FOOD_RADIUS) ** 2:
                agent.eat_food()
                foods.remove(food)

        if pygame.time.get_ticks() - last_food_spawn > FOOD_SPAWN_TIME:
            foods.append(Food())
            last_food_spawn = pygame.time.get_ticks()

        pygame.draw.circle(screen, BLUE, (int(agent.x), int(agent.y)), PARTICLE_RADIUS)
        for food in foods:
            pygame.draw.circle(screen, GREEN, (int(food.x), int(food.y)), FOOD_RADIUS)

        font = pygame.font.Font(None, 36)
        hunger_text = font.render(f"Hunger: {int(agent.hunger)}", True, RED)
        screen.blit(hunger_text, (10, 10))

        pygame.display.flip()
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    end_time = time.time()

    elapsed_time = end_time - start_time
    print(f"Tempo decorrido: {elapsed_time:.5f} segundos")

    pygame.quit()

if __name__ == "__main__":
    main()
