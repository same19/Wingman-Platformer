import pygame
import random
import numpy as np
import cProfile

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Constants
WIDTH = 800
HEIGHT = 400
GROUND_HEIGHT = 200
PLAYER_SCALE = (80, 100)
OBSTACLE_WIDTH = 50
OBSTACLE_HEIGHT = 80
SPEED = 5
GRAVITY = 1
JUMP_STRENGTH = 20
GLIDE_CONSTANT = 5
GLIDE_VELOCITY_Y = 1
BOUNCE_DELAY = 20

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

class Player(pygame.sprite.Sprite):
    def set_image(self, img):
        self.image = pygame.transform.scale(img, PLAYER_SCALE)
        self.mask = pygame.mask.from_surface(self.image)
    
    def __init__(self, collision_function):
        super().__init__()

        # initialize frames
        self.frames = [stick_run1, stick_run2]
        self.gliding_frames = [stick_fly1, stick_fly2]
        self.frame_list = self.frames
        self.current_frame = 0

        self.collision_function = collision_function
        self.set_image(self.frames[self.current_frame])
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = HEIGHT - GROUND_HEIGHT - self.rect.height
        self.velocity_y = 0
        self.jumping = False
        self.animation_time = 0
        self.gliding = False  # Added gliding state
        self.dropping = False
        self.glide_velocity_y = 1  # Adjust glide speed as needed
        self.last_time_touched_ground = 0
        self.animate = True
        self.is_touching_ground = False
        self.amount_to_move = 0
        self.updating = True
    
    def turn_on_animation(self):
        self.animate = True
    
    def turn_off_animation(self):
        self.animate = False
    
    def update_frame(self, l = None):
        if l != None:
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
        self.gliding = False  # Reset gliding state when touching the ground
        self.update_frame(self.frames)

    def unhit_ground(self):
        self.is_touching_ground = False
    
    def touching_ground(self):
        return self.is_touching_ground

    def update(self):
        self.rect.y += self.velocity_y
        self.updating = False
        if self.dropping:
            self.velocity_y += 2*GRAVITY
        if not self.gliding:
            self.velocity_y += GRAVITY

        self.collision_function()

        # Ground collision
        if self.touching_ground(): #need 3x for some reason???
            self.rect.y += self.amount_to_move
            self.velocity_y = -GRAVITY
            
        # self.is_touching_ground = False
        
        # Animation
        self.animation_time += 1
        if self.animation_time > 10:  # Adjust this value to change animation speed
            self.animation_time = 0
            if self.animate:
                self.current_frame = (self.current_frame + 1) % len(self.frame_list)
            self.update_frame()
        self.updating = True
    
    def drop(self):
        if self.jumping or self.gliding:
            self.dropping = True
        self.gliding = False
        self.update_frame(self.frames)
    
    def new_jump(self):
        if self.touching_ground():#and pygame.time.get_ticks() - self.last_time_touched_ground > BOUNCE_DELAY:
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
        
        if self.jumping == True and self.velocity_y >= 0:
            self.gliding = True
            self.jumping = False
            self.velocity_y = GLIDE_VELOCITY_Y
            self.update_frame(self.gliding_frames)
    def unjump(self):
        self.gliding = False
        self.update_frame(self.frames)

def generate_obstacle_texture(image):
    green_color = np.array([23, 37, 7])  # Green color in RGB format
    brown_color = np.array([139, 69, 19])  # Brown color in RGB format
    image_data = pygame.surfarray.array3d(image)
    # alphas = pygame.surfarray.array_alpha(image)
    black_threshold = 10
    thread_count = 0
    thread_max_count = 10
    while thread_count < thread_max_count:
        break
        y = random.randint(0,image_data.shape[0]-1)
        x = random.randint(0,image_data.shape[1]-1)
        direction = (random.randint(-1,1), random.randint(-1,1))
        print(image.get_at((y,x)))
        if np.all(image_data[y,x] == 0) and image.get_at(y,x):
            print()
            while np.all(image_data[y,x] == 0) and alphas[y,x] != 255:
                image_data[y,x] = green_color
                x += direction[0]
                y += direction[1]
                direction = (random.randint(-1,2), random.randint(-1,2))
        thread_count += 1
    # for y in range(image_data.shape[0]):
    #     for x in range(image_data.shape[1]):
    #         pixel_color = image_data[y, x]
    #         if np.all(pixel_color < black_threshold):
    #             # Replace black pixels with green and brown in a pattern
    #             if (x + y) % 2 == 0:
    #                 image_data[y, x] = green_color
    #             else:
    #                 image_data[y, x] = brown_color
    # modified_image = pygame.surfarray.make_surface(image_data)
    # # return modified_image
    # return pygame.surfarray.make_surface(pygame.surfarray.array3d(image))
    return image

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, img = 'assets/level_1.png'):
        super().__init__()
        # if is_top_obstacle:
        self.win_function = lambda:None
        self.height = random.randint(70, 120)
        # self.image = generate_rock_texture(OBSTACLE_WIDTH, self.height)
        self.scale = (HEIGHT*10, HEIGHT)
        self.image = pygame.transform.scale(generate_obstacle_texture(pygame.image.load(img).convert_alpha()), self.scale)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0  # Top obstacle starts at the top of the screen

        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.x -= SPEED
        if self.rect.x < -self.scale[0]:
            self.win_function()
            self.kill()
        # if self.rect.x < -OBSTACLE_WIDTH:
        #     self.kill()

            
    # def __init__(self):
    #     super().__init__()
    #     self.image = generate_rock_texture(OBSTACLE_WIDTH, OBSTACLE_HEIGHT)
    #     self.rect = self.image.get_rect()
    #     self.rect.x = WIDTH
    #     self.rect.y = HEIGHT - GROUND_HEIGHT - OBSTACLE_HEIGHT
    #     self.mask = pygame.mask.from_surface(self.image)

    # def update(self):
    #     self.rect.x -= SPEED
    #     if self.rect.x < -OBSTACLE_WIDTH:
    #         self.kill()

"""---start of ChatGPT generated code block"""
def load_assets():
    global stick_run1, stick_run2, stick_fly1, stick_fly2
    stick_run1 = pygame.image.load('assets/stick_run1.png').convert_alpha()
    stick_run2 = pygame.image.load('assets/stick_run2.png').convert_alpha()
    stick_fly1 = pygame.image.load('assets/stick_fly1.png').convert_alpha()
    stick_fly2 = pygame.image.load('assets/stick_fly2.png').convert_alpha()

def run():
    global running
    running = True
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Platformer Game")
    
    load_assets()  # Load assets after setting the display mode

    # ... rest of the code ...


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
    top_color = (135, 206, 235)  # Sky blue
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

def run():
    global running
    running = True
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.DOUBLEBUF) #ChatGPT showed how to do double buffer
    pygame.display.set_caption("Platformer Game")

    load_assets()

    sky_texture = generate_sky_texture(WIDTH, HEIGHT)
    ground_texture = generate_ground_texture(WIDTH, GROUND_HEIGHT)

    all_sprites = pygame.sprite.Group()
    obstacles = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    # grounds = pygame.sprite.Group()
    obstacle_top = Obstacle('assets/level_color.png')

    def temp():
        global running
        global state
        running = False
        state = 1 #win

    obstacle_top.win_function = temp
    all_sprites.add(obstacle_top)
    obstacles.add(obstacle_top)
    
    def check_collide(running = True):
        player_mask = player.mask
        obstacle_mask = obstacle_top.mask

        # Calculate the offset between the two sprites
        offset_x = player.rect.x - obstacle_top.rect.x
        offset_y = player.rect.y - obstacle_top.rect.y

        # Check for collision
        overlap_surf = ground_texture
        if pygame.sprite.collide_mask(player, obstacle_top):
            offset = (offset_x, offset_y)
            # overlap_mask = mask1.overlap_mask(mask2, (offset_x, offset_y))
            collide = obstacle_top.mask.overlap_mask(player.mask, offset)
            # collide_pt = (collide[0] + obstacle_top.rect.x - player.rect.x, collide[1]+obstacle_top.rect.y - player.rect.y)
            overlap_surf = collide.to_surface(setcolor = (255, 0, 0))
            overlap_surf.set_colorkey((0, 0, 0))
            net_col = sub(collide.centroid(),offset)
            net_col_shift = sub(net_col,player.mask.centroid())
            print(obstacle_top.image.get_at(collide.centroid()))
            if obstacle_top.image.get_at(collide.centroid()) == (255,0,0,255) or (net_col_shift[0] > 1 and net_col_shift[1] < player.rect.height/4) or net_col_shift[1] < 0:
                # Death
                running = False
            else:
                #Touching ground
                overlap_point = pygame.sprite.collide_mask(player, obstacle_top)
                screen_y = overlap_point[1] + player.rect.y
                player.hit_ground(screen_y - player.rect.bottom+2)
        elif player.rect.y >= HEIGHT - player.rect.height:#HEIGHT - GROUND_HEIGHT - player.rect.height:
            running = False #game ends when hit the ground
            #player.hit_ground(-player.rect.y + (HEIGHT - GROUND_HEIGHT - player.rect.height))
        else:
            player.unhit_ground()
        return running, overlap_surf

    player = Player(check_collide)
    player_group.add(player)

    clock = pygame.time.Clock()
    obstacle_timer = 0
    space_held = False
    next_obstacle_time = 50

    
    # ground = Obstacle('assets/ground.png')
    # grounds.add(ground)
    # all_sprites.add(ground)

    space_pressed_time = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return -1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    if not space_held:  # Only record the time of the initial key press
                        space_pressed_time = pygame.time.get_ticks()
                    space_held = True
                    player.new_jump()
                elif event.key == pygame.K_DOWN:
                    player.drop()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    player.unjump()  # Stop gliding when the key is released
                    space_held = False

        # Check for gliding outside the event loop
        if space_held:
            player.jump()

        # all_sprites.update()
        player_group.update()
        obstacles.update()

        running, overlap_surf = check_collide(running)
        
        # Draw everything
        screen.blit(sky_texture, (0, 0))
        all_sprites.draw(screen)
        player_group.draw(screen)
        # screen.blit(ground_texture, (0, HEIGHT - GROUND_HEIGHT))
        # screen.blit(overlap_surf, obstacle_top.rect)

        pygame.display.flip()
        clock.tick(60)
    current_time = pygame.time.get_ticks()
    end_time = 1000
    if state == 1:
        print("You win!")
    while pygame.time.get_ticks() - current_time < end_time:
        player.unjump()
        player.turn_off_animation()
        # player.update()
        # Draw everything
        screen.blit(sky_texture, (0, 0))
        all_sprites.draw(screen)
        player_group.draw(screen)
        screen.blit(ground_texture, (0, HEIGHT - GROUND_HEIGHT))
        #pygame.draw.rect(screen, (0, 0, 0), [0, HEIGHT - GROUND_HEIGHT, WIDTH, GROUND_HEIGHT])

        
        pygame.display.flip()
        clock.tick(60)
    clock.tick(60)
    # pygame.quit()
    return 0

running = True
state = 0

if __name__ == "__main__":
    profiler = cProfile.Profile()
    profiler.enable()

    restart = 0

    # ChatGPT showed how to implement soundtrack
    pygame.mixer.music.load('assets/soundtrack.mp3')
    pygame.mixer.music.play(-1)

    while restart == 0:
        restart = run()

    profiler.disable()
    profiler.print_stats(sort='cumulative')
    profiler.dump_stats("stats/profile_results.txt")




# base ChatGPT Prompt:
#We are creating a platform game with obstacles where the individual can run and jump. Please code a simple platformer with object oriented python where the user is perpetually running when they're not jumping. It should use pygame. 