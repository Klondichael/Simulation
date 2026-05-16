import pygame
import random
import math

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
font = pygame.freetype.SysFont("Arial", 24)

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

with open("adjectives.txt", "r") as file:
    adjectives = file.read().splitlines()

with open("names.txt", "r") as file:
    names = file.read().splitlines()

FPS = 60
show_names = True
num_guys = 50
turn_radius = 10 * ((2*math.pi) / 360)

class Guy:

    def __init__(self):
        self.name = f"{random.choice(adjectives)} {random.choice(names)}"
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.speed = random.randint(5, 10) * 10
        self.size = random.randint(10, 50)
        self.position = (random.randint(self.size, screen.get_width()-self.size), random.randint(self.size, screen.get_height()-self.size))
        self.direction = (random.uniform(0, 2*math.pi))
        self.turn_weight = random.uniform(0.005, 0.01)
    
    def draw_guy(self):
        pygame.draw.circle(screen, self.color, self.position, self.size)

    def draw_name(self):
        text_rect = font.get_rect(self.name)
        text_rect.center = (self.position[0], self.position[1] - (self.size+30))
        font.render_to(screen, text_rect, self.name, "white")

    def move_guy(self, dt):
        next_pos = (self.position[0] + (self.speed*math.cos(self.direction)*dt), self.position[1] + (self.speed*math.sin(self.direction)*dt))
        if not ((next_pos[0]-self.size < 0 or next_pos[0]+self.size > screen.get_width()) or (next_pos[1]-self.size < 0 or next_pos[1]+self.size > screen.get_height())):
            self.position = next_pos
        elif (next_pos[0]-self.size < 0 or next_pos[0]+self.size > screen.get_width()):
            self.direction = (math.pi/2) + ((math.pi/2)-self.direction)
            self.position = (self.position[0] + (self.speed*math.cos(self.direction)*dt), self.position[1] + (self.speed*math.sin(self.direction)*dt))
        else:
            self.direction = math.pi + (math.pi-self.direction)
            self.position = (self.position[0] + (self.speed*math.cos(self.direction)*dt), self.position[1] + (self.speed*math.sin(self.direction)*dt))

    def turn_guy(self):
        if random.random() < self.turn_weight:
            self.direction = (random.uniform(self.direction-turn_radius, self.direction+turn_radius))

guys = []

for i in range(num_guys):
    guys.append(Guy())

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    dt = clock.tick(FPS) / 1000.0
    
    screen.fill("black")

    for guy in guys:
        guy.draw_guy()
        if show_names: guy.draw_name()
        guy.move_guy(dt)
        guy.turn_guy()

    pygame.display.flip()

pygame.quit()