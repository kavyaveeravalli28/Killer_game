import math
import pygame
import random


pygame.init()

#creation of a game window
screen=pygame.display.set_mode((800,600))

#icon and title
title="Killer Game"
icon=pygame.image.load('data/logo.png')
pygame.display.set_caption(title)
pygame.display.set_icon(icon)

#background
bg=pygame.image.load('data/background.png')

pygame.mixer.music.load('data/bg_music.wav')
pygame.mixer.music.play(-1)

bullet_sound=pygame.mixer.Sound('data/laser.wav')
explosion_sound=pygame.mixer.Sound('data/explosion.wav')

#player
player_img=pygame.image.load('data/player.jpg')
playerX=368
playerY=516
playerX_change=0

#enemy
no_of_enemies=6

enemy_img=[]
enemyX=[]
enemyY=[]
enemyX_change=[]
enemyY_change=[]

for i in range(no_of_enemies):
     enemy_img.append(pygame.image.load('data/enemy.png'))
     enemyX.append(random.randint(0,736))
     enemyY.append(random.randint(20,120))
     enemyX_change.append(1.5)
     enemyY_change.append(40)

#bullet
bullet_img=pygame.image.load('data/bullet.jpg')
bulletX=0
bulletY=516
bulletY_change=-2.5
bullet_state='ready'

score=0
score_font=pygame.font.Font('data/Aldrich-Regular.ttf',32)
scoreX=10
scoreY=10

game_over_font=pygame.font.Font('data/Aldrich-Regular.ttf',64)
game_overX=200
game_overY=200




restart_font=pygame.font.Font('data/Aldrich-Regular.ttf',32)
restartX=180
restartY=300

game_status='running'

def  show_restart(x,y):
    restart_img=restart_font.render('To Restart the game Press R ',True,(0,255,0))
    screen.blit(restart_img,(x,y))

def show_game_over(x,y):
    global game_status
    game_over_img=game_over_font.render('GAME OVER',True,(255,255,255))
    screen.blit(game_over_img,(x,y))
    pygame.mixer.music.stop()
    game_status='end'

def show_score(x,y):
    score_img=score_font.render('score: '+ str(score),True,(255,255,255))
    screen.blit(score_img,(x,y))

def iscollision(x1,y1,x2,y2):
    distance=math.sqrt(math.pow((x2-x1),2)+math.pow((y2-y1),2))
    if distance < 25:
        return True
    else:
        return False    

def bullet(x,y):
    screen.blit(bullet_img,(x+16,y+10))
def enemy(x,y,i):
    screen.blit(enemy_img[i],(x,y))

def player(x,y):
    screen.blit(player_img,(x,y))

game_on=True
while game_on:
    #background
    screen.fill((45,51,71))
    screen.blit(bg,(0,0))

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            game_on=False

        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_LEFT:
               playerX_change=-0.7
            if event.key==pygame.K_RIGHT:
                playerX_change=+0.7
            if event.key==pygame.K_SPACE:
                if bullet_state=='ready':
                  bullet_state='fire'
                  bulletX=playerX
                  bullet(bulletX,bulletY)
                  bullet_sound.play()
                  #restarting the game
            if event.key==pygame.K_r:
                if game_status=='end':
                    game_status='running'
                    score=0
                    playerX=366
                    pygame.mixer.music.play(-1)
                    for i in range(no_of_enemies):
                        enemyX[i]=random.randint(0,736)
                        enemyY[i]=random.randint(20,120)

        if event.type==pygame.KEYUP:
            if event.key==pygame.K_LEFT  or event.key==pygame.K_RIGHT:
                playerX_change=0

     #bullet movements
    if bullet_state=='fire':
        if bulletY<10:
            bulletY=516
            bullet_state='ready'
        bulletY+=bulletY_change
        bullet(bulletX,bulletY)
    
    #enemy movements
    for i in range(no_of_enemies):
        #game over
        if enemyY[i]>466:
            show_game_over(game_overX,game_overY)
            show_restart(restartX,restartY)
            for j in range(no_of_enemies):
                enemyY[j]=1200
        #***
        enemyX[i]+=enemyX_change[i]
        if enemyX[i]<=0:
            enemyX[i]=0
            enemyX_change[i]=1.5
            enemyY[i]+=enemyY_change[i]
        elif enemyX[i] >=736:
            enemyX[i]=736
            enemyX_change[i]=-1.5
            enemyY[i]+=enemyY_change[i]

        enemy(enemyX[i],enemyY[i],i)

    #collision   
        collision=iscollision(enemyX[i],enemyY[i],bulletX,bulletY)
        if collision:
           bulletY=516
           bullet_state='ready'
           enemyX[i]=random.randint(0,736)
           enemyY[i]=random.randint(20,120)
           score+=1
           explosion_sound.play()
         #  print(score)
    show_score(scoreX,scoreY)

    #player movements
    playerX += playerX_change
    if playerX<=0:
        playerX=0
    elif playerX>=736:
        playerX=736

    player(playerX,playerY)


    pygame.display.update()