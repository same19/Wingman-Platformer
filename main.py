import pygame
import random

# Initialize pygame
pygame.init()

# Constants
WIDTH = 800
HEIGHT = 400
GROUND_HEIGHT = 50
PLAYER_WIDTH = 40
PLAYER_HEIGHT = 60
OBSTACLE_WIDTH = 50
OBSTACLE_HEIGHT = 50
SPEED = 5
GRAVITY = 1
JUMP_STRENGTH = 15

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.frames = [
            pygame.image.load('assets/stick_run1.png').convert_alpha(),
            pygame.image.load('assets/stick_run2.png').convert_alpha()
        ]
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = HEIGHT - GROUND_HEIGHT - self.rect.height
        self.velocity_y = 0
        self.jumping = False
        self.animation_time = 0
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.velocity_y += GRAVITY
        self.rect.y += self.velocity_y
        self.mask = pygame.mask.from_surface(self.image)

        # Ground collision
        if self.rect.y > HEIGHT - GROUND_HEIGHT - self.rect.height:
            self.rect.y = HEIGHT - GROUND_HEIGHT - self.rect.height
            self.jumping = False

        # Animation
        self.animation_time += 1
        if self.animation_time > 10:  # Adjust this value to change animation speed
            self.animation_time = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]


    def jump(self):
        if not self.jumping:
            self.velocity_y = -JUMP_STRENGTH
            self.jumping = True

class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = generate_rock_texture(OBSTACLE_WIDTH, OBSTACLE_HEIGHT)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH
        self.rect.y = HEIGHT - GROUND_HEIGHT - OBSTACLE_HEIGHT
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.x -= SPEED
        if self.rect.x < -OBSTACLE_WIDTH:
            self.kill()

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

def main():
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

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.jump()

        all_sprites.update()
        obstacles.update()

        # Add obstacles
        obstacle_timer += 1
        if obstacle_timer > 100:
            obstacle = Obstacle()
            all_sprites.add(obstacle)
            obstacles.add(obstacle)
            obstacle_timer = 0

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

    pygame.quit()

if __name__ == "__main__":
    main()



# base ChatGPT Prompt:
#We are creating a platform game with obstacles where the individual can run and jump. Please code a simple platformer with object oriented python where the user is perpetually running when they're not jumping. It should use pygame. 