""" Jules Clam Collecting Game """

# simple game were you collect clams and avoid fish

# --- imports ---

import pygame
import random

# --- Global Constants ---

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500

class Player(pygame.sprite.Sprite):
    # represents Jules the Ocotopus
    
    def __init__(self):
        # call the constructor
        super().__init__()
        
        # eat or bitten?
        self.bit = False
        
        # set the image
        self.image = pygame.image.load("Jules.png").convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        
        # set up flash images
        self.image_b = pygame.image.load("Jules_B.png").convert()
        self.image_b.set_colorkey(WHITE)
        
        # define movement stuff
        self.rect.x = 0
        self.rect.y = 406
        self.x_move = 0
        self.y_move = 0
        self.x_speed = 3
        self.y_speed = 3
    
    # grow Jules as he eats
    def grow(self, score, x, y):
        if score > 24:
            self.image = pygame.image.load("Jules_big.png").convert()
            self.image.set_colorkey(WHITE)
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            # set new flahs image too
            self.image_b = pygame.image.load("Jules_big_B.png").convert()
            self.image_b.set_colorkey(WHITE)            

        else:
            self.image = pygame.image.load("Jules.png").convert()
            self.image.set_colorkey(WHITE)
           
        
    # update position and keep in screen
    def update(self):
        self.rect.x += self.x_move
        self.rect.y += self.y_move
        
        #stop move off edge
        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.x > SCREEN_WIDTH - self.image.get_width():
            self.rect.x = SCREEN_WIDTH -self.image.get_width()
        if self.rect.y < 0:
            self.rect.y = 0
        elif self.rect.y > SCREEN_HEIGHT - self.image.get_height():
            self.rect.y = SCREEN_HEIGHT - self.image.get_height()
    
    # movement methods    
    def move_right(self):
        self.x_move += self.x_speed
    def move_left(self):
        self.x_move -= self.x_speed
    def move_up(self):
        self.y_move -= self.y_speed
    def move_down(self):
        self.y_move += self.y_speed
        
    #resets movement update variable to 0 to stop infinite movement
    def stop_x(self):
        self.x_move = 0
    def stop_y(self):
        self.y_move = 0
        
class Food(pygame.sprite.Sprite):
    # seaweed for Jules to eat
    
    #constructor
    def __init__(self):
        super().__init__()
        
        # set image
        self.image = pygame.image.load("Food.png").convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        
    def coord_gen(self):
        # generate random coordinates for the food
        self.rect.x = random.randrange(500, 2000)
        self.rect.y = random.randrange(0, 478)
        # gen move speed
        self.move = random.randrange(2, 6)
        
    def update(self):
        # update position, move it across the screen
        self.rect.x -= self.move
        #if moves off screen reset pos
        if self.rect.x < -200:
            self.coord_gen()
            
class Star(Food):
    # star to give Jules points
    
    #constructor
    def __init__(self):
        super().__init__()
        
        # set image
        self.image = pygame.image.load("Star.png").convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()

    def coord_gen(self):
        # generate random coordinates for the food
        self.rect.x = random.randrange(2000, 5000)
        self.rect.y = random.randrange(0, 478)
        # gen move speed
        self.move = 7
         
class Heart(Star):
    # heart to give Jules life
    
    #constructor
    def __init__(self):
        super().__init__()
        
        # set image
        self.image = pygame.image.load("Health.png").convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()    

class Fish(pygame.sprite.Sprite):
    # scary fish that want to eat you
    
    def __init__(self):
        super().__init__()
        
        # set the image
        self.image = pygame.image.load("Fish.png").convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        
        
    def coord_gen(self, diff):
        self.rect.x = random.randrange(500, 2000)
        self.rect.y = random.randrange(0, 468)
        
        # also reset 'has it bitten player?'
        self.bite = False
        #reset move speed based on difficulty
        self.diff = diff
        if self.diff == 0:
            self.move = random.randrange(2, 5)
        elif self.diff == 1:
            self.move = random.randrange(3, 6)
        elif self.diff == 2:
            self.move = random.randrange(4, 7)
        
    def update(self):
        # update position, move it across the screen
        # if it bites player run it off screen
        if self.bite:
            self.rect.x -= 8
            self.rect.y += 2
        else:
            self.rect.x -= self.move
        #if moves off screen reset pos
        if self.rect.x < -200:
            self.coord_gen(self.diff)    
            
class Big_Fish(pygame.sprite.Sprite):
    # big insta death fish
    
    # call constructor
    def __init__(self, diff):
        super().__init__()
        
        # image
        self.image = pygame.image.load("Fish_2.png")
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        
        # game difficulty
        self.diff = diff
        
    def coord_gen(self, diff):
        self.rect.x = random.randrange(2000, 5000)
        self.rect.y = random.randrange(0, 458)
        
        # define movement speed based on difficulty
        self.diff = diff
        if self.diff == 0:
            self.move = random.randrange(4, 6)
        elif self.diff == 1:
            self.move = random.randrange(6, 9)
        elif self.diff == 2:
            self.move = random.randrange(8, 11)
        
    def update(self):
        self.rect.x -= self.move
        if self.rect.x < -200:
            self.coord_gen(self.diff)         
            
class Life(pygame.sprite.Sprite):
    # players lives
    
    def __init__(self):
        super().__init__()
        
        # import live image
        self.image = pygame.image.load("heart.png").convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = 40
        self.rect.y = 5
        
    def l_update(self, life_num):
        # change image based on how often Jules been bit
        if life_num < 2:
            self.image = pygame.image.load("heart_1.png").convert()
            self.image.set_colorkey(WHITE)
        elif life_num < 3:
            self.image = pygame.image.load("heart_2.png").convert()
            self.image.set_colorkey(WHITE)
        elif life_num < 4:
            self.image = pygame.image.load("heart_3.png").convert()
            self.image.set_colorkey(WHITE)
        elif life_num < 5:
            self.image = pygame.image.load("heart_4.png").convert()
            self.image.set_colorkey(WHITE)
        else:
            self.image = pygame.image.load("heart.png").convert()
            self.image.set_colorkey(WHITE)            

class Point(pygame.sprite.Sprite):
    # score image
    
    def __init__(self, point, x, y):
        super().__init__()
        
        #score image
        if point == 1:
            self.image = pygame.image.load("score_1.png").convert()
        elif point == 10:
            self.image = pygame.image.load("score_10.png").convert()
        elif point == "heart":
            self.image = pygame.image.load("score_heart.png").convert()
        elif point == "bite":
            self.image = pygame.image.load("score_bite.png").convert()
        self.image.set_colorkey(WHITE)
        
        # coords
        self.rect = self.image.get_rect()     
        self.rect.x = x
        self.rect.y = y
        
        # update number
        self.up_num = 0
        
    def update(self):
        # move the image up
        self.rect.y -= 3
        self.up_num += 1
        if self.up_num > 30:
            self.kill()
                
        
class Background(pygame.sprite.Sprite):
    # the ocean
    
    def __init__(self):
        super().__init__()
        
        # set the image
        self.image = pygame.image.load("Sea.jpg").convert()
        self.rect = self.image.get_rect()
        
# ---- game object Class ---- 
class Game(object):
    
    # constructor
    def __init__(self):
        
        # ---- game variables ----
        
        # set gamestate
        self.game_state = 0
        
        # game difficulty
        self.game_diff = 0
        
        # how many seaweeds have been eaten?
        self.score = 0
        
        # how often has Jules been bit?
        self.life_num = 5
        
        # ---- Sprite lists ----
        self.all_sprites_list = pygame.sprite.Group()
        self.food_list = pygame.sprite.Group()
        self.star_list = pygame.sprite.Group()
        self.heart_list = pygame.sprite.Group()
        self.fish_list = pygame.sprite.Group()
        self.big_fish_list = pygame.sprite.Group()
        self.life_list = pygame.sprite.Group()
        self.background_list = pygame.sprite.Group()
        
        # ---- Create Game Objects ---- 
        
        # create the background
        self.background = Background()
        self.background_list.add(self.background)       
        
        # create the player
        self.player = Player()
        self.all_sprites_list.add(self.player)
        
        # create 50 foods
        for i in range(25):
            self.food = Food()
            self.food.coord_gen()
            self.food_list.add(self.food)
            self.all_sprites_list.add(self.food)
            
        # creat a pointiful star!
        self.star = Star()
        self.star.coord_gen()
        self.star_list.add(self.star)
        self.all_sprites_list.add(self.star)   
        
        # creat 2 live giving stars!
        for i in range(2):
            self.heart = Heart()
            self.heart.coord_gen()
            self.heart_list.add(self.heart)
            self.all_sprites_list.add(self.heart)            
            
        # create 10 fish
        for i in range(10):
            self.fish = Fish()
            self.fish_list.add(self.fish)
            self.all_sprites_list.add(self.fish)
            
        # create big fish
        self.big_fish = Big_Fish(self.game_diff)
        self.big_fish_list.add(self.big_fish)
        self.all_sprites_list.add(self.big_fish)
        
        # create player lives counter
        self.life = Life()
        self.all_sprites_list.add(self.life)
        
    def process_events(self):
        # process events, return True if game is closed
        for event in pygame.event.get():
            # has player quit?
            if event.type == pygame.QUIT:
                return True    
            
            # if the game is over and player clicks, restart game
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.game_state == 2:
                    self.__init__()   
                    self.game_state = 0
            
            # keyboard controls
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.player.move_right()
                elif event.key == pygame.K_LEFT:
                    self.player.move_left()
                if event.key == pygame.K_UP:
                    self.player.move_up()
                elif event.key == pygame.K_DOWN:
                    self.player.move_down()
                    
                # set game dificulty on intro screen, control fish speed
                if self.game_state == 0:
                    if event.key == pygame.K_1:
                        self.game_diff = 0
                    elif event.key == pygame.K_2:
                        self.game_diff = 1
                    elif event.key == pygame.K_3:
                        self.game_diff = 2
                    for fish in self.fish_list:
                        fish.coord_gen(self.game_diff)
                    self.game_state = 1
                    self.big_fish.coord_gen(self.game_diff)
                    

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                    self.player.stop_x()                    
                elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    self.player.stop_y()
                    
        return False #don't quit if the player hasn't quit

    def run_logic(self):
        # runs each frame, updates positon and looks for collision  
        
        # if game isn't over
        if self.game_state == 1:
            
            # check to see if Jules grows
            self.player.grow(self.score, self.player.rect.x, self.player.rect.y)
            
            # game over parameters
            if self.life_num == 0:
                self.game_state = 2
                
            #update sprites positon
            self.all_sprites_list.update()    
            
            # ------ collisions ------
            
            # ---- food ----
            
            #check for food collisions, reset pos of seaweed if it's eaten
            self.food_eaten_list = pygame.sprite.spritecollide(self.player, self.food_list, False)
            
            # score for collisions by running through those foods added to the eaten list
            for food in self.food_eaten_list:
                #spawn the point image
                self.point_num = 1
                self.point = Point(self.point_num, food.rect.x, food.rect.y)
                self.all_sprites_list.add(self.point)
                # increase score
                self.score += 1
                # respawn the food
                food.coord_gen()                
                
            # -- star--
            #check for food collisions, reset pos of seaweed if it's eaten
            self.star_eaten_list = pygame.sprite.spritecollide(self.player, self.star_list, False)
            
            # score for collisions by running through those foods added to the eaten list
            if self.star_eaten_list:
                #spawn the point image
                self.point_num = 10
                self.point = Point(self.point_num, self.star.rect.x, self.star.rect.y)
                self.all_sprites_list.add(self.point)
                # increase score
                self.score += 10
                # respawn star
                self.star.coord_gen()         
                
            # -- hearts --
            #check for food collisions, reset pos of seaweed if it's eaten
            self.heart_eaten_list = pygame.sprite.spritecollide(self.player, self.heart_list, False)
            
            # increase health for hearts eaten if player injured, otherwise points
            for heart in self.heart_eaten_list:
                if self.life_num < 5:
                    # increase health
                    self.life_num += 1
                    self.life.l_update(self.life_num)
                    #spawn the point image
                    self.point_num = "heart"
                    self.point = Point(self.point_num, heart.rect.x, heart.rect.y)
                    self.all_sprites_list.add(self.point)                    
                heart.coord_gen()            
            
            # ---- fish ----
                
            # check to see if bit by a fish
            self.bitten_list = pygame.sprite.spritecollide(self.player, self.fish_list, False)
            
            # deduct score for each bite
            for fish in self.bitten_list:
                if not fish.bite:
                    # update how often player been bitten and change lives image
                    self.life_num -= 1
                    self.life.l_update(self.life_num)
                    # run fish off if it feeds
                    fish.bite = True
                    # flash injured player image
                    self.player.bit = True
                    #spawn the point image
                    self.point_num = "bite"
                    self.point = Point(self.point_num, fish.rect.x, fish.rect.y)
                    self.all_sprites_list.add(self.point)                     
            
            # -- big fish --
            
            # check if big fish bites
            self.bitten_list = pygame.sprite.spritecollide(self.player, self.big_fish_list, False)
            
            # Jules needs the hospital if the big fish bites him
            if self.bitten_list:
                self.life_num = 0
            
    def display_frame(self, screen):
        # put everything up on screen
        
        #fill the screen with white
        screen.fill(WHITE)
        
        # ---- Game Start Screen ----
        
        if self.game_state == 0:
            self.start_image = pygame.image.load("game_start.png").convert()
            screen.blit(self.start_image, [0, 0])
        
        # ---- Game Over Screen ----
        
        elif self.game_state == 2:
            
            # put up game over background
            self.over_image = pygame.image.load("game_over.png").convert()
            screen.blit(self.over_image, [0, 0])
            
            # put up score
            # format score to blit it
            font = pygame.font.SysFont("serif", 25)
            self.str_score = "Score: " + str(self.score)
            text = font.render(self.str_score, True, BLACK)
            # calculate screen centre
            centre_x = (SCREEN_WIDTH // 2) - (text.get_width() // 2)
            centre_y = (SCREEN_HEIGHT // 2) - (text.get_height() // 2)
            # put text on screen
            screen.blit(text, [centre_x, centre_y + 40])                          
            
            # put up restart text
            # define some fonts
            font = pygame.font.SysFont("serif", 25)
            text = font.render("Game Over, click to restart", True, BLACK)
            # work out central coords for the text
            centre_x = (SCREEN_WIDTH // 2) - (text.get_width() // 2)
            centre_y = (SCREEN_HEIGHT // 2) - (text.get_height() // 2)            
            # put text on screen
            screen.blit(text, [centre_x, centre_y])              
        
        # ---- Game Screen ----
        
        # draw everything
        elif self.game_state == 1:
            self.background_list.draw(screen)
            self.all_sprites_list.draw(screen)
            
            # flash images up for events
            if self.player.bit:
                screen.blit(self.player.image_b, [self.player.rect.x, self.player.rect.y])
                self.player.bit = False                
            
            # format score to blit it
            font = pygame.font.SysFont("serif", 25)
            self.str_score = str(self.score)
            self.text = font.render(self.str_score, True, BLACK)
            # put text on screen
            screen.blit(self.text, [0, 0])        
        
        # flip the screen    
        pygame.display.flip()        
        
# ---- main program ----
def main():
    
    # initialise pygame
    pygame.init()
    
    # set up screen
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)
    
    pygame.display.set_caption("Jules' Adventure")
    
    # game is not done
    done = False
    
    # set up clock
    clock = pygame.time.Clock()
    
    # creat an instance of the game
    game = Game()
    
    # set the main game loop going
    while not done:
        
        # process events, see if game is done via quitting
        done = game.process_events()
        
        # run game logic, updating positions and collision checking
        game.run_logic()
        
        # draw everthing
        game.display_frame(screen)
        
        # set the frame rate
        clock.tick(60)
        
    # close window and exit
    pygame.quit()
    
# call the main function if this is the program, get everything going
if __name__ == "__main__":
    main()