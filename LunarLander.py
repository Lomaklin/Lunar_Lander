import pygame
import pygame.mixer             #<------allows for sound files to be played
import pygame.freetype          #<----allows for bliting text to the screen
import pygame.surface
import time                     #<------------ used to adjust screen refresh and object render times
import random                   #<---------- used in the generation of random numbers for the lunar surface
from statistics import mean     #<--- needed for performing averaging and statistics
import ctypes                   #<----------- needed later to gather system screen resolution
import os                       #<------used to guage starting location of game window
import sys, os 

def main():
    
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (50,50)  #<---set start location (must run before pygame.init() )

    pygame.init()
    pygame.mixer.pre_init(44100, 16, 2, 4096) #<--defines the sound file types accepted
    pygame.mixer.init(44100)                  #<------initializes the sound engine
    GAME_FONT = pygame.freetype.Font("LLFont.ttf", 36)   #<-- must have a font by this name in the game folder

    user32 = ctypes.windll.user32                    #--|
    xscreensize = user32.GetSystemMetrics(0)         #  |----Grabs the native screen resolution from system
    yscreensize = user32.GetSystemMetrics(1)         #--|
    width = (xscreensize - xscreensize * 15 // 100)  #   <---- screen width set to 85% of native resolution
    height = (yscreensize - yscreensize * 15 // 100) #   <---- screen height set to 85% of native resolution
    size = width, height                             #   <---- defines window size based on variables set above
    screen = pygame.display.set_mode(size)           #   <----sets the actual window to the size defined

    x = 0                  #<-------starting horizontal movement variable
    y = 1                  #<-------starting vertical movement variable
    gravity = 0.2
    speed = [x, y]
    black = 0, 0, 0
    thrust = 2
    rcs = 1.2
    f_status = 100          #<---this is the text starting color (grey)
    end_game = 0
    LPL = 1                 #<----Landing pad lights starting counter
    grey = 179, 179, 179    #<----lunar surface color
    regolith = 300          #<----thickness of ground surface
    offset = 50             #<----starting distance from bottom of screen for lunar surface to be created
    start = 0               #<----starting position on the left for lunar surface to be created
    rngpos = 25
    rngneg = -25
    w_rnd = random.randrange(width -200)
    h_rnd = height - 230
    clock = pygame.time.Clock()  #<--------------sets framerate variable
    pygame.key.set_repeat(1, 100)  #<------------determines the keyboard repeat speed
    lander = pygame.image.load("LanderSmall.jpg")
    crash = pygame.image.load("crash.jpg")
    plume = pygame.image.load("plume.jpg")
    rcsleft = pygame.image.load("RCS_left.jpg")
    rcsright = pygame.image.load("RCS_right.jpg")
    rcs_sound = pygame.mixer.Sound("rcs.wav")
    rcs_sound.set_volume(0.1)
    engine_sound = pygame.mixer.Sound("engine.wav")
    engine_sound.set_volume(0.1)
    landed_sound = pygame.mixer.Sound("tada.wav")
    landed_sound.set_volume(10)
    explosion_sound = pygame.mixer.Sound("explode.wav")
    explosion_sound.set_volume(0.5)
    landerrect = lander.get_rect(center=(width //2, 50))   #<------ start location of Lander
    landingpad = pygame.image.load("LPL1.png")
    landingpadrect = landingpad.get_rect(center=(w_rnd, h_rnd))   #------start location of Landing Pad

#----------------Fuel Levels at start (plan to add inputs for users to adjust----------    
    initial_fuel = 500
    fuel = initial_fuel


#----------Error Trap for a bad Y/N answser-------
    def bad_answer():
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    pygame.quit()
                    exit()
            screen.fill(black)
            pygame.display.flip()
            GAME_FONT.render_to(screen, (200, 200), "Bad Key Input!", (100, 100, 100))
            pygame.display.flip()
            time.sleep(2)
            play_again()

#-----------Displays the option to play again or quit-----------
    def play_again():
        screen.fill(black)
        GAME_FONT.render_to(screen, (200, 200), "Play Again? Y/N", (100, 100, 100))
        screen.blit(landingpad, landingpadrect)
        landscape()
        pygame.display.flip()
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    pygame.quit()
                    exit() 
                screen.fill(black)
                GAME_FONT.render_to(screen, (200, 200), "Play Again? Y/N", (100, 100, 100))
                screen.blit(landingpad, landingpadrect)
                landscape()
                pygame.display.flip()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_y:
                        main()
                    if event.key == pygame.K_n:
                        pygame.display.quit()
                        pygame.quit()
                        exit()
                    else:
                        bad_answer()

#-----------defined function for rendering the landscape----------
    def landscape():
        pygame.draw.lines(screen, grey, False, [
            [p1x, p1y],
            [p2x, p2y],
            [p3x, p3y],
            [p4x, p4y],
            [p5x, p5y],
            [p6x, p6y],
            [p7x, p7y]], regolith)
#--------------defined function for rendering the crash----------
    def landercrash():
        speed[y] = 0
        screen.fill(black)
        screen.blit(crash, landerrect)
        screen.blit(landingpad, landingpadrect)
        landscape()
        explosion_sound.play(0)
        pygame.display.flip()
        pygame.key.set_repeat(1, 1)
        time.sleep(3)
        play_again()
#------------defined function for rendering the ship landed on pad---------
    def landerlanded():
        speed[y] = 0
        screen.fill(black)
        screen.blit(lander, landerrect)
        screen.blit(landingpad, landingpadrect)
        landscape()
        landed_sound.play(0)
        pygame.display.flip()
        pygame.key.set_repeat(1, 1)
        time.sleep(3)
        play_again()
            
#----------Sets the caption at top of screen---------
    pygame.display.set_caption("Lunar Lander")

#--------START Landscape variable generation-------------
    p1x = start
    p1y = height - offset
    offset = offset + random.randrange(rngneg, rngpos, 1)
    start = random.randrange(start, width // 4, 1)

    p2x = start
    p2y = height - offset
    offset = offset + random.randrange(rngneg, rngpos, 1)
    if offset + height >= height:
        offset = offset + 10
    start = random.randrange(start, width // 4, 1)

    p3x = start
    p3y = height - offset
    offset = offset + random.randrange(rngneg, rngpos, 1)
    if offset + height >= height:
        offset = offset + 10
    start = random.randrange(start, width // 3, 1)

    p4x = start
    p4y = height - offset
    offset = offset + random.randrange(rngneg, rngpos, 1)
    if offset + height >= height:
        offset = offset + 10
    start = random.randrange(start, width // 2, 1)

    p5x = start
    p5y = height - offset
    offset = offset + random.randrange(rngneg, rngpos, 1)
    if offset + height >= height:
        offset = offset + 10
    start = random.randrange(start, width, 1)

    p6x = start
    p6y = height - offset
    offset = offset + random.randrange(rngneg, rngpos, 1)
    if offset + height >= height:
        offset = offset + 10

    p7x = width
    p7y = height - offset

#---------------END Landscape Variable Generation---------------
#---------------calculates average lunar surface height, to be used for collision calculation--------
    lst = [p1y, p2y, p3y, p4y, p5y, p6y, p7y]  #<----variables compiled above for surface height
    s_avg = mean(lst)  #<-- this is the average height of the surface
#---------------START of main program loop---------------
    while end_game == 0:  #---until landing or wrecking continue to loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                exit()
                
            if fuel > 0:
#-------------Looks for keypress------------
                if event.type == pygame.KEYDOWN:
#------------up arrow vertical thrust loop--------------
                    if event.key == pygame.K_UP:
                        engine_sound.play(0, 0)
                        speed[y] = speed[y] - thrust
                        fuel = fuel - 10
                        screen.fill(black)
                        screen.blit(plume, landerrect)
                        screen.blit(lander, landerrect)
                        screen.blit(landingpad, landingpadrect)
                        landscape()
                        pygame.display.flip()
#------------right arrow thrust to the left loop--------                
                    if event.key == pygame.K_RIGHT:
                        rcs_sound.play(0)
                        speed[x] = speed[x] - rcs
                        fuel = fuel - 3
                        screen.fill(black)
                        screen.blit(rcsright, landerrect)
                        screen.blit(landingpad, landingpadrect)
                        landscape()
                        pygame.display.flip()
#------------left arrow thrust to the right loop-----------
                    if event.key == pygame.K_LEFT:
                        rcs_sound.play(0)
                        speed[x] = speed[x] + rcs
                        fuel = fuel - 3
                        screen.fill(black)
                        screen.blit(rcsleft, landerrect)
                        screen.blit(landingpad, landingpadrect)
                        landscape()
                        pygame.display.flip()
#-------------exceleration due to gravity loop--------                
        landerrect = landerrect.move(speed)
        speed[y] = speed[y] + gravity
        clock.tick(20)   #<---set maximum framerate, slows down animations, smooths out jitters
        screen.fill(black)
        screen.blit(lander, landerrect)
        screen.blit(landingpad, landingpadrect)
        landscape()
        GAME_FONT.render_to(screen, (width - 300, height - height + 200), "FUEL  " + str(fuel), (f_status, 100, 100))
        pygame.display.flip()
#-------------checks if landed on platform-----------
        if landerrect.bottom == landingpadrect.top \
            and landerrect.left >= landingpadrect.left \
            and landerrect.right <= landingpadrect.right:
            end_game = 1
            landerlanded()
#---------------checks if Lander HIT platform BOOM!------
        if landerrect.bottom >= landingpadrect.top + 3 \
            and landerrect.left >= landingpadrect.left \
            and landerrect.right <= landingpadrect.right:
            end_game = 1
            landercrash()
#------------checks boundaries and impacts--------------
        if landerrect.left < 0 or landerrect.right > width \
           or landerrect.top < 0 \
           or landerrect.bottom >= height - (offset + 75) - height + round(s_avg, 0):
            end_game = 1
            landercrash()
#--------------checks fuel status sets status to red at half fuel
        if fuel <= initial_fuel * .5:
            f_status = 255
#--------------cycle landing lights on landing pad---------------
        LPL = LPL + 1    #<-------moves the landing pad light counter up        
        if LPL in range(1, 5):
            landingpad = pygame.image.load("LPL1.png")
        if LPL in range(5, 10):
            landingpad = pygame.image.load("LPL2.png")
        if LPL in range(10, 15):
            landingpad = pygame.image.load("LPL3.png")
        if LPL in range(15, 20):
            landingpad = pygame.image.load("LPL4.png")
        if LPL > 25:
            LPL = 1


main()
