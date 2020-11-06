#===============================================================# woo imports
import os, math, random
#==========================# import checker and installer thing. https://youtu.be/NATtwV2SDOM
tryimportlist = ('pygame') 
try: import pygame
except ImportError: 
    input('import error, not all modules found. press enter to try to install them')
    for module in tryimportlist: os.system('pip3 install '+module)
    try: import pygame
    except ImportError: input('another import error, yay! press enter to exit'); exit()
#===============================================================# window size
WIDTH = 650; HEIGHT = 650; WINDOWSIZE = [WIDTH,HEIGHT]
#===============================================================# g r a p h i c s
RTX="ON" #yes
DOSHADOWS = True
DODISTANCEFADE = True
#==========================# fancy numbers
FPS=60 #target fps
SHADOW=20 #higher is darker shadows
VIEWDISTANCEMULTIPLIER=.17 #effects distance fading, lower is less. 
RAYNUM=325 #number of rays cast, effects horizontal resolution. 60 or 325 is recommended
DOFMAX = 15 #actual maximum view distance
#===============================================================# gameplay variables
px = 350; py = 350; pa = 1 #player starting position and rotation
ROTATIONSPEED = .035
MOVEMENTSPEED = 2
#===============================================================# worldmap stuff
#'''
mapWidth = 9; mapHeight = 9 #starting at 0
worldMap = [
 1,1,1,1,1,1,1,1,1,1,
 1,0,0,0,0,0,0,0,0,1,
 1,0,0,1,0,0,0,0,0,1,
 1,0,0,0,0,0,0,0,0,1,
 1,0,0,0,0,0,0,0,0,1,
 1,0,0,0,0,0,0,0,0,1,
 1,0,0,0,0,0,0,0,0,1,
 1,0,0,0,0,0,0,0,0,1,
 1,0,0,0,0,0,0,0,0,1,
 1,1,1,1,1,1,1,1,1,1]
#'''
'''
mapWidth = 19; mapHeight = 19
worldMap = [
1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,1,
1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1
]
'''
#==========================#
GRIDSIZE = 64 #locked to 64
offset = round(WIDTH-((mapWidth+1)*GRIDSIZE/5))
#===============================================================# colors
SKYCOLOR=(0,0,0)
GROUNDCOLOR=(20,20,20)
WALLCOLOR=(128,128,128)
MINIMAPCOLOR=(204,0,0)
RAYCOLOR=(255,255,255)
#===============================================================# other assorted variable goodies
PI = math.pi; PI2 = PI/2; PI3 = 3*PI2; DR = 0.0174533 #DR is one degree in radians
deltaX = math.cos(pa)*MOVEMENTSPEED; deltaY = math.sin(pa)*MOVEMENTSPEED
#===============================================================# pygame init gang
pygame.init(); screen = pygame.display.set_mode(WINDOWSIZE)
pygame.display.set_caption('Python Raycast Engine 0.1')
pygame.key.set_repeat(1,0)
#===============================================================# main loop
clock = pygame.time.Clock()
while RTX == "ON":
    screen.fill(SKYCOLOR) #mr black sky
    pygame.draw.rect(screen, GROUNDCOLOR, (0, int(HEIGHT/2), WIDTH, HEIGHT)) #the ground
#===============================================================# inputs
    keys = pygame.key.get_pressed() #keybrord
    for event in pygame.event.get(): 
            if event.type == pygame.QUIT: pygame.quit(); exit() #quit the game if the lil X is done did
#==========================# movement
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a: #right
                    pa -= ROTATIONSPEED
                    if pa < .001: pa += PI*2
                    deltaX = math.cos(pa)*MOVEMENTSPEED; deltaY = math.sin(pa)*MOVEMENTSPEED
                elif event.key == pygame.K_d: #left
                    pa += ROTATIONSPEED
                    if pa > PI*2: pa -= PI*2
                    deltaX = math.cos(pa)*MOVEMENTSPEED; deltaY = math.sin(pa)*MOVEMENTSPEED
                elif event.key == pygame.K_w: py -= deltaY; px -= deltaX #forwards
                elif event.key == pygame.K_s: py += deltaY; px += deltaX #backwards
#===============================================================# ah yes, math
    ra=pa-(DR*30)+(DR*180); r=0; minimapRays=[]
    while r < RAYNUM:
        if ra < .001: ra += PI*2
        if ra > PI*2: ra -= PI*2
#==========================# horizontal raycast
        disH = math.inf; hx = px; hy = py; dof = 0; aTan = -1/math.tan(ra)
#==========================# check if facing up or down
        if ra>PI: ry=((int(py)>>6)<<6)-0.0001; rx=(py-ry)*aTan+px; yo=-64; xo=-yo*aTan #looking up
        elif ra<PI: ry=((int(py)>>6)<<6)+64; rx=(py-ry)*aTan+px; yo= 64; xo=-yo*aTan #looking down
#==========================# looptastical
        while dof<DOFMAX: 
#==========================# getting the raycast's map position
            my=int(ry)>>6; mx=(int(rx)>>6)+my
            mp=(my*mapWidth+mx)
#==========================# if the position is a wall, set le variables accordingly 
            if mp<len(worldMap) and mp > 0 and worldMap[mp]==1: dof=DOFMAX; hx=rx; hy=ry; disH = math.dist([px,py],[hx,hy])
            else: rx+=xo; ry+=yo; dof+=1
#==========================# vertical raycast
        disV = math.inf; vx = px; vy = py; dof = 0; nTan = -math.tan(ra)
#==========================# check if facing left or right
        if ra>PI2 and ra<PI3: rx=((int(px)>>6)<<6)-0.0001; ry=(px-rx)*nTan+py; xo=-64; yo=-xo*nTan #facing left
        elif ra<PI2 or ra>PI3: rx=((int(px)>>6)<<6)+64; ry=(px-rx)*nTan+py; xo= 64; yo=-xo*nTan #facing right
#==========================# looptastical x2
        while dof<DOFMAX: 
#==========================# getting the raycast's map position
            my=int(ry)>>6; mx=(int(rx)>>6)+my
            mp=(my*mapWidth+mx)
#==========================# if the position is a wall, set le variables accordingly 
            if mp<len(worldMap) and mp >= 0 and worldMap[mp]==1: dof=DOFMAX; vx=rx; vy=ry; disV = math.dist([px,py],[vx,vy])
            else: rx+=xo; ry+=yo; dof+=1
#==========================# checking which raycast was shorter
        if disV<=disH: rx=vx; ry=vy; disT=disV; wall = 0 #hit vertical wall
        else:          rx=hx; ry=hy; disT=disH; wall = 1 #hit horizontal wall
#==========================# correcting the fisheye effect
        ca=pa-ra
        if ca<0: ca+=2*PI
        if ca>2*PI: ca-=2*PI
        disTc = disT*math.cos(ca)
#==========================# fading and shading
        if VIEWDISTANCEMULTIPLIER and DODISTANCEFADE:
            fadedWallColor = [0,0,0]; m = (disT*VIEWDISTANCEMULTIPLIER); i = 0
            for color in WALLCOLOR: 
                if WALLCOLOR[i]-m>0: fadedWallColor[i]=WALLCOLOR[i]-m
                i+=1
        else: fadedWallColor = [WALLCOLOR[0],WALLCOLOR[1],WALLCOLOR[2]]
        if SHADOW and DOSHADOWS and wall==0: 
            i=0
            for color in WALLCOLOR:
                if fadedWallColor[i]-SHADOW>0: fadedWallColor[i]-=SHADOW
                else: fadedWallColor[i]=0
                i+=1
#==========================# drawing the walls
        lineH=(len(worldMap)*HEIGHT)/disTc
        if lineH > HEIGHT: lineH = HEIGHT
        lineThiccness = round(WIDTH/RAYNUM)
        if lineThiccness<1: lineThiccness=1
        lineOffset = int(HEIGHT/2-lineH/2)
        lineX = int(r*lineThiccness)
        pygame.draw.line(screen, fadedWallColor, [lineX,lineOffset],[lineX,int(lineH+lineOffset)],lineThiccness)
        #==========================# storing our juicy freshly harvested rays for the minimap
        if r%1==0: minimapRays.append([rx,ry])
#==========================# inumerating ra and r
        ra+=DR*(60/RAYNUM)
        if ra<0: ra+=2*PI
        else: ra-=2*PI
        r+=1
#==========================# drawing the minimap walls
    squareX=0; squareY=0
    for square in worldMap:
        if square==1:
            playerDist = int((math.sqrt((px - squareX*(GRIDSIZE+1))**2 + (py - squareY*(GRIDSIZE+1))**2))*VIEWDISTANCEMULTIPLIER)
            pygame.draw.rect(screen,MINIMAPCOLOR, (int((squareX*GRIDSIZE)/5)+offset, int((squareY*GRIDSIZE)/5), 13, 13))
        if squareX < mapWidth: squareX += 1
        else:
            squareX=0; squareY+=1
#==========================# drawing the rays on the minimap
    for ray in minimapRays:
        rx = ray[0]; ry = ray[1]
        pygame.draw.line(screen, RAYCOLOR, [int(px/5+offset),int(py/5)],[int(rx/5+offset),int(ry/5)],1) 
#===============================================================# updating the window and game clock
    pygame.display.flip(); clock.tick(FPS)
#===============================================================# doggo
#
#░░░░░░░░░░░▄▀▄▀▀▀▀▄▀▄░░░░░░░░░░░░░░░░░░ 
#░░░░░░░░░░░█░░░░░░░░▀▄░░░░░░▄░░░░░░░░░░ 
#░░░░░░░░░░█░░▀░░▀░░░░░▀▄▄░░█░█░░░░░░░░░ 
#░░░░░░░░░░█░▄░█▀░▄░░░░░░░▀▀░░█░░░░░░░░░ 
#░░░░░░░░░░█░░▀▀▀▀░░░░░░░░░░░░█░░░░░░░░░ 
#░░░░░░░░░░█░░░░░░░░░░░░░░░░░░█░░░░░░░░░ 
#░░░░░░░░░░█░░░░░░░░░░░░░░░░░░█░░░░░░░░░ 
#░░░░░░░░░░░█░░▄▄░░▄▄▄▄░░▄▄░░█░░░░░░░░░░ 
#░░░░░░░░░░░█░▄▀█░▄▀░░█░▄▀█░▄▀░░░░░░░░░░ 
#░░░░░░░░░░░░▀░░░▀░░░░░▀░░░▀░░░░░░░░░░░░ 
#╔═════════════════════════════════════╗
#║ * You feel like you're going to     ║
#║ have a ruff time.                   ║
#║                                     ║
#╚═════════════════════════════════════╝
#┌───────┐ ┌───────┐ ┌───────┐ ┌───────┐
#│/ FIGHT| │ ) PET | |6 ITEM | |X MERCY| 
#└───────┘ └───────┘ └───────┘ └───────┘
