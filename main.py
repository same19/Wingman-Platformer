import pygame
import random

# Initialize pygame
pygame.init()

# Constants
WIDTH = 800
HEIGHT = 400
GROUND_HEIGHT = 50
PLAYER_SCALE = (80, 100)
OBSTACLE_WIDTH = 50
OBSTACLE_HEIGHT = 80
SPEED = 5
GRAVITY = 1
JUMP_STRENGTH = 20
GLIDE_CONSTANT = 5
GLIDE_VELOCITY_Y = 1
BOUNCE_DELAY = 50

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

class Player(pygame.sprite.Sprite):
    def set_image(self, img):
        self.image = pygame.transform.scale(img, PLAYER_SCALE)
    def __init__(self):
        super().__init__()
        self.frames = [
            pygame.image.load('assets/stick_run1.png').convert_alpha(),#MIGHT NEED TO CROP IMAGES SO THE HITBOXES ARE SMALLER
            pygame.image.load('assets/stick_run2.png').convert_alpha()
        ]
        self.gliding_frames = [
            pygame.image.load('assets/stick_fly1.png').convert_alpha(),
            pygame.image.load('assets/stick_fly2.png').convert_alpha()
        ]
        self.current_frame = 0
        self.set_image(self.frames[self.current_frame])
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = HEIGHT - GROUND_HEIGHT - self.rect.height
        self.velocity_y = 0
        self.jumping = False
        self.animation_time = 0
        self.mask = pygame.mask.from_surface(self.image)
        self.gliding = False  # Added gliding state
        self.dropping = False
        self.glide_velocity_y = 1  # Adjust glide speed as needed
        self.last_time_touched_ground = 0
        self.animate = True
    def turn_on_animation(self):
        self.animate = True
    def turn_off_animation(self):
        self.animate = False
    def touching_ground(self):
        return self.rect.y > HEIGHT - GROUND_HEIGHT - self.rect.height
    def update(self):
        if self.dropping:
            self.velocity_y += 2*GRAVITY
        if not self.gliding:
            self.velocity_y += GRAVITY

        self.rect.y += self.velocity_y
        # Ground collision
        if self.touching_ground(): #need 3x for some reason???
            if self.jumping:
                self.last_time_touched_ground = pygame.time.get_ticks()
            self.rect.y = HEIGHT - GROUND_HEIGHT - self.rect.height
            self.jumping = False
            self.dropping = False
            self.gliding = False  # Reset gliding state when touching the ground
        
        # Animation
        self.animation_time += 1
        if self.animation_time > 10:  # Adjust this value to change animation speed
            self.animation_time = 0
            if self.animate:
                self.current_frame = (self.current_frame + 1) % len(self.frames)
            if self.gliding:
                self.set_image(self.gliding_frames[self.current_frame])
                self.rect = self.image.get_rect(center=self.rect.center)
            else:
                self.set_image(self.frames[self.current_frame])
                self.rect = self.image.get_rect(center = self.rect.center)

    def drop(self):
        self.gliding = False
        if self.jumping:
            self.dropping = True
    def jump(self):
        if not self.jumping and pygame.time.get_ticks() - self.last_time_touched_ground > BOUNCE_DELAY:
            self.velocity_y = -JUMP_STRENGTH
            self.jumping = True
        elif self.velocity_y >= 0:
            self.gliding = True
            self.velocity_y = GLIDE_VELOCITY_Y
    def unjump(self):
        self.gliding = False

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, is_top_obstacle):
        super().__init__()
        self.height = random.randint(50, 120)
        if is_top_obstacle:
            self.image = generate_rock_texture(OBSTACLE_WIDTH, self.height)
            self.rect = self.image.get_rect()
            self.rect.x = WIDTH
            self.rect.y = 0  # Top obstacle starts at the top of the screen
        else:
            self.image = generate_rock_texture(OBSTACLE_WIDTH, self.height)
            self.rect = self.image.get_rect()
            self.rect.x = WIDTH
            self.rect.y = HEIGHT - GROUND_HEIGHT - self.height

        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.x -= SPEED
        if self.rect.x < -OBSTACLE_WIDTH:
            self.kill()

            
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

def run():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Platformer Game")

    sky_texture = generate_sky_texture(WIDTH, HEIGHT)
    ground_texture = generate_ground_texture(WIDTH, GROUND_HEIGHT)

    all_sprites = pygame.sprite.Group()
    obstacles = pygame.sprite.Group()

    player = Player()
    all_sprites.add(player)

    clock = pygame.time.Clock()
    running = True
    obstacle_timer = 0
    space_held = False
    next_obstacle_time = 100


    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return -1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    space_pressed_time = pygame.time.get_ticks()  # Record the time when space is pressed
                    space_held = True
                    player.jump()
                elif event.key == pygame.K_DOWN:
                    player.drop()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    player.unjump()  # Space button is released after a hold
                    space_held = False
            if space_held and pygame.time.get_ticks() - space_pressed_time > 10:  # Check if space was held for less than 10 ms
                player.jump()


        all_sprites.update()
        obstacles.update()

        # Add obstacles
        obstacle_timer += 1
        if obstacle_timer > next_obstacle_time:
            obstacle_top = Obstacle(True)
            obstacle_bottom = Obstacle(False)
            all_sprites.add(obstacle_top)
            all_sprites.add(obstacle_bottom)
            obstacles.add(obstacle_top)
            obstacles.add(obstacle_bottom)
            obstacle_timer = 0
            next_obstacle_time = random.randint(10, 75)

        # Check for collisions
        if pygame.sprite.spritecollide(player, obstacles, False, pygame.sprite.collide_mask):
            running = False

        # Draw everything
        screen.blit(sky_texture, (0, 0))
        screen.blit(ground_texture, (0, HEIGHT - GROUND_HEIGHT))
        #pygame.draw.rect(screen, (0, 0, 0), [0, HEIGHT - GROUND_HEIGHT, WIDTH, GROUND_HEIGHT])

        all_sprites.draw(screen)

        pygame.display.flip()
        clock.tick(60)
    current_time = pygame.time.get_ticks()
    end_time = 1000
    while pygame.time.get_ticks() - current_time < end_time:
        player.unjump()
        player.turn_off_animation()
        player.update()
        # Draw everything
        screen.blit(sky_texture, (0, 0))
        screen.blit(ground_texture, (0, HEIGHT - GROUND_HEIGHT))
        #pygame.draw.rect(screen, (0, 0, 0), [0, HEIGHT - GROUND_HEIGHT, WIDTH, GROUND_HEIGHT])

        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(60)
    clock.tick(60)
    # pygame.quit()
    return 0

if __name__ == "__main__":
    restart = 0
    while restart == 0:
        restart = run()



# base ChatGPT Prompt:
#We are creating a platform game with obstacles where the individual can run and jump. Please code a simple platformer with object oriented python where the user is perpetually running when they're not jumping. It should use pygame. 