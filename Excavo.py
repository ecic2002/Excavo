import pygame
import sys
import math
from pygame.locals import *
 
pygame.init()
vec = pygame.math.Vector2  # 2 for two dimensional

#Initialize Game Data to system defaults
#System
WIDTH = 1920
HEIGHT = 1080
SFACTOR = 1
FPS = 60
FULLSCREEN = False

#Game Data
MONEY = 100000
STONE = 100
COAL = 10
IRON = 0
SILICON = 0
QUARTZ = 0
GOLD = 0
RAREMINERAL = 0

#Planets
# #Key;MiniPlanets = ["Directory of Image", Width, Height, Orbit Radius, Speed, Trail Color, Trail Lenght, FocusMode, Name]
#For trail lenght, 2 is about half, less is longer, higher is shorter, Make sure direction and length match!
SunInfo = ["Resources/MiniPlanets/Sun.png",200,200,0,0,(0,0,0), 0, False, "Sun"]
RedPlanetInfo = ["Resources/MiniPlanets/RedPlanet.png",100,100,400,-0.5,(102,69,71), -3, False, "Red Planet"]
EmiPlanetInfo = ["Resources/MiniPlanets/EmiPlanet.png",100,100,300,-1,(200,200,200), -2, False, "Cow Planet"]
ChetoPlanetInfo = ["Resources/MiniPlanets/ChetoPlanet.png",250,250,1000,1,(200,69,71), 4, False, "Cheto Planet"]

#PlanetDescriptor
#Key;MiniPlanets = [Who It is Describing, Link to Description, BKG Color, BKG Opacity, Text Color, Active]
SunData = ["Sun","Resources/Info/Sun.txt", (137,137,137), 156, (255,255,255), True]

#DataDrawer
#Key; DataValue = [Pre Text, Variable, DefaultSize, Location X(%), Location Y(%), Text Color, Enable0, Enable1, Enable2, Enable3, Planet]
MoneyInfo = ["Money: ","MONEY", 30, 0.01, 0.01, (255,255,255), True, True, True, True, ""]

#Buttons
#Key; [Image link, Default x, Defaul y, Width, Height, Action, Enable0, Enable1, Enable2, Enable3, Planet]
MarketButtonInfo = ["Resources/Visuals/MarketLogo.png", 16, 221, 66, 66, "Toggle MARKETENABLE", True, True, True, True, "", "CornerLeft"]
SettingsButtonInfo = ["Resources/Visuals/SettingsLogo.png", 86, 221, 66, 66, "", True, True, True, True, "", "CornerLeft"]
HelpButtonInfo = ["Resources/Visuals/HelpLogo.png", 156, 221, 66, 66, "", True, True, True, True, "", "CornerLeft"]

#All Market Buy Sell Buttons
StSellInf = ["Resources/Visuals/Sell.png", -507, 170, 118, 29, "Sell Stone", True, True, True, True, "", "Center"] 
StBuyInf = ["Resources/Visuals/Buy.png", -507, 270, 118, 29, "Buy Stone", True, True, True, True, "", "Center"]
CoSellInf = ["Resources/Visuals/Sell.png", -338, 170, 118, 29, "Sell Coal", True, True, True, True, "", "Center"] 
CoBuyInf = ["Resources/Visuals/Buy.png", -338, 270, 118, 29, "Buy Coal", True, True, True, True, "", "Center"]
IrSellInf = ["Resources/Visuals/Sell.png", -170, 170, 118, 29, "Sell Iron", True, True, True, True, "", "Center"] 
IrBuyInf = ["Resources/Visuals/Buy.png", -170, 270, 118, 29, "Buy Iron", True, True, True, True, "", "Center"]
SiSellInf = ["Resources/Visuals/Sell.png", 0, 170, 118, 29, "Sell Silicon", True, True, True, True, "", "Center"] 
SiBuyInf = ["Resources/Visuals/Buy.png", 0, 270, 118, 29, "Buy Silicon", True, True, True, True, "", "Center"]
QuSellInf = ["Resources/Visuals/Sell.png", 170, 170, 118, 29, "Sell Quartz", True, True, True, True, "", "Center"] 
QuBuyInf = ["Resources/Visuals/Buy.png", 170, 270, 118, 29, "Buy Quartz", True, True, True, True, "", "Center"]
GoSellInf = ["Resources/Visuals/Sell.png", 338, 170, 118, 29, "Sell Gold", True, True, True, True, "", "Center"] 
GoBuyInf = ["Resources/Visuals/Buy.png", 338, 270, 118, 29, "Buy Gold", True, True, True, True, "", "Center"]
RMSellInf = ["Resources/Visuals/Sell.png", 507, 170, 118, 29, "Sell RareMineral", True, True, True, True, "", "Center"] 
RMBuyInf = ["Resources/Visuals/Buy.png", 507, 270, 118, 29, "Buy RareMineral", True, True, True, True, "", "Center"]



#Market Builder
SellPrices = [10, 15, 50, 110, 160, 430, 2800]
BuyPrices = [25, 35, 90, 280, 340, 880, 6300]

DefaultLocationSell = [[-507, 130],[-338, 130],[-170, 130],[0, 120],[170, 130],[338, 130],[507, 130]]
DefaultLocationBuy = [[-507, 230],[-338, 230],[-170, 230],[0, 230],[170, 230],[338, 230],[507, 230]]

#Replace Defaults with save file
    #Save File Codes

#Some Initialization code
FramePerSec = pygame.time.Clock()
EVENTRESIZE = False
CLOCK = 0
PI = math.pi
ZFACTOR = 1
OFFSET = 0.8 #Left Right planet offeset when focused
ZLOCATION = [0,0]
FOCUSACTIVE = True
MARKETENABLE = False
#Gamestate allows for porper components to be on screen, 0 for no focus, 1 for focusing, 2 for focused, 3 for defocusing
GAMESTATE = 0
EASE = 1 #Creates Smoother Trasitions
MONITOR_SIZE = [pygame.display.Info().current_w,pygame.display.Info().current_h]
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT),RESIZABLE)
pygame.display.set_caption("Space Miner")

#Font and text setup
#sysfont = pygame.font.get_default_font()
sysfont = pygame.font.get_default_font()
print('Font :', sysfont)
font = pygame.font.SysFont(None, 28)
font1 = pygame.font.Font('PressStart2P-Regular.ttf', 20)
#Depreciated
#TARGET = 0

def ActionCenter(Action):
    global MONEY
    global STONE
    global COAL
    global IRON
    global SILICON
    global QUARTZ
    global GOLD
    global RAREMINERAL
    if "Buy" in Action:
        if "Stone" in Action:
            if MONEY >= BuyPrices[0]:
                MONEY -= BuyPrices[0]
                STONE +=1
        if "Coal" in Action:
            if MONEY >= BuyPrices[1]:
                MONEY -= BuyPrices[1]
                COAL +=1
        if "Iron" in Action:
            if MONEY >= BuyPrices[2]:
                MONEY -= BuyPrices[2]
                IRON +=1
        if "Silicon" in Action:
            if MONEY >= BuyPrices[3]:
                MONEY -= BuyPrices[3]
                SILICON +=1
        if "Quartz" in Action:
            if MONEY >= BuyPrices[4]:
                MONEY -= BuyPrices[4]
                QUARTZ +=1
        if "Gold" in Action:
            if MONEY >= BuyPrices[5]:
                MONEY -= BuyPrices[5]
                GOLD +=1
        if "RareMineral" in Action:
            if MONEY >= BuyPrices[6]:
                MONEY -= BuyPrices[6]
                RAREMINERAL +=1
    elif "Sell" in Action:
        if "Stone" in Action:
            if STONE >= 1:
                MONEY += SellPrices[0]
                STONE -=1
        if "Coal" in Action:
            if COAL >= 1:
                MONEY += SellPrices[1]
                COAL -=1
        if "Iron" in Action:
            if IRON >= 1:
                MONEY += SellPrices[2]
                IRON -=1
        if "Silicon" in Action:
            if SILICON >= 1:
                MONEY += SellPrices[3]
                SILICON -=1
        if "Quartz" in Action:
            if QUARTZ >= 1:
                MONEY += SellPrices[4]
                QUARTZ -=1
        if "Gold" in Action:
            if GOLD >= 1:
                MONEY += SellPrices[5]
                GOLD -=1
        if "RareMineral" in Action:
            if RAREMINERAL >= 1:
                MONEY += SellPrices[6]
                RAREMINERAL -=1
    elif "Toggle" in Action:
        ToggleMe = Action.replace("Toggle ", "")
        if (globals()[ToggleMe]):
            globals()[ToggleMe] = False
        else: 
            globals()[ToggleMe] = True
        if ToggleMe == "MARKETENABLE":
            if MARKETENABLE:
                ClickableEntities.add(StSellBt)
                ClickableEntities.add(StBuyBt)
                ClickableEntities.add(CoSellBt)
                ClickableEntities.add(CoBuyBt)
                ClickableEntities.add(IrSellBt)
                ClickableEntities.add(IrBuyBt)
                ClickableEntities.add(SiSellBt)
                ClickableEntities.add(SiBuyBt)
                ClickableEntities.add(QuSellBt)
                ClickableEntities.add(QuBuyBt)
                ClickableEntities.add(GoSellBt)
                ClickableEntities.add(GoBuyBt)
                ClickableEntities.add(RMSellBt)
                ClickableEntities.add(RMBuyBt)
            else:
                ClickableEntities.remove(StSellBt)
                ClickableEntities.remove(StBuyBt)
                ClickableEntities.remove(CoSellBt)
                ClickableEntities.remove(CoBuyBt)
                ClickableEntities.remove(IrSellBt)
                ClickableEntities.remove(IrBuyBt)
                ClickableEntities.remove(SiSellBt)
                ClickableEntities.remove(SiBuyBt)
                ClickableEntities.remove(QuSellBt)
                ClickableEntities.remove(QuBuyBt)
                ClickableEntities.remove(GoSellBt)
                ClickableEntities.remove(GoBuyBt)
                ClickableEntities.remove(RMSellBt)
                ClickableEntities.remove(RMBuyBt)

def MarketDrawer():
    FontData3 = pygame.font.Font('PressStart2P-Regular.ttf', int(21*SFACTOR))
    for i in range(7):
        surf = FontData3.render(str(SellPrices[i]), True, (255,255,255))
        rect = surf.get_rect()
        rect.center = (int((WIDTH/2)+(DefaultLocationSell[i][0]*SFACTOR)),int((HEIGHT/2)+(DefaultLocationSell[i][1]*SFACTOR)))
        displaysurface.blit(surf, rect)
    for i in range(7):
        surf = FontData3.render(str(BuyPrices[i]), True, (255,255,255))
        rect = surf.get_rect()
        rect.center = (int((WIDTH/2)+(DefaultLocationBuy[i][0]*SFACTOR)),int((HEIGHT/2)+(DefaultLocationBuy[i][1]*SFACTOR)))
        displaysurface.blit(surf, rect)





#Object classes
class MiniPlanet(pygame.sprite.Sprite):
    def __init__(self, Info):
        super().__init__()
        self.surf = pygame.image.load(Info[0]).convert_alpha()
        self.rect = self.surf.get_rect()
        self.rect.center = (int(WIDTH/2),int(HEIGHT/2))
        self.info = Info
        #self.surf.fill((128,255,40))
    #Creates the orbits and does all of the scaling work
    def Orbit(self, Clock):
        global GAMESTATE
        global ZFACTOR
        global ZLOCATION
        global EASE
        global EVENTRESIZE
        #This allows a planet to be foucesed on, ZLOCATION acts an offset tool, The feect looks like the camera is moving, but in reality all the planets actually are
        if self.info[7]:
            if (EASE >= 1):
                ZLOCATION[0] = -(SFACTOR*ZFACTOR*self.info[3]*(math.cos(Clock*self.info[4]/360))+(SFACTOR*ZFACTOR*self.info[1]*WIDTH/HEIGHT*OFFSET))
                ZLOCATION[1] = -(SFACTOR*ZFACTOR*self.info[3]*(math.sin(Clock*self.info[4]/360)))
                #ZFACTOR = ((HEIGHT)*0.3)/(self.info[1])/SFACTOR
            else:
                EASE = (EASE + 0.001) * 1.1
                EVENTRESIZE = True
                ZLOCATION[0] = (((-(SFACTOR*(((HEIGHT)*0.3)/(self.info[1])/SFACTOR)*self.info[3]*(math.cos(Clock*self.info[4]/360))+(SFACTOR*(((HEIGHT)*0.3)/(self.info[1])/SFACTOR)*self.info[1]*WIDTH/HEIGHT*OFFSET)))*EASE)+((1-EASE)*ZLOCATION[0]))
                ZLOCATION[1] = (((-(SFACTOR*(((HEIGHT)*0.3)/(self.info[1])/SFACTOR)*self.info[3]*(math.sin(Clock*self.info[4]/360))))*EASE)+((1-EASE)*ZLOCATION[1]))
                ZFACTOR = (((((HEIGHT)*0.3)/(self.info[1])/SFACTOR)*EASE)+((1-EASE)*ZFACTOR))
        #Handles resizing the actual image
        if EVENTRESIZE:
            self.surf = pygame.image.load(self.info[0]).convert_alpha()
            self.surf = pygame.transform.smoothscale(self.surf, (int(self.info[1]*SFACTOR*ZFACTOR),int(self.info[2]*SFACTOR*ZFACTOR)))
        #Primary orbit and loaction code
        
        #Fixes collison
        self.rect = self.surf.get_rect()

        #I engineered all of this code to handle window scaling, different image size, focusing, pain,  ughhhhhhhhhhhhhhhhhhhhhhh
        self.rect.topleft = int((SFACTOR*ZFACTOR*self.info[3]*(math.cos(Clock*self.info[4]/360)))+\
                             (WIDTH/2)-\
                              (self.info[1]*SFACTOR*ZFACTOR*0.5)+\
                              ZLOCATION[0]),\
                            int((SFACTOR*ZFACTOR*self.info[3]*(math.sin(Clock*self.info[4]/360)))+\
                             (HEIGHT/2)-\
                              (self.info[2]*SFACTOR*ZFACTOR*0.5)+\
                              ZLOCATION[1])
        #Test click area size:
        #self.surf.fill((128,255,40)) #Fills in sprites with just green rectangles

        #Create the trail aroound the planets
        if (self.info[6] > 0): #Clockwise Paths
            pygame.draw.arc(displaysurface, self.info[5], [int(WIDTH/2-self.info[3]*SFACTOR*ZFACTOR+ZLOCATION[0]),int(HEIGHT/2-self.info[3]*SFACTOR*ZFACTOR+ZLOCATION[1]),int(SFACTOR*ZFACTOR*self.info[3]*2),int(SFACTOR*ZFACTOR*self.info[3]*2)], ((-1*Clock*self.info[4]/360)), ((-1*Clock*self.info[4]/360)+(PI/(self.info[6]*0.5))), int(10*SFACTOR*ZFACTOR))
            pygame.draw.arc(displaysurface, self.info[5], [int(WIDTH/2-self.info[3]*SFACTOR*ZFACTOR+ZLOCATION[0]),int(HEIGHT/2-self.info[3]*SFACTOR*ZFACTOR+ZLOCATION[1]),int(SFACTOR*ZFACTOR*self.info[3]*2),int(SFACTOR*ZFACTOR*self.info[3]*2)], ((-1*Clock*self.info[4]/360)+(PI/(self.info[6]*0.51))), ((-1*Clock*self.info[4]/360)+(PI/(self.info[6]*0.45))), int(10*SFACTOR*ZFACTOR*(2/3)))
            pygame.draw.arc(displaysurface, self.info[5], [int(WIDTH/2-self.info[3]*SFACTOR*ZFACTOR+ZLOCATION[0]),int(HEIGHT/2-self.info[3]*SFACTOR*ZFACTOR+ZLOCATION[1]),int(SFACTOR*ZFACTOR*self.info[3]*2),int(SFACTOR*ZFACTOR*self.info[3]*2)], ((-1*Clock*self.info[4]/360)+(PI/(self.info[6]*0.46))), ((-1*Clock*self.info[4]/360)+(PI/(self.info[6]*0.42))), int(10*SFACTOR*ZFACTOR*(1/3)))
        if (self.info[6] < 0): #CounterClockwise Paths
            pygame.draw.arc(displaysurface, self.info[5], [int(WIDTH/2-self.info[3]*SFACTOR*ZFACTOR+ZLOCATION[0]),int(HEIGHT/2-self.info[3]*SFACTOR*ZFACTOR+ZLOCATION[1]),int(SFACTOR*ZFACTOR*self.info[3]*2),int(SFACTOR*ZFACTOR*self.info[3]*2)], ((-1*Clock*self.info[4]/360)+(PI/(self.info[6]*0.5))), ((-1*Clock*self.info[4]/360)), int(10*SFACTOR*ZFACTOR))
            pygame.draw.arc(displaysurface, self.info[5], [int(WIDTH/2-self.info[3]*SFACTOR*ZFACTOR+ZLOCATION[0]),int(HEIGHT/2-self.info[3]*SFACTOR*ZFACTOR+ZLOCATION[1]),int(SFACTOR*ZFACTOR*self.info[3]*2),int(SFACTOR*ZFACTOR*self.info[3]*2)], ((-1*Clock*self.info[4]/360)+(PI/(self.info[6]*0.45))), ((-1*Clock*self.info[4]/360)+(PI/(self.info[6]*0.51))), int(10*SFACTOR*ZFACTOR*(2/3)))
            pygame.draw.arc(displaysurface, self.info[5], [int(WIDTH/2-self.info[3]*SFACTOR*ZFACTOR+ZLOCATION[0]),int(HEIGHT/2-self.info[3]*SFACTOR*ZFACTOR+ZLOCATION[1]),int(SFACTOR*ZFACTOR*self.info[3]*2),int(SFACTOR*ZFACTOR*self.info[3]*2)], ((-1*Clock*self.info[4]/360)+(PI/(self.info[6]*0.42))), ((-1*Clock*self.info[4]/360)+(PI/(self.info[6]*0.46))), int(10*SFACTOR*ZFACTOR*(1/3)))

        if (self.info[7] and EASE >= 1):
            GAMESTATE = 2


    #These are the defenitions for handeling focusing, mainly just change and read the variable
    def FocusToggle(self):
        if (self.info[7]):
            wself.info[7] = False
        else:
            self.info[7] = True
    def FocusSet(self, SetTo):
        self.info[7] = SetTo
    def GetFocus(self):
        return self.info[7]

    #Mirrors get_rect from pygame, this normally cannot exist outside of a class
    def get_rect_class(self):
        return [int(WIDTH/2-self.info[3]*SFACTOR*ZFACTOR+ZLOCATION[0]),int(HEIGHT/2-self.info[3]*SFACTOR*ZFACTOR+ZLOCATION[1]),int(SFACTOR*ZFACTOR*self.info[3]*2),int(SFACTOR*ZFACTOR*self.info[3]*2)]

    #Planets can be clicked on, but are not considered to be a gui
    def IsGui(self):
        return False

class Descriptor(pygame.sprite.Sprite):
    def __init__(self, Info):
        super().__init__()
        self.info = Info
        self.surf = pygame.Surface((int(WIDTH*0.5*EASE), int(50)))
        self.surf.fill(self.info[2])
        self.surf.set_alpha(self.info[3])
        self.rect = self.surf.get_rect()
        self.rect.midright = (int(WIDTH), int(HEIGHT/2))
    def Update(self):
        if GAMESTATE == 0:
            self.surf.set_alpha(0)
        elif GAMESTATE == 1:
            self.surf = pygame.Surface((int(WIDTH*0.5*(min(EASE*5,1))), int(HEIGHT * 0.9)))
            self.surf.fill(self.info[2])
            self.surf.set_alpha(self.info[3])
            self.rect = self.surf.get_rect()
            self.rect.midright = (int(WIDTH), int(HEIGHT/2))
        elif GAMESTATE == 2:
            self.surf = pygame.Surface((int(WIDTH*0.5), int(HEIGHT * 0.9)))
            self.surf.fill(self.info[2])
            self.surf.set_alpha(self.info[3])
            self.rect = self.surf.get_rect()
            self.rect.midright = (int(WIDTH), int(HEIGHT/2))
        elif GAMESTATE == 3 and EASE < 1:
            self.surf = pygame.Surface((int(WIDTH*0.5*(1-(EASE**(1/2)))), int(HEIGHT * 0.9)))
            self.surf.fill(self.info[2])
            self.surf.set_alpha(self.info[3])
            self.rect = self.surf.get_rect()
            self.rect.midright = (int(WIDTH), int(HEIGHT/2))

class TextDrawer(pygame.sprite.Sprite):
    def __init__(self, Info):
        super().__init__()
        self.info = Info
        self.surf = font1.render('Hello! Test', True, (255,255,255))
        self.rect = self.surf.get_rect()
        self.rect.center = (int(WIDTH*(3/4)), int(HEIGHT/2))
    def Update(self):
        global GAMESTATE
        global font1
        if (GAMESTATE == 0 or GAMESTATE == 1 or GAMESTATE == 3):
            self.surf = pygame.Surface((int(0),int(0)))
        elif (GAMESTATE == 2):
            self.surf = font1.render(TARGET.info[8], True, (255,255,255))
            self.rect = self.surf.get_rect()
            self.rect.center = (int(WIDTH*(3/4)), int(HEIGHT*0.2))

class DataDrawer(pygame.sprite.Sprite):
    def __init__(self, Info):
        super().__init__()
        self.info = Info
        self.surf = font1.render(' ', True, (255,255,255))
        self.rect = self.surf.get_rect()
        self.rect.center = (int(WIDTH*(self.info[2])), int(HEIGHT*(self.info[3])))
    def Update(self):
        global GAMESTATE
        FontData = pygame.font.Font('PressStart2P-Regular.ttf', int(WIDTH/(1920/self.info[2])))
        if (GAMESTATE == 0 and self.info[6]):
            self.surf = FontData.render((self.info[0]+str(globals()[self.info[1]])), True, self.info[5])
            self.rect = self.surf.get_rect()
            self.rect.topleft = (int(WIDTH*(self.info[3])), int(HEIGHT*(self.info[4])))
        elif (GAMESTATE == 1 and self.info[1]):
            self.surf = FontData.render((self.info[0]+str(globals()[self.info[1]])), True, self.info[5])
            self.rect = self.surf.get_rect()
            self.rect.topleft = (int(WIDTH*(self.info[3])), int(HEIGHT*(self.info[4])))
        elif (GAMESTATE == 2 and self.info[2]):
            self.surf = FontData.render((self.info[0]+str(globals()[self.info[1]])), True, self.info[5])
            self.rect = self.surf.get_rect()
            self.rect.topleft = (int(WIDTH*(self.info[3])), int(HEIGHT*(self.info[4])))
        elif (GAMESTATE == 3 and self.info[3]):
            self.surf = FontData.render((self.info[0]+str(globals()[self.info[1]])), True, self.info[5])
            self.rect = self.surf.get_rect()
            self.rect.topleft = (int(WIDTH*(self.info[3])), int(HEIGHT*(self.info[4])))
        else:
            self.surf = pygame.Surface((int(0),int(0)))

class MineralDraw(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = font1.render(' ', True, (255,255,255))
        self.rect = self.surf.get_rect()
        self.rect.topleft = (0, 0)
        #Setup all the surfaces
        self.surfBoxes = pygame.image.load("Resources/Visuals/BoxOverlay.png").convert_alpha()
        self.surfOverlay = pygame.image.load("Resources/Visuals/MineralsOverlay.png").convert_alpha()
        self.surfMoney = font1.render('0', True, (255,255,255))
        self.surfStone = font1.render('0', True, (255,255,255))
        self.surfCoal = font1.render('0', True, (255,255,255))
        self.surfIron = font1.render('0', True, (255,255,255))
        self.surfSilicon = font1.render('0', True, (255,255,255))
        self.surfQuartz = font1.render('0', True, (255,255,255))
        self.surfGold = font1.render('0', True, (255,255,255))
        self.surfRareMineral = font1.render('0', True, (255,255,255))

    def Update(self):
        global MONEY
        global STONE
        global COAL
        global IRON
        global SILICON
        global QUARTZ
        global GOLD
        global RAREMINERAL

        FontData2 = pygame.font.Font('PressStart2P-Regular.ttf', int(21*SFACTOR))

        self.surfMoney = FontData2.render((str(MONEY)), True, (255,255,255))
        self.surfStone = FontData2.render((str(STONE)), True, (255,255,255))
        self.surfCoal = FontData2.render((str(COAL)), True, (255,255,255))
        self.surfIron = FontData2.render((str(IRON)), True, (255,255,255))
        self.surfSilicon = FontData2.render((str(SILICON)), True, (255,255,255))
        self.surfQuartz = FontData2.render((str(QUARTZ)), True, (255,255,255))
        self.surfGold = FontData2.render((str(GOLD)), True, (255,255,255))
        self.surfRareMineral = FontData2.render((str(RAREMINERAL)), True, (255,255,255))

        self.surfBoxes = pygame.image.load("Resources/Visuals/BoxOverlay.png").convert_alpha()
        self.surfOverlay = pygame.image.load("Resources/Visuals/MineralsOverlay.png").convert_alpha()
        self.surfBoxes = pygame.transform.smoothscale(self.surfBoxes, (int(222*SFACTOR),int(218*SFACTOR)))
        self.surfOverlay = pygame.transform.smoothscale(self.surfOverlay, (int(222*SFACTOR),int(218*SFACTOR)))

        displaysurface.blit(self.surfBoxes, (0,0))
        displaysurface.blit(self.surfOverlay, (0,0))
        displaysurface.blit(self.surfMoney, (int(50*SFACTOR),int(21*SFACTOR)))
        displaysurface.blit(self.surfStone, (int(50*SFACTOR),int(46*SFACTOR)))
        displaysurface.blit(self.surfCoal, (int(50*SFACTOR),int(71*SFACTOR)))
        displaysurface.blit(self.surfIron, (int(50*SFACTOR),int(96*SFACTOR)))
        displaysurface.blit(self.surfSilicon, (int(50*SFACTOR),int(121*SFACTOR)))
        displaysurface.blit(self.surfQuartz, (int(50*SFACTOR),int(146*SFACTOR)))
        displaysurface.blit(self.surfGold, (int(50*SFACTOR),int(171*SFACTOR)))
        displaysurface.blit(self.surfRareMineral, (int(50*SFACTOR),int(196*SFACTOR)))
       
class ButtonObject(pygame.sprite.Sprite):
    def __init__(self, Info):
        super().__init__()
        self.info = Info
        self.surf = pygame.image.load(Info[0]).convert_alpha()
        self.rect = self.surf.get_rect()
        self.rect.topleft = (int(Info[1]*SFACTOR),int(Info[2]*SFACTOR))
    def Update(self):
        if self.info[11] == "CornerLeft":
            self.surf = pygame.image.load(self.info[0]).convert_alpha()
            self.surf = pygame.transform.smoothscale(self.surf, (int(self.info[3]*SFACTOR),int(self.info[4]*SFACTOR)))
            self.rect = self.surf.get_rect()
            self.rect.topleft = (int(self.info[1]*SFACTOR),int(self.info[2]*SFACTOR))
        elif self.info[11] == "Center":
            self.surf = pygame.image.load(self.info[0]).convert_alpha()
            self.surf = pygame.transform.smoothscale(self.surf, (int(self.info[3]*SFACTOR),int(self.info[4]*SFACTOR)))
            self.rect = self.surf.get_rect()
            self.rect.center = (int((WIDTH/2)+(self.info[1]*SFACTOR)),int((HEIGHT/2)+(self.info[2]*SFACTOR)))
    def IsGui(self):
        return True
    def Clicked(self):
        ActionCenter(self.info[5])

class Market(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.image.load("Resources/Visuals/Market.png").convert_alpha()
        self.rect = self.surf.get_rect()
        self.rect.center = (int((WIDTH/2)),int((HEIGHT/2)))
    def Update(self):
        self.surf = pygame.image.load("Resources/Visuals/Market.png").convert_alpha()
        self.surf = pygame.transform.smoothscale(self.surf, (int(1207*SFACTOR),int(640*SFACTOR)))
        self.rect = self.surf.get_rect()
        self.rect.center = (int((WIDTH/2)),int((HEIGHT/2)))

    def IsGui(self):
        return True
    def Clicked(self):
        print("I was clicked")

#Planets
#To add a planet create an info vairable, create an object, add that object to planet_list
Sun = MiniPlanet(SunInfo)
RedPlanet = MiniPlanet(RedPlanetInfo)
EmiPlanet = MiniPlanet(EmiPlanetInfo)
ChetoPlanet = MiniPlanet(ChetoPlanetInfo)
#Add to Planet List
planet_list = pygame.sprite.Group()
planet_list.add(Sun)
planet_list.add(RedPlanet)
planet_list.add(EmiPlanet)
planet_list.add(ChetoPlanet)

#Renderer for all non planets
SunDescriptor = Descriptor(SunData)
SunTextDrawer = TextDrawer(SunData)
MoneyDrawer = DataDrawer(MoneyInfo)
MarketButton = ButtonObject(MarketButtonInfo)
SettingsButton = ButtonObject(SettingsButtonInfo)
HelpButton = ButtonObject(HelpButtonInfo)

render_me = pygame.sprite.Group()
render_me.add(SunDescriptor)
render_me.add(SunTextDrawer)
render_me.add(MarketButton)
render_me.add(SettingsButton)
render_me.add(HelpButton)
#render_me.add(MoneyDrawer)

#All markett objects, allows easier render
MarketGUI = Market()
StSellBt = ButtonObject(StSellInf)
StBuyBt = ButtonObject(StBuyInf)
CoSellBt = ButtonObject(CoSellInf)
CoBuyBt = ButtonObject(CoBuyInf)
IrSellBt = ButtonObject(IrSellInf)
IrBuyBt = ButtonObject(IrBuyInf) 
SiSellBt = ButtonObject(SiSellInf)
SiBuyBt = ButtonObject(SiBuyInf) 
QuSellBt = ButtonObject(QuSellInf)
QuBuyBt = ButtonObject(QuBuyInf) 
GoSellBt = ButtonObject(GoSellInf)
GoBuyBt = ButtonObject(GoBuyInf) 
RMSellBt = ButtonObject(RMSellInf)
RMBuyBt = ButtonObject(RMBuyInf) 

market_render = pygame.sprite.Group()
market_render.add(MarketGUI)
market_render.add(StSellBt)
market_render.add(StBuyBt)
market_render.add(CoSellBt)
market_render.add(CoBuyBt)
market_render.add(IrSellBt)
market_render.add(IrBuyBt)
market_render.add(SiSellBt)
market_render.add(SiBuyBt)
market_render.add(QuSellBt)
market_render.add(QuBuyBt)
market_render.add(GoSellBt)
market_render.add(GoBuyBt)
market_render.add(RMSellBt)
market_render.add(RMBuyBt)


#All Objects that can be clciked on
#GUI OBJECTS MUST COME BEFORE NON GUI OBJECTS (Planets)
ClickableEntities = pygame.sprite.Group()
ClickableEntities.add(MarketButton)
ClickableEntities.add(SettingsButton)
ClickableEntities.add(HelpButton)
ClickableEntities.add(RedPlanet)
ClickableEntities.add(EmiPlanet)
ClickableEntities.add(ChetoPlanet)

MineralDrawer = MineralDraw()
#Main Game loop
while True:

    #Check focus state of each planet
    FOCUSACTIVE = False
    for entity in planet_list:
        if (entity.GetFocus()):
            FOCUSACTIVE = True
    #Handles all of the events
    for event in pygame.event.get():
        #Exit Game through x
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        #Resize The Window
        if event.type == pygame.VIDEORESIZE:
            if not FULLSCREEN:
                displaysurface = pygame.display.set_mode((event.w, event.h),RESIZABLE)
                WIDTH = event.w
                HEIGHT = event.h
                EVENTRESIZE = True

        #Keyboard Events
        if event.type == KEYDOWN:
            #Close game using ESC key
            if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            #Go into full screen using f key
            if event.key == K_f:
                FULLSCREEN = not FULLSCREEN
                if FULLSCREEN:
                    displaysurface = pygame.display.set_mode((MONITOR_SIZE), pygame.FULLSCREEN)
                    WIDTH = displaysurface.get_width()
                    HEIGHT = displaysurface.get_height()
                    EVENTRESIZE = True
                else:
                    displaysurface = pygame.display.set_mode((displaysurface.get_width(), displaysurface.get_height()),RESIZABLE)
                    WIDTH = displaysurface.get_width()
                    HEIGHT = displaysurface.get_height()
                    EVENTRESIZE = True

        #Mouse Actions
        if event.type == MOUSEBUTTONDOWN:
            #Left click action
            #This is what allows focusing between the different planets
            if (event.button == 1) & (EASE>0.2) & (CLOCK > 15):
                FOCUSADJUSTED = False
                PLANETCLICKED = False
                WASGUI = False

                ClickedObjects = pygame.sprite.Group()
                #Grabs the planet that was clicked, if it was one
                for entity in ClickableEntities:
                    if entity.rect.collidepoint(event.pos):
                        ClickedObjects.add(entity)

                #Something was Clicked On
                if ClickedObjects:
                    for entity in ClickedObjects:
                        if entity.IsGui():
                            WASGUI = True
                            entity.Clicked()
                        elif not WASGUI:
                            TARGET = entity
                    #If clicked on self
                            if (TARGET.info[7]):
                                TARGET.FocusSet(False)
                                FOCUSACTIVE = False
                                EASE = 0
                                GAMESTATE = 3
                    #If clicked on another planet
                            else:
                                for entity in planet_list:
                                    entity.FocusSet(False)
                                TARGET.FocusSet(True)
                                EASE = 0
                                FOCUSACTIVE = True
                                GAMESTATE = 1                            
                #EmptySpace was clicked
                else:
                    if FOCUSACTIVE:
                        FOCUSACTIVE = False
                        EASE = 0
                        for entity in planet_list:
                            entity.FocusSet(False)
                        GAMESTATE = 3


            #Scroll whell actions
            elif (event.button == 4) and (EASE>0.99):
                ZFACTOR += 0.2
                EVENTRESIZE = True
                ZFACTOR = max(min(ZFACTOR, 10), 0.1)
            elif (event.button == 5) and (EASE>0.99):
                ZFACTOR -= 0.2
                EVENTRESIZE = True
                ZFACTOR = max(min(ZFACTOR, 10), 0.1)
        #Sytem uses SFACTOR to determine how to scale the planets based off the window size. Everything is built for 1080p, and this value calculates how things should be scaled to work properly
        SFACTOR = displaysurface.get_width()/1920 #Scaling is just done based off the width

    #Creates bkg color        
    displaysurface.fill((21,36,60))

    #Render all the planets
    for entity in planet_list:
        entity.Orbit(CLOCK)
        displaysurface.blit(entity.surf, entity.rect)

    #Render everything else
    for entity in render_me:
        displaysurface.blit(entity.surf, entity.rect)
        entity.Update()

    if MARKETENABLE:
        for entity in market_render:
            displaysurface.blit(entity.surf, entity.rect)
            entity.Update()
        MarketDrawer()

    MineralDrawer.Update()
    #Handles clock and sprite refreshing, to help improve performance updating disables after each half second
    CLOCK += 1
    pygame.display.update()
    FramePerSec.tick(FPS)
    #The point of this code is to prevent sprite refreshing if it doesnt need to, can however sometime brake the animation system
    if (CLOCK%30 == 0):
        EVENTRESIZE = False


    #Planet focusing allows for focusing on a single planet, this returns to the defaault view if no planet is active
    if not FOCUSACTIVE:
        if (EASE >= 1):
            ZLOCATION[0] = 0
            ZLOCATION[1] = 0
            GAMESTATE = 0
        else:
            EASE = (EASE + 0.001) * 1.1
            EVENTRESIZE = True
            ZLOCATION[0] = ((EASE)+((1-EASE)*ZLOCATION[0]))-1
            ZLOCATION[1] = ((EASE)+((1-EASE)*ZLOCATION[1]))-1
            ZFACTOR = ((EASE)+((1-EASE)*ZFACTOR))
            GAMESTATE = 3

    #Rounds the Ease value, helps witrh performance
    EASE = min((int(EASE * 10000) / 10000),1)

    if EVENTRESIZE:
        WIDTH = displaysurface.get_width()
        HEIGHT = displaysurface.get_height()


    # MONEY = CLOCK*89
    # RAREMINERAL = int(23982893*math.sin(CLOCK/334))


    ## KNOWN ISSUES ##
    #Poor zooming performance
    #Zooming with scroll wheel is not super smooth
    #Trails technically off center

    #Plan
    #Setup a techtree system
    #Have different miners -  Unlocked using tech tree, increaasing with what minerals can mine
    #Buy/Sell System?
    #Mineral Machines cost minerals to get,
    #Can sell minerals for Money, variable mineral market, Randomizer and game clock?
    #