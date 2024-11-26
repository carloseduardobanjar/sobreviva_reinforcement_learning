import pygame
import random

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
PARTICLE_RADIUS = 10
FOOD_RADIUS = 5
HUNGER_RATE = 0.1
FOOD_SPAWN_TIME = 2000

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Sobreviva")
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

class PlayerParticle:
    def __init__(self):
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2
        self.speed = 5
        self.hunger = 100

    def move(self, dx, dy):
        self.x += dx * self.speed
        self.y += dy * self.speed

        if self.x < 0:
            self.x = SCREEN_WIDTH
        elif self.x > SCREEN_WIDTH:
            self.x = 0
        if self.y < 0:
            self.y = SCREEN_HEIGHT
        elif self.y > SCREEN_HEIGHT:
            self.y = 0

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
    player = PlayerParticle()
    foods = [Food() for _ in range(5)] 
    running = True
    last_food_spawn = pygame.time.get_ticks()

    while running:
        screen.fill(WHITE)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        dx = dy = 0
        if keys[pygame.K_LEFT]:
            dx = -1
        if keys[pygame.K_RIGHT]:
            dx = 1
        if keys[pygame.K_UP]:
            dy = -1
        if keys[pygame.K_DOWN]:
            dy = 1

        player.move(dx, dy)

        if player.update_hunger():
            print("Você morreu de fome!")
            running = False

        pygame.draw.circle(screen, BLUE, (int(player.x), int(player.y)), PARTICLE_RADIUS)

        for food in foods[:]:
            if (player.x - food.x) ** 2 + (player.y - food.y) ** 2 < (PARTICLE_RADIUS + FOOD_RADIUS) ** 2:
                player.eat_food()
                foods.remove(food)

        if pygame.time.get_ticks() - last_food_spawn > FOOD_SPAWN_TIME:
            foods.append(Food())
            last_food_spawn = pygame.time.get_ticks()

        for food in foods:
            pygame.draw.circle(screen, GREEN, (int(food.x), int(food.y)), FOOD_RADIUS)

        font = pygame.font.Font(None, 36)
        hunger_text = font.render(f"Fome: {int(player.hunger)}", True, RED)
        screen.blit(hunger_text, (10, 10))

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()