import pygame
import sys
import random

pygame.init()

width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Virtual Chemistry Lab")

BLACK = (0, 0, 0)
tablecolor = (200, 200, 200)
bubblecolor = (222, 244, 252)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
buttoncolor = (100, 100, 255)

flask = pygame.image.load("flask.png").convert_alpha()
screen.blit(flask,(100,100))
baking_soda = pygame.image.load("baking_soda.png").convert_alpha()
screen.blit(baking_soda,(300,320))
vinegar = pygame.image.load("vinegar.png").convert_alpha()
screen.blit(vinegar,(100,100))

# Positions
flask_pos = [300, 320]
baking_pos = [80, 450]
vinegar_pos = [630, 430]
baking_size = baking_soda.get_rect().size
vinegar_size = vinegar.get_rect().size
flask_size = flask.get_rect().size

font = pygame.font.SysFont("Arial", 20)
title_font = pygame.font.SysFont("Arial", 24, bold=True)
button_font = pygame.font.SysFont("Arial", 18)

restart_button = pygame.Rect(650, 20, 130, 40)

dragging_item = None
offset_x = offset_y = 0
baking_in = vinegar_in = False
reaction_done = False

reaction_name = "Baking Soda + Vinegar Reaction"
reaction_explanation = "They react to form carbon dioxide gas."

instructions = [
    "Step 1: Drag Baking Soda into the Flask.",
    "Step 2: Drag Vinegar into the Flask.",
    "Step 3: Observe the reaction!"
]

class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = random.randint(10, 18)
        self.color = bubblecolor
        self.lifetime = random.randint(40, 70)
        self.dy = random.uniform(-1.0, -2.5)
        self.dx = random.uniform(-0.5, 0.5)

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.lifetime -= 1

    def draw(self, surface):
        if self.lifetime > 0:
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)

particles = []

running = True
clock = pygame.time.Clock()
while running:
    clock.tick(60)
    screen.fill(BLACK)


    pygame.draw.rect(screen, tablecolor, (0, 500, width, 100))

    screen.blit(flask, flask_pos)

    if not baking_in:
        screen.blit(baking_soda, baking_pos)
    if not vinegar_in:
        screen.blit(vinegar, vinegar_pos)


    if baking_in:
        screen.blit(pygame.transform.scale(baking_soda, (40, 40)), (flask_pos[0] + 60, flask_pos[1] + 120))
    if vinegar_in:
        screen.blit(pygame.transform.scale(vinegar, (30, 30)), (flask_pos[0] + 30, flask_pos[1] + 100))

   
    if baking_in and vinegar_in:
        instructions[2] = "Reaction Occurred! "
        if not reaction_done:
            reaction_done = True
        

        if len(particles) < 20:  
            px = flask_pos[0] + flask_size[0] // 2 + random.randint(-5, 5)
            py = flask_pos[1] + 30
            particles.append(Particle(px, py))

      
        reaction_text = title_font.render(reaction_name, True, RED)
        explanation_text = font.render(reaction_explanation, True, WHITE)
        screen.blit(reaction_text, (width // 2 - reaction_text.get_width() // 2, 80))
        screen.blit(explanation_text, (width // 2 - explanation_text.get_width() // 2, 120))


    for p in particles[:]:
        p.update()
        p.draw(screen)
        if p.lifetime <= 0:
            particles.remove(p)

    for i, line in enumerate(instructions):
        text = font.render(line, True, WHITE)
        screen.blit(text, (20, 20 + i * 30))

    pygame.draw.rect(screen, buttoncolor, restart_button)
    restart_text = button_font.render("Restart", True, WHITE)
    screen.blit(restart_text, (restart_button.x + 25, restart_button.y + 10))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()
            if restart_button.collidepoint(mouse):
              #reset
                baking_pos = [80, 480]
                vinegar_pos = [630, 430]
                baking_in = vinegar_in = False
                reaction_done = False
                dragging_item = None
                particles.clear()
                instructions = [
                    "Step 1: Drag Baking Soda into the Flask.",
                    "Step 2: Drag Vinegar into the Flask.",
                    "Step 3: Observe the reaction!"
                ]
            elif not baking_in and pygame.Rect(baking_pos, baking_size).collidepoint(mouse):
                dragging_item = "baking"
                offset_x = mouse[0] - baking_pos[0]
                offset_y = mouse[1] - baking_pos[1]
            elif not vinegar_in and pygame.Rect(vinegar_pos, vinegar_size).collidepoint(mouse):
                dragging_item = "vinegar"
                offset_x = mouse[0] - vinegar_pos[0]
                offset_y = mouse[1] - vinegar_pos[1]

        elif event.type == pygame.MOUSEMOTION and dragging_item:
            mouse = pygame.mouse.get_pos()
            if dragging_item == "baking":
                baking_pos[0] = mouse[0] - offset_x
                baking_pos[1] = mouse[1] - offset_y
            elif dragging_item == "vinegar":
                vinegar_pos[0] = mouse[0] - offset_x
                vinegar_pos[1] = mouse[1] - offset_y

        elif event.type == pygame.MOUSEBUTTONUP:
            flask_rect = pygame.Rect(flask_pos, flask_size)
            if dragging_item == "baking" and flask_rect.collidepoint(baking_pos[0] + 30, baking_pos[1] + 30):
                baking_in = True
            elif dragging_item == "vinegar" and flask_rect.collidepoint(vinegar_pos[0] + 30, vinegar_pos[1] + 30):
                vinegar_in = True
            dragging_item = None

    pygame.display.flip()

pygame.quit()
sys.exit()
