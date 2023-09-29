"""---start of ChatGPT generated code block---"""
"""Everything is edited by both ChatGPT and human authors"""
import pygame
import random
import numpy as np
import cProfile
import time

# Constants
WIDTH = 800
HEIGHT = 400
START_X = 50
BLOCK_HEIGHT = 20
PLAYER_SCALE = (80, 100)
OBSTACLE_WIDTH = 50
OBSTACLE_HEIGHT = 80
SPEED = 3.5
GRAVITY = 0.9
JUMP_HEIGHT = 8.5*BLOCK_HEIGHT
JUMP_STRENGTH = (2*GRAVITY * JUMP_HEIGHT) ** (0.5)
FRAME_RATE = 60
VEL_SCALE = 0.06
GLIDE_CONSTANT = 5
GLIDE_VELOCITY_Y = 1
BOUNCE_DELAY = 20

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
SKY_BLUE = (135, 206, 235)
BLACK = (0,0,0)

class Player(pygame.sprite.Sprite):
    def __init__(self, collision_function):
        super().__init__()
        self.frames = [stick_run1, stick_run2]
        self.gliding_frames = [stick_fly1, stick_fly2]
        self.frame_list = self.frames
        self.current_frame = 0
        self.collision_function = collision_function
        self.set_image(self.frames[self.current_frame])
        self.rect = self.image.get_rect()
        self.rect.x = START_X
        self.rect.y = HEIGHT - 10 * BLOCK_HEIGHT - self.rect.height
        self.velocity_y = 0
        self.jumping = False
        self.animation_time = 0
        self.gliding = False
        self.dropping = False
        self.glide_velocity_y = 1
        self.last_time_touched_ground = 0
        self.animate = True
        self.is_touching_ground = False
        self.amount_to_move = 0
        self.updating = True
        self.last_frame = pygame.time.get_ticks()

    def set_image(self, img):
        self.image = pygame.transform.scale(img, PLAYER_SCALE)
        self.mask = pygame.mask.from_surface(self.image)

    def turn_on_animation(self):
        self.animate = True
    
    def turn_off_animation(self):
        self.animate = False
    
    def update_frame(self, l=None):
        if l is not None:
            self.frame_list = l
        self.set_image(self.frame_list[self.current_frame])
        self.rect = self.image.get_rect(center=self.rect.center)
    
    def hit_ground(self, amount_to_move):
        if not self.touching_ground():
            self.last_time_touched_ground = pygame.time.get_ticks()
        self.amount_to_move = amount_to_move
        self.is_touching_ground = True
        self.jumping = False
        self.dropping = False
        self.gliding = False
        self.update_frame(self.frames)

    def unhit_ground(self):
        self.is_touching_ground = False
    
    def touching_ground(self):
        return self.is_touching_ground

    def update(self):
        self.rect.y += self.velocity_y * VEL_SCALE * (pygame.time.get_ticks() - self.last_frame)
        print(self.velocity_y * VEL_SCALE * (pygame.time.get_ticks() - self.last_frame))
        #Progress:
        #Gliding not working properly in different frame rates
        #Space bar slows down the program?
        #still visual glitching regardless of rate and with double buffering active.
        self.updating = False
        if self.dropping:
            self.velocity_y += 3 * GRAVITY * VEL_SCALE * (pygame.time.get_ticks() - self.last_frame)
        elif not self.gliding:
            self.velocity_y += GRAVITY * VEL_SCALE * (pygame.time.get_ticks() - self.last_frame)
        self.collision_function()

        if self.touching_ground():
            self.rect.y += self.amount_to_move
            self.velocity_y = -GRAVITY
        
        self.animation_time += 1
        if self.animation_time > 10:
            self.animation_time = 0
            if self.animate:
                self.current_frame = (self.current_frame + 1) % len(self.frame_list)
            self.update_frame()
        self.updating = True
        self.last_frame = pygame.time.get_ticks()
    
    def drop(self):
        if self.jumping or self.gliding:
            self.dropping = True
        self.gliding = False
        self.update_frame(self.frames)
    
    def new_jump(self):
        if self.touching_ground():
            self.velocity_y = -JUMP_STRENGTH
            self.jumping = True
            self.is_touching_ground = False
        else:
            self.gliding = True
            self.jumping = False
            self.velocity_y = GLIDE_VELOCITY_Y
            self.update_frame(self.gliding_frames)
    
    def jump(self):
        self.dropping = False
        
        if self.jumping and self.velocity_y >= 0:
            self.gliding = True
            self.jumping = False
            self.velocity_y = GLIDE_VELOCITY_Y
            self.update_frame(self.gliding_frames)
    
    def unjump(self):
        self.gliding = False
        self.update_frame(self.frames)
    
def generate_obstacle_texture(image):
    return image

# Define the Obstacle class
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, img='assets/level_0.png'):
        super().__init__()
        self.win_function = lambda: None
        self.height = random.randint(70, 120)
        self.scale = (HEIGHT * 10, HEIGHT)
        self.image = pygame.transform.scale(generate_obstacle_texture(pygame.image.load(img).convert_alpha()), self.scale)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.mask = pygame.mask.from_surface(self.image)
        self.last_frame = pygame.time.get_ticks()

    def update(self):
        self.rect.x -= SPEED * VEL_SCALE * (pygame.time.get_ticks() - self.last_frame)
        self.last_frame = pygame.time.get_ticks()
        if self.rect.x <= -self.scale[0] + START_X:
            self.win_function()
            self.kill()

def load_assets():
    global stick_run1, stick_run2, stick_fly1, stick_fly2
    stick_run1 = pygame.image.load('assets/stick_run1.png').convert_alpha()
    stick_run2 = pygame.image.load('assets/stick_run2.png').convert_alpha()
    stick_fly1 = pygame.image.load('assets/stick_fly1.png').convert_alpha()
    stick_fly2 = pygame.image.load('assets/stick_fly2.png').convert_alpha()

def generate_ground_texture(width, height):
    texture = pygame.Surface((width, height))
    colors = [(139, 69, 19), (160, 82, 45), (185, 102, 58)]  # Different shades of brown for dirt

    for x in range(width):
        for y in range(height):
            random_color = random.choice(colors)
            texture.set_at((x, y), random_color)

    return texture

def generate_rock_texture(width, height):
    texture = pygame.Surface((width, height))
    colors = [(105, 105, 105), (128, 128, 128), (169, 169, 169)]  # Different shades of grey for rock

    for x in range(width):
        for y in range(height):
            random_color = random.choice(colors)
            texture.set_at((x, y), random_color)

    return texture

def generate_sky_texture(width, height):
    texture = pygame.Surface((width, height))
    top_color = SKY_BLUE  # Sky blue
    bottom_color = (240, 248, 255)  # Alice blue

    for y in range(height):
        alpha = y / height
        color = (
            int((1 - alpha) * top_color[0] + alpha * bottom_color[0]),
            int((1 - alpha) * top_color[1] + alpha * bottom_color[1]),
            int((1 - alpha) * top_color[2] + alpha * bottom_color[2])
        )
        texture.fill(color, (0, y, width, 1))

    return texture
"""---end of ChatGPT generated code block"""

def sub(u, v):
  return [ u[i]-v[i] for i in range(len(u)) ]

def run(level_name, clock):
    global state, running
    state = 0
    running = True
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.DOUBLEBUF)
    pygame.display.set_caption("Platformer Game")

    sky_texture = generate_sky_texture(WIDTH, HEIGHT)

    all_sprites = pygame.sprite.Group()
    obstacles = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    obstacle_top = Obstacle('assets/' + level_name)

    def win():
        global state, running
        running = False
        state = 1

    obstacle_top.win_function = win
    all_sprites.add(obstacle_top)
    obstacles.add(obstacle_top)

    def check_collide(running=True):
        offset_x = player.rect.x - obstacle_top.rect.x
        offset_y = player.rect.y - obstacle_top.rect.y

        overlap_surf = sky_texture
        if pygame.sprite.collide_mask(player, obstacle_top):
            offset = (offset_x, offset_y)
            collide = obstacle_top.mask.overlap_mask(player.mask, offset)
            overlap_surf = collide.to_surface(setcolor=(255, 0, 0))
            overlap_surf.set_colorkey((0, 0, 0))
            net_col = sub(collide.centroid(), offset)
            net_col_shift = sub(net_col, player.mask.centroid())
            if obstacle_top.image.get_at(collide.centroid()) == (255, 0, 0, 255) \
                    or (net_col_shift[0] > 1 and net_col_shift[1] < player.rect.height / 4) or net_col_shift[1] < 0:
                running = False
            else:
                overlap_point = pygame.sprite.collide_mask(player, obstacle_top)
                screen_y = overlap_point[1] + player.rect.y
                player.hit_ground(screen_y - player.rect.bottom + 2)
        elif player.rect.y >= HEIGHT - player.rect.height:
            running = False
        else:
            player.unhit_ground()
        return running, overlap_surf

    player = Player(check_collide)
    player_group.add(player)

    space_held = False
    back_buffer = pygame.Surface((WIDTH, HEIGHT))

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return -1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    space_held = True
                    player.new_jump()
                elif event.key == pygame.K_DOWN:
                    player.drop()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    player.unjump()
                    space_held = False

        if space_held:
            player.jump()

        player_group.update()
        obstacles.update()

        running, overlap_surf = check_collide(running)

        back_buffer.blit(sky_texture, (0, 0))
        all_sprites.draw(back_buffer)
        player_group.draw(back_buffer)

        screen.blit(back_buffer, (0,0))
        pygame.display.flip()
        clock.tick(FRAME_RATE)

    current_time = pygame.time.get_ticks()
    end_time = 1000
    if state == 1:
        return 1
    while pygame.time.get_ticks() - current_time < end_time:
        player.unjump()
        player.turn_off_animation()
        screen.blit(sky_texture, (0, 0))
        all_sprites.draw(screen)
        player_group.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    clock.tick(60)
    return 0

def text_screen(txt):
    screen.fill(SKY_BLUE)
    FONT = pygame.font.Font(None, 64)
    WIN_TEXT = FONT.render(txt, True, BLACK)
    WIN_TEXT_RECT = WIN_TEXT.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(WIN_TEXT, WIN_TEXT_RECT)

    pygame.display.flip()

if __name__ == "__main__":
    # initialize pygame stuff
    pygame.init()
    pygame.mixer.init()

    # initialize display, clock
    pygame.display.set_caption("Platformer Game")
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.DOUBLEBUF)
    clock = pygame.time.Clock()

    # load music
    pygame.mixer.music.load('assets/soundtrack.mp3')
    pygame.mixer.music.play(-1)

    # load assets
    load_assets()

    # misc vars
    level = 0
    restart = 1
    running = True
    state = 0

    # main game loop
    while restart >= 0:
        if restart == 1:
            text_screen("Level " + str(level + 1))
            time.sleep(2)
        try:
            restart = run("level_" + str(level) + ".png", clock)
        except FileNotFoundError:
            restart = -1
            text_screen("You Win!")
            time.sleep(3)
            break
        if restart == 1:
            level += 1

    # finish game
    pygame.quit()

'''
Base ChatGPT Prompt:
    We are creating a platform game with obstacles where the individual can run and jump. Please code a simple platformer with object oriented python where the user is perpetually running when they're not jumping. It should use pygame. 
'''