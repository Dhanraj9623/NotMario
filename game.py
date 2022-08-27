import pygame
pygame.init()
win=pygame.display.set_mode((1000,600))
pygame.display.set_caption("Shooting game")

walkR=pygame.image.load('L3.png')
walkl=pygame.image.load('L2.png')
enemyL=pygame.image.load('L1.png')
bg= pygame.image.load('bg1.png')
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
        self.vel=5
        self.left=False
        self.right=False
        self.isJump=False
        self.jumpCount=20
        self.hitbox=(self.x + 10,self.y,45,64)
    def draw(self,win):
        if self.left:
            win.blit(walkl,(self.x,self.y))
        else:
            win.blit(walkR,(self.x,self.y))
        self.hitbox=(self.x + 10,self.y,45,64)
        h=pygame.draw.rect(win,(255,0,0),self.hitbox,2)
        #print(h)
        
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
    def __init__(self,x,y,width,height,end):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.end=end
        self.path=[self.x,self.end]
        self.vel = 5
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
            pygame.draw.rect(win,(255,0,0),self.hitbox,2)                                                                                                                       
    
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
        
        
        
def draw_gamewindow():
    win.blit(bg,(0,0))
    text = font.render('Score:'+ str(score),1,(0,0,0))
    win.blit(text,(830,50))
    man.draw(win)
    enemy1.draw(win)
    # man2.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    pygame.display.update()
    
font = pygame.font.SysFont('comicsans',30,True)    
man = player(50,455,64,64)
enemy1 = enemy(50,455,64,64,900)

bullets = []

run=True
while run:
    clock.tick(60)
    #pygame.time.delay(15)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run= False
    for bullet in bullets:
        if bullet.y - bullet.radius < enemy1.hitbox[1] + enemy1.hitbox[3] and bullet.y + bullet.radius > enemy1.hitbox[1]:
            if bullet.x + bullet.radius > enemy1.hitbox[0] and bullet.x - bullet.radius < enemy1.hitbox[0] + enemy1.hitbox[2]:
                hitsound.play()
                enemy1.hit()
                score+=1
                bullets.pop(bullets.index(bullet))
        
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
        if len(bullets) < 3:
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

    draw_gamewindow()
pygame.quit()


