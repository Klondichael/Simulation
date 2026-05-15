import pygame
import random
import math

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
FPS = 60
running = True
font = pygame.freetype.SysFont("Arial", 24)

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

with open("adjectives.txt", "r") as file:
    adjectives = file.read().splitlines()

with open("names.txt", "r") as file:
    names = file.read().splitlines()

class Guy:

    def __init__(self):
        self.name = f"{random.choice(adjectives)} {random.choice(names)}"
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.speed = random.randint(1, 10) * 10
        self.position = (random.randint(0, screen.get_width()), random.randint(0, screen.get_height()))
        self.size = random.randint(5, 50)
        self.direction = (math.cos(random.uniform(0, 2*math.pi)), math.sin(random.uniform(0, 2*math.pi)))
        self.turn_weight = random.uniform(0.005, 0.01)
    
    def draw_guy(self):
        pygame.draw.circle(screen, self.color, self.position, self.size)
        text_rect = font.get_rect(self.name)
        text_rect.center = (self.position[0], self.position[1] - (self.size+30))
        font.render_to(screen, text_rect, self.name, "white")

    def move_guy(self, dt):
        next_pos = (self.position[0] + (self.speed*self.direction[0]*dt), self.position[1] + (self.speed*self.direction[1]*dt))
        if not ((next_pos[0] < 0 or next_pos[0] > screen.get_width()) or (next_pos[1] < 0 or next_pos[1] > screen.get_height())):
            self.position = next_pos
        elif (next_pos[0] < 0 or next_pos[0] > screen.get_width()):
            self.direction = (self.direction[0] * -1, self.direction[1])
            self.position = (self.position[0] + (self.speed*self.direction[0]*dt), self.position[1] + (self.speed*self.direction[1]*dt))
        else:
            self.direction = (self.direction[0], self.direction[1] * -1)
            self.position = (self.position[0] + (self.speed*self.direction[0]*dt), self.position[1] + (self.speed*self.direction[1]*dt))

    def turn_guy(self):
        if random.random() < self.turn_weight:
            self.direction = (math.cos(random.uniform(0, 2*math.pi)), math.sin(random.uniform(0, 2*math.pi)))

guys = []

for i in range(1):
    guys.append(Guy())

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    dt = clock.tick(FPS) / 1000.0
    
    screen.fill("black")

    for guy in guys:
        guy.draw_guy()
        guy.move_guy(dt)
        #guy.turn_guy()

    pygame.display.flip()

pygame.quit()