import pygame
import random
import tkinter
import threading

    # functions
# function to reset the game
def reset():
    global player, score, player_change, cactuses, time
    player = Dinosaur()
    score = 0
    player_change = 0
    time = [0,0]
    cactuses.empty()
    cactus = Cactus()
    cactuses.add(cactus)

# function to update the timer
def timer():
    global time, game_over, settings
    while running:
        while game_over:
            pass
        while settings:
            pass
        time[1] += 1
        if time[1] == 60:
            time[0] += 1
            time[1] = 0
        pygame.time.wait(1000)

# function to display the game over screen
def game_over_screen():
    global running, game_over
    game_over = True
    while game_over:
        # Handling events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                game_over = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game_over = False
                    reset()
        # background
        win.fill((255, 255, 255))
        # drawing a straight line to represent the ground
        pygame.draw.line(win, (0, 0, 0), (0, 500), (800, 500), 5)
        # drawing end message
        text = font.render("Game Over! your score is "+str(score), True, (0, 0, 0))
        win.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))

        # Updating the display
        pygame.display.update()
        # Frame rate
        clock.tick(60)

# function to apply the settings
def apply_settings(window):
    window.destroy()

# function for the settings window
def settings_window():
    window = tkinter.Tk()
    window.title("Settings")
    window.geometry("300x300")
    window.resizable(False, False)
    #window.iconbitmap("icon.ico")
    # setting up the main label
    label = tkinter.Label(window, text="Settings", font=("Arial", 24))
    label.pack()
    # setting up a frame for the settings
    frame = tkinter.Frame(window)
    frame.pack()
    # setting up the first setting
    setting1 = tkinter.Label(frame, text="Setting 1", font=("Arial", 16))
    setting1.grid(row=0, column=0)
    setting1_entry = tkinter.Entry(frame, font=("Arial", 16))
    setting1_entry.grid(row=0, column=1)
    # setting up the second setting
    setting2 = tkinter.Label(frame, text="Setting 2", font=("Arial", 16))
    setting2.grid(row=1, column=0)
    setting2_entry = tkinter.Entry(frame, font=("Arial", 16))
    setting2_entry.grid(row=1, column=1)
    # setting up the third setting
    setting3 = tkinter.Label(frame, text="Setting 3", font=("Arial", 16))
    setting3.grid(row=2, column=0)
    setting3_entry = tkinter.Entry(frame, font=("Arial", 16))
    setting3_entry.grid(row=2, column=1)

    # setting up the apply button
    apply_button = tkinter.Button(window, text="Apply", font=("Arial", 16), command= lambda: apply_settings(window))
    apply_button.pack(side="bottom")
    window.mainloop()

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

cactus_sizes = [70,75,80]
cactus1 = pygame.image.load('cactus1.png')
cactus2 = pygame.image.load('cactus2.png')
cactus3 = pygame.image.load('cactus3.png')
cactus4 = pygame.image.load('cactus4.png')
cactus5 = pygame.image.load('cactus5.png')
cactus6 = pygame.image.load('cactus6.png')
cactuses_images = [cactus1, cactus2, cactus3, cactus4, cactus5, cactus6]

pterodactyl = pygame.image.load('pterodactyl_temporary.png')
resized_pterodactyl = pygame.transform.scale(pterodactyl, (100, 100))

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
# setting up a thread for the timer
timer_thread = threading.Thread(target=timer)
time = [0,0]

# main loop
running = True
game_over = False
settings = False
day_night_cycle = False # I will use this later
while running:

    # starting the timer thread
    if not timer_thread.is_alive():
        timer_thread.start()
    # Handling events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_UP or event.key == pygame.K_w:
                player_change = -resized_dinosaur.get_height()*1.8
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
                settings = True
                settings_window()
    
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
    # drawing the time in the top middle of the screen
    text = font.render(str(time[0])+"m "+str(time[1]) + "s", True, (0, 0, 0))
    win.blit(text, (350, 10))

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
    
    # checking for collisions between the player and the cactuses
    if pygame.sprite.spritecollide(player, cactuses, False):
        game_over_screen()
    
    # if the code reaches this part then the settings window is closed
    settings = False

    # Updating the display
    pygame.display.update()
    # Frame rate
    clock.tick(60)


pygame.quit()