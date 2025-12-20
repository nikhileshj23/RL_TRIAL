#importing necessary modules
import os
import random
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
PIPE_WIDTH = 52
PIPE_GAP = 150
PIPE_SPACING = 150

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
    pg.font.init()

    score_font = pg.font.SysFont(None, 40)

    #setting the screen size and the caption
    screen = pg.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    pg.display.set_caption("Flappy Bird")

    #initialising clock and frame counter
    clock = pg.time.Clock()
    frame_counter = 0
    game_score = 0

    #loading the images of all necessary sprites
    background, bg_rect = load_image("flappy-bird-assets-master/sprites/background-night.png")
    
    base_offset = 0
    base, base_rect = load_image("flappy-bird-assets-master/sprites/base.png")
    base_rect.topleft = (base_offset,GROUND_Y)

    #PIPE PAIR 1
    pipe1, pipe1_rect = load_image("flappy-bird-assets-master/sprites/pipe-green.png")
    inverted_pipe1 = pg.transform.flip(pipe1, False, True)
    inverted_pipe1_rect = inverted_pipe1.get_rect(center = pipe1_rect.center)
    gap1_y = random.randint(90,300)
    pipe1_x = SCREEN_WIDTH + PIPE_SPACING
    pipe1_rect.topleft = (pipe1_x, gap1_y + PIPE_GAP // 2)
    inverted_pipe1_rect.topleft = (pipe1_x, gap1_y - PIPE_GAP // 2 - PIPE_LENGTH)
    pipe1_scored = False

    #PIPE PAIR 2
    pipe2, pipe2_rect = load_image("flappy-bird-assets-master/sprites/pipe-green.png")
    inverted_pipe2 = pg.transform.flip(pipe2, False, True)
    inverted_pipe2_rect = inverted_pipe2.get_rect(center = pipe2_rect.center)
    gap2_y = random.randint(90,300)
    pipe2_x = SCREEN_WIDTH +  2 * PIPE_SPACING
    pipe2_rect.topleft = (pipe2_x, gap2_y + PIPE_GAP // 2)
    inverted_pipe2_rect.topleft = (pipe2_x, gap2_y - PIPE_GAP // 2 - PIPE_LENGTH)
    pipe2_scored = False

    #PIPE PAIR 3
    pipe3, pipe3_rect = load_image("flappy-bird-assets-master/sprites/pipe-green.png")
    inverted_pipe3 = pg.transform.flip(pipe3, False, True)
    inverted_pipe3_rect = inverted_pipe3.get_rect(center = pipe3_rect.center)
    gap3_y = random.randint(90,300)
    pipe3_x = SCREEN_WIDTH + 3 * PIPE_SPACING
    pipe3_rect.topleft = (pipe3_x, gap3_y + PIPE_GAP // 2)
    inverted_pipe3_rect.topleft = (pipe3_x, gap3_y - PIPE_GAP // 2 - PIPE_LENGTH)
    pipe3_scored = False

    red_bird_midflap, red_bird_midflap_rect = load_image("flappy-bird-assets-master/sprites/redbird-midflap.png")
    red_bird_upflap, red_bird_upflap_rect = load_image("flappy-bird-assets-master/sprites/redbird-upflap.png")
    red_bird_downflap, red_bird_downflap_rect = load_image("flappy-bird-assets-master/sprites/redbird-downflap.png")
    
    digits = []

    for i in range(10):
        img, _ = load_image(f"flappy-bird-assets-master/sprites/{i}.png")
        digits.append(img)
    
    BIRD_HEIGHT = red_bird_midflap_rect.height
    current_bird, current_bird_rect = red_bird_midflap, red_bird_midflap_rect

    current_bird_rect.topleft = (60,200)
    bird_y = float(current_bird_rect.y)
    running = True
    bird_alive = True

    bird_downward_velocity = GRAVITY
    bird_rotation = -5

    while running:
        if bird_alive:    
            if pipe1_scored == False and current_bird_rect.left > pipe1_rect.right:
                game_score += 1
                pipe1_scored = True
            
            if pipe2_scored == False and current_bird_rect.left > pipe2_rect.right:
                game_score += 1
                pipe2_scored = True
            
            if pipe3_scored == False and current_bird_rect.left > pipe3_rect.right:
                game_score += 1
                pipe3_scored = True
            
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
            pipe1_x -= PIPE_SPEED
            pipe1_rect.x = pipe1_x
            inverted_pipe1_rect.x = pipe1_x

            if(pipe1_rect.right  < 0):
                pipe1_scored = False
                max_x_cord_pipe = max(pipe2_rect.right, pipe3_rect.right)
                pipe1_x = max_x_cord_pipe + PIPE_SPACING
                gap1_y = random.randint(70,330)
                pipe1_rect.topleft = (pipe1_x, gap1_y + PIPE_GAP // 2)
                inverted_pipe1_rect.topleft = (pipe1_x, gap1_y - PIPE_GAP // 2 - PIPE_LENGTH)

            pipe2_x -= PIPE_SPEED
            pipe2_rect.x = pipe2_x
            inverted_pipe2_rect.x = pipe2_x

            if(pipe2_rect.right  < 0):
                pipe2_scored = False
                max_x_cord_pipe = max(pipe1_rect.right, pipe3_rect.right)
                pipe2_x = max_x_cord_pipe + PIPE_SPACING
                gap2_y = random.randint(70,330)
                pipe2_rect.topleft = (pipe2_x, gap2_y + PIPE_GAP // 2)
                inverted_pipe2_rect.topleft = (pipe2_x, gap2_y - PIPE_GAP // 2 - PIPE_LENGTH)

            pipe3_x -= PIPE_SPEED
            pipe3_rect.x = pipe3_x
            inverted_pipe3_rect.x = pipe3_x

            if(pipe3_rect.right  < 0):
                pipe3_scored = False
                max_x_cord_pipe = max(pipe1_rect.right, pipe2_rect.right)
                pipe3_x = max_x_cord_pipe + PIPE_SPACING
                gap3_y = random.randint(70,330)
                pipe3_rect.topleft = (pipe3_x, gap3_y + PIPE_GAP // 2)
                inverted_pipe3_rect.topleft = (pipe3_x, gap3_y - PIPE_GAP // 2 - PIPE_LENGTH)

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

            if current_bird_rect.colliderect(pipe1_rect) or current_bird_rect.colliderect(pipe2_rect) or current_bird_rect.colliderect(pipe3_rect):
                bird_alive = False

            score_str = str(game_score)
            score_width = 0
            for ch in score_str:
                score_width += digits[int(ch)].get_width()

            score_x = SCREEN_WIDTH // 2 - score_width // 2
            score_y = 30

            #drawing and projecting onto the screen
            screen.blit(background, bg_rect)
            screen.blit(rotated_bird,rotated_bird_rect)
            screen.blit(pipe1,pipe1_rect)
            screen.blit(inverted_pipe1,inverted_pipe1_rect)
            screen.blit(pipe2,pipe2_rect)
            screen.blit(inverted_pipe2,inverted_pipe2_rect)
            screen.blit(pipe3,pipe3_rect)
            screen.blit(inverted_pipe3,inverted_pipe3_rect)

            for ch in score_str:
                digit_img = digits[int(ch)]
                screen.blit(digit_img,(score_x,score_y))
                score_x += digit_img.get_width()
            
            screen.blit(base,base_rect)
            pg.display.flip()

        else:
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        current_bird, current_bird_rect = red_bird_midflap, red_bird_midflap_rect
                        bird_downward_velocity = 0
                        bird_rotation = 0
                        game_score = 0
                        bird_alive = True
                        
            screen.blit(background, bg_rect)
            screen.blit(base,base_rect)
            pg.display.flip()

            #clock tick and increment frame counter
            clock.tick(FPS)
            frame_counter += 1

            if frame_counter % 10 == 0:
                running = False

    pg.quit()

if __name__ == "__main__":
    main()
