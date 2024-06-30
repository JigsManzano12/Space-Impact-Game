import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up display
width, height = 800, 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Space Impact 2007")

# Set up colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Set up the game clock
clock = pygame.time.Clock()

# Player settings
player_size = 50
player_color = WHITE
player_speed = 5

# Enemy settings
enemy_size = 50
enemy_color = RED
enemy_speed = 5

# Bullet settings
bullet_size = 10
bullet_color = GREEN
bullet_speed = 10

# Enemy bullet settings
enemy_bullet_color = BLUE
enemy_bullet_speed = 7

# Boss settings
boss_size = 100
boss_color = RED
boss_speed = 3
boss_health = 20

# Score
font = pygame.font.SysFont("monospace", 35)

# Menu font
menu_font = pygame.font.SysFont("monospace", 75)

# Game state
menu = True

# Initialize game variables
def reset_game():
    global player_pos, enemy_list, bullet_list, enemy_bullet_list, boss_pos, boss_health, boss_active, score
    player_pos = [width // 2, height - 2 * player_size]
    enemy_list = []
    bullet_list = []
    enemy_bullet_list = []
    boss_pos = [width // 2 - boss_size // 2, 50]
    boss_health = 20
    boss_active = False
    score = 0

# Add enemy function
def add_enemy(enemy_list):
    delay = random.random()
    if len(enemy_list) < 10 and delay < 0.1:
        x_pos = random.randint(0, width - enemy_size)
        y_pos = 0
        enemy_list.append([x_pos, y_pos])

# Draw enemies
def draw_enemies(enemy_list):
    for enemy_pos in enemy_list:
        pygame.draw.rect(window, enemy_color, (enemy_pos[0], enemy_pos[1], enemy_size, enemy_size))

# Update enemy position
def update_enemy_positions(enemy_list):
    global score
    for idx, enemy_pos in enumerate(enemy_list):
        if enemy_pos[1] >= 0 and enemy_pos[1] < height:
            enemy_pos[1] += enemy_speed
        else:
            enemy_list.pop(idx)
            score += 1

# Enemy firing function
def enemy_fire(enemy_bullet_list, enemy_list):
    delay = random.random()
    if delay < 0.1:
        for enemy_pos in enemy_list:
            enemy_bullet_list.append([enemy_pos[0] + enemy_size // 2, enemy_pos[1] + enemy_size])

# Draw enemy bullets
def draw_enemy_bullets(enemy_bullet_list):
    for bullet_pos in enemy_bullet_list:
        pygame.draw.rect(window, enemy_bullet_color, (bullet_pos[0], bullet_pos[1], bullet_size, bullet_size))

# Update enemy bullet position
def update_enemy_bullet_positions(enemy_bullet_list):
    for idx, bullet_pos in enumerate(enemy_bullet_list):
        if bullet_pos[1] < height:
            bullet_pos[1] += enemy_bullet_speed
        else:
            enemy_bullet_list.pop(idx)

# Collision check
def collision_check(object_list, target_pos, target_size):
    for obj_pos in object_list:
        if detect_collision(obj_pos, target_pos, target_size):
            return True
    return False

# Detect collision
def detect_collision(object1, object2, object2_size):
    x1, y1 = object1
    x2, y2 = object2
    if (x1 >= x2 and x1 < (x2 + object2_size)) or (x2 >= x1 and x2 < (x1 + bullet_size)):
        if (y1 >= y2 and y1 < (y2 + object2_size)) or (y2 >= y1 and y2 < (y1 + bullet_size)):
            return True
    return False

# Bullet firing function
def fire_bullet(bullet_list, player_pos):
    bullet_list.append([player_pos[0] + player_size // 2, player_pos[1]])

# Draw bullets
def draw_bullets(bullet_list):
    for bullet_pos in bullet_list:
        pygame.draw.rect(window, bullet_color, (bullet_pos[0], bullet_pos[1], bullet_size, bullet_size))

# Update bullet position
def update_bullet_positions(bullet_list):
    for idx, bullet_pos in enumerate(bullet_list):
        if bullet_pos[1] > 0:
            bullet_pos[1] -= bullet_speed
        else:
            bullet_list.pop(idx)

# Bullet collision check
def bullet_collision_check(bullet_list, enemy_list, enemy_size):
    for bullet_pos in bullet_list:
        for enemy_pos in enemy_list:
            if detect_collision(bullet_pos, enemy_pos, enemy_size):
                bullet_list.remove(bullet_pos)
                enemy_list.remove(enemy_pos)
                return

# Draw menu
def draw_menu():
    window.fill(BLACK)
    title_text = menu_font.render("Space Impact 2007", True, WHITE)
    start_text = font.render("Press ENTER to Start", True, WHITE)
    quit_text = font.render("Press Q to Quit", True, WHITE)

    window.blit(title_text, (width // 2 - title_text.get_width() // 2, height // 3))
    window.blit(start_text, (width // 2 - start_text.get_width() // 2, height // 2))
    window.blit(quit_text, (width // 2 - quit_text.get_width() // 2, height // 2 + 50))

    pygame.display.flip()

# Draw boss
def draw_boss(boss_pos):
    pygame.draw.rect(window, boss_color, (boss_pos[0], boss_pos[1], boss_size, boss_size))

# Update boss position
def update_boss_position(boss_pos):
    boss_pos[0] += boss_speed
    if boss_pos[0] <= 0 or boss_pos[0] >= width - boss_size:
        boss_speed *= -1

# Main game loop
reset_game()
running = True
while running:
    if menu:
        draw_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    menu = False
                    reset_game()
                if event.key == pygame.K_q:
                    running = False
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_pos[0] > 0:
            player_pos[0] -= player_speed
        if keys[pygame.K_RIGHT] and player_pos[0] < width - player_size:
            player_pos[0] += player_speed
        if keys[pygame.K_SPACE]:
            fire_bullet(bullet_list, player_pos)

        # Add and update enemies
        add_enemy(enemy_list)
        update_enemy_positions(enemy_list)

        # Enemy firing
        enemy_fire(enemy_bullet_list, enemy_list)
        update_enemy_bullet_positions(enemy_bullet_list)

        # Update bullets
        update_bullet_positions(bullet_list)

        # Check for collisions
        if collision_check(enemy_list, player_pos, player_size) or collision_check(enemy_bullet_list, player_pos, player_size):
            menu = True

        bullet_collision_check(bullet_list, enemy_list, enemy_size)

        # Activate and update boss
        if score >= 50 and not boss_active:
            boss_active = True
        if boss_active:
            draw_boss(boss_pos)
            update_boss_position(boss_pos)
            if detect_collision(boss_pos, player_pos, boss_size):
                menu = True
            bullet_collision_check(bullet_list, [boss_pos], boss_size)
            boss_health -= 1
            if boss_health <= 0:
                boss_active = False
                score += 10

        # Draw everything
        window.fill(BLACK)
        draw_enemies(enemy_list)
        draw_bullets(bullet_list)
        draw_enemy_bullets(enemy_bullet_list)
        pygame.draw.rect(window, player_color, (player_pos[0], player_pos[1], player_size, player_size))

        # Draw score
        score_text = font.render("Score: {}".format(score), True, WHITE)
        window.blit(score_text, (10, 10))

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(30)

# Quit Pygame
pygame.quit()
sys.exit()
