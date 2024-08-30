import pygame
import sys
import time
import random

# Inizializza Pygame
pygame.init()
# Creazione della finestra
width=480
height=800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("PONG")

#Setting colori
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

arr = (1, -1)
# Creazione pallina
ball_x = width/2 
ball_y = height/2
ball_radius = 10
ball_speed = 6
ball_color = WHITE
vx = 1
vy = 1

# Creazione player1
player1_score = 0
player1_width = 60
player1_height = 30
player1_x = width/2 - (player1_width/2)
player1_y = height - player1_height
player1_color = WHITE
player1_speed = 7
rect = pygame.Rect(player1_x, player1_y, player1_width, player1_height)

# Creazione player2
player2_score = 0
player2_width = 60
player2_height = 30
player2_x = width/2 - (player2_width/2)
player2_y = 0
player2_color = WHITE
player2_speed = 7
rect = pygame.Rect(player2_x, player2_y, player1_width, player1_height)

# Font nel menu
title = pygame.font.Font("font/score.ttf", int(width/5))
menu_font = pygame.font.Font("font/score.ttf", int(width/25))

#Font in gioco e in pausa
score_font = pygame.font.Font("font/score.ttf", int(width/15))
impact = pygame.font.SysFont("Impact", int(width/10))

#Creazione del testo nel menu
menu_title = title.render("PONG", True, WHITE)
menu_title_rect = menu_title.get_rect(center =(width/2, height/4))

menu_bot = menu_font.render("Gioca contro il computer", True, WHITE)
menu_bot_rect = menu_bot.get_rect(center =(width/2, height/2))

menu_friend = menu_font.render("Gioca contro un amico", True, WHITE)
menu_friend_rect = menu_friend.get_rect(center =(width/2, height/2 + 100))

#menu_shop = menu_font.render("Negozio", True, WHITE)
#menu_shop_rect = menu_shop.get_rect(center =(width/2, height/2 + 200))

menu_settings = menu_font.render("Impostazioni", True, WHITE)
menu_settings_rect = menu_settings.get_rect(center =(width/2, height/2 + 300))

menu_exit = menu_font.render("Esci dal gioco", True, WHITE)
menu_exit_rect = menu_exit.get_rect(center =(width/2, height/2 + 350))

# Creazione del testo in game
score_player1_text = score_font.render(str(player1_score), True, WHITE)
score_player1_text_rect = score_player1_text.get_rect(center=(width/2, height/4))

score_player2_text = score_font.render(str(player2_score), True, WHITE)
score_player2_text_rect = score_player2_text.get_rect(center=(width/2, height*(3/4)))

# Creazione del testo in pausa

resume_text = menu_font.render("Riprendi", True, WHITE)
resume_text_rect = resume_text.get_rect(center=(width/2, height/2 - 100))

# Creazione del testo nelle impostazioni

music_ON = menu_font.render("Musica: ON", True, WHITE)
music_ON_rect = music_ON.get_rect(center=(width/2, height/2 - 100))
music_OFF = menu_font.render("Musica: OFF", True, WHITE)
music_OFF_rect = music_OFF.get_rect(center=(width/2, height/2 - 100))

goback = menu_font.render("Torna al menu", True, WHITE)
goback_rect = goback.get_rect(center=(width/2, height/2 + 100))
goback_center_rect = goback.get_rect(center=(width/2, height/2 + 100))

# Creazione dei file audio
pygame.mixer.init()
pygame.mixer.music.load('music/%d.mp3' %random.randint(0,11))
pygame.mixer.music.set_volume(1)
pygame.mixer.music.play(loops=-1)

#score = pygame.mixer.Sound("score.mp3")
#paddle = pygame.mixer.Sound("paddle.mp3")
#wall = pygame.mixer.Sound("wall.mp3")

last_switch = pygame.time.get_ticks()
visible = False

# Setting dello stato del gioco iniziale
paused = False
play = False
settings = False
shop = False
bot = False
music = True
menu = True

def drawPlay():
    screen.fill(BLACK)
    pygame.draw.circle(screen, ball_color, (ball_x, ball_y), ball_radius)
    pygame.draw.rect(screen, player1_color, (player1_x, player1_y, player1_width, player1_height))
    pygame.draw.rect(screen, player2_color, (player2_x, player2_y, player2_width, player2_height))
    screen.blit(score_font.render(str(player1_score), True, WHITE), score_player1_text_rect)
    screen.blit(score_font.render(str(player2_score), True, WHITE), score_player2_text_rect)

def ballScores(ball_y):
    if ball_y >= height-ball_radius or ball_y<= ball_radius:
        return True

def ballTouchingWall(ball_x):
    if ball_x >= width-ball_radius or ball_x <= ball_radius:
        return True

def drawMenu():
    screen.fill(BLACK)
    screen.blit(menu_title, menu_title_rect)
    screen.blit(menu_bot, menu_bot_rect)
    screen.blit(menu_friend, menu_friend_rect)
    screen.blit(menu_settings, menu_settings_rect)
    screen.blit(menu_exit, menu_exit_rect)

def closeAll():
    pygame.mixer.music.stop()
    pygame.quit()
    sys.exit()

# Loop principale
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Logica del menu
    if menu == True:

        #Riporta i valori a quelli di default
        ball_x = width/2 
        ball_y = height/2
        player2_score = 0
        player1_score = 0
        player1_x = width/2 - (player1_width/2)
        player2_x = width/2 - (player2_width/2)
        ball_speed = 6
        vx = random.uniform(-0.99, 0.99)
        vy = arr[random.randint(0,1)]

        drawMenu()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pressed = True

        if event.type == pygame.MOUSEBUTTONUP and mouse_pressed == True:  
            mouse_pos = event.pos
            if menu_bot_rect.collidepoint(mouse_pos):
                menu = False
                play = True
                bot = True
            elif menu_friend_rect.collidepoint(mouse_pos):
                menu = False
                play = True
                bot = False
            elif menu_settings_rect.collidepoint(mouse_pos):
                menu = False
                settings = True
            elif menu_exit_rect.collidepoint(mouse_pos):
                closeAll()
            
            mouse_pressed = False

    #Logica di gioco
    if play == True:

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                paused = not paused
                play = not play
                

        #Loop della pallina
        ball_x = ball_x + (ball_speed * vx)
        ball_y = ball_y + (ball_speed * vy)

        #Logica dei rimbalzi della pallina sulla parete o quando segna
        if ballTouchingWall(ball_x):
            vx = -vx
            #wall.play()

        if ball_y >= height-ball_radius:
            ball_speed = 8
            #score.play()
            ball_x = width/2 
            ball_y = height/2
            vx = random.uniform(-0.99, 0.99)
            vy = arr[random.randint(0,1)]
            player1_score += 1
        elif ball_y <= ball_radius:
            ball_speed = 8
            ball_speed = 8
            #score.play()
            ball_x = width/2 
            ball_y = height/2
            vx = random.uniform(-0.99, 0.99)
            vy = arr[random.randint(0,1)]
            player2_score += 1

                    
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            if player1_x > 0:
                player1_x -= player1_speed
        if keys[pygame.K_RIGHT]:
            if player1_x < width - player1_width:
                player1_x += player1_speed

        # Comandi secondo giocatore
        if bot == False:
            if keys[pygame.K_a]:
                if player2_x > 0:
                    player2_x -= player2_speed
            if keys[pygame.K_d]:
                if player2_x < width - player2_width:
                    player2_x += player2_speed
        else:
            if vy == -1:
                if ball_y <= height/2:

                    if 0 <= player2_x <= width-player2_width:
                        if ball_x >= player2_x + player2_width:
                            player2_x += player2_speed
                        if ball_x <= player2_x:
                            player2_x -= player2_speed
                    if player2_x <0:
                        player2_x =0
                    if player2_x > width-player2_width:
                        player2_x = width-player2_width
                
                
                # Logica dei rimbalzi della pallina sul giocatore 1
        if ((player1_x  < ball_x < player1_x + player1_width) and (ball_y >= height - (player1_height + ball_radius))):
            vx = random.uniform(-0.99, 0.99)
            vy = -1
            if ball_speed <20:
                ball_speed += 0.25
            #paddle.play()

                #Logica dei rimbalzi della pallina sul giocatore 2
        if ((player2_x <= ball_x <= player2_x + player2_width) and (ball_y <= player2_height + ball_radius)):
            vx = random.uniform(-0.99, 0.99)
            vy = 1
            if ball_speed <20:
                ball_speed += 0.25
            #paddle.play()
        
        drawPlay()
                
    if paused == True:
        pygame.mixer.music.pause()
        screen.blit(resume_text, resume_text_rect)
        screen.blit(goback, goback_rect)

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pressed = True

        if event.type == pygame.MOUSEBUTTONUP and mouse_pressed == True:  
            mouse_pos = event.pos
            if resume_text_rect.collidepoint(mouse_pos):
                paused = False
                play = True
                pygame.mixer.music.unpause()
            if goback_rect.collidepoint(mouse_pos):
                menu = True
                play = False
                pygame.mixer.music.stop()
                pygame.mixer.music.play(-1)
                paused = False
            mouse_pressed = False



    if settings == True:
        screen.fill(RED)

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pressed = True

        if event.type == pygame.MOUSEBUTTONUP and mouse_pressed == True:    

            if music_OFF_rect.collidepoint(event.pos):
                if music:
                    pygame.mixer.music.pause()
                    music = False
                else:
                    pygame.mixer.music.unpause()
                    music = True

            if goback_center_rect.collidepoint(event.pos):
                menu = True
                play = False
                settings = False
            
            mouse_pressed = False

        if music:
            screen.blit(music_ON, music_ON_rect)
        else:
            screen.blit(music_OFF, music_OFF_rect)

        screen.blit(goback, goback_center_rect)

    pygame.display.flip()
    pygame.time.Clock().tick(60)

closeAll()
