import pygame
import random
pygame.init()
win=pygame.display.set_mode((1000,600))
pygame.display.set_caption("Shooting game")

walkR=pygame.image.load('L3.png')
walkl=pygame.image.load('L2.png')
enemyL=pygame.image.load('L1.png')
enemy2=pygame.image.load('xyz.png')
bg= pygame.image.load('bg1.png')
over=pygame.image.load('over.png')
clock = pygame.time.Clock()
score=0
hitsound = pygame.mixer.Sound('ugh.wav')
bulletsound = pygame.mixer.Sound('bullet.wav')
music = pygame.mixer.music.load('mario.mp3')
pygame.mixer.music.play(-1)


class player():
    def __init__(self,x,y,width,height):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.vel=8
        self.left=False
        self.right=False
        self.isJump=False
        self.jumpCount=20
        self.visible=True
        self.hitbox=(self.x + 10,self.y,45,64)
        self.health=100
    def draw(self,win):
        if self.left:
            win.blit(walkl,(self.x,self.y))
        else:
            win.blit(walkR,(self.x,self.y))
        self.hitbox=(self.x + 10,self.y,45,64)
        pygame.draw.rect(win, (255,0,0), (self.hitbox[0], self.hitbox[1] - 20, 100, 10)) 
        pygame.draw.rect(win, (0,128,0), (self.hitbox[0], self.hitbox[1] - 20, self.health, 10))
        # h=pygame.draw.rect(win,(255,0,0),self.hitbox,2)
        #print(h)
    def hit(self):
        if self.health > 0:
            self.health -= 1/2
        else :
            man.visible=False
            
        
class projectile():                 
    def __init__(self,x,y,radius,colour,facing):
        self.x=x
        self.y=y
        self.radius=radius
        self.colour=colour
        self.facing=facing
        self.vel=15*facing

    def draw(self,win):
        pygame.draw.circle(win, self.colour, (self.x,self.y), self.radius)

class enemy():
    def __init__(self,x,y,width,height,end,vel):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.end=end
        self.path=[self.x,self.end]
        self.vel = vel
        self.hitbox=(self.x +20,self.y+10,30,64)
        self.health=10
        self.visible=True
        

    def draw(self,win):
        if self.visible:
            self.move()
            
            win.blit(enemyL,(self.x,self.y))
            self.hitbox=(self.x +20,self.y+10,30,64)
            pygame.draw.rect(win, (255,0,0), (self.hitbox[0], self.hitbox[1] - 20, 64, 10)) 
            u=pygame.draw.rect(win, (0,128,0), (self.hitbox[0], self.hitbox[1] - 20, self.width, 10))
            #print(u)
            # pygame.draw.rect(win,(255,0,0),self.hitbox,2) draw hitbox for enemy                                                                                                                        
    
    def move(self):
        if self.vel > 0:
            if self.x < self.path[1] + self.vel:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.x += self.vel
                
        else:
            if self.x > self.path[0] - self.vel:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.x += self.vel
      
    def hit(self):
        if self.width > 0:
            self.width -= 1/2
        else :
            self.visible = False
            self.hitbox=(0,0,0,0)
        
        
def draw_exit():
    win.blit(over,(0,0))
    pygame.display.update()
    
def draw_gamewindow():
    win.blit(bg,(0,0))
    text = font.render('Score:'+ str(score),1,(0,0,0))
    win.blit(text,(830,50))
    man.draw(win)
    # enemy1.draw(win)
    # enemy2.draw(win)
    for enemy in enemies:
        enemy.draw(win)
    # man2.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    pygame.display.update()


    
    
font = pygame.font.SysFont('comicsans',30,True)    
man = player(50,455,64,64)
# enemy1 = enemy(50,455,64,64,900,5)
# enemy2 = enemy(100,455,64,64,400,20)
enemies = [enemy(-60, 455, 64, 64, 1000, 5), enemy(100, 455, 64, 64, 400, 5)]
bullets = []
num=3      #bullets capacity initially

run=True
while run:
    clock.tick(60)
    #pygame.time.delay(15)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run= False
    

    for i in range(len(enemies)):
        if enemies[i].visible==False :
            del enemies[i]
            num+=3
            man.health=100
            enemies.append(enemy(random.randint(-30,40), 455, 64, 64, random.randint(900, 1000), random.randint(2, 30)))
            enemies.append(enemy(random.randint(-30,40), 455, 64, 64, random.randint(400, 1000), random.randint(2, 8)))
            
    for enemyy in enemies:
        for bullet in bullets:
        
            
            if bullet.y - bullet.radius < enemyy.hitbox[1] + enemyy.hitbox[3] and bullet.y + bullet.radius > enemyy.hitbox[1]:
                if bullet.x + bullet.radius > enemyy.hitbox[0] and bullet.x - bullet.radius < enemyy.hitbox[0] + enemyy.hitbox[2]:
                    hitsound.play()
                    enemyy.hit()
                    score+=1
                    
                    bullets.pop(bullets.index(bullet))
                
        if man.hitbox[1] < enemyy.hitbox[1] + enemyy.hitbox[3] and man.hitbox[1] + man.hitbox[3] > enemyy.hitbox[1]:
            if man.hitbox[0] + man.hitbox[2] > enemyy.hitbox[0] and man.hitbox[0] < enemyy.hitbox[0] + enemyy.hitbox[2]:
                man.hit()

                        
    for bullet in bullets:
        if bullet.x<1000 and bullet.x>0:
            bullet.x+=bullet.vel
        else:
            bullets.pop(bullets.index(bullet))
            
    keys = pygame.key.get_pressed()

    if event.type == pygame.MOUSEBUTTONDOWN:
        bulletsound.play()
        if man.left :
            facing=-1
        else :
            facing=1
        if len(bullets) < num:
            bullets.append(projectile(round(man.x + man.width //2), round(man.y + man.height//2), 6, (0,0,0), facing))
        
    if keys[pygame.K_a] and man.x>-10 :
        man.x-= man.vel
        man.left=True
        man.right=False
    if keys[pygame.K_d]and man.x<1000-man.width:
        man.x+= man.vel
        man.left=False
        man.right=True
    
    if not (man.isJump):    
        if keys[pygame.K_w]:
            man.isJump = True
            # man.left=True
            # man.right=True
    else:
        if man.jumpCount >= -20:
            man.y-= man.jumpCount 
            man.jumpCount -=1
        else:
            man.isJump = False
            man.jumpCount = 20

    if man.visible==False:
        draw_exit()
    else:    
        draw_gamewindow()
pygame.quit()


