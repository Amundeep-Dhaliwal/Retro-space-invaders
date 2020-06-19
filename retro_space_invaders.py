import pygame, random
from pygame import mixer
pygame.init()
pygame.font.init()

# main game clock
clock = pygame.time.Clock()

width, height = 800, 800
icon = pygame.image.load(r"C:\Users\Amundeep\Pictures\Camera Roll\retro_spaceship.png")
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Retro Space Invaders')
pygame.display.set_icon(icon)

# player items
player_ship = pygame.image.load(r"C:\Users\Amundeep\Pictures\Camera Roll\player.png")
health = pygame.image.load(r"C:\Users\Amundeep\Pictures\Camera Roll\health_pack2.png")
player_laser = pygame.image.load(r"C:\Users\Amundeep\Pictures\Camera Roll\red_laser.png")
heart = pygame.image.load(r"C:\Users\Amundeep\Pictures\Camera Roll\heart_add.PNG")

# enemies
spider = pygame.image.load(r"C:\Users\Amundeep\Pictures\Camera Roll\enemy5.png")
teal = pygame.image.load(r"C:\Users\Amundeep\Pictures\Camera Roll\enemy3.png")
blue_spikes = pygame.image.load(r"C:\Users\Amundeep\Pictures\Camera Roll\enemy1.png")
long_sword = pygame.image.load(r"C:\Users\Amundeep\Pictures\Camera Roll\enemy2.png")
evil_ship = pygame.image.load(r"C:\Users\Amundeep\Pictures\Camera Roll\enemy4_b.png")

# enemy lasers 
yellow_laser = pygame.image.load(r"C:\Users\Amundeep\Pictures\Camera Roll\pixel_laser_yellow.png")
red_laser = pygame.image.load(r"C:\Users\Amundeep\Pictures\Camera Roll\pixel_laser_red.png")
blue_laser = pygame.image.load(r"C:\Users\Amundeep\Pictures\Camera Roll\pixel_laser_blue.png")
green_laser = pygame.image.load(r"C:\Users\Amundeep\Pictures\Camera Roll\pixel_laser_green.png")

# backgrounds
menu_back = pygame.transform.scale(pygame.image.load(r"C:\Users\Amundeep\Pictures\Camera Roll\menu_background.png"), (width, height))
playing_back = pygame.transform.scale(pygame.image.load(r"C:\Users\Amundeep\Pictures\Camera Roll\play_menu.png"), (width, height))

# sounds 
playing_music = mixer.Sound(r"C:\Users\Amundeep\Music\Program sounds\space_background.wav")
playing_music.set_volume(0.5)
laser_sound = mixer.Sound(r"C:\Users\Amundeep\Music\Program sounds\laser_shot.wav")
shields_recharge = mixer.Sound(r"C:\Users\Amundeep\Music\Program sounds\shields_recharge.wav")
additional_life = mixer.Sound(r"C:\Users\Amundeep\Music\Program sounds\additional_life.wav")
space_explosion = mixer.Sound(r"C:\Users\Amundeep\Music\Program sounds\space_explosion.wav")

class Button():
    def __init__(self, color, x, y, width, height, text = ''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
    
    def draw(self, screen, outline = None):
        if outline: # draws the outline
            pygame.draw.rect(screen, outline, (int(self.x - 2), int(self.y - 2), int(self.width + 4), int(self.height +4)))
        
        pygame.draw.rect(screen, self.color, (int(self.x), int(self.y), int(self.width), int(self.height)))
        
        if self.text != '':
            font = pygame.font.SysFont('comicsans', 60)
            text = font.render(self.text, 1, (0,0,0))
            screen.blit(text, (int(self.x + (self.width - text.get_width())/2), int(self.y + ((self.height - text.get_height())/2))))
        
    def hover(self, pos):
        # for the rollover effects
        if self.x <= pos[0] <= self.x +self.width:
            if self.y <= pos[1] <= self.y +self.height:
                return True

class Pickups():
    items = {1:health, 2:heart}
    def __init__(self, img_value):
        self.x = random.randrange(75, width-75)
        self.y = random.randrange(-height, -75) 
        self.type = img_value
        self.item_img = self.items[img_value]
        self.mask = pygame.mask.from_surface(self.item_img)


    def draw(self):
        screen.blit(self.item_img, (self.x, self.y))

    def move(self, vel):
        self.y += vel
    
    def off_screen(self):
         return height <= self.y <= -self.item_img.get_height()

    def collision(self, obj):
        return collided(self, obj)
    
class Laser():
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)
    
    def draw(self):
        screen.blit(self.img, (self.x,self.y))
    
    def move(self, vel):
        self.y += vel
    
    def off_screen(self):
        return height <= self.y <= -self.img.get_height()
    
    def collision(self, obj):
        return collided(self, obj)

def collided(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (int(offset_x), int(offset_y))) != None

class Ship():
    cooling_down = 30

    def __init__(self, x, y, health = 100):
        self.x = x 
        self.y = y
        self.max_health = health
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down = 0
    
    def draw(self):
        screen.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw()
    
    def cannon_cool(self):
        if self.cool_down >= self.cooling_down:
            self.cool_down = 0
        elif self.cool_down > 0:
            self.cool_down += 1

    def move_lasers(self, vel, obj):
        self.cannon_cool()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen():
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)

    def shoot(self):
        if self.cool_down == 0:
            laser_sound.play()
            laser = Laser(self.x+60, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down = 1
    
    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()

class Player(Ship):
    def __init__(self, x, y, health = 100):
        super().__init__(x,y,health)
        self.ship_img = player_ship
        self.laser_img = player_laser
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.lives = 5
        self.max_health = health
        self.score = 0

    def move_lasers(self,vel,objs):
        self.cannon_cool()
        for laser in self.lasers:
            laser.move(-vel)
            if laser.off_screen():
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        #space_explosion.play()
                        self.score += 1
                        if laser in self.lasers:
                            self.lasers.remove(laser)
    
    def health_bar(self,add_health= 0):
        pygame.draw.rect(screen, (255,0,0), (int(self.x), int(self.y + self.ship_img.get_height() +10), int(self.ship_img.get_width()),10))
        pygame.draw.rect(screen, (0,255,0), (int(self.x), int(self.y + self.ship_img.get_height() +10), int(self.ship_img.get_width()* (self.health/self.max_health)),10))

        if health != 0: 
            if (self.health + add_health) <= self.max_health:
                self.health += add_health
    
    def draw(self):
        super().draw()
        self.health_bar()
    
  

class Enemy(Ship):
    ship_colors = {'spider':(spider, red_laser),
                    'teal':(teal,blue_laser), 
                    'long':(long_sword, yellow_laser),
                    'blue':(blue_spikes,blue_laser),
                    'big':(evil_ship,green_laser)}    
    def __init__(self, x, y, color, health = 1):
        super().__init__(x,y,health)
        self.ship_img, self.laser_img = self.ship_colors[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def shoot(self):
        if self.cool_down == 0 and self.y + self.ship_img.get_height() > 0:
            laser_sound.play()
            laser = Laser(self.x - 25, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down = 1
            
    
    def move(self, vel):
        self.y += vel



def main():
    playing = True
    playing_music.play(-1)
    frames_per_second = 60
    level = 0
    

    player = Player((width + player_ship.get_width())/2, (height + player_ship.get_height())/2)
    player_vel = 10

    main_font = pygame.font.SysFont('comicsans', 60)
    lost_font = pygame.font.SysFont('comicsans', 100)

    enemies = []
    wave_length = 5
    enemy_vel = 1

    laser_vel = 20  
    
    packages = [] 

    lost = False
    lost_count = 0

    def redraw_window():
        screen.blit(playing_back, (0,0))
        
        level_label = main_font.render(f'Level: {level}', 1 ,(255,255,255))
        score_label = main_font.render(f'Score: {player.score}',1, (255,255,255))
        lives_label = main_font.render(f'Lives: {player.lives}', 1 ,(255,255,255))
        screen.blit(level_label, (10,10))
        screen.blit(score_label, (10, 50))
        screen.blit(lives_label, (width- lives_label.get_width(), 10))

        
        for enemy in enemies:
            enemy.draw()
            for laser in player.lasers:
                if laser.collision(enemy):
                    space_explosion.play()

        
        for package in packages:
            package.draw()
        
        player.draw()

        if lost:
            playing_music.stop()
            lost_label = lost_font.render('You lost!', 1, (255,255,255))
            screen.blit(lost_label, (int((width - lost_label.get_width())/2), int((height - lost_label.get_height())/2 ) ))
        
        pygame.display.update()

    while playing:
        clock.tick(frames_per_second)
        redraw_window()

        if player.lives < 1 or player.health <1:
            lost = True
            lost_count += 1
        
        if lost:
            if lost_count > frames_per_second*2:
                playing = False
                lost_count += 1
            else:
                continue
        
        if len(enemies) == 0:
            level += 1
            wave_length += 2
            for _ in range(wave_length):
                enemy = Enemy(random.randrange(75, width-150), random.randrange(-height,-75), random.choice(['big','spider','teal','long','blue']), health = level *5)
                enemies.append(enemy)

        
        for event in pygame.event.get():
            if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
                quit()
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x - player_vel >-1:
            player.x -= player_vel
        if keys[pygame.K_d] and player.x + player_vel < width - player.get_width():
            player.x += player_vel
        if keys[pygame.K_w] and player.y - player_vel > -1:
            player.y -= player_vel
        if keys[pygame.K_s] and player.y + player_vel < height - player.get_height()-15:
            player.y += player_vel
        if keys[pygame.K_SPACE]:
            player.shoot()
        
        if random.randrange(0, 15*frames_per_second) == 1:
            package = Pickups(random.choice([1,2]))
            packages.append(package)
        
        for package in packages:
            package.move(enemy_vel)
            if package.collision(player):
                if package.type == 1:
                    player.health_bar(30)
                    shields_recharge.play()
                    packages.remove(package)
                else:
                    player.lives += 1
                    additional_life.play()
                    packages.remove(package)
            elif package.off_screen():
                packages.remove(package)

            
        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel, player)

            if random.randrange(0, 5*frames_per_second) == 1:
                enemy.shoot()
            
            if collided(enemy, player):
                player.health -= 30
                enemies.remove(enemy)
            
            
            elif enemy.y > height:
                player.lives -= 1
                enemies.remove(enemy)
            
            for laser in player.lasers:
                if collided(laser, player):
                    space_explosion.play()
        
        player.move_lasers(laser_vel, enemies)
        
            
def main_menu():
    running = True
    title_font = pygame.font.SysFont('Comicsans', 60)
    play_button = Button((192,192,192), (width-100)/2, (height - 50)/2, 200, 100,'Play')
    while running:
        screen.blit(menu_back, (0,0)) # blit background first!
        play_button.draw(screen, True)
        
        
        main_menu_label = title_font.render('Main Menu', 1, (255,255,255))
        screen.blit(main_menu_label, (int((width-main_menu_label.get_width())/2), 50))
        pygame.display.update()

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.hover(pos):
                    main()
            if event.type == pygame.MOUSEMOTION:
                if play_button.hover(pos):
                    play_button.color = (169,169,169)
                else:
                    play_button.color =(192,192,192)
            
        clock.tick(60)


main_menu()
