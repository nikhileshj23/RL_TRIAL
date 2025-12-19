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
GRAVITY = 0.5
JUMP_IMPULSE = -8
ROT_UP = 10
ROT_DOWN = -90
ROT_SMOOTH = 0.15
VEL_UP = -2
VEL_DOWN = 2.5

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

    #initialising clock
    clock = pg.time.Clock()

    #loading the images of all necessary sprites
    background, bg_rect = load_image("flappy-bird-assets-master/sprites/background-night.png")
    
    base_offset = 0
    base, base_rect = load_image("flappy-bird-assets-master/sprites/base.png")
    base_rect.topleft = (base_offset,GROUND_Y)

    red_bird, red_bird_rect = load_image("flappy-bird-assets-master/sprites/redbird-midflap.png")
    BIRD_HEIGHT = red_bird_rect.height
    red_bird_rect.topleft = (60,200)
    bird_y = float(red_bird_rect.y)
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

        
        #base scrolling
        base_offset += BASE_SPEED
        if(base_offset >= 48):
            base_offset = 0
        base_rect.topleft = (-base_offset,GROUND_Y)

        #bird gravity
        bird_downward_velocity += GRAVITY
        bird_y += bird_downward_velocity
        red_bird_rect.y = int(bird_y)

        #ground collision
        if bird_y + BIRD_HEIGHT >= GROUND_Y:
            bird_y = GROUND_Y - BIRD_HEIGHT
            red_bird_rect.y = int(bird_y)
            bird_downward_velocity = 0
            bird_rotation = -10

        #bird rotation from its velocity
        target_rotation = -(bird_downward_velocity / VEL_DOWN) * abs(ROT_DOWN)

        if target_rotation > ROT_UP:
            target_rotation = ROT_UP
        elif target_rotation < ROT_DOWN:
            target_rotation = ROT_DOWN

        bird_rotation += (target_rotation - bird_rotation) * ROT_SMOOTH

        rotated_bird = pg.transform.rotate(red_bird, bird_rotation)
        rotated_bird_rect = rotated_bird.get_rect(center = red_bird_rect.center)

        #clock tick
        clock.tick(FPS)

        #drawing and projecting onto the screen
        screen.blit(background, bg_rect)
        screen.blit(rotated_bird,rotated_bird_rect)
        screen.blit(base,base_rect)
        pg.display.flip()

    pg.quit()

if __name__ == "__main__":
    main()
