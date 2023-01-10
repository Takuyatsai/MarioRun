import pygame, time, numpy as np
pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=512)
pygame.mixer.init()
pygame.init()

display_width = 1200
display_height = 600
white = (255, 255, 255)
black =(0, 0, 0)
canvas = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption(u'Mario run')
clock = pygame.time.Clock()
gaming = True
fps = 60
vel = 5

#showFont
font0 = pygame.font.Font('font/msjhbd.ttc', 18)
font1 = pygame.font.Font('font/ammo.ttf', 30)
def showFont( text, x, y, font=font0, color=black):
    global canvas    
    text = font.render(text, 1, color)
    canvas.blit( text, (x,y))
    
#sound
theme = pygame.mixer.Sound('sound/Theme.wav')
theme.set_volume(0.2)    #0~1
die = pygame.mixer.Sound('sound/die.wav')
die.set_volume(0.1)    

#Mario
mario = [pygame.image.load('image/mario'+str(i)+'.png') for i in range(4)]
guy = [pygame.image.load('image/guy'+str(i)+'.png') for i in range(2)]
jump = pygame.mixer.Sound('sound/jump.wav')
jump.set_volume(0.1)
mario_size = [50,70]
guy_size = [40,50]
mario = [pygame.transform.scale(mario[i], mario_size) for i in range(4)]
guy = [pygame.transform.scale(guy[i], guy_size) for i in range(2)]
background = pygame.image.load('image/background.jpg').convert( )
background_pos = [0,0]
#mario_pos = [100,450]
#guy_pos = [1200,470]
#walkcount = 0
#jumpcount = 0
#jumping = False
#score = 0
#theme.play()

#def mario_motion():
#    mario_i = 0
#    global mario_n
#    while gaming:
#        mario_n = mario[mario_i]
#        mario_i +=1
#        if mario_i >0

mario_moving_fps = pygame.time.Clock()
def mario_moving():
    global mario_pos, walkcount, guy_pos, background_pos
#    mario_pos[0] += 5
    guy_pos[0] -= 5
    walkcount += 1
    if guy_pos[0] < -100 :
        guy_pos = [1200,470]
    background_pos[0] -= 3
    if background_pos[0] < -1066:
        background_pos[0] = 0

def restart():
    global mario_pos, guy_pos, walkcount, jumpcount, jumping, score, background_pos
    mario_pos = [100,450]
    guy_pos = [1200,470]
    walkcount = 0
    jumpcount = 0
    jumping = False
    score = 0
    background_pos = [0,0]
    theme.play()
restart()

def game_loop():
    global gaming, canvas, mario_pos, jumping, jumpcount, score
    while gaming:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gaming = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    gaming = False
                elif event.key == pygame.K_SPACE and jumping == False:
                    jumping = True
                    jump.play()
        mario_moving()
        if jumping:
            if jumpcount < 10:mario_pos[1] -= 7
            elif jumpcount < 20: mario_pos[1] -= 5
            elif jumpcount < 30: mario_pos[1] -= 3
            elif jumpcount < 40: mario_pos[1] += 3
            elif jumpcount < 50: mario_pos[1] += 5
            else: mario_pos[1] += 7
            jumpcount += 1
            if jumpcount == 60:
                jumpcount = 0
                jumping = False
        score += 1

        canvas.fill(white)  #刷新白畫面
        canvas.blit(background, background_pos)
        #顯示馬力歐
        if jumping: canvas.blit(mario[3], mario_pos)
        elif walkcount%15 < 5: canvas.blit(mario[0], mario_pos)
        elif walkcount%15 < 10: canvas.blit(mario[1], mario_pos)
        else: canvas.blit(mario[2], mario_pos)
        if walkcount%20 < 10: canvas.blit(guy[0], guy_pos)
        else: canvas.blit(guy[1], guy_pos)
        
        showFont('Score:'+str(score),50,50)
        #碰撞判定
        if mario_pos[0] < guy_pos[0] < mario_pos[0] + mario_size[0]-10 and mario_pos[1] < guy_pos[1]+5 < mario_pos[1] + mario_size[1]:
            die.play()
            theme.stop()
            showFont('No delate!', 200, 200)
            pygame.display.update()
            time.sleep(4)
            restart()
        pygame.display.update()
        clock.tick(fps)
game_loop()
pygame.quit()
quit()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    