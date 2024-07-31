import pygame
import random
import tkinter
import threading

    # functions
# function to reset the game
def reset():
    # resizing everything based on the new width
    global resized_dinosaur_day, resized_dinosaur_night, resized_pterodactyl_day, resized_pterodactyl_night, resized_settings_button, resized_settings_button_night, cactuses_images_day, WIDTH, HEIGHT, base_size, cactuses_images_night, win, cactus_sizes
    WIDTH = win.get_width()
    HEIGHT = WIDTH - WIDTH//4
    base_size = WIDTH//16
    cactus_sizes = [HEIGHT//9,HEIGHT//8,HEIGHT//7.5]
    win = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    # resizing player and pterodactyls and settings button
    resized_dinosaur_day = pygame.transform.scale(dinosaur_day, (base_size*2, base_size*2))
    resized_dinosaur_night = pygame.transform.scale(dinosaur_night, (base_size*2, base_size*2))
    resized_pterodactyl_day = pygame.transform.scale(pterodactyl_day, (base_size*1.5, base_size))
    resized_pterodactyl_night = pygame.transform.scale(pterodactyl_night, (base_size*1.5, base_size))
    resized_settings_button = pygame.transform.scale(settings_button, (base_size, base_size))
    resized_settings_button_night = pygame.transform.scale(settings_button_night, (base_size, base_size))
    # resizing cactuses
    cactuses_images_day = [pygame.transform.scale(cactus1, (base_size, base_size)), 
                           pygame.transform.scale(cactus2, (base_size, base_size)), 
                           pygame.transform.scale(cactus3, (base_size, base_size)), 
                           pygame.transform.scale(cactus4, (base_size, base_size)), 
                           pygame.transform.scale(cactus5, (base_size, base_size)), 
                           pygame.transform.scale(cactus6, (base_size, base_size)), 
                           pygame.transform.scale(cactus7, (base_size, base_size)), 
                           pygame.transform.scale(cactus8, (base_size, base_size)), 
                           pygame.transform.scale(cactus9, (base_size, base_size)), 
                           pygame.transform.scale(cactus10, (base_size, base_size))]
    cactuses_images_night = [pygame.transform.scale(cactus1_night, (base_size, base_size)),
                            pygame.transform.scale(cactus2_night, (base_size, base_size)),
                            pygame.transform.scale(cactus3_night, (base_size, base_size)),
                            pygame.transform.scale(cactus4_night, (base_size, base_size)),
                            pygame.transform.scale(cactus5_night, (base_size, base_size)),
                            pygame.transform.scale(cactus6_night, (base_size, base_size)),
                            pygame.transform.scale(cactus7_night, (base_size, base_size)),
                            pygame.transform.scale(cactus8_night, (base_size, base_size)),
                            pygame.transform.scale(cactus9_night, (base_size, base_size)),
                            pygame.transform.scale(cactus10_night, (base_size, base_size))]

    # reseting values and objects
    global player, score, player_change, enemies, time, cactus, pterodactyls, cycle, switch_cycle
    cycle = "day"
    player = Dinosaur()
    score = 0
    player_change = 0
    time = [0,0]
    enemies.empty()
    cactus = Cactus()
    enemies.add(cactus)
    pterodactyls.empty()
    switch_cycle = False

# function to update the timer
def timer():
    global time, game_over, settings, running, switch_cycle, cycle, cactus
    while running:
        while game_over:
            pass
        while settings:
            pass
        time[1] += 1
        if time[1] == 60:
            time[0] += 1
            time[1] = 0
        # the reason why this is here is because if it were in the main loop it would switch the cycle multiple times in a second
        if switch_cycle:
            if cycle == "day":
                cycle = "night"
                cactus.image = cactus.image_night
            else:
                cycle = "day"
                cactus.image = cactus.image_day
            switch_cycle = False
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

        # what gets displayed depends on the cycle
        if cycle == "day":
            win.fill((255, 255, 255))
            # drawing the ground
            pygame.draw.line(win, (0, 0, 0), (0, HEIGHT//3*2+resized_dinosaur_day.get_height()), (WIDTH, HEIGHT//3*2+resized_dinosaur_day.get_height()), 5)
            # drawing the score
            text = font.render("Score: "+str(score), True, (0, 0, 0))
            win.blit(text, (10, 10))
            # drawing the game over text
            text = font.render("Game Over", True, (0, 0, 0))
            win.blit(text, (win.get_width()//2-text.get_width()//2, win.get_height()//2-text.get_height()//2))
            # drawing the timer
            text = font.render(str(time[0])+"m "+str(time[1]) + "s", True, (0, 0, 0))
            win.blit(text, (WIDTH//2-text.get_width()//2, 10))
        else:
            win.fill((0, 0, 0))
            # drawing the ground
            pygame.draw.line(win, (255, 255, 255), (0, HEIGHT//3*2+resized_dinosaur_day.get_height()), (WIDTH, HEIGHT//3*2+resized_dinosaur_day.get_height()), 5)
            # drawing the score
            text = font.render("Score: "+str(score), True, (255, 255, 255))
            win.blit(text, (10, 10))
            # drawing the game over text
            text = font.render("Game Over", True, (255, 255, 255))
            win.blit(text, (win.get_width()//2-text.get_width()//2, win.get_height()//2-text.get_height()//2))
            # drawing the timer
            text = font.render(str(time[0])+"m "+str(time[1]) + "s", True, (255, 255, 255))
            win.blit(text, (WIDTH//2-text.get_width()//2, 10))

        # drawing the player
        player.draw(win)
        
        # drawing the cactuses and the pterodactyls
        enemies.draw(win)

        # Updating the display
        pygame.display.update()
        # Frame rate
        clock.tick(60)

# function to apply the settings
def apply_settings(window, setting1):
    window.destroy()
    global day_night_cycle
    if setting1:
        day_night_cycle = True
    else:
        day_night_cycle = False

    
    # reseting the game to apply the changes
    reset()

# function for the settings window
def settings_window():
    window = tkinter.Tk()
    window.title("Settings")
    window.geometry("500x400")
    window.resizable(False, False)
    window.iconbitmap("setting.ico")
    # setting up the main label
    label = tkinter.Label(window, text="Settings", font=("Arial", 24))
    label.pack()
    # setting up a frame for the settings
    frame = tkinter.Frame(window)
    frame.pack()
    # setting up the first setting
    setting1 = tkinter.Label(frame, text="Day night cycle", font=("Arial", 16))
    setting1.grid(row=0, column=0)
    e1 = tkinter.StringVar()
    if cycle == "day":
        e1.set("Day")
    else:
        e1.set("Night")
    setting1_checkbox = tkinter.Checkbutton(frame, font=("Arial", 16), variable=e1)
    setting1_checkbox.grid(row=0, column=1)
    # setting up the second setting
    setting2 = tkinter.Label(frame, text="Difficulty", font=("Arial", 16))
    setting2.grid(row=1, column=0)
    e2 = tkinter.StringVar()
    e2.set("Easy")
    option_menu = tkinter.OptionMenu(frame, e2, "Easy", "Medium", "Hard")
    option_menu.grid(row=1, column=1)
    # setting up the third setting
    setting3 = tkinter.Label(frame, text="Pterodactyls", font=("Arial", 16))
    setting3.grid(row=2, column=0)
    e3 = tkinter.StringVar()
    e3.set("On")
    setting3_checkbox = tkinter.Checkbutton(frame, font=("Arial", 16), variable=e3)
    setting3_checkbox.grid(row=2, column=1)
    # setting up timer setting
    setting4 = tkinter.Label(frame, text="Timer", font=("Arial", 16))
    setting4.grid(row=3, column=0)
    e4 = tkinter.StringVar()
    e4.set("On")
    setting4_checkbox = tkinter.Checkbutton(frame, font=("Arial", 16), variable=e4)
    setting4_checkbox.grid(row=3, column=1)
    

    # setting up the apply button
    apply_button = tkinter.Button(window, text="Apply", font=("Arial", 16), command= lambda: apply_settings(window, e1.get()))
    apply_button.pack(side="bottom")
    window.mainloop()

    # classes 
class Dinosaur(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image_day = resized_dinosaur_day
        self.image_night = resized_dinosaur_night
        if cycle == "day":
            self.rect = self.image_day.get_rect()
        else:
            self.rect = self.image_night.get_rect()
        self.rect.y = HEIGHT//3 * 2
        self.rect.x = self.rect.y//10
    def draw(self, win):
        if cycle == "day":
            win.blit(self.image_day, (self.rect.x, self.rect.y))
        else:
            win.blit(self.image_night, (self.rect.x, self.rect.y))
    def move(self, change):
        # if the players y is close enough to the ground then he will be placed on the ground
        if self.rect.y > HEIGHT//3*2-10 and self.rect.y < HEIGHT//3*2:
            self.rect.y = HEIGHT//3 * 2
        if self.rect.y > HEIGHT//3*2 and self.rect.y < HEIGHT//3*2+10:
            self.rect.y = HEIGHT//3 * 2
        # if the player is in the air then he will fall down and he can't jump while he is in the air
        if self.rect.y != HEIGHT//3 * 2:
            if self.rect.y < HEIGHT//3 * 2:
                self.rect.y +=4
        else:
            self.rect.y += change

class Cactus(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # getting a random cactus image
        rand = random.randint(0,len(cactuses_images_day)-1)
        self.image_day = cactuses_images_day[rand]
        self.image_night = cactuses_images_night[rand]
        self.size = random.choice(cactus_sizes)
        self.image_day = pygame.transform.scale(self.image_day, (self.size, self.size))
        self.image_night = pygame.transform.scale(self.image_night, (self.size, self.size))
        self.rect = self.image_day.get_rect()
        if cycle == "day":
            self.image = self.image_day
        else:
            self.image = self.image_night
        self.rect.x = WIDTH
        self.rect.y = HEIGHT//3*2-self.size+resized_dinosaur_day.get_height()
        self.type = "cactus"
    def move(self):
        self.rect.x -= 10

class Pterodactyl(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image_day = resized_pterodactyl_day
        self.image_night = resized_pterodactyl_night
        if cycle == "day":
            self.image = self.image_day
        else:
            self.image = self.image_night
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH
        self.rect.y = random.choice(pterodactyl_heights)
        self.type = "pterodactyl"
        self.size = self.image.get_height()
    def move(self):
        self.rect.x -= 10

# Initializing the game
pygame.init()

# Setting up the screen
WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Dino Game")
icon = pygame.image.load('dinosaur1.png')
pygame.display.set_icon(icon)
base_size = WIDTH//16

# setting up images of dinosaur and the cactuses
dinosaur_day = pygame.image.load('dinosaur1.png')
resized_dinosaur_day = pygame.transform.scale(dinosaur_day, (base_size*2, base_size*2))
dinosaur_night = pygame.image.load('dinosaur2.png')
resized_dinosaur_night = pygame.transform.scale(dinosaur_night, (base_size*2, base_size*2))

# cycle has to be defined pretty high, because its used in the classes
cycle = "day"

# creating a sprite group for the enemies
enemies = pygame.sprite.Group()

# these are for day
cactus_sizes = [HEIGHT//9,HEIGHT//8,HEIGHT//7.5]
cactus1 = pygame.image.load('cactus1.png')
cactus2 = pygame.image.load('cactus2.png')
cactus3 = pygame.image.load('cactus3.png')
cactus4 = pygame.image.load('cactus4.png')
cactus5 = pygame.image.load('cactus5.png')
cactus6 = pygame.image.load('cactus6.png')
cactus7 = pygame.image.load('cactus7.png')
cactus8 = pygame.image.load('cactus8.png')
cactus9 = pygame.image.load('cactus9.png')
cactus10 = pygame.image.load('cactus10.png')
cactuses_images_day = [cactus1, cactus2, cactus3, cactus4, cactus5, cactus6, cactus7, cactus8, cactus9, cactus10]

# these are for night
cactus1_night = pygame.image.load('cactus1_night.png')
cactus2_night = pygame.image.load('cactus2_night.png')
cactus3_night = pygame.image.load('cactus3_night.png')
cactus4_night = pygame.image.load('cactus4_night.png')
cactus5_night = pygame.image.load('cactus5_night.png')
cactus6_night = pygame.image.load('cactus6_night.png')
cactus7_night = pygame.image.load('cactus7_night.png')
cactus8_night = pygame.image.load('cactus8_night.png')
cactus9_night = pygame.image.load('cactus9_night.png')
cactus10_night = pygame.image.load('cactus10_night.png')
cactuses_images_night = [cactus1_night, cactus2_night, cactus3_night, cactus4_night, cactus5_night, cactus6_night, cactus7_night, cactus8_night, cactus9_night, cactus10_night]

pterodactyl_day = pygame.image.load('pterodactyl_temporary.png')
resized_pterodactyl_day = pygame.transform.scale(pterodactyl_day, (base_size*1.5, base_size))
pterodactyl_night = pygame.image.load('pterodactyl_temporary2.png')
resized_pterodactyl_night = pygame.transform.scale(pterodactyl_night, (base_size*1.5, base_size))

chance_of_pterodactyl = 20
pterodactyl_spawn = False
pterodactyl_heights = [HEIGHT//3*2-resized_pterodactyl_day.get_height(), HEIGHT//3*2+50-resized_pterodactyl_day.get_height(), HEIGHT//3*2+100-resized_pterodactyl_day.get_height()]
pterodactyls = pygame.sprite.Group()

settings_button = pygame.image.load('settings.png')
resized_settings_button = pygame.transform.scale(settings_button, (base_size, base_size))
settings_button_night = pygame.image.load('settings_night.png')
resized_settings_button_night = pygame.transform.scale(settings_button_night, (base_size, base_size))

# setting up a font for the texts
font = pygame.font.Font(None, HEIGHT//18)

# creating the dinosaur/player
player = Dinosaur()
score = 0
player_change = 0

# spawning one cactus for testing
cactus = Cactus()
enemies.add(cactus)

# Setting up the clock
clock = pygame.time.Clock()

# setting up a thread for the timer
timer_thread = threading.Thread(target=timer)
time = [0,0]

# main loop
running = True
game_over = False
settings = False
day_night_cycle = True
switch_cycle = False
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
                player_change = -resized_dinosaur_day.get_height()*1.8
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                player_change = resized_dinosaur_day.get_height()//2
            if event.key == pygame.K_r:
                reset()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                player_change = 0
                player.rect.y = HEIGHT//3 * 2
            if event.key == pygame.K_UP or event.key == pygame.K_w or event.key == pygame.K_SPACE:
                player_change = 0
        if event.type == pygame.MOUSEBUTTONDOWN:
            if WIDTH-resized_settings_button.get_width() <= event.pos[0] <= WIDTH and 10 <= event.pos[1] <= resized_settings_button_night.get_height()+10:
                settings = True
                settings_window()
    
    # applying changes in position
    player.move(player_change)

    # background
    if cycle == "day":
        win.fill((255, 255, 255))
    else:
        win.fill((0, 0, 0))
    # drawing a straight line to represent the ground
    if cycle == "day":
        pygame.draw.line(win, (0, 0, 0), (0, HEIGHT//3*2+resized_dinosaur_day.get_height()), (WIDTH, HEIGHT//3*2+resized_dinosaur_day.get_height()), 5)
    else:
        pygame.draw.line(win, (255, 255, 255), (0, HEIGHT//3*2+resized_dinosaur_day.get_height()), (WIDTH, HEIGHT//3*2+resized_dinosaur_day.get_height()), 5)
    # drawing score in the top left corner
    if cycle == "day":
        text = font.render("Score: "+str(score), True, (0, 0, 0))
    else:
        text = font.render("Score: "+str(score), True, (255, 255, 255))
    win.blit(text, (10, 10))
    # drawing the settings button in the top right corner
    if cycle == "day":
        win.blit(resized_settings_button, (WIDTH-resized_settings_button_night.get_width(), 10))
    else:
        win.blit(resized_settings_button_night, (WIDTH-resized_settings_button_night.get_width(), 10))
    # drawing the time in the top middle of the screen
    if cycle == "day":
        text = font.render(str(time[0])+"m "+str(time[1]) + "s", True, (0, 0, 0))
    else:
        text = font.render(str(time[0])+"m "+str(time[1]) + "s", True, (255, 255, 255))
    win.blit(text, (WIDTH//2-text.get_width()//2, 10))

    # Drawing the player
    player.draw(win)

    # drawing the cactuses
    enemies.draw(win)

    # moving the cactuses
    for enemy in enemies:
        enemy.move()
        if enemy.rect.x < -100-enemy.size:
            if enemy.type == "cactus":
                enemies.remove(enemy)
                # this ensures that there is only 1 cactus or 1 pterodactyl on the screen at the same time
                if pterodactyl_spawn:
                    pterodactyl = Pterodactyl()
                    enemies.add(pterodactyl)
                    pterodactyls.add(pterodactyl)
                    pterodactyl_spawn = False
                else:
                    cactus = Cactus()
                    enemies.add(cactus)
            if enemy.type == "pterodactyl":
                enemies.remove(enemy)
                if pterodactyl_spawn:
                    pterodactyl = Pterodactyl()
                    enemies.add(pterodactyl)
                    pterodactyls.add(pterodactyl)
                    pterodactyl_spawn = False
                else:
                    cactus = Cactus()
                    enemies.add(cactus)
            score += 1

    # spawning the pterodactyl
    if score > 0 and len(pterodactyls) == 0:
        rand = random.randint(0, 100)
        if rand < chance_of_pterodactyl:
            pterodactyl_spawn = True
    
    # checking for collisions between the player and the enemies
    if pygame.sprite.spritecollide(player, enemies, False):
        game_over_screen()

    # this is the day night cycle switching, it will be used later when I add the opposite color images
    if time[1] == 9 and day_night_cycle:
        switch_cycle = True
    
    # if the code reaches this part then the settings window is closed
    settings = False

    # Updating the display
    pygame.display.update()

    # Frame rate
    clock.tick(60)


pygame.quit()