import pygame
from sys import exit
from random import randint, choice
from enum import Enum

pygame.init()
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

class game_state(Enum):
    START_PAGE = 1
    ACTIVE = 2
    DEAD = 3
    LEVELS = 4

class levels(Enum):
    ONE = 1
    SECOND = 2

number_of_levels = 2



player_frames = {}
player_index = 0
player_count = 0
def initialize_player_dict():
    global player_count
    for i in [2, 3, 4, 5, 6,7, 8, 9]:
        image = pygame.image.load(f'graphics/spaceshooter_ByJanaChumi/items/{i}.png').convert_alpha()
        image = pygame.transform.rotozoom(image, 0, .5)
        player_frames[player_count] = image
        player_count+=1


enemy_frames = {}
def initialize_enemy_dict():
    for i in range(16, 20):
        enemy_frames[i] = pygame.image.load(f'graphics/spaceshooter_ByJanaChumi/items/{i}.png').convert_alpha()


player_bullet_frames = {}
player_bullet_index = 0
player_bullet_count = 0
def initialize_player_bullet_dict():
    global player_bullet_count
    for i in [5, 7, 17, 18]:
        player_bullet_frames[player_bullet_count] = pygame.image.load(f'graphics/spaceshooter_ByJanaChumi/items/bullets/{i}.png').convert_alpha()
        player_bullet_count+=1



enemy_bullet_map = {
    16: 'Yellow',
    17: 'Blue',
    18: 'Red',
    19: 'Green'
}
enemy_bullet_frames = {}
def initialize_enemy_bullet_dict():
    for i in range(16, 20):
        lis = []
        for j in range (1, 7):
            frame = pygame.image.load(f'graphics/Spinnig Orb/{enemy_bullet_map[i]}/frame {j}.png').convert_alpha()
            lis.append(pygame.transform.rotozoom(frame, 0, 0.06))
        enemy_bullet_frames[i] = lis
def fill(surface, color):
    w, h = surface.get_size()
    r, g, b = color
    for x in range(w):
        for y in range(h):
            a = surface.get_at((x, y))[3]
            surface.set_at((x, y), pygame.Color(r, g, b, a))


class Enemy_Bullet(pygame.sprite.Sprite):
    def __init__(self, enemy_type, pos):
        super().__init__()
        self.pos = pos
        self.frames = enemy_bullet_frames[enemy_type]
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center = self.pos)
        self.speed = 2

    def animate(self):
        self.frame_index += .2
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def update(self):
        self.animate()
        self.rect.top += self.speed
        if(self.rect.top >= SCREEN_HEIGHT):
            self.kill()

class Player_Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, type):
        super().__init__()
        self.pos = pos
        self.image = player_bullet_frames[player_bullet_index]
        self.rect = self.image.get_rect(center = self.pos)
        self.speed = 2
    def update(self):
        self.rect.top -= self.speed
        if(self.rect.bottom <= 0):
            self.kill()


class Enemy(pygame.sprite.Sprite):
    def __init__(self, type, pos, direction, vertical_spacing, speed):
        super().__init__()
        self.pos = pos
        enemy_surf = enemy_frames[type]
        enemy_surf = pygame.transform.rotozoom(enemy_surf, 0, .5)
        self.image = enemy_surf
        self.rect = self.image.get_rect(midtop = self.pos)        
        self.direction = direction
        self.speed = speed
        self.cnt = 0
        self.type = type
        self.vertical_spacing = vertical_spacing / self.speed

    def shoot(self):
        enemy_bullets.add(Enemy_Bullet(self.type, self.rect.center))

    def move(self):
        if self.direction == RIGHT:
            self.rect.right = min(self.speed + self.rect.right, SCREEN_WIDTH)
        elif self.direction == LEFT:
            self.rect.left = max(self.rect.left - self.speed, 0)
        else:
            #DOWN
            self.cnt+=1
            self.rect.bottom = min(self.speed + self.rect.bottom, SCREEN_HEIGHT)

        if (self.rect.right >= SCREEN_WIDTH or self.rect.left <= 0) \
            and (self.direction == LEFT or self.direction == RIGHT):
            self.direction += 1
            self.direction %= 4

        if self.cnt >= self.vertical_spacing:
            self.direction += 1
            self.direction %= 4
            self.cnt = 0


        if(self.rect.bottom >= SCREEN_HEIGHT):
            game_over()
    
    def update(self):
        self.move()



class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.original_image = player_frames[player_index]
        # pygame.transform.rotozoom(ship_surf, 0, .8)
        self.image = self.original_image
        self.rect = self.image.get_rect()
        # self.rect = self.rect.ni
        self.direction = 0
        self.old_pos = (0, 0)
        self.pos = (0, 0)
        self.weight = 3

    def player_input(self):
        self.pos = pygame.mouse.get_pos()
        self.rect.center = self.pos

        if self.old_pos[0] == self.pos[0]:
            if self.direction > 0:
                self.direction = max(self.direction - 2*self.weight, 0)
            else:
                self.direction = min(self.direction + 2*self.weight, 0)
            self.rotation()
        else:
            if self.pos[0] > self.old_pos[0]:
                if self.direction > 0:
                    self.direction = min(self.weight + self.direction, 90)
                else:
                    self.direction += 2*self.weight
            elif self.pos[0] < self.old_pos[0]:
                if self.direction < 0:
                    self.direction = max(self.direction - self.weight, -90)
                    self.direction -= self.weight
                else:
                    self.direction -= 2*self.weight
                # self.direction -= self.weight
            self.rotation()

        # if self.direction - self.rect.x < 0:
        #     self.rotation(0)
        # elif self.direction - self.rect.x > 0:
        #     self.rotation(1)
        # else:
        #     self.rotation(2)
        self.old_pos = self.pos

    def shoot(self):
        if player_bullet_index >= 2:
            player_bullets.add(Player_Bullet((self.rect.centerx-12, self.rect.centery), player_bullet_index))    
            player_bullets.add(Player_Bullet((self.rect.centerx+12, self.rect.centery), player_bullet_index))    
        else:
            player_bullets.add(Player_Bullet((self.rect.centerx, self.rect.centery), player_bullet_index))
        player_shoot_music.play()
        # player_bullets.add(Player_Bullet((self.rect.centerx + 10, self.rect.centery)))
    def rotation(self):
        if self.direction < 0:
            self.image = pygame.transform.rotozoom(self.original_image, min(-0.5*self.direction, 45) , 1)
        elif self.direction > 0:
            self.image = pygame.transform.rotozoom(self.original_image, -min(0.5*(self.direction), 45), 1)
        else:
            self.image = self.original_image
        # elif self.rotation = 0

    def change_skin(self):
        self.original_image = player_frames[player_index]
        self.image = player_frames[player_index]
    def update(self):
        # self.rotation()
        self.player_input()

def game_over():
    level_music.stop()
    death_music.play(loops = -1)
    global game_state_index
    hit_music.play()
    game_state_index = game_state.DEAD.value
    player_bullets.empty()
    enemies.empty()
    enemy_bullets.empty()

def set_levels(level_num):
    
    match level_num:
        case 1:
            horizontal_spacing = SCREEN_WIDTH / 12
            vertical_spacing = 120
            start = 20
            x = horizontal_spacing / 2
            while x < SCREEN_WIDTH:
                enemies.add(Enemy(16, (x, start), RIGHT, vertical_spacing, 3))
                x += horizontal_spacing
            x = horizontal_spacing / 2
            while x < SCREEN_WIDTH:
                enemies.add(Enemy(17, (x, start + vertical_spacing), LEFT, vertical_spacing, 3))
                x += horizontal_spacing
            x = horizontal_spacing / 2
            while x < SCREEN_WIDTH:
                enemies.add(Enemy(18, (x, start + 2* vertical_spacing), RIGHT, vertical_spacing, 3))
                x += horizontal_spacing
            
        case 2:
            horizontal_spacing = SCREEN_WIDTH / 14
            vertical_spacing = 60
            start = 20
            x = horizontal_spacing / 2
            while x < SCREEN_WIDTH:
                enemies.add(Enemy(16, (x, start), RIGHT, vertical_spacing, 2))
                x += horizontal_spacing
            x = horizontal_spacing / 2
            while x < SCREEN_WIDTH:
                enemies.add(Enemy(17, (x, start + vertical_spacing), LEFT, vertical_spacing, 2))
                x += horizontal_spacing
            x = horizontal_spacing / 2
            while x < SCREEN_WIDTH:
                enemies.add(Enemy(18, (x, start + 2* vertical_spacing), RIGHT, vertical_spacing, 2))
                x += horizontal_spacing
            x = horizontal_spacing / 2
            while x < SCREEN_WIDTH:
                enemies.add(Enemy(19, (x, start + 3* vertical_spacing), LEFT, vertical_spacing, 2))
                x += horizontal_spacing
            
        case default:
            return
    global game_state_index
    game_state_index = game_state.ACTIVE.value
    intro_music.stop()
    death_music.stop()
    level_music.stop()
    level_music.play(loops=-1)
            


pygame.mouse.set_visible(False)
initialize_player_dict()
initialize_enemy_dict()
initialize_player_bullet_dict()
initialize_enemy_bullet_dict()
RIGHT = 0
LEFT = 2
enemy_height = 0
pygame.display.set_caption('Sky Shooter')
clock = pygame.time.Clock()
game_state_index = game_state.START_PAGE.value
player_shooting_delay = 45
player_shooting_counter = 0

#Backgrounds
active_back_ground = pygame.image.load('graphics/spaceshooter_ByJanaChumi/background.png').convert()
active_back_ground = pygame.transform.rotozoom(active_back_ground, 0, 1.5)

start_page_background = pygame.image.load('graphics/Pixel/spr_stars01.png').convert()
# start_page_background = pygame.transform.rotozoom(start_page_background, 0, 1)
moon_background = pygame.image.load('graphics/Pixel/moon.png').convert_alpha()
earth_background = pygame.image.load('graphics/Pixel/earth.png').convert_alpha()
earth_background = pygame.transform.rotozoom(earth_background, 0, 2)
sun_background = pygame.image.load('graphics/Pixel/sun.png').convert_alpha()


fork = pygame.image.load('graphics/fork.png').convert_alpha()
fork = pygame.transform.rotozoom(fork, 90, .1)
fill(fork, (79, 112, 156))

#Font
pixel_font = pygame.font.Font('Font/Pixeltype.ttf', 70)
start_message = pixel_font.render('Welcome to Sky Shooter!!', False, (255,255,255))
start_message_rect = start_message.get_rect(center = (SCREEN_WIDTH/2, 70))

win_message = pixel_font.render('Good Job!!', False, (255,215,0))
win_message_rect = win_message.get_rect(center = (SCREEN_WIDTH/2, 70))
won = False

death_message = pixel_font.render('You Are Dead :(', False, (255,5,5))
death_message_rect = death_message.get_rect(center = (SCREEN_WIDTH/2, 70))

levels_message = pixel_font.render('Choose Your Level:', False, (255,5,5))
levels_message_rect = levels_message.get_rect(topleft = (30, 340))


levels_text_rect = levels_message_rect.copy()
levels_text_rect.right += 50
levels_rects_list = []
for i in range(number_of_levels):
    levels_text_rect.top += 50
    levels_rects_list.append(levels_text_rect.copy())


#Sound
intro_music = pygame.mixer.Sound('graphics/release/intro.ogg')
intro_music.play(loops=-1)
player_shoot_music = pygame.mixer.Sound('graphics/Misc Lasers/Fire 6.MP3')
player_shoot_music.set_volume(.4)
hit_music = pygame.mixer.Sound('graphics/Misc Lasers/Game Over.MP3')
hit_music.set_volume(.2)
level_music = pygame.mixer.Sound('graphics/release/level1.ogg')
death_music = pygame.mixer.Sound('graphics/release/death.ogg')
#Groups

player = pygame.sprite.GroupSingle()
player.add(Player())

enemies = pygame.sprite.Group()

player_bullets = pygame.sprite.Group()

enemy_bullets = pygame.sprite.Group()

#Buttons
start_button_text = pixel_font.render('Start Game', False, 'White')
start_button_rect = start_button_text.get_rect(topleft = (80, 440))
# start_button = pygame.Rect(80, 440, 200, 80)

#Timers
user_event_counter = 1
enemies_timer = pygame.USEREVENT + user_event_counter
user_event_counter += 1
pygame.time.set_timer(enemies_timer, 50)

enemy_bullets_timer = pygame.USEREVENT + user_event_counter
user_event_counter += 1
pygame.time.set_timer(enemy_bullets_timer, 800)


#Game Loop 
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_state_index == game_state.ACTIVE.value:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    player_bullet_index += 1
                    player_bullet_index %= player_bullet_count
                if event.key == pygame.K_f:
                    player_index += 1
                    player_index %= player_count
                    player.sprite.change_skin()
            if event.type == enemies_timer:
                enemies.update()
            if player_shooting_counter <= 0 and pygame.mouse.get_pressed()[0]:
                player.sprite.shoot()
                player_shooting_counter = player_shooting_delay
            if event.type == enemy_bullets_timer:
                choice(enemies.sprites()).shoot()


        elif game_state_index == game_state.START_PAGE.value:

            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button_rect.collidepoint(pygame.mouse.get_pos()):
                    game_state_index = game_state.LEVELS.value


        elif game_state_index == game_state.DEAD.value:

            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button_rect.collidepoint(pygame.mouse.get_pos()):
                    game_state_index = game_state.LEVELS.value

                    
        elif game_state_index == game_state.LEVELS.value:

            if event.type == pygame.MOUSEBUTTONDOWN:
                i = 0
                for levels in levels_rects_list:
                    i += 1
                    if levels.collidepoint(pygame.mouse.get_pos()):
                        set_levels(i)
                        break
            
    if game_state_index == game_state.ACTIVE.value:
        player_shooting_counter = max(player_shooting_counter - 1, 0)
        screen.blit(active_back_ground, (0, 0))

        player.update()
        player.draw(screen)
        player_bullets.update()
        player_bullets.draw(screen)

        enemy_bullets.update()
        enemy_bullets.draw(screen)

        # enemies.update()
        enemies.draw(screen)
        pygame.sprite.groupcollide(player_bullets, enemies, True, True,
                                    pygame.sprite.collide_circle_ratio(.4))
        #Borders
        # p = player.sprite.rect
        # for e in enemies.sprites():
        #     pygame.draw.rect(screen, (255,0,0), e.rect, 2)
        # pygame.draw.rect(screen, (0,0,255), p, 2)

        #Collisions
        if not enemies.sprites():
            player_bullets.empty()
            enemy_bullets.empty()
            won = True
            game_state_index = game_state.START_PAGE.value
        elif pygame.sprite.spritecollide(player.sprite, enemies, False, pygame.sprite.collide_circle_ratio(.4)):
            game_over()
        elif pygame.sprite.spritecollide(player.sprite, enemy_bullets, True, pygame.sprite.collide_circle_ratio(.4)):
            game_over()
    else:
        mouse_pos = pygame.mouse.get_pos()
        screen.blit(start_page_background, (0, 0))
        screen.blit(moon_background, (30, 30))
        screen.blit(sun_background, (650, 10))
        screen.blit(earth_background, (300, 100))
        screen.blit(fork, mouse_pos)
        if game_state_index == game_state.START_PAGE.value:
            if won: 
                screen.blit(win_message, win_message_rect)    
                text = 'Play Again'
            else: 
                screen.blit(start_message, start_message_rect)
                text = 'Start Game'
            tutorial_text = pixel_font.render('Press D to change bulltes', False, '#45FFCA')
            screen.blit(tutorial_text, (30, 600))
            tutorial_text = pixel_font.render('Press F to change skin', False, '#45FFCA')
            screen.blit(tutorial_text, (30, 650))
            if start_button_rect.collidepoint(mouse_pos):
                start_button_text = pixel_font.render(text, False, '#45FFCA')
                screen.blit(start_button_text, start_button_rect)
            else:
                start_button_text = pixel_font.render(text, False, 'White')
                screen.blit(start_button_text, start_button_rect)
        elif game_state_index == game_state.DEAD.value:
            screen.blit(death_message, death_message_rect)
            if start_button_rect.collidepoint(mouse_pos):
                start_button_text = pixel_font.render('Play Again', False, '#45FFCA')
                screen.blit(start_button_text, start_button_rect)
            else:
                start_button_text = pixel_font.render('Play Again', False, 'White')
                screen.blit(start_button_text, start_button_rect)
        elif game_state_index == game_state.LEVELS.value:
            screen.blit(levels_message, levels_message_rect)
            i = 0
            for rectangle in levels_rects_list:
                i += 1
                if rectangle.collidepoint(mouse_pos):
                    level_text = pixel_font.render(f'Level {i}', False, '#45FFCA')
                    screen.blit(level_text, rectangle)
                else:
                    level_text = pixel_font.render(f'Level {i}', False, 'White')
                    screen.blit(level_text, rectangle)


        # if start_button.collidepoint(pygame.mouse.get_pos()):
        #     pygame.draw.rect(screen, (5, 59, 80), start_button)
        # else:
        #     pygame.draw.rect(screen, '#A6FF96', start_button)
    pygame.display.update()
    clock.tick(60)