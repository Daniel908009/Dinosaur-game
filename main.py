import pygame
import random
import tkinter
import threading
from pygame import mixer

    # functions
# function to reset the game
def reset():
    # resizing everything based on the new width
    global resized_dinosaur_day, resized_dinosaur_night, resized_pterodactyl_day, resized_pterodactyl_night, resized_settings_button, resized_settings_button_night, cactuses_images_day, WIDTH, HEIGHT, base_size, cactus_sizes, resized_dinosaur_day2, resized_dinosaur_night2, win, pterodactyl_spawn, cactuses_images_night
    WIDTH = win.get_width()
    HEIGHT = WIDTH - WIDTH//4
    base_size = WIDTH//16
    cactus_sizes = [HEIGHT//9,HEIGHT//8,HEIGHT//7.5]
    win = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    # resetting the pterodactyl spawn
    pterodactyl_spawn = False
    # resizing player and pterodactyls and settings button
    dev_mode_images_change()

    # resizing the settings button
    global resized_settings_button, resized_settings_button_night, resized_home_button, resized_home_button_night
    settings_button = pygame.image.load('main_assets/settings.png')
    resized_settings_button = pygame.transform.scale(settings_button, (base_size, base_size))
    settings_button_night = pygame.image.load('main_assets/settings_night.png')
    resized_settings_button_night = pygame.transform.scale(settings_button_night, (base_size, base_size))
    resized_home_button = pygame.transform.scale(home_button, (base_size, base_size))
    resized_home_button_night = pygame.transform.scale(home_button_night, (base_size, base_size))
    # resizing the buttons
    global resized_play_button, resized_scores_button, resized_exit_button, resized_back_arrow
    resized_exit_button = pygame.transform.scale(exit_button, (base_size*5, base_size*2))
    resized_play_button = pygame.transform.scale(play_button, (base_size*5, base_size*2))
    resized_scores_button = pygame.transform.scale(scores_button, (base_size*5, base_size*2))
    resized_back_arrow = pygame.transform.scale(back_arrow, (base_size*2, base_size*2))
    # reseting the background objects
    global background_objects, spawn_background_object, when_will_spawn_background_object, score
    background_objects.empty()
    spawn_background_object = False
    score = 0
    when_will_spawn_background_object = random.randint(score+5, score+20)
    # getting the new cloud sizes
    global clouds_sizes
    clouds_sizes = [base_size*3, base_size*2, base_size*2.5]

    # reseting values and objects
    global player, player_change, enemies, time, cactus, pterodactyls, cycle, switch_cycle, clouds_group
    cycle = "day"
    player = Dinosaur()
    player_change = 0
    time = [0,0]
    enemies.empty()
    cactus = Cactus()
    enemies.add(cactus)
    pterodactyls.empty()
    switch_cycle = False
    clouds_group.empty()
    # reseting the background music and background loudness, and sound loudness
    global background_music, background_music_on, current_background_music_loudness, current_sound_loudness, background_music_playing, selected_music
    if background_music_on:
        mixer.music.load(str(selected_music))
        mixer.music.set_volume(current_background_music_loudness/100)
        background_music_playing = False
    else:
        mixer.music.stop()
    # reseting the sound effects
    global touchdown, game_over_sound, sound_effects_on, current_sound_loudness, hit_sound
    touchdown = mixer.Sound("sounds/energy_sound.mp3")
    game_over_sound = mixer.Sound("sounds/game_over_sound.mp3")
    hit_sound = mixer.Sound("sounds/hit_sound.mp3")
    touchdown.set_volume(current_sound_loudness/100)
    game_over_sound.set_volume(current_sound_loudness/100)
    hit_sound.set_volume(current_sound_loudness/100)
    # getting the new ptarodactyl height
    global pterodactyl_heights
    pterodactyl_heights = [HEIGHT//3*2-resized_pterodactyl_day.get_height(), HEIGHT//3*2-resized_pterodactyl_day.get_height()*2, HEIGHT//3*2+resized_pterodactyl_day.get_height()]

# function to update the timer
def timer():
    global time, game_over, settings, running, switch_cycle, cycle, cactus, timer_stop, background_objects, spawn_background_object, when_will_spawn_background_object, when_will_cloud, spawn_cloud, clouds_group, score
    while running:
        while game_over and running:
            pass
        while settings and running:
            pass
        while timer_stop and running:
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
                for object in background_objects:
                    object.image = object.image_night
                for object in clouds_group:
                    object.image = object.image_night
            else:
                cycle = "day"
                cactus.image = cactus.image_day
                for object in background_objects:
                    object.image = object.image_day
                for object in clouds_group:
                    object.image = object.image_day
            switch_cycle = False
        # spawning background objects
        if spawn_background_object:
            background_objects.add(BackgroundObject())
            spawn_background_object = False
            when_will_spawn_background_object = random.randint(score+5, score+20)
        # spawning clouds
        if spawn_cloud:
            clouds_group.add(Clouds())
            spawn_cloud = False
            when_will_cloud = random.randint(score+5, score+20)

        clock.tick(1)

# function for the main menu loop
def main_menu_window(screen):
    global running, settings, main_menu, selected_music
    main_menu_running = True
    main_menu_font = pygame.font.Font("freesansbold.ttf", 60)
    scores_window = False
    # getting the first 10 scores from the file
    try:
        with open("scores.txt", "r") as file:
            scores = file.readlines()
        scores = [score.strip() for score in scores]
        scores = [score.split() for score in scores]
        scores = sorted(scores, key=lambda x: int(x[1]), reverse=True)
        file.close()
    except FileNotFoundError:
        scores = []
    # creating a font for the scores
    scores_font = pygame.font.Font("freesansbold.ttf", HEIGHT//20)
    # main menu loop
    while main_menu_running:
        # in case player wants to see the scores, it will be done through this loop
        while scores_window:
            # Handling events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    main_menu_running = False
                    running = False
                    settings = False
                    scores_window = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        settings_window()
                    if event.key == pygame.K_r:
                        reset()
                    if event.key == pygame.K_q:
                        scores_window = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # checking if the back arrow was clicked
                    if 10 <= event.pos[0] <= 10+resized_back_arrow.get_width() and 10 <= event.pos[1] <= 10+resized_back_arrow.get_height():
                        scores_window = False
            # background color
            win.fill((255, 255, 255))
            # displaying the main label
            text = main_menu_font.render("Scores", True, (0, 0, 0))
            win.blit(text, (WIDTH//2-text.get_width()//2, HEIGHT//6))
            # displaying a back arrow
            win.blit(resized_back_arrow, (10, 10))
            # displaying the scores(only the top 10/which means the first 10 lines)
            if scores == []:
                text = main_menu_font.render("No scores yet", True, (0, 0, 0))
                win.blit(text, (WIDTH//2-text.get_width()//2, HEIGHT//3))
            else:
                for i in range(10):
                    try:
                        text = scores_font.render(str(i+1)+". Name: "+scores[i][0]+", score: "+scores[i][1], True, (0, 0, 0))
                        win.blit(text, (WIDTH//2-text.get_width()//2, HEIGHT//3+text.get_height()*i))
                    except IndexError:
                        pass
            pygame.display.update()

        # Handling events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                main_menu_running = False
                running = False
                settings = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    settings_window()
                if event.key == pygame.K_r:
                    reset()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # checking if the play button was clicked
                if WIDTH//2-resized_play_button.get_width()//2 <= event.pos[0] <= WIDTH//2+resized_play_button.get_width()//2 and HEIGHT//3 <= event.pos[1] <= HEIGHT//3+resized_play_button.get_height():
                    mixer.music.load(str(selected_music))
                    reset()
                    main_menu_running = False
                    main_menu = False
                # checking if the scores button was clicked
                if WIDTH//2-resized_scores_button.get_width()//2 <= event.pos[0] <= WIDTH//2+resized_scores_button.get_width()//2 and HEIGHT//3+resized_play_button.get_height()*1.2 <= event.pos[1] <= HEIGHT//3+resized_play_button.get_height()*1.2+resized_scores_button.get_height():
                    scores_window = True
                # checking if the exit button was clicked
                if WIDTH//2-resized_exit_button.get_width()//2 <= event.pos[0] <= WIDTH//2+resized_exit_button.get_width()//2 and HEIGHT//3+resized_play_button.get_height()*2*1.2 <= event.pos[1] <= HEIGHT//3+resized_play_button.get_height()*2*1.2+resized_exit_button.get_height():
                    main_menu_running = False
                    running = False
                    settings = False
            # displaying the different buttons and texts
        #background
        win.fill((255, 255, 255))
        # drawing a main label
        text = main_menu_font.render("Dino Run", True, (0, 0, 0))
        win.blit(text, (WIDTH//2-text.get_width()//2, HEIGHT//6))
        # drawing the first button(play)
        screen.blit(resized_play_button, (WIDTH//2-resized_play_button.get_width()//2, HEIGHT//3))
        # drawing the second button(scores)
        screen.blit(resized_scores_button, (WIDTH//2-resized_scores_button.get_width()//2, HEIGHT//3+resized_play_button.get_height()*1.2))
        # drawing the third button(exit)
        screen.blit(resized_exit_button, (WIDTH//2-resized_exit_button.get_width()//2, HEIGHT//3+resized_play_button.get_height()*2*1.2))

        pygame.display.update()

# function that will get a random fact about dinosaurs, this will be displayed on the screen for a few seconds
def fact_func():
    # this will be done later
    pass

# function to display the game over screen
def game_over_screen():
    global running, game_over, game_over_sound, main_menu, player_name, score
    game_over = True
    global background_music
    background_music = mixer.music.stop()
    game_over_sound.play()
    if sound_effects_on:
        game_over_sound.play()
    # now writing the score to a file(each score on a new line)
    try:
        with open("scores.txt", "a") as file:
            file.write(str(player_name)+" "+str(score)+"\n")
    except FileNotFoundError:
        with open("scores.txt", "w") as file:
            file.write(str(player_name)+" "+str(score)+"\n")
    file.close()
    # now reading the content of the file and ordering it from the highest to the lowest(this will be usefull in the scores button)
    with open("scores.txt", "r") as file:
        scores = file.readlines()
    scores = [score.strip() for score in scores]
    #print(scores)
    scores = [score.split() for score in scores]
    #print(scores)
    scores = sorted(scores, key=lambda x: int(x[1]), reverse=True)
    file.close()
    # now writing the ordered scores to the file
    with open("scores.txt", "w") as file:
        for score1 in scores:
            file.write(score1[0]+" "+score1[1]+"\n")
    file.close()
    # game over loop
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
                if event.key == pygame.K_q:
                    main_menu = True
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
            # drawing the sun
            win.blit(resized_sun, (10,text.get_height()*2.5))
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
            # drawing the moon
            win.blit(resized_moon, (10,text.get_height()*2.5))

        # drawing the player
        player.draw(win)
        
        # drawing the cactuses and the pterodactyls
        enemies.draw(win)

        # drawing the clouds
        clouds_group.draw(win)

        # Updating the display
        pygame.display.update()
        # Frame rate
        clock.tick(60)

# function to change the images when dev mode is on
def dev_mode_images_change():
    global dev_mode
    if dev_mode:
        global dinosaur_day, dinosaur_day2, dinosaur_night, cactus1, cactus2, cactus3, cactus4, cactus5, cactus6, cactus7, cactus8, cactus9, cactus10, cactus1_night, cactus2_night, cactus3_night, cactus4_night, cactus5_night, cactus6_night, cactus7_night, cactus8_night, cactus9_night, cactus10_night, pterodactyl_day, pterodactyl_night, powerup1_day, powerup2_day, powerup3_day, powerup1_night, powerup2_night, powerup3_night, resized_dinosaur_day, resized_dinosaur_day2, resized_dinosaur_night, resized_dinosaur_night2, resized_pterodactyl_day, resized_pterodactyl_night, resized_powerup1_day, resized_powerup2_day, resized_powerup3_day, resized_powerup1_night, resized_powerup2_night, resized_powerup3_night, dinosaur_night2, dinosaur_day_ducked, dinosaur_night_ducked, dinosaur_day2_ducked, dinosaur_night2_ducked, resized_dinosaur_day_ducked, resized_dinosaur_night_ducked, resized_dinosaur_day2_ducked, resized_dinosaur_night2_ducked, powerup4_day, powerup4_night
        # i will need to do global twice, because there are so many variables I dont want to scroll all the way to the right
        global resized_powerup4_day, resized_powerup4_night
        dinosaur_day = pygame.image.load('dev_mode_assets/dinosaur1_dev.png')
        dinosaur_day2 = pygame.image.load('dev_mode_assets/dinosaur1_2_dev.png')
        dinosaur_night = pygame.image.load('dev_mode_assets/dinosaur2_dev.png')
        dinosaur_night2 = pygame.image.load('dev_mode_assets/dinosaur2_2_dev.png')
        dinosaur_day_ducked = pygame.image.load('dev_mode_assets/dinosaur1_ducked_dev.png')
        dinosaur_night_ducked = pygame.image.load('dev_mode_assets/dinosaur2_ducked_dev.png')
        dinosaur_day2_ducked = pygame.image.load('dev_mode_assets/dinosaur1_2_ducked_dev.png')
        dinosaur_night2_ducked = pygame.image.load('dev_mode_assets/dinosaur2_2_ducked_dev.png')
        cactus1 = pygame.image.load('dev_mode_assets/cactus1_dev.png')
        cactus2 = pygame.image.load('dev_mode_assets/cactus2_dev.png')
        cactus3 = pygame.image.load('dev_mode_assets/cactus3_dev.png')
        cactus4 = pygame.image.load('dev_mode_assets/cactus4_dev.png')
        cactus5 = pygame.image.load('dev_mode_assets/cactus5_dev.png')
        cactus6 = pygame.image.load('dev_mode_assets/cactus6_dev.png')
        cactus7 = pygame.image.load('dev_mode_assets/cactus7_dev.png')
        cactus8 = pygame.image.load('dev_mode_assets/cactus8_dev.png')
        cactus9 = pygame.image.load('dev_mode_assets/cactus9_dev.png')
        cactus10 = pygame.image.load('dev_mode_assets/cactus10_dev.png')
        cactus1_night = pygame.image.load('dev_mode_assets/cactus1_night_dev.png')
        cactus2_night = pygame.image.load('dev_mode_assets/cactus2_night_dev.png')
        cactus3_night = pygame.image.load('dev_mode_assets/cactus3_night_dev.png')
        cactus4_night = pygame.image.load('dev_mode_assets/cactus4_night_dev.png')
        cactus5_night = pygame.image.load('dev_mode_assets/cactus5_night_dev.png')
        cactus6_night = pygame.image.load('dev_mode_assets/cactus6_night_dev.png')
        cactus7_night = pygame.image.load('dev_mode_assets/cactus7_night_dev.png')
        cactus8_night = pygame.image.load('dev_mode_assets/cactus8_night_dev.png')
        cactus9_night = pygame.image.load('dev_mode_assets/cactus9_night_dev.png')
        cactus10_night = pygame.image.load('dev_mode_assets/cactus10_night_dev.png')
        pterodactyl_day = pygame.image.load('dev_mode_assets/pterodactyl_temporary_dev.png')
        pterodactyl_night = pygame.image.load('dev_mode_assets/pterodactyl_temporary2_dev.png')
        powerup1_day = pygame.image.load('dev_mode_assets/power_up1_day_dev.png')
        powerup2_day = pygame.image.load('dev_mode_assets/power_up2_day_dev.png')
        powerup3_day = pygame.image.load('dev_mode_assets/power_up3_day_dev.png')
        powerup1_night = pygame.image.load('dev_mode_assets/power_up1_night_dev.png')
        powerup2_night = pygame.image.load('dev_mode_assets/power_up2_night_dev.png')
        powerup3_night = pygame.image.load('dev_mode_assets/power_up3_night_dev.png')
        #powerup4_day = pygame.image.load('dev_mode_assets/power_up4_day_dev.png')
        #powerup4_night = pygame.image.load('dev_mode_assets/power_up4_night_dev.png')
    else:
        dinosaur_day = pygame.image.load('main_assets/dinosaur1.png')
        dinosaur_day2 = pygame.image.load('main_assets/dinosaur1_2.png')
        dinosaur_night = pygame.image.load('main_assets/dinosaur2.png')
        dinosaur_night2 = pygame.image.load('main_assets/dinosaur2_2.png')
        dinosaur_day_ducked = pygame.image.load('main_assets/dinosaur1_ducked.png')
        dinosaur_night_ducked = pygame.image.load('main_assets/dinosaur2_ducked.png')
        dinosaur_day2_ducked = pygame.image.load('main_assets/dinosaur1_2_ducked.png')
        dinosaur_night2_ducked = pygame.image.load('main_assets/dinosaur2_2_ducked.png')
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
        pterodactyl_day = pygame.image.load('main_assets/pterodactyl_temporary.png')
        pterodactyl_night = pygame.image.load('main_assets/pterodactyl_temporary2.png')
        powerup1_day = pygame.image.load('powerups/power_up1_day.png')
        powerup2_day = pygame.image.load('powerups/power_up2_day.png')
        powerup3_day = pygame.image.load('powerups/power_up3_day.png')
        powerup1_night = pygame.image.load('powerups/power_up1_night.png')
        powerup2_night = pygame.image.load('powerups/power_up2_night.png')
        powerup3_night = pygame.image.load('powerups/power_up3_night.png')
        powerup4_day = pygame.image.load('powerup4.png')
        powerup4_night = pygame.image.load('powerup4_night.png')
    # resizing the images
    resized_dinosaur_day = pygame.transform.scale(dinosaur_day, (base_size*2, base_size*2))
    resized_dinosaur_night = pygame.transform.scale(dinosaur_night, (base_size*2, base_size*2))
    resized_dinosaur_day2 = pygame.transform.scale(dinosaur_day2, (base_size*2, base_size*2))
    resized_dinosaur_night2 = pygame.transform.scale(dinosaur_night2, (base_size*2, base_size*2))
    resized_dinosaur_day_ducked = pygame.transform.scale(dinosaur_day_ducked, (base_size*2, base_size*1.5))
    resized_dinosaur_night_ducked = pygame.transform.scale(dinosaur_night_ducked, (base_size*2, base_size*1.5))
    resized_dinosaur_day2_ducked = pygame.transform.scale(dinosaur_day2_ducked, (base_size*2, base_size*1.5))
    resized_dinosaur_night2_ducked = pygame.transform.scale(dinosaur_night2_ducked, (base_size*2, base_size*1.5))
    resized_pterodactyl_day = pygame.transform.scale(pterodactyl_day, (base_size*1.5, base_size))
    resized_pterodactyl_night = pygame.transform.scale(pterodactyl_night, (base_size*1.5, base_size))
    resized_powerup1_day = pygame.transform.scale(powerup1_day, (base_size, base_size))
    resized_powerup2_day = pygame.transform.scale(powerup2_day, (base_size, base_size))
    resized_powerup3_day = pygame.transform.scale(powerup3_day, (base_size, base_size))
    resized_powerup4_day = pygame.transform.scale(powerup4_day, (base_size, base_size))
    resized_powerup1_night = pygame.transform.scale(powerup1_night, (base_size, base_size))
    resized_powerup2_night = pygame.transform.scale(powerup2_night, (base_size, base_size))
    resized_powerup3_night = pygame.transform.scale(powerup3_night, (base_size, base_size))
    resized_powerup4_night = pygame.transform.scale(powerup4_night, (base_size, base_size))
    # now filling the lists with the resized images, also here was a mistake, for some reason I resized the powerups twice
    # however it didnt visibly affect the game, its fixed now
    global resized_powerups_day, resized_powerups_night
    resized_powerups_day = [resized_powerup1_day, resized_powerup2_day, resized_powerup3_day, resized_powerup4_day]
    resized_powerups_night = [resized_powerup1_night, resized_powerup2_night, resized_powerup3_night, resized_powerup4_night]
    # pterodactyls images resizing
    resized_pterodactyl_day = pygame.transform.scale(pterodactyl_day, (base_size*1.5, base_size))
    resized_pterodactyl_night = pygame.transform.scale(pterodactyl_night, (base_size*1.5, base_size))
    # resizing cactuses
    global cactuses_images_day, cactuses_images_night
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

# function to apply the dev mode settings
def apply_dev_mode(setting1, setting2, setting3, setting4, setting5, setting6, setting7):
    global dev_mode
    if setting1 == "1":
        dev_mode = True
    else:
        dev_mode = False
    global infinite_lives_on
    if setting2 == "1":
        infinite_lives_on = True
    else:
        infinite_lives_on = False
    global super_jump_on
    if setting3 == "1":
        super_jump_on = True
    else:
        super_jump_on = False
    global manual_cycle_switch_on
    if setting4 == "1":
        manual_cycle_switch_on = True
    else:
        manual_cycle_switch_on = False
    global manual_pterodactyl_spawn_on
    if setting5 == "1":
        manual_pterodactyl_spawn_on = True
    else:
        manual_pterodactyl_spawn_on = False
    global manual_powerup_spawn_on
    if setting6 == "1":
        manual_powerup_spawn_on = True
    else:
        manual_powerup_spawn_on = False
    global fps_on
    if setting7 == "1":
        fps_on = True
    else:
        fps_on = False

# function to apply the settings
def apply_settings(window, setting1, setting2, setting3, setting4, setting5, setting6, setting7, setting8, setting9, setting10, setting11, setting12, setting13, background_music_loudness, sound_loudness, setting14):
    window.destroy()
    # applying the dev mode settings
    apply_dev_mode(setting7, setting8, setting9, setting10, setting11, setting12, setting13)
    # applying the setting for the loudness
    global current_sound_loudness, current_background_music_loudness
    current_sound_loudness = sound_loudness
    current_background_music_loudness = background_music_loudness
    # applying the setting for the day night cycle
    global day_night_cycle
    if setting1 == "1":
        day_night_cycle = True
    else:
        day_night_cycle = False
    # applying the setting for the dificulty
    global dificulty
    dificulty = setting2
    global pterodactyl_on
    # applying the setting for the pterodactyls
    if setting3 == "1":
        pterodactyl_on = True
    else:
        pterodactyl_on = False
    # applying the setting for the timer
    global timer_stop
    if setting4 == "1":
        timer_stop = False
    else:
        timer_stop = True
    # applying the setting for the background music and sound effects
    global background_music_on
    if setting5 == "0":
        background_music_on = False
    else:
        background_music_on = True
    global sound_effects_on
    if setting6 == "0":
        sound_effects_on = False
    else:
        sound_effects_on = True
    # applying the setting for the background music type
    global selected_music
    if setting14 == "country":
        selected_music = "sounds/background_music.mp3"
    elif setting14 == "rock":
        selected_music = "sounds/rock_question_mark.mp3"
    elif setting14 == "opera":
        selected_music = "sounds/opera.mp3"
    elif setting14 == "techno":
        selected_music = "sounds/techno.mp3"
    # reseting the game to apply the changes
    reset()

# function for the settings window
def settings_window():
    window = tkinter.Tk()
    window.title("Settings")
    window.geometry("700x450")
    window.resizable(False, False)
    window.iconbitmap("main_assets/setting.ico")
    # setting up the main label
    label = tkinter.Label(window, text="Settings X Dev menu", font=("Arial", 24))
    label.pack()
    # setting up a frame for the settings
    frame = tkinter.Frame(window)
    frame.pack()
    # setting up the first setting
    setting1 = tkinter.Label(frame, text="Day night cycle", font=("Arial", 16))
    setting1.grid(row=0, column=0)
    e1 = tkinter.StringVar()
    if day_night_cycle:
        e1.set(1)
    else:
        e1.set(0)
    setting1_checkbox = tkinter.Checkbutton(frame, font=("Arial", 16), variable=e1)
    setting1_checkbox.grid(row=0, column=1)
    # setting up the second setting
    setting2 = tkinter.Label(frame, text="Difficulty", font=("Arial", 16))
    setting2.grid(row=1, column=0)
    e2 = tkinter.StringVar()
    e2.set(str(dificulty))
    option_menu = tkinter.OptionMenu(frame, e2, "Easy", "Medium", "Hard")
    option_menu.grid(row=1, column=1)
    # setting up the third setting
    setting3 = tkinter.Label(frame, text="Pterodactyls", font=("Arial", 16))
    setting3.grid(row=2, column=0)
    e3 = tkinter.StringVar()
    if pterodactyl_on:
        e3.set(1)
    else:
        e3.set(0)
    setting3_checkbox = tkinter.Checkbutton(frame, font=("Arial", 16), variable=e3)
    setting3_checkbox.grid(row=2, column=1)
    # setting up timer setting
    setting4 = tkinter.Label(frame, text="Timer", font=("Arial", 16))
    setting4.grid(row=3, column=0)
    e4 = tkinter.StringVar()
    if timer_stop:
        e4.set(0)
    else:
        e4.set(1)
    setting4_checkbox = tkinter.Checkbutton(frame, font=("Arial", 16), variable=e4)
    setting4_checkbox.grid(row=3, column=1)
    # setting for background music
    setting5 = tkinter.Label(frame, text="Background music", font=("Arial", 16))
    setting5.grid(row=4, column=0)
    e5 = tkinter.StringVar()
    if background_music_on:
        e5.set(1)
    else:
        e5.set(0)
    setting5_checkbox = tkinter.Checkbutton(frame, font=("Arial", 16), variable=e5, onvalue=1, offvalue=0)
    setting5_checkbox.grid(row=4, column=1)
    # setting for sound effects
    setting6 = tkinter.Label(frame, text="Sound effects", font=("Arial", 16))
    setting6.grid(row=5, column=0)
    e6 = tkinter.StringVar()
    if sound_effects_on:
        e6.set(1)
    else:
        e6.set(0)
    setting6_checkbox = tkinter.Checkbutton(frame, font=("Arial", 16), variable=e6, onvalue=1, offvalue=0)
    setting6_checkbox.grid(row=5, column=1)
    # setting for the sound loudness
    sound_loudness = tkinter.Label(frame, text="Sound loudness", font=("Arial", 16))
    sound_loudness.grid(row=6, column=0)
    sound_loud = tkinter.StringVar()
    sound_loud.set(current_sound_loudness)
    sound_loudness_slider = tkinter.Scale(frame, from_=0, to=100, orient="horizontal", variable=sound_loud)
    sound_loudness_slider.grid(row=6, column=1)
    # setting for the background music loudness
    background_music_loudness = tkinter.Label(frame, text="Background music loudness", font=("Arial", 16))
    background_music_loudness.grid(row=7, column=0)
    background_music_loud = tkinter.StringVar()
    background_music_loud.set(current_background_music_loudness)
    background_music_loudness_slider = tkinter.Scale(frame, from_=0, to=100, orient="horizontal", variable=background_music_loud)
    background_music_loudness_slider.grid(row=7, column=1)
    # setting for the background music type
    background_music_type = tkinter.Label(frame, text="Background music type", font=("Arial", 16))
    background_music_type.grid(row=8, column=0)
    e14 = tkinter.StringVar()
    if selected_music == "sounds/background.mp3":
        e14.set("country")
    elif selected_music == "sounds/rock_question_mark.mp3":
        e14.set("rock")
    elif selected_music == "sounds/opera.mp3":
        e14.set("opera")
    elif selected_music == "sounds/techno.mp3":
        e14.set("techno")
    option_menu2 = tkinter.OptionMenu(frame, e14, "country", "rock", "opera", "techno")
    option_menu2.grid(row=8, column=1)
    # settings for dev mode
    setting7 = tkinter.Label(frame, text="Dev mode", font=("Arial", 16))
    setting7.grid(row=0, column=2)
    e7 = tkinter.StringVar()
    if dev_mode:
        e7.set(1)
    else:
        e7.set(0)
    setting7_checkbox = tkinter.Checkbutton(frame, font=("Arial", 16), variable=e7, onvalue=1, offvalue=0)
    setting7_checkbox.grid(row=0, column=3)
    # setting for infinite lives
    setting8 = tkinter.Label(frame, text="Infinite lives", font=("Arial", 16))
    setting8.grid(row=1, column=2)
    e8 = tkinter.StringVar()
    if infinite_lives_on:
        e8.set(1)
    else:
        e8.set(0)
    setting8_checkbox = tkinter.Checkbutton(frame, font=("Arial", 16), variable=e8, onvalue=1, offvalue=0)
    setting8_checkbox.grid(row=1, column=3)
    # setting for super jump
    setting9 = tkinter.Label(frame, text="Super jump", font=("Arial", 16))
    setting9.grid(row=2, column=2)
    e9 = tkinter.StringVar()
    if super_jump_on:
        e9.set(1)
    else:
        e9.set(0)
    setting9_checkbox = tkinter.Checkbutton(frame, font=("Arial", 16), variable=e9, onvalue=1, offvalue=0)
    setting9_checkbox.grid(row=2, column=3)
    # setting for manual cycle switch
    setting10 = tkinter.Label(frame, text="Manual cycle switch", font=("Arial", 16))
    setting10.grid(row=3, column=2)
    e10 = tkinter.StringVar()
    if manual_cycle_switch_on:
        e10.set(1)
    else:
        e10.set(0)
    setting10_checkbox = tkinter.Checkbutton(frame, font=("Arial", 16), variable=e10, onvalue=1, offvalue=0)
    setting10_checkbox.grid(row=3, column=3)
    # setting for manual pterodactyl spawn
    setting11 = tkinter.Label(frame, text="Manual pterodactyl spawn", font=("Arial", 16))
    setting11.grid(row=4, column=2)
    e11 = tkinter.StringVar()
    if manual_pterodactyl_spawn_on:
        e11.set(1)
    else:
        e11.set(0)
    setting11_checkbox = tkinter.Checkbutton(frame, font=("Arial", 16), variable=e11, onvalue=1, offvalue=0)
    setting11_checkbox.grid(row=4, column=3)
    # setting for manual powerup spawn
    setting12 = tkinter.Label(frame, text="Manual powerup spawn", font=("Arial", 16))
    setting12.grid(row=5, column=2)
    e12 = tkinter.StringVar()
    if manual_powerup_spawn_on:
        e12.set(1)
    else:
        e12.set(0)
    setting12_checkbox = tkinter.Checkbutton(frame, font=("Arial", 16), variable=e12, onvalue=1, offvalue=0)
    setting12_checkbox.grid(row=5, column=3)
    # setting for fps
    setting13 = tkinter.Label(frame, text="FPS", font=("Arial", 16))
    setting13.grid(row=6, column=2)
    e13 = tkinter.StringVar()
    if fps_on:
        e13.set(1)
    else:
        e13.set(0)
    setting13_checkbox = tkinter.Checkbutton(frame, font=("Arial", 16), variable=e13, onvalue=1, offvalue=0)
    setting13_checkbox.grid(row=6, column=3)

    # setting up the apply button
    apply_button = tkinter.Button(window, text="Apply", font=("Arial", 16), command= lambda: apply_settings(window, e1.get(), e2.get(), e3.get(), e4.get(), e5.get(), e6.get(), e7.get(), e8.get(), e9.get(), e10.get(), e11.get(), e12.get(), e13.get(), background_music_loudness_slider.get(), sound_loudness_slider.get(), e14.get()))
    apply_button.pack(side="bottom")
    window.mainloop()

    # classes 
class Dinosaur(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.lives = 3
        self.state = "alive"
        self.ducked = False
        self.images_day = [resized_dinosaur_day, resized_dinosaur_day2]
        self.images_night = [resized_dinosaur_night, resized_dinosaur_night2]
        self.images_day_ducked = [resized_dinosaur_day_ducked, resized_dinosaur_day2_ducked]
        self.images_night_ducked = [resized_dinosaur_night_ducked, resized_dinosaur_night2_ducked]
        self.index = 0
        self.image_day = self.images_day[self.index]
        self.image_night = self.images_night[self.index]
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

        # I think that the player movement is to simple, I will have to later adjust it to be more nice

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
            if not super_jump_on:
                self.rect.y += change
            elif change>0:
                self.rect.y += change
            else:
                self.rect.y += change*2
    def update(self):
        self.index += 0.1
        if int(self.index) == 2:
            self.index = 0
        self.image_day = self.images_day[int(self.index)]
        self.image_night = self.images_night[int(self.index)]
        if self.ducked:
            self.image_day = self.images_day_ducked[int(self.index)]
            self.image_night = self.images_night_ducked[int(self.index)]
            self.rect.y = HEIGHT//3*2+base_size//2

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
        self.rect.x = random.choice([WIDTH, WIDTH+100, WIDTH+200, WIDTH+300, WIDTH+400, WIDTH+500])
        self.rect.y = HEIGHT//3*2-self.size+resized_dinosaur_day.get_height()
        self.type = "cactus"
    def move(self):
        self.rect.x -= 10
        global distance_travelled
        distance_travelled += 10

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
        self.rect.x = random.choice([WIDTH, WIDTH+100, WIDTH+200, WIDTH+300, WIDTH+400, WIDTH+500])
        self.rect.y = random.choice(pterodactyl_heights)
        self.type = "pterodactyl"
        self.size = self.image.get_height()
    def move(self):
        self.rect.x -= 10
        global distance_travelled
        distance_travelled += 10

class PowerUp(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.index = random.randint(0,len(resized_powerups_day)-1)
        if cycle == "day":
            self.image = resized_powerups_day[self.index]
        else:
            self.image = resized_powerups_night[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH
        self.rect.y = random.choice(powerup_heights)
        if self.index == 0:
            self.type = "powerup1"
        elif self.index == 1:
            self.type = "powerup2"
        else:
            self.type = "powerup3"
    def move(self):
        self.rect.x -= 10

class BackgroundObject(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.index = random.randint(0, len(day_background_images)-1)
        self.size = random.choice(backgroundimage_sizes)
        self.image_day = day_background_images[self.index]
        self.image_night = night_background_images[self.index]
        self.image_day = pygame.transform.scale(self.image_day, (self.size, self.size))
        self.image_night = pygame.transform.scale(self.image_night, (self.size, self.size))
        if cycle == "day":
            self.image = self.image_day
        else:
            self.image = self.image_night
        self.rect = self.image.get_rect()
        self.rect.x = random.choice([WIDTH, WIDTH+100, WIDTH+200, WIDTH+300, WIDTH+400, WIDTH+500])
        self.rect.y = random.randint(HEIGHT//3*2+resized_dinosaur_day.get_height(), HEIGHT-self.image.get_height())
    def move(self):
        self.rect.x -= 10
    def draw(self, win):
        win.blit(self.image, (self.rect.x, self.rect.y))

class Clouds(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.index = random.randint(0, len(clouds_images_day)-1)
        self.size = random.choice(clouds_sizes)
        self.image_day = clouds_images_day[self.index]
        self.image_night = clouds_images_night[self.index]
        self.image_day = pygame.transform.scale(self.image_day, (self.size, self.size))
        self.image_night = pygame.transform.scale(self.image_night, (self.size, self.size))
        if cycle == "day":
            self.image = self.image_day
        else:
            self.image = self.image_night
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH
        self.rect.y = random.randint(0, HEIGHT//3)
    def move(self):
        self.rect.x -= 1
    def draw(self, win):
        win.blit(self.image, (self.rect.x, self.rect.y))

# Initializing the game
pygame.init()

# Setting up the screen
WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Dino Game")
icon = pygame.image.load('main_assets/dinosaur1.png')
pygame.display.set_icon(icon)
base_size = WIDTH//16
current_background_music_loudness = 50
current_sound_loudness = 50
mixer.music.load("sounds/main_menu_music.mp3")
mixer.music.set_volume(current_background_music_loudness/100)
selected_music = "sounds/background.mp3"
background_music_on = True
background_music_playing = False
game_over_sound = mixer.Sound("sounds/game_over_sound.mp3")
game_over_sound.set_volume(current_sound_loudness/100)
sound_effects_on = True
dev_mode = False
infinite_lives_on = False
super_jump_on = False
manual_cycle_switch_on = False
manual_pterodactyl_spawn_on = False
manual_powerup_spawn_on = False
fps_on = False
score = 0
main_menu = True

# setting up images through the dev image change function
dev_mode_images_change()

touchdown = mixer.Sound("sounds/energy_sound.mp3")
touchdown.set_volume(current_sound_loudness/100)
hit_sound = mixer.Sound("sounds/hit_sound.mp3")
hit_sound.set_volume(current_sound_loudness/100)

# cycle has to be defined pretty high, because its used in the classes
cycle = "day"

# creating a sprite group for the enemies
enemies = pygame.sprite.Group()

# variables for the pterodactyls
chance_of_pterodactyl = 20
pterodactyl_spawn = False
pterodactyl_heights = [HEIGHT//3*2-resized_pterodactyl_day.get_height(), HEIGHT//3*2-resized_pterodactyl_day.get_height()*2, HEIGHT//3*2+resized_pterodactyl_day.get_height()]
pterodactyls = pygame.sprite.Group()

# images used in the menu
play_button = pygame.image.load('play_button.png')
resized_play_button = pygame.transform.scale(play_button, (base_size*5, base_size*2))
exit_button = pygame.image.load('exit_button.png')
resized_exit_button = pygame.transform.scale(exit_button, (base_size*5, base_size*2))
scores_button = pygame.image.load('scores_button.png')
resized_scores_button = pygame.transform.scale(scores_button, (base_size*5, base_size*2))
back_arrow = pygame.image.load('back_arrow.png')
resized_back_arrow = pygame.transform.scale(back_arrow, (base_size*2, base_size*2))

# images used in the background
backgrounddino1 = pygame.image.load('background_dinosaur1.png')
backgrounddino1_night = pygame.image.load('background_dinosaur1_night.png')
backgroundegg = pygame.image.load('egg.png')
backgroundegg_night = pygame.image.load('egg_night.png')
backgroundcrater1 = pygame.image.load('crater1.png')
backgroundcrater1_night = pygame.image.load('crater1_night.png')
backgroundcrater2 = pygame.image.load('crater2.png')
backgroundcrater2_night = pygame.image.load('crater2_night.png')
backgroundcrater3 = pygame.image.load('crater3.png')
backgroundcrater3_night = pygame.image.load('crater3_night.png')
backgroundcrater4 = pygame.image.load('crater4.png')
backgroundcrater4_night = pygame.image.load('crater4_night.png')
tumble = pygame.image.load('tumble1.png')
tumble_night = pygame.image.load('tumble1_night.png')


night_background_images = [backgrounddino1_night, backgroundegg_night, backgroundcrater1_night, backgroundcrater2_night, tumble_night, backgroundcrater3_night, backgroundcrater4_night]
day_background_images = [backgrounddino1, backgroundegg, backgroundcrater1, backgroundcrater2, tumble, backgroundcrater3, backgroundcrater4]
# clouds images
cloud1_day = pygame.image.load('sky_images/cloud1_day.png')
cloud2_day = pygame.image.load('sky_images/cloud2_day.png')
cloud1_night = pygame.image.load('sky_images/cloud1_night.png')
cloud2_night = pygame.image.load('sky_images/cloud2_night.png')
cloud3_day = pygame.image.load('sky_images/cloud3_day.png')
cloud3_night = pygame.image.load('sky_images/cloud3_night.png')
cloud4_day = pygame.image.load('sky_images/cloud4_day.png')
cloud4_night = pygame.image.load('sky_images/cloud4_night.png')

clouds_images_day = [cloud1_day, cloud2_day, cloud3_day, cloud4_day]
clouds_images_night = [cloud1_night, cloud2_night, cloud3_night, cloud4_night]
clouds_sizes = [base_size*3, base_size*2, base_size*2.5]
clouds_group = pygame.sprite.Group()
when_will_cloud = random.randint(score+5, score+20)
spawn_cloud = False

backgroundimage_sizes = [base_size*1.6, base_size*1.5, base_size]
background_objects = pygame.sprite.Group()
spawn_background_object = False
when_will_spawn_background_object = random.randint(score+5, score+20)

# loading the sun and moon images
sun = pygame.image.load('sky_images/sun.png')
moon = pygame.image.load('sky_images/moon.png')
resized_sun = pygame.transform.scale(sun, (base_size*1.5, base_size*1.5))
resized_moon = pygame.transform.scale(moon, (base_size*1.5, base_size*1.5))

# variables for the cactuses
cactus_sizes = [HEIGHT//9,HEIGHT//8,HEIGHT//7.5]

# settings button images
settings_button = pygame.image.load('main_assets/settings.png')
resized_settings_button = pygame.transform.scale(settings_button, (base_size, base_size))
settings_button_night = pygame.image.load('main_assets/settings_night.png')
resized_settings_button_night = pygame.transform.scale(settings_button_night, (base_size, base_size))
home_button = pygame.image.load('home_button.png')
resized_home_button = pygame.transform.scale(home_button, (base_size, base_size))
home_button_night = pygame.image.load('home_button_night.png')
resized_home_button_night = pygame.transform.scale(home_button_night, (base_size, base_size))

# powerups variables and group
powerups = pygame.sprite.Group()
powerup_heights = [HEIGHT//3*2-resized_powerup1_day.get_height(), HEIGHT//3*2-resized_powerup1_day.get_height()*2, HEIGHT//3*2+resized_powerup1_day.get_height()]
powerup_picked_up = pygame.mixer.Sound("sounds/powerup_pickedup.mp3")
powerup_picked_up.set_volume(current_sound_loudness/100)
chance_of_powerup_spawn = 5
spawn_powerup = False

# setting up a font for the texts
font = pygame.font.Font(None, HEIGHT//18)

# creating the dinosaur/player
player = Dinosaur()
player_name = "Player"
player_change = 0
distance_travelled = 0
distance_when_hit = 0

# spawning one cactus for testing
cactus = Cactus()
enemies.add(cactus)

# Setting up the clock
clock = pygame.time.Clock()

# setting up a thread for the timer
timer_thread = threading.Thread(target=timer)
time = [0,0]
timer_stop = False

# main loop
running = True
game_over = False
settings = False
day_night_cycle = True
switch_cycle = False
dificulty = "Medium"
pterodactyl_on = True

while running:

    # checking if the main menu is on
    if main_menu:
        mixer.music.stop()
        mixer.music.load("sounds/main_menu_music.mp3")
        mixer.music.play(-1)
        main_menu_window(win)

    # starting the timer thread
    if not timer_thread.is_alive():
        timer_thread.start()

    # playing the background music
    if background_music_on and not background_music_playing:
        mixer.music.play(-1)
        background_music_playing = True

    # Handling events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_UP or event.key == pygame.K_w:
                player_change = -resized_dinosaur_day.get_height()*1.8
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                if player.rect.y == HEIGHT//3*2:
                    player.ducked = True
            if event.key == pygame.K_r:
                reset()
            if event.key == pygame.K_p and manual_pterodactyl_spawn_on:
                pterodactyl_spawn = True
            if event.key == pygame.K_c and manual_cycle_switch_on:
                switch_cycle = True
            if event.key == pygame.K_m and manual_powerup_spawn_on:
                spawn_powerup = True
            if event.key == pygame.K_q:
                mixer.music.stop()
                main_menu = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                if player.rect.y > HEIGHT//3*2:
                    player.ducked = False
                    player.rect.y = HEIGHT//3*2
            if event.key == pygame.K_UP or event.key == pygame.K_w or event.key == pygame.K_SPACE:
                player_change = 0
        if event.type == pygame.MOUSEBUTTONDOWN:
            # checking if the settings button is clicked
            if WIDTH-resized_settings_button.get_width() <= event.pos[0] <= WIDTH and 10 <= event.pos[1] <= resized_settings_button_night.get_height()+10:
                settings = True
                settings_window()
            # checking if the home button is clicked
            if WIDTH-resized_home_button.get_width() <= event.pos[0] <= WIDTH and 30+resized_settings_button.get_height() <= event.pos[1] <= 30+resized_settings_button.get_height()+resized_home_button.get_height():
                mixer.music.stop()
                main_menu = True
    
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
    # drawing the background objects
    background_objects.draw(win)
    # drawing the clouds
    clouds_group.draw(win)
    # drawing score in the top left corner
    if cycle == "day":
        text = font.render("Score: "+str(score), True, (0, 0, 0))
    else:
        text = font.render("Score: "+str(score), True, (255, 255, 255))
    win.blit(text, (10, 10))
    # drawing the sun or the moon
    if cycle == "day":
        win.blit(resized_sun, (10, text.get_height()*2.5))
    else:
        win.blit(resized_moon, (10, text.get_height()*2.5))
    # drawing the settings button in the top right corner
    if cycle == "day":
        win.blit(resized_settings_button, (WIDTH-resized_settings_button_night.get_width(), 10))
    else:
        win.blit(resized_settings_button_night, (WIDTH-resized_settings_button_night.get_width(), 10))
    # drawing a home button in the top right corner below the settings button
    if cycle == "day":
        win.blit(resized_home_button, (WIDTH-resized_home_button.get_width(), 30+resized_settings_button.get_height()))
    else:
        win.blit(resized_home_button_night, (WIDTH-resized_home_button.get_width(), 30+resized_settings_button.get_height()))
    # drawing the time in the top middle of the screen
    if cycle == "day":
        text = font.render(str(time[0])+"m "+str(time[1]) + "s", True, (0, 0, 0))
    else:
        text = font.render(str(time[0])+"m "+str(time[1]) + "s", True, (255, 255, 255))
    win.blit(text, (WIDTH//2-text.get_width()//2, 10))
    # drawing the number of lives in the top left corner below the score
    if cycle == "day":
        text = font.render("Lives: "+str(player.lives), True, (0, 0, 0))
    else:
        text = font.render("Lives: "+str(player.lives), True, (255, 255, 255))
    win.blit(text, (10, 10+text.get_height()))
    # drawing the fps in the bottom left corner
    if fps_on:
        text = font.render("FPS: "+str(int(clock.get_fps())), True, (0, 255, 0))
        win.blit(text, (10, HEIGHT-text.get_height()-10))

    # updating the player
    player.update()

    # Drawing the player
    player.draw(win)

    # drawing the cactuses and the pterodactyls
    enemies.draw(win)

    # drawing the powerups
    powerups.draw(win)

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
                    if spawn_powerup:
                        powerup = PowerUp()
                        powerups.add(powerup)
                        spawn_powerup = False
                else:
                    cactus = Cactus()
                    enemies.add(cactus)
                    if spawn_powerup:
                        powerup = PowerUp()
                        powerups.add(powerup)
                        spawn_powerup = False
            if enemy.type == "pterodactyl":
                enemies.remove(enemy)
                if pterodactyl_spawn:
                    pterodactyl = Pterodactyl()
                    enemies.add(pterodactyl)
                    pterodactyls.add(pterodactyl)
                    pterodactyl_spawn = False
                    if spawn_powerup:
                        powerup = PowerUp()
                        powerups.add(powerup)
                        spawn_powerup = False
                else:
                    cactus = Cactus()
                    enemies.add(cactus)
                    if spawn_powerup:
                        powerup = PowerUp()
                        powerups.add(powerup)
                        spawn_powerup = False

    # moving the powerups
    for powerup in powerups:
        powerup.move()
        if powerup.rect.x < -100-powerup.rect.width:
            powerups.remove(powerup)

    # spawning the pterodactyl
    if pterodactyl_on and not manual_pterodactyl_spawn_on:
        if score > 100 and len(pterodactyls) == 0:
            rand = random.randint(0, 100)
            if rand < chance_of_pterodactyl:
                pterodactyl_spawn = True

    # spawning the powerups
    if score > 50 and len(powerups) == 0 and not spawn_powerup and score % 50 == 0 and not manual_powerup_spawn_on:
        rand = random.randint(0, 100)
        if rand < chance_of_powerup_spawn:
            spawn_powerup = True
            rand = 1001

    # checking for collisions between the player and the enemies
    if pygame.sprite.spritecollide(player, enemies, False) and player.state == "alive" and not infinite_lives_on:
        player.lives -= 1
        if sound_effects_on and player.lives > 0:
            hit_sound.play()
        player.state = "protected"
        distance_when_hit = score
        if player.lives == 0:
            game_over_screen()

    # if the player has been hit he will be protected for 5 score points
    if player.state == "protected" and distance_when_hit+5 < score:
        player.state = "alive"

    # if a background object is off the screen then it will be removed
    for background_object in background_objects:
        background_object.move()
        if background_object.rect.x < -100-background_object.rect.width:
            background_objects.remove(background_object)
    # if a cloud is off the screen then it will be removed
    for cloud in clouds_group:
        cloud.move()
        if cloud.rect.x < 0-cloud.rect.width:
            clouds_group.remove(cloud)

    # checking for collisions between the player and the powerups
    if pygame.sprite.spritecollide(player, powerups, False):
        if sound_effects_on:
            powerup_picked_up.play()
        if powerup.type == "powerup1":
            score += 50
        elif powerup.type == "powerup2":
            player.lives += 1
        elif powerup.type == "powerup3":
            chance_of_powerup_spawn += 0.5
        elif powerup.type == "powerup4":
            fact_func()
        powerups.remove(powerup)

    # this is the day night cycle switching, it will be used later when I add the opposite color images
    if time[1] == 59 and day_night_cycle and not manual_cycle_switch_on:
        switch_cycle = True
    
    # every once in a while spawning a background object
    if score  > when_will_spawn_background_object and score != 0 and not spawn_background_object:
        spawn_background_object = True

    # sometimes a cloud will spawn
    if score > when_will_cloud and len(clouds_group) < 10:
        spawn_cloud = True

    # getting the score from the distance travelled
    if distance_travelled >= 100:
        score += 1
        distance_travelled = 0
        # playing the touchdown sound when the score is a multiple of 100
        if score % 100 == 0 and score != 0:
            if sound_effects_on:
                touchdown.play()
    
    # if the code reaches this part then the settings window is closed
    settings = False

    # Updating the display
    pygame.display.update()

    # Frame rate
    clock.tick(60)

pygame.quit()