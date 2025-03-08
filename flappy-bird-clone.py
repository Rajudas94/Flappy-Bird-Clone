import pygame
import sys
import random

def update_score(score,high_score):
     if score > high_score:
          high_score = score

     return high_score     

def display_score(game_state):
     if game_state == 'main_game':
          
          score_surface = game_font.render(f'Score: {int(score)}',True,(255,0,0))     #rendering  score on screen
          score_rect = score_surface.get_rect(midtop = (200,10))                      #surrounding score with a rectangle so as to place the score easily
          wind.blit(score_surface,score_rect)

     if game_state == 'game_over':

           wind.blit(board_image_surface, board_image_rect)
          
           high_score_surface = game_font.render(f'  Score:   {int(score)}',True,(255,255,255))     #rendering  score on screen
           high_score_rect = high_score_surface.get_rect(center = (152,290))           #surrounding score with a rectangle so as to place the score easily,225 and 50 so that after game is over score gets displayed on the top center
           wind.blit(high_score_surface,high_score_rect)   

           high_score_surface = game_font.render(f'  High Score:   {int(high_score)}',True,(255,255,255))     #rendering  score on screen
           high_score_rect = high_score_surface.get_rect(center = (177,340))
           wind.blit(high_score_surface,high_score_rect)

           message_surface = game_font.render("Press ''Space'' to Begin",True,(255,255,255))
           message_surface_rect = message_surface.get_rect(center = (200,30))
           wind.blit(message_surface,message_surface_rect)
          

def rotate_bird(bird):   #Function for rotating bird
     new_bird = pygame.transform.rotozoom(bird,-bird_movement * 3,1)
     return new_bird

def collision_check(pipes):
     for pipe in pipes:
          if bird_rect.colliderect(pipe):   #if bird collide with pipes collision check will return false
               death_sound.play()
               return False                 #if bird collides with the pipe false is returned and the game is over

     if bird_rect.top <= -12  or bird_rect.bottom >= 590 :  #540 for ground height
          death_sound.play()
          return False

     return True    #if bird doesn't collide with the pipes then carry on and play the game

def ground_movement():
     wind.blit(ground_img, (ground_x_pos,600))  #putting floor on top of background
     wind.blit(ground_img, (ground_x_pos+450,600))  #putting floor on top of background

def create_pipe():
     random_pipe_position = random.choice(pipe_heights)
     bottom_pipe = pipe_image.get_rect(midtop = (400,random_pipe_position))     #pipe incoming from left and height can be 400,600,800
     top_pipe = pipe_image.get_rect(center = (450,random_pipe_position - 500))
     return bottom_pipe,top_pipe

def move_pipes(pipes):
     for pipe in pipes:
          pipe.centerx -= 5
     return pipes

def draw_pipes(pipes):
     for pipe in pipes:
          if pipe.bottom >= 650:        #ie if base of the pipe is greater than the height
               wind.blit(pipe_image,pipe)

          else:     
               flip_pipe = pygame.transform.flip(pipe_image,False,True) #False because pipe is not to be placed in the x axis, True because pipe is to be placed in the y axis 
               wind.blit(flip_pipe,pipe)
   
pygame.init()
wind = pygame.display.set_mode((400,650))    #creating window of width= 450,height = 450
clock = pygame.time.Clock()
game_font = pygame.font.SysFont('Agency FB',30,bold = True) #game font
pygame.display.set_caption("Flappy Bird Clone")

#game variables
gravity = 0.52  #gravity of field set to 0.60
bird_movement = 0
game_active = True            #true if you want to play , False if you don't want to play the game
score = 0
high_score = 0

bg_img = pygame.image.load(r'C:\Users\user\Pictures\neon_city(1).jpg').convert()    #loading image
bg_img = pygame.transform.scale(bg_img,(400,650))   #scaling image to window size

ground_img = pygame.image.load(r'C:\Users\user\Pictures\57066.png').convert()
ground_img = pygame.transform.scale2x(ground_img)
ground_x_pos = 0

#bird_downflap = pygame.transform.scale2x(pygame.image.load(r'C:\Users\user\Pictures\bluebird-downflap.png').convert_alpha())
#bird_upflap = pygame.transform.scale2x(pygame.image.load(r'C:\Users\user\Pictures\bluebird-upflap.png').convert_alpha())
#bird_midflap = pygame.transform.scale2x(pygame.image.load(r'C:\Users\user\Pictures\bluebird-midflap.png').convert_alpha())
#bird_frames = [bird_downflap,bird_upflap,bird_midflap]  
#bird_index = 2
#bird_image = bird_frames[bird_index]
#bird_rect = bird_image.get_rect(center = (100,300))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP,200)

#bird
bird_image = pygame.image.load(r'C:\Users\user\Pictures\redbird-midflap.png').convert_alpha()  #starting bird
bird_rect = bird_image.get_rect(center = (100,300)) #rectangle created for checking collisions 

#pipes
pipe_image = pygame.image.load(r'C:\Users\user\Pictures\pipe.png')
pipe_image = pygame.transform.scale2x(pipe_image)
pipe_list = []
SPAWNPIPE = pygame.USEREVENT    #user event without pressing any key from the keyboard
pygame.time.set_timer(SPAWNPIPE, 2000)  #1200 is seconds i.e, 1.2s for pipe to come in the screen
pipe_heights = [100,150,200,250,300,350,400,450,475]

#gameover
game_over_image = pygame.image.load(r'C:\Users\user\Pictures\game_over.png').convert_alpha()
game_over_surface = pygame.transform.scale(game_over_image,(200,325))
game_over_rect = game_over_surface.get_rect(center=(200,325))

#sounds
flap_sound = pygame.mixer.Sound(r'C:\Users\user\Pictures\wing.wav')
death_sound = pygame.mixer.Sound(r'C:\Users\user\Pictures\hit.wav')
score_sound = pygame.mixer.Sound(r'C:\Users\user\Pictures\point.wav')
score_sound_countdown = 100

#board
board_image = pygame.image.load(r'C:\Users\user\Pictures\board.jpg').convert_alpha()
board_image_surface = pygame.transform.scale(board_image, (300,400))
board_image_rect = board_image_surface.get_rect(center = (200,325))



while True:                             #for holding screen
    for event in pygame.event.get():    #getting event from user, in this case clicking the "x" button 
        if event.type == pygame.QUIT:   #closing window 
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active: #if users presses space from the keyboard the bird goes up hence the gravity  should decrease
                bird_movement = 0
                bird_movement -= 12   #bird power of jump when space is pressed
                flap_sound.play()
                

            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()               #reverting pipe list by clearing all the pipes from the list
                bird_rect.center = (100,300)    #reverting bird to same position as beginning of the game  
                bird_movement = 0               #also reverting bird movement back to zero
                score = 0                       #every time the bird respawns, score gets initialised to zero
                  

        if event.type == SPAWNPIPE:
             pipe_list.extend(create_pipe()) #extend so that top and bottom pipe gets in the list
             
     
             

    wind.blit(bg_img,(0,0))         #putting background to the screen


    if game_active:           #if game is active only then you will get a bird to play
    #bird
         bird_movement += gravity
         bird_rotation = rotate_bird(bird_image) 
         bird_rect.centery += bird_movement
         wind.blit(bird_rotation,bird_rect)
         game_active = collision_check(pipe_list)
         
    
    #pipes
         pipe_list = move_pipes(pipe_list)
         draw_pipes(pipe_list)
         score += 0.01

    #score
         display_score('main_game')     #main game argument gets passed on the display score
         score_sound_countdown -= 1
         if score_sound_countdown <= 0:
              score_sound.play()
              score_sound_countdown = 100
              

    else:
         wind.blit(game_over_surface,game_over_rect)
         high_score = update_score(score,high_score)
         display_score('game_over')

    #floor
    ground_x_pos -= 1
    ground_movement()
    if ground_x_pos <= -450:
         ground_x_pos = 0

     
    pygame.display.update()
    clock.tick(60)
            
