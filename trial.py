#importing necessary modules
import os
import pygame as pg

#main directory path of this project
main_dir = os.path.split(os.path.abspath(__file__))[0]

#constants
SCREEN_WIDTH = 288
SCREEN_HEIGHT = 512
GROUND_Y = 400
FPS = 60
BASE_SPEED = 2
PIPE_SPEED = 3
GRAVITY = 0.5
JUMP_IMPULSE = -6
ROT_UP = 10
ROT_DOWN = -90
ROT_SMOOTH = 0.15
VEL_UP = -2
VEL_DOWN = 2.5
FLAP_FREQUENCY = 5
PIPE_LENGTH = 320
PIPE_GAP = 100

#codes to get a specified image or sound
def load_image(name,scale = 1):
    fullname = os.path.join(main_dir,name)
    image = pg.image.load(fullname)

    size = image.get_size()
    size = (size[0] * scale, size[1] * scale)
    image = pg.transform.scale(image,size)

    image = image.convert()

    return image,image.get_rect()

def load_sound(name):
    class NoneSound:
        def play(self):
            pass

    if not pg.mixer or not pg.mixer.get_init():
        return NoneSound()
    fullname = os.path.join(main_dir, name)
    sound = pg.mixer.Sound(fullname)

    return sound

#main loop of the game
def main():

    pg.init()

    #setting the screen size and the caption
    screen = pg.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    pg.display.set_caption("Flappy Bird")

    #initialising clock and frame counter
    clock = pg.time.Clock()
    frame_counter = 0

    #loading the images of all necessary sprites
    background, bg_rect = load_image("flappy-bird-assets-master/sprites/background-night.png")
    
    base_offset = 0
    base, base_rect = load_image("flappy-bird-assets-master/sprites/base.png")
    base_rect.topleft = (base_offset,GROUND_Y)

    pipe, pipe_rect = load_image("flappy-bird-assets-master/sprites/pipe-green.png")
    inverted_pipe = pg.transform.flip(pipe, False, True)
    inverted_pipe_rect = inverted_pipe.get_rect(center = pipe_rect.center)
    gap_y = 250
    pipe_rect.topleft = (SCREEN_WIDTH - 60, gap_y + PIPE_GAP // 2)
    inverted_pipe_rect.topleft = (SCREEN_WIDTH - 60, gap_y - PIPE_GAP // 2 - PIPE_LENGTH)

    red_bird_midflap, red_bird_midflap_rect = load_image("flappy-bird-assets-master/sprites/redbird-midflap.png")
    red_bird_upflap, red_bird_upflap_rect = load_image("flappy-bird-assets-master/sprites/redbird-upflap.png")
    red_bird_downflap, red_bird_downflap_rect = load_image("flappy-bird-assets-master/sprites/redbird-downflap.png")
    
    BIRD_HEIGHT = red_bird_midflap_rect.height
    current_bird, current_bird_rect = red_bird_midflap, red_bird_midflap_rect

    current_bird_rect.topleft = (60,200)
    bird_y = float(current_bird_rect.y)
    running = True

    bird_downward_velocity = GRAVITY
    bird_rotation = -5

    while(running):
        #event
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False

                if event.key == pg.K_SPACE:
                    bird_downward_velocity = JUMP_IMPULSE
                    bird_rotation = ROT_UP

        #flapping animation
        if(frame_counter % FLAP_FREQUENCY == 0):
            curr_frame_index = frame_counter / FLAP_FREQUENCY
            curr_x, curr_y = current_bird_rect.topleft
            if curr_frame_index % 2 == 0:
                #should change the current bird to midflap
                current_bird, current_bird_rect = red_bird_midflap, red_bird_midflap_rect
            elif curr_frame_index % 4 == 1:
                #should change the current bird to downflap
                current_bird, current_bird_rect = red_bird_downflap, red_bird_downflap_rect
            elif curr_frame_index % 4 == 3:
                #should change the current bird to upflap
                current_bird, current_bird_rect = red_bird_upflap, red_bird_upflap_rect

            current_bird_rect.topleft = (curr_x, curr_y)
       
        #base scrolling
        base_offset += BASE_SPEED
        if(base_offset >= 48):
            base_offset = 0
        base_rect.topleft = (-base_offset,GROUND_Y)

        #pipes scrolling
        pipe_rect.x -= PIPE_SPEED
        inverted_pipe_rect.x -= PIPE_SPEED

        #bird gravity
        bird_downward_velocity += GRAVITY
        bird_y += bird_downward_velocity
        current_bird_rect.y = int(bird_y)

        #ground collision
        if bird_y + BIRD_HEIGHT >= GROUND_Y:
            bird_y = GROUND_Y - BIRD_HEIGHT
            current_bird_rect.y = int(bird_y)
            bird_downward_velocity = 0
            bird_rotation = -10

        #bird rotation from its velocity
        target_rotation = -(bird_downward_velocity / VEL_DOWN) * abs(ROT_DOWN)

        if target_rotation > ROT_UP:
            target_rotation = ROT_UP
        elif target_rotation < ROT_DOWN:
            target_rotation = ROT_DOWN

        bird_rotation += (target_rotation - bird_rotation) * ROT_SMOOTH

        rotated_bird = pg.transform.rotate(current_bird, bird_rotation)
        rotated_bird_rect = rotated_bird.get_rect(center = current_bird_rect.center)

        #clock tick and increment frame counter
        clock.tick(FPS)
        frame_counter += 1

        #drawing and projecting onto the screen
        screen.blit(background, bg_rect)
        screen.blit(rotated_bird,rotated_bird_rect)
        screen.blit(pipe,pipe_rect)
        screen.blit(inverted_pipe,inverted_pipe_rect)
        screen.blit(base,base_rect)
        pg.display.flip()

    pg.quit()

if __name__ == "__main__":
    main()
