import pygame
import random
import time

    # functions
def reset():
    pass

    # classes 
class Dinosaur(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = resized_dinosaur
        self.rect = self.image.get_rect()
        self.rect.x = 20
        self.rect.y = 400
    def draw(self, win):
        win.blit(self.image, (self.rect.x, self.rect.y))
    def move(self, change):
        print(self.rect.y)
        # if the players y is close enough to the ground then he will be placed on the ground
        if self.rect.y > 390 and self.rect.y < 400:
            self.rect.y = 400
        if self.rect.y > 400 and self.rect.y < 410:
            self.rect.y = 400
        # if the player is in the air then he will fall down and he can't jump while he is in the air
        if self.rect.y != 400:
            if self.rect.y < 400:
                self.rect.y +=4
        else:
            self.rect.y += change

class Cactus(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = random.choice(cactuses_images)
        self.size = random.choice(cactus_sizes)
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.rect = self.image.get_rect()
        self.rect.x = 800
        self.rect.y = 500 - self.image.get_height()
    def draw(self, win):
        win.blit(self.image, (self.rect.x, self.rect.y))
    def move(self):
        self.rect.x -= 10


# Initializing the game
pygame.init()

# setting up images of dinosaur and the cactuses
dinosaur = pygame.image.load('dinosaur1.png')
resized_dinosaur = pygame.transform.scale(dinosaur, (100, 100))

cactus_sizes = [70,75,80,85,90]
cactus1 = pygame.image.load('cactus1.png')
cactus2 = pygame.image.load('cactus2.png')
cactus3 = pygame.image.load('cactus3.png')
cactuses_images = [cactus1, cactus2, cactus3]
#resized_cactuses = [pygame.transform.scale(cactus1, (cactus_scale , cactus_scale )), pygame.transform.scale(cactus2, (cactus_scale , cactus_scale )), pygame.transform.scale(cactus3, (cactus_scale , cactus_scale ))]

settings_button = pygame.image.load('settings.png')
resized_settings_button = pygame.transform.scale(settings_button, (50, 50))
# setting up a font for the texts
font = pygame.font.Font(None, 36)

# creating the dinosaur/player
player = Dinosaur()
score = 0
player_change = 0

# creating a sprite group for the cactuses
cactuses = pygame.sprite.Group()

# spawning one cactus for testing
cactus = Cactus()
cactuses.add(cactus)

# Setting up the screen
WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dino Game")
pygame.display.set_icon(resized_dinosaur)

# Setting up the clock
clock = pygame.time.Clock()

# main loop
running = True
while running:
    # Handling events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_UP or event.key == pygame.K_w:
                player_change = -resized_dinosaur.get_height()*1.5
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                player_change = resized_dinosaur.get_height()//2
            if event.key == pygame.K_r:
                reset()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                player_change = 0
                player.rect.y = 400
            if event.key == pygame.K_UP or event.key == pygame.K_w or event.key == pygame.K_SPACE:
                player_change = 0
        if event.type == pygame.MOUSEBUTTONDOWN:
            if 750 <= event.pos[0] <= 800 and 10 <= event.pos[1] <= 60:
                print("Settings button clicked")
    
    # applying changes in position
    player.move(player_change)

    # background
    win.fill((255, 255, 255))
    # drawing a straight line to represent the ground
    pygame.draw.line(win, (0, 0, 0), (0, 500), (800, 500), 5)
    # drawing score in the top left corner
    text = font.render("Score: "+str(score), True, (0, 0, 0))
    win.blit(text, (10, 10))
    # drawing the settings button in the top right corner
    win.blit(resized_settings_button, (750, 10))

    # Drawing the player
    player.draw(win)

    # drawing the cactuses
    cactuses.draw(win)

    # moving the cactuses
    for cactus in cactuses:
        cactus.move()
        # removing the cactus if it goes off the screen
        if cactus.rect.x < -50:
            cactuses.remove(cactus)
            score += 1
            # respawning the testing cactus
            cactus = Cactus()
            cactuses.add(cactus)

    # Updating the display
    pygame.display.update()
    # Frame rate
    clock.tick(60)


pygame.quit()