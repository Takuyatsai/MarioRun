import pygame, time, numpy as np, matplotlib.pyplot as plt
pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=512)
pygame.mixer.init()
pygame.init()

display_width = 800
display_height = 600
white = (255, 255, 255)
black =(0, 0, 0)
canvas = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption(u'Mario run')
clock = pygame.time.Clock()
gaming = True
fps = 60
vel = 5


runtick = 0
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
background = pygame.image.load('image/background.jpg').convert()
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
    

best_score = 0
score = 0
def restart(first_time=False):
    global mario_pos, guy_pos, walkcount, jumpcount, jumping, score, background_pos, runtick, chromosome, generation, fitness_array, best_fitness_array, best_score
    mario_pos = [100,450]
    guy_pos = [1200,470]
    walkcount = 0
    jumpcount = 0
    jumping = False
    if score > best_score: best_score = score
    background_pos = [0,0]
    runtick = 0
    theme.play()
    
    if not first_time:
        fitness_array.append(score)
        score = 0
        chromosome += 1
        if chromosome > chromosome_num-1:
            nextround()
            best_fitness_array.append(np.max(fitness_array))
            chromosome = 0
            generation += 1
            fitness_array = []
            plt.clf()
            plt.title("Mario Run")
            plt.xlabel("Genetarion")
            plt.ylabel("Score")
            plt.plot(best_fitness_array)
            plt.grid()
            plt.pause(0.001)


#GA
chromosome = 0
chromosome_num = 10 
jumptime = 1000
jumprate = 0.5
population = np.array([[0]*jumptime]*chromosome_num)
generation = 0
fitness_array = []
best_fitness_array = [0]
sel_num = round(chromosome_num*0.3)
copy_num = chromosome_num - sel_num
for i in range(chromosome_num):
    for j in range(jumptime): 
        if np.random.rand() < jumprate: population[i,j] = 1

def nextround():
    global population
    #Selection
    sel_idx = np.argsort(fitness_array)[-sel_num:]
    sel_idx = np.flipud(sel_idx)
    tmppopulation = np.copy(population[sel_idx])
    print(sel_idx)
    #copy
    for i in range(copy_num):
        copy_idx = np.random.choice(sel_idx)
        tmppopulation = np.concatenate((tmppopulation, population[copy_idx].reshape(1,jumptime)), axis = 0)
    population = np.copy(tmppopulation)
    #Crossover
    for i in range(sel_num, chromosome_num):
        for j in range(jumptime): #跳
            if np.random.rand() < 0.3:
                change_chromosome = np.random.randint(sel_num, chromosome_num)
                while i == change_chromosome: change_chromosome = np.random.randint(sel_num, chromosome_num)
                #swap
                tmp = np.copy(population[i,j])
                population[i,j] = np.copy(population[change_chromosome,j])
                population[change_chromosome,j] = np.copy(tmp)
    #Mutation
    for i in range(sel_num, chromosome_num):
        for j in range(jumptime):
            if np.random.rand() < 0.3:
                if np.random.rand() < jumprate: population[i,j] = 1
                else: population[i,j] = 0


restart(True)
def game_loop():
    global gaming, canvas, mario_pos, jumping, jumpcount, score, runtick, fps
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
                elif event.key == pygame.K_a:
                    fps = 600
                    theme.set_volume(0)
                    die.set_volume(0)
                    jump.set_volume(0)
                elif event.key == pygame.K_s:
                    fps = 60
                    theme.set_volume(0.2)
                    die.set_volume(0.1)
                    jump.set_volume(0.1)
        mario_moving()
        
        runtick += 1
        jump_idx = runtick//30
        if runtick > 30 and runtick % 30 == 0 and jump_idx < jumptime - 1:
            if population[chromosome, jump_idx] == 1 and jumping == False:
                jumping = True
                jump.play()
        
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
        if fps == 60: canvas.blit(background, background_pos) #背景 很卡
        #顯示馬力歐
        if jumping: canvas.blit(mario[3], mario_pos)
        elif walkcount%15 < 5: canvas.blit(mario[0], mario_pos)
        elif walkcount%15 < 10: canvas.blit(mario[1], mario_pos)
        else: canvas.blit(mario[2], mario_pos)
        if walkcount%20 < 10: canvas.blit(guy[0], guy_pos)
        else: canvas.blit(guy[1], guy_pos)
        
        showFont(f'得分：{score}, 最高分: {best_score}, Generation: {generation}, Chromosome: {chromosome}, 跳躍次數: {jump_idx}',50,50)
        
        #碰撞判定
        if mario_pos[0] < guy_pos[0] < mario_pos[0] + mario_size[0]-10 and mario_pos[1] < guy_pos[1]+5 < mario_pos[1] + mario_size[1]:
            die.play()
            theme.stop()
            showFont('You died!', 200, 200)
            pygame.display.update()
            if fps == 60: time.sleep(4)
            restart()
        pygame.display.update()
        clock.tick(fps)
game_loop()
pygame.quit()
quit()
        
    
    
    
    
    
    
    
    