import pygame
import random
import math

#initialize pygame
pygame.init()

#create screen
screen = pygame.display.set_mode((795,589))

#background image
background = pygame.image.load('892.png')

# an event is anything that happens inside your game window; pressing any key etc.

#title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

#player image
player_img = pygame.image.load('spaceship.png')
playerX = 370
playerY = 480
playerX_change = 0


enemy_img = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
no_enemies = 6

for i in range(no_enemies):
#enemy image
    enemy_img.append(pygame.image.load('ghost.png'))
    enemyX.append(random.randint(0,735))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(0.3)
    enemyY_change.append(40)

#bullet image
bullet_img = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 2
bullet_state  = "ready"
#ready = not fired yet, not on screen
#fire = fired, on screen

#score 
score_value = 0
font = pygame.font.Font('freesansbold.ttf',32)
textX = 10
textY = 10

#game over text
game_over_font = pygame.font.Font('freesansbold.ttf',64)

def show_score(x,y):
    score = font.render("Score: "+ str(score_value),True,(255,255,255))
    screen.blit(score,(x,y))

def game_over():
    over_text = game_over_font.render("GAME OVER",True,(255,255,255))
    screen.blit(over_text,(200,250))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img,(x+16,y+10)) #so that bullet appears at the centre of the spaceship

def isCollision(enemyX,enemyY,bulletX,bulletY):
    distance = math.sqrt(math.pow(enemyX-bulletX,2) + math.pow(enemyY-bulletY,2))
    if distance < 27:
        return True
    else:
        return False
def player(x,y):
    screen.blit(player_img,(x,y)) #to draw image of player on screen

def enemy(x,y,i):
    screen.blit(enemy_img[i],(x,y))
#game loop - game runs inside this only
running = True
while running:
    screen.fill((50,0,100))
    screen.blit(background,(0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
        #if keystroke, then which one
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.5
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletX = playerX
                    fire_bullet(bulletX,bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    if playerX >= 736: # = 800-64
        playerX = 736



    for i in range(no_enemies):

        # game over
        if enemyY[i] >= 440:
            for j in range(no_enemies):
                enemyY[j] = 2000
            game_over()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.3
            enemyY[i] += enemyY_change[i]
        if enemyX[i] >= 736:
            enemyX_change[i] = -0.3
            enemyY[i] += enemyY_change[i]

        
        #collision 
        collision = isCollision(enemyX[i],enemyY[i],bulletX,bulletY)
        if collision:
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            #print(score)
            enemyX[i] = random.randint(0,735)
            enemyY[i] = random.randint(50,150)

        enemy(enemyX[i],enemyY[i],i)

    #bullet movement
    if bulletY<=0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX,bulletY)
        bulletY -= bulletY_change



    # RGB values
   
    player(playerX,playerY)
    show_score(textX,textY)
    pygame.display.update() #always included