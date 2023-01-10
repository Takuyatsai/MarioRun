import pygame
pygame.init()
win = pygame.display.set_mode((1440,1200))

pygame.display.set_caption("Mario")

Rmario = [pygame.image.load('image/Rmario'+str(i)+'.png') for i in range(2)]
Lmario = [pygame.image.load('image/Lmario'+str(i)+'.png') for i in range(2)]
char = pygame.image.load('image/Rmario0.png')

clock = pygame.time.Clock()

x = 50
y = 425
width = 64
height = 64
vel = 5

isJump = False
jumpCount = 10
left = False
right = False
walkCount = 10

def redrawGameWindows():
    global walkCount
    win.fill((255,255,255))
    
    if walkCount +1 >=27:
        walkCount = 0
    
    if left:
        win.blit(Lmario[walkCount//2], (x, y))
        walkCount += 1
    elif right:
        win.blit(Rmario[walkCount//2], (x, y))
        walkCount += 1 
    else:
        win.blit(char, (x, y))
        
    pygame.display.update()
    
#loop
run = True
while run:
    clock.tick(27)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_LEFT] and x > vel:
        x -= vel
        left = True
        right = False
    if keys[pygame.K_RIGHT] and x < 500 - width - vel:
        x += vel
        left = False
        right = True
    else:
        right = False
        left = False
        walkCount = 0
        
    if not(isJump):
        if keys[pygame.K_SPACE]:
            isJump = True
            right = False
            left = False
            walkCount = 0
    else:
        if jumpCount >= -10:
            neg = 1
            if jumpCount < 0:
                neg = -1
            y -= (jumpCount **2) * 0.5 * neg
            jumpCount -= 1
        else:
            isJump = False
            jumpCount = 10
            
    redrawGameWindows()
    
pygame.quit()