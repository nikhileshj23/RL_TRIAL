import os
import pygame as pg

main_dir = os.path.split(os.path.abspath(__file__))[0]

SCREEN_WIDTH = 288
SCREEN_HEIGHT = 512
FPS = 60

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

def main():
    pg.init()

    screen = pg.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    pg.display.set_caption("Flappy Bird")

    clock = pg.time.Clock()
    background, bg_rect = load_image("flappy-bird-assets-master/sprites/background-day.png")

    running = True

    while(running):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    running = False
        

        screen.blit(background, bg_rect)
        pg.display.flip()

        clock.tick(FPS)

    pg.quit()

if __name__ == "__main__":
    main()
