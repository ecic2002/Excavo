import pygame
import sys, os
import math
from pygame.locals import *
import random
import shelve

 
pygame.init()
vec = pygame.math.Vector2  # 2 for two dimensional

#Initialize Game Data to system defaults
#System
WIDTH = 1920
HEIGHT = 1080
SFACTOR = 1
FPS = 60
FULLSCREEN = False

#Check the reset flag
#Setting to true will ignore Reset File and force game to bbe reset
RESET = False

ResetFile = 'Reset.txt'
try:
    FlagCheck = open(ResetFile, 'r+')
    print("Reading Reset File...")
    if (FlagCheck.readline()[0] == "T"):
        RESET = True
        EntireContents = FlagCheck.read()
        FlagCheck.seek(0)
        FlagCheck.write("F")
        FlagCheck.truncate()
except:
    print("Missing or Corrupted Reset Flag!")
    print("Avoiding Game Reset")


#Start Save Game
SaveGame = "Save1"
try:
    SaveData = shelve.open(SaveGame)
except:
    print("Missing Save File")
    FlagCheck.close()
    pygame.quit()
    sys.exit()

#Handle a game reset
if RESET:
    print("Resetting The game")
    MONEY = 200
    STONE = 100
    COAL = 20
    IRON = 0
    SILICON = 0
    QUARTZ = 0
    GOLD = 0
    RAREMINERAL = 0
    ID = 1
    Miners = []
    MinerDictionary = {
    "DL" : [[100,50,20,0,0,0,0,0], [0.5, 0.1, 0.01, 0, 0, 0, 0], 30, 0],
    "DM" : [[250,60,40,10,0,0,0,0], [0.6, 0.2, 0.03, 0, 0, 0, 0], 15, 0],
    "DH" : [[500,100,60,20,0,0,0,0], [0.7, 0.2, 0.1, 0.01, 0, 0, 0], 40, 0],

    "EL" : [[1000,300,100,20,5,0,0,0], [0.2, 0.4, 0.3, 0.01, 0, 0, 0], 60, 0],
    "EM" : [[2000,400,200,40,10,0,0,0], [0.3, 0.5, 0.4, 0.02, 0.01, 0, 0], 30, 0],
    "EH" : [[4000,600,300,60,20,5,0,0], [0.2, 0.6, 0.5, 0.03, 0.02, 0, 0], 10, 0],

    "CL" : [[8000,0,0,100,120,100,0,0], [0, 0, 0.05, 0.10, 0.05, 0.01, 0], 20, 0],
    "CM" : [[12000,0,0,150,180,160,5,0], [0, 0, 0.1, 0.4, 0.2, 0.02, 0], 30, 0],
    "CH" : [[16000,0,0,300,200,200,20,40], [0, 0, 0, 0, 0, 0.04, 0.01], 30, 0],

    "RL" : [[20000,0,40,300,200,200,50,10], [0.68, 0, 0.1, 0.3, 0.2, 0.05, 0.02], 40, 0],
    "RM" : [[40000,0,40,300,200,200,50,20], [0.7, 0.05, 0.1, 0.3, 0.2, 0.05, 0.03], 20, 0],
    "RH" : [[80000,20,80,600,400,400,100,30], [1, 1, 0.2, 0.8, 0.7, 0.2, 0.04], 120, 0],
    }
else:
    #Game Data
    MONEY = SaveData['MONEY']
    STONE = SaveData['STONE']
    COAL = SaveData['COAL']
    IRON = SaveData['IRON']
    SILICON = SaveData['SILICON']
    QUARTZ = SaveData['QUARTZ']
    GOLD = SaveData['GOLD']
    RAREMINERAL = SaveData['RAREMINERAL']
    #Miner Object Lists, must be rebuilt
    ID = 1
    Miners = []
    #Dictionary with all atributes
    MinerDictionary = SaveData['MinerDictionary']
    print("No Reset, Loaded save game")


#Class need to go here so I can rebuild the Miners from Save
class Miner(pygame.sprite.Sprite):
    #Miner Attributes
    #[Miner ID (#Planet (DECR) + #Miner Class (LMH) + Number), Random Value (int 0-59)]
    #1 Cycle = 1 Second = 60 Frames
    def __init__(self, ID, Offset):
        global MinerDictionary
        super().__init__()
        self.ID = ID
        self.type = ID[0:2]
        self.offset = Offset
        self.yields = MinerDictionary[self.type][1]
        self.cycle = MinerDictionary[self.type][2]
    def Mine(self):
        global CLOCK
        global STONE
        global COAL
        global IRON
        global SILICON
        global QUARTZ
        global GOLD
        global RAREMINERAL

        if ((CLOCK+self.offset)%self.cycle == 0):
            if random.random() < self.yields[0]:
                STONE += 1
            if random.random() < self.yields[1]:
                COAL += 1
            if random.random() < self.yields[2]:
                IRON += 1
            if random.random() < self.yields[3]:
                SILICON += 1
            if random.random() < self.yields[4]:
                QUARTZ += 1
            if random.random() < self.yields[5]:
                GOLD += 1
            if random.random() < self.yields[6]:
                RAREMINERAL += 1

if not RESET:
    for t in MinerDictionary:
        for m in range(MinerDictionary[t][3]):
            MinerID = t
            MinerID += str(ID)
            ID += 1
            Miners.append(Miner(MinerID, random.randint(0,59)))

#Save and quit the game
def SaveNQuit(Save):
    if Save:
        print("Goodbye!")
        SaveData['MONEY'] = MONEY
        SaveData['STONE'] = STONE
        SaveData['COAL'] = COAL
        SaveData['IRON'] = IRON
        SaveData['SILICON'] = SILICON
        SaveData['QUARTZ'] = QUARTZ
        SaveData['GOLD'] = GOLD
        SaveData['RAREMINERAL'] = RAREMINERAL
        SaveData['MinerDictionary'] = MinerDictionary
        SaveData.close()
        FlagCheck.close()
        print("File Saved")
        pygame.quit()
        sys.exit()

#Planets
# #Key;MiniPlanets = ["Directory of Image", Width, Height, Orbit Radius, Speed, Trail Color, Trail Lenght, FocusMode, Name]
#For trail lenght, 2 is about half, less is longer, higher is shorter, Make sure direction and length match!
SunInfo = ["Resources/MiniPlanets/Sun.png",200,200,0,0,(0,0,0), 0, False, "Sun"]
DitheaPlanetInfo = ["Resources/MiniPlanets/DitheaPlanet.png",120,120,550,-0.5,(32,186,102), -3, False, "Dithea"]
EurusPlanetInfo = ["Resources/MiniPlanets/EurusPlanet.png",100,100,800,-1,(191,191,191), -2, False, "Eurus"]
CrystinePlanetInfo = ["Resources/MiniPlanets/CrystinePlanet.png",60,60,1000,1,(188,255,237), 4, False, "Crystine"]
RunothPlanetInfo = ["Resources/MiniPlanets/RunothPlanet.png",100,100,300,1,(191,46,69), 4, False, "Runoth"]

#PlanetDescriptor
#DEPRECIATED
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

IncrementBuyInf = ["Resources/Visuals/RArrow.png", -400, -100, 18, 30, "Increment MARKETMULT", True, True, True, True, "", "Center"]
DecrementBuyInf = ["Resources/Visuals/LArrow.png", -500, -100, 18, 30, "Decrement MARKETMULT", True, True, True, True, "", "Center"]

#All Miner Buy Buttons
DLBtnInf = ["Resources/Visuals/BuyMiner.png", 426, -199, 59, 29, "New Dithea T1", True, True, True, True, "Dithea", "Miner"]
DMBtnInf = ["Resources/Visuals/BuyMiner.png", 426, -76, 59, 29, "New Dithea T2", True, True, True, True, "Dithea", "Miner"]
DHBtnInf = ["Resources/Visuals/BuyMiner.png", 426, 47, 59, 29, "New Dithea T3", True, True, True, True, "Dithea", "Miner"]
ELBtnInf = ["Resources/Visuals/BuyMiner.png", 426, -199, 59, 29, "New Eurus T1", True, True, True, True, "Eurus", "Miner"]
EMBtnInf = ["Resources/Visuals/BuyMiner.png", 426, -76, 59, 29, "New Eurus T2", True, True, True, True, "Eurus", "Miner"]
EHBtnInf = ["Resources/Visuals/BuyMiner.png", 426, 47, 59, 29, "New Eurus T3", True, True, True, True, "Eurus", "Miner"]
CLBtnInf = ["Resources/Visuals/BuyMiner.png", 426, -199, 59, 29, "New Crystine T1", True, True, True, True, "Crystine", "Miner"]
CMBtnInf = ["Resources/Visuals/BuyMiner.png", 426, -76, 59, 29, "New Crystine T2", True, True, True, True, "Crystine", "Miner"]
CHBtnInf = ["Resources/Visuals/BuyMiner.png", 426, 47, 59, 29, "New Crystine T3", True, True, True, True, "Crystine", "Miner"]
RLBtnInf = ["Resources/Visuals/BuyMiner.png", 426, -199, 59, 29, "New Runoth T1", True, True, True, True, "Runoth", "Miner"]
RMBtnInf = ["Resources/Visuals/BuyMiner.png", 426, -76, 59, 29, "New Runoth T2", True, True, True, True, "Runoth", "Miner"]
RHBtnInf = ["Resources/Visuals/BuyMiner.png", 426, 47, 59, 29, "New Runoth T3", True, True, True, True, "Runoth", "Miner"]

#Market Builder
SellPrices = [2, 10, 30, 80, 100, 430, 2800]
BuyPrices = [5, 15, 60, 140, 240, 880, 6300]

DefaultLocationSell = [[-507, 110],[-338, 110],[-170, 110],[0, 110],[170, 110],[338, 110],[507, 110]]
DefaultLocationBuy = [[-507, 210],[-338, 210],[-170, 210],[0, 210],[170, 210],[338, 210],[507, 210]]

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
MARKETMULT = 1
#Gamestate allows for porper components to be on screen, 0 for no focus, 1 for focusing, 2 for focused, 3 for defocusing
GAMESTATE = 0
EASE = 1 #Creates Smoother Trasitions
MONITOR_SIZE = [pygame.display.Info().current_w,pygame.display.Info().current_h]
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT),RESIZABLE)
pygame.display.set_caption("Space Miner")

#Font and text setup
#sysfont = pygame.font.get_default_font()
sysfont = pygame.font.get_default_font()
#print('Font :', sysfont)
font = pygame.font.SysFont(None, 28)
font1 = pygame.font.Font('PressStart2P-Regular.ttf', 20)
#Depreciated
#TARGET = 0

#Main Functions
def TaskHandler(Action):
    global MONEY
    global STONE
    global COAL
    global IRON
    global SILICON
    global QUARTZ
    global GOLD
    global RAREMINERAL
    global ID
    global Miners

    if "Buy" in Action:
        if "Stone" in Action:
            if MONEY >= BuyPrices[0] * MARKETMULT:
                MONEY -= BuyPrices[0] * MARKETMULT
                STONE +=1 * MARKETMULT
                Success()
            else:
                Fail()
        if "Coal" in Action:
            if MONEY >= BuyPrices[1] * MARKETMULT:
                MONEY -= BuyPrices[1] * MARKETMULT
                COAL +=1 * MARKETMULT
                Success()
            else:
                Fail()
        if "Iron" in Action:
            if MONEY >= BuyPrices[2] * MARKETMULT:
                MONEY -= BuyPrices[2] * MARKETMULT
                IRON +=1 * MARKETMULT
                Success()
            else:
                Fail()
        if "Silicon" in Action:
            if MONEY >= BuyPrices[3] * MARKETMULT:
                MONEY -= BuyPrices[3] * MARKETMULT
                SILICON +=1 * MARKETMULT
                Success()
            else:
                Fail()
        if "Quartz" in Action:
            if MONEY >= BuyPrices[4] * MARKETMULT:
                MONEY -= BuyPrices[4] * MARKETMULT
                QUARTZ +=1 * MARKETMULT
                Success()
            else:
                Fail()
        if "Gold" in Action:
            if MONEY >= BuyPrices[5] * MARKETMULT:
                MONEY -= BuyPrices[5] * MARKETMULT
                GOLD +=1 * MARKETMULT
                Success()
            else:
                Fail()
        if "RareMineral" in Action:
            if MONEY >= BuyPrices[6] * MARKETMULT:
                MONEY -= BuyPrices[6] * MARKETMULT
                RAREMINERAL +=1 * MARKETMULT
                Success()
            else:
                Fail()
    elif "Sell" in Action:
        if "Stone" in Action:
            if STONE >= 1 * MARKETMULT:
                MONEY += SellPrices[0] * MARKETMULT
                STONE -=1 * MARKETMULT
                Success()
            else:
                Fail()
        if "Coal" in Action:
            if COAL >= 1 * MARKETMULT:
                MONEY += SellPrices[1] * MARKETMULT
                COAL -=1 * MARKETMULT
                Success()
            else:
                Fail()
        if "Iron" in Action:
            if IRON >= 1 * MARKETMULT:
                MONEY += SellPrices[2] * MARKETMULT
                IRON -=1 * MARKETMULT
                Success()
            else:
                Fail()
        if "Silicon" in Action:
            if SILICON >= 1 * MARKETMULT:
                MONEY += SellPrices[3] * MARKETMULT
                SILICON -=1 * MARKETMULT
                Success()
            else:
                Fail()
        if "Quartz" in Action:
            if QUARTZ >= 1 * MARKETMULT:
                MONEY += SellPrices[4] * MARKETMULT
                QUARTZ -=1 * MARKETMULT
                Success()
            else:
                Fail()
        if "Gold" in Action:
            if GOLD >= 1 * MARKETMULT:
                MONEY += SellPrices[5] * MARKETMULT
                GOLD -=1 * MARKETMULT
                Success()
            else:
                Fail()
        if "RareMineral" in Action:
            if RAREMINERAL >= 1 * MARKETMULT:
                MONEY += SellPrices[6] * MARKETMULT
                RAREMINERAL -=1 * MARKETMULT
                Success()
            else:
                Fail()
    elif "Toggle" in Action:
        ToggleMe = Action.replace("Toggle ", "")
        Settings()
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
                ClickableEntities.add(MarketGUI)
                ClickableEntities.add(IncrementBuyBt)
                ClickableEntities.add(DecrementBuyBt)
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
                ClickableEntities.remove(MarketGUI)
                ClickableEntities.remove(IncrementBuyBt)
                ClickableEntities.remove(DecrementBuyBt)
    elif "New" in Action:
        MinerID = ""
        if "Dithea" in Action:
            MinerID = "D"
        elif "Eurus" in Action:
            MinerID = "E"
        elif "Crystine" in Action:
            MinerID = "C"
        elif "Runoth" in Action:
            MinerID = "R"
        
        if "T1" in Action:
            MinerID += "L"
        elif "T2" in Action:
            MinerID += "M"
        elif "T3" in Action:
            MinerID += "H"
        
        if PriceChecker(MinerID):
            MinerDictionary[MinerID][3] += 1
            MinerID += str(ID)
            ID += 1
            Miners.append(Miner(MinerID, random.randint(0,59)))
            Success()
        else:
            Fail()

    elif "Increment" in Action:
        EditMe = Action.replace("Increment ", "")
        if (globals()[EditMe]<100):
            globals()[EditMe] += 1
            Settings()
        else:
            Fail()
    elif "Decrement" in Action:
        EditMe = Action.replace("Decrement ", "")
        if (globals()[EditMe]>1):
            globals()[EditMe] -= 1
            Settings()
        else:
            Fail()

def MarketDrawer():
    FontDataS = pygame.font.Font('PressStart2P-Regular.ttf', int(13*SFACTOR))
    FontDataL = pygame.font.Font('PressStart2P-Regular.ttf', int(22*SFACTOR))

    surfN = FontDataL.render(str(MARKETMULT), True, (255,255,255))
    rectN = surfN.get_rect()
    rectN.center = (int((WIDTH/2)+(-450*SFACTOR)),int((HEIGHT/2)+(-100*SFACTOR)))
    displaysurface.blit(surfN, rectN)

    for i in range(7):
        surfT = FontDataS.render("Sell " + str(MARKETMULT) + " for", True, (255,255,255))
        rectT = surfT.get_rect()
        rectT.center = (int((WIDTH/2)+(DefaultLocationSell[i][0]*SFACTOR)),int((HEIGHT/2)+(DefaultLocationSell[i][1]*SFACTOR)))
        displaysurface.blit(surfT, rectT)

        surfL = FontDataL.render("$"+str(SellPrices[i]*MARKETMULT), True, (255,255,255))
        rectL = surfL.get_rect()
        rectL.center = (int((WIDTH/2)+(DefaultLocationSell[i][0]*SFACTOR)),int((HEIGHT/2)+((DefaultLocationSell[i][1]+30)*SFACTOR)))
        displaysurface.blit(surfL, rectL)
    for i in range(7):
        surfT = FontDataS.render("Buy " + str(MARKETMULT) + " for", True, (255,255,255))
        rectT = surfT.get_rect()
        rectT.center = (int((WIDTH/2)+(DefaultLocationBuy[i][0]*SFACTOR)),int((HEIGHT/2)+(DefaultLocationBuy[i][1]*SFACTOR)))
        displaysurface.blit(surfT, rectT)

        surfL = FontDataL.render("$"+str(BuyPrices[i]*MARKETMULT), True, (255,255,255))
        rectL = surfL.get_rect()
        rectL.center = (int((WIDTH/2)+(DefaultLocationBuy[i][0]*SFACTOR)),int((HEIGHT/2)+((DefaultLocationBuy[i][1]+30)*SFACTOR)))
        displaysurface.blit(surfL, rectL)

def PriceChecker(ID):
    global MONEY
    global STONE
    global COAL
    global IRON
    global SILICON
    global QUARTZ
    global GOLD
    global RAREMINERAL

    if ((MONEY >= MinerDictionary[ID[0:2]][0][0]) and (STONE >= MinerDictionary[ID[0:2]][0][1]) and (COAL >= MinerDictionary[ID[0:2]][0][2]) and (IRON >= MinerDictionary[ID[0:2]][0][3]) and (SILICON >= MinerDictionary[ID[0:2]][0][4]) and (QUARTZ >= MinerDictionary[ID[0:2]][0][5]) and (GOLD >= MinerDictionary[ID[0:2]][0][6]) and (RAREMINERAL >= MinerDictionary[ID[0:2]][0][7])):
        MONEY -= MinerDictionary[ID[0:2]][0][0]
        STONE -= MinerDictionary[ID[0:2]][0][1]
        COAL -= MinerDictionary[ID[0:2]][0][2]
        IRON -= MinerDictionary[ID[0:2]][0][3]
        SILICON -= MinerDictionary[ID[0:2]][0][4]
        QUARTZ -= MinerDictionary[ID[0:2]][0][5]
        GOLD -= MinerDictionary[ID[0:2]][0][6]
        RAREMINERAL -= MinerDictionary[ID[0:2]][0][7]
        
        return True 
    else:
        return False

def Success():
    #Play + sound
    print("Action Success")

def Fail():
    #Play fail sound
    print("Action Fail")

def Settings():
    print("Action Occured")

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
        #This allows a planet to be foucesed on, ZLOCATION acts an offset tool, The effect looks like the camera is moving, but in reality all the planets actually are
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
            self.info[7] = False
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
    def __init__(self):
        super().__init__()
        self.surf = font1.render('Hello! Test', True, (255,255,255))
        self.rect = self.surf.get_rect()
        self.rect.center = (int(WIDTH*(3/4)), int(HEIGHT/2))
    def Update(self):
        global GAMESTATE
        global font1
        if (GAMESTATE == 0 or GAMESTATE == 1 or GAMESTATE == 3):
            self.surf = pygame.Surface((int(0),int(0)))
        elif (GAMESTATE == 2):
            self.surf = pygame.Surface((int(0),int(0)))
            if (TARGET.info[8] == "Dithea"):
                DitheaButtons.Update()
            elif (TARGET.info[8] == "Eurus"):
                EurusButtons.Update()
            elif (TARGET.info[8] == "Crystine"):
                CrystineButtons.Update()
            elif (TARGET.info[8] == "Runoth"):
                RunothButtons.Update()

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
        elif self.info[11] == "Miner":
            if (GAMESTATE == 2) and (TARGET.info[8] == self.info[10]):
                self.surf = pygame.image.load(self.info[0]).convert()
                self.surf = pygame.transform.smoothscale(self.surf, (int(self.info[3]*SFACTOR),int(self.info[4]*SFACTOR)))
                self.rect = self.surf.get_rect()
                self.rect.center = (int((WIDTH/2)+(self.info[1]*SFACTOR)),int((HEIGHT/2)+(self.info[2]*SFACTOR)))
            else:
                self.rect.center = (-2000,-2000)
            # Hide
    def IsGui(self):
        return True
    def Clicked(self):
        TaskHandler(self.info[5])

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
        pass

class MinerSellButtons(pygame.sprite.Sprite):
    def __init__(self, PlanetID):
        super().__init__()
        self.id = PlanetID
        self.Imgsurf = pygame.image.load("Resources/Visuals/" + self.id + "Menu.png").convert_alpha()
    def Update(self):
        if (True):
            global MinerDictionary
            OffsetsPurchase = [-50, 16, 79, 139, 196, 262, 330, 396]
            OffsetsYield = [16, 79, 139, 196, 262, 330, 396]
            OffsetSeperate = [-199, -76, 47]
            Classes = ["L","M","H"]
            fontMenu = pygame.font.Font('PressStart2P-Regular.ttf', int(14*SFACTOR) )
            Imgsurf = self.Imgsurf
            Imgsurf = pygame.transform.smoothscale(Imgsurf, (int(1920*SFACTOR),int(1080*SFACTOR)))
            Imgrect = Imgsurf.get_rect()
            Imgrect.center = (int((WIDTH/2)),int((HEIGHT/2)))
            displaysurface.blit(Imgsurf, Imgrect)

            for v in range(len(OffsetSeperate)):
                CurrentData = MinerDictionary[(self.id+Classes[v])]

                #Cycle
                Cyclesurf = fontMenu.render(str((60/CurrentData[2]))+"/s", True, (255,255,255))
                Cyclerect = Cyclesurf.get_rect()
                Cyclerect.center = (int(WIDTH*(3/4)+(-170*SFACTOR)), int((HEIGHT*0.5)+((-27+OffsetSeperate[v])*SFACTOR)))
                displaysurface.blit(Cyclesurf, Cyclerect)

                #Owned
                Ownedsurf = fontMenu.render(str(CurrentData[3]), True, (255,255,255))
                Ownedrect = Ownedsurf.get_rect()
                Ownedrect.center = (int(WIDTH*(3/4)+(-200*SFACTOR)), int((HEIGHT*0.5)+((5+OffsetSeperate[v])*SFACTOR)))
                displaysurface.blit(Ownedsurf, Ownedrect)

                #Buy Button


                #Purchase
                for p in range(len(OffsetsPurchase)):
                    surf = fontMenu.render(str(CurrentData[0][p]), True, (255,255,255))
                    rect = surf.get_rect()
                    rect.center = (int(WIDTH*(3/4)+(OffsetsPurchase[p]*SFACTOR)), int((HEIGHT*0.5)+((-27+OffsetSeperate[v])*SFACTOR)))
                    displaysurface.blit(surf, rect)

                #Yields
                for y in range(len(OffsetsYield)):
                    surf = fontMenu.render(str(int(CurrentData[1][y]*100))+"%", True, (255,255,255))
                    rect = surf.get_rect()
                    rect.center = (int(WIDTH*(3/4)+(OffsetsYield[y]*SFACTOR)), int((HEIGHT*0.5)+(OffsetSeperate[v]*SFACTOR)))
                    displaysurface.blit(surf, rect)
    def IsGui(self):
        return True
    def Clicked(self):
        TaskHandler(self.info[5])
                

#Planets
#To add a planet create an info vairable, create an object, add that object to planet_list
Sun = MiniPlanet(SunInfo)
DitheaPlanet = MiniPlanet(DitheaPlanetInfo)
EurusPlanet = MiniPlanet(EurusPlanetInfo)
CrystinePlanet = MiniPlanet(CrystinePlanetInfo)
RunothPlanet = MiniPlanet(RunothPlanetInfo)

#Add to Planet List
planet_list = pygame.sprite.Group()
planet_list.add(Sun)
planet_list.add(DitheaPlanet)
planet_list.add(EurusPlanet)
planet_list.add(CrystinePlanet)
planet_list.add(RunothPlanet)

#Renderer for all non planets
SunDescriptor = Descriptor(SunData)
SunTextDrawer = TextDrawer()
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
IncrementBuyBt = ButtonObject(IncrementBuyInf)
DecrementBuyBt = ButtonObject(DecrementBuyInf)

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
market_render.add(IncrementBuyBt)
market_render.add(DecrementBuyBt)

#All Miners
DLBtn = ButtonObject(DLBtnInf)
DMBtn = ButtonObject(DMBtnInf)
DHBtn = ButtonObject(DHBtnInf)
ELBtn = ButtonObject(ELBtnInf)
EMBtn = ButtonObject(EMBtnInf)
EHBtn = ButtonObject(EHBtnInf)
CLBtn = ButtonObject(CLBtnInf)
CMBtn = ButtonObject(CMBtnInf)
CHBtn = ButtonObject(CHBtnInf)
RLBtn = ButtonObject(RLBtnInf)
RMBtn = ButtonObject(RMBtnInf)
RHBtn = ButtonObject(RHBtnInf)

render_me.add(DLBtn)
render_me.add(DMBtn)
render_me.add(DHBtn)
render_me.add(ELBtn)
render_me.add(EMBtn)
render_me.add(EHBtn)
render_me.add(CLBtn)
render_me.add(CMBtn)
render_me.add(CHBtn)
render_me.add(RLBtn)
render_me.add(RMBtn)
render_me.add(RHBtn)

#Miner Purchase Buttons and Such
DitheaButtons = MinerSellButtons("D")
EurusButtons = MinerSellButtons("E")
CrystineButtons = MinerSellButtons("C")
RunothButtons = MinerSellButtons("R")

#All Objects that can be clciked on
#GUI OBJECTS MUST COME BEFORE NON GUI OBJECTS (Planets)
ClickableEntities = pygame.sprite.Group()
ClickableEntities.add(MarketButton)
ClickableEntities.add(SettingsButton)
ClickableEntities.add(HelpButton)
ClickableEntities.add(DitheaPlanet)
ClickableEntities.add(EurusPlanet)
ClickableEntities.add(CrystinePlanet)
ClickableEntities.add(RunothPlanet)

#All Miner Buy Buttons
ClickableEntities.add(DLBtn)
ClickableEntities.add(DMBtn)
ClickableEntities.add(DHBtn)
ClickableEntities.add(ELBtn)
ClickableEntities.add(EMBtn)
ClickableEntities.add(EHBtn)
ClickableEntities.add(CLBtn)
ClickableEntities.add(CMBtn)
ClickableEntities.add(CHBtn)
ClickableEntities.add(RLBtn)
ClickableEntities.add(RMBtn)
ClickableEntities.add(RHBtn)


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
            SaveNQuit(True)

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
                if MARKETENABLE:
                    TaskHandler("Toggle MARKETENABLE")
                elif FOCUSACTIVE:
                    TARGET.FocusSet(False)
                    FOCUSACTIVE = False
                    EASE = 0
                    GAMESTATE = 3
                else:
                    SaveNQuit(True)  
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
                    if not WASGUI:
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
                    if FOCUSACTIVE and not WASGUI:
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

    for mObject in Miners:
        mObject.Mine()

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

    #Uncomment for FPS counter
    #print(str(int(FramePerSec.get_fps())))

    # MONEY = CLOCK*89
    # RAREMINERAL = int(23982893*math.sin(CLOCK/334))


    ## KNOWN ISSUES ##
    #Poor zooming performance
    #Zooming with scroll wheel is not super smooth
    #Trails technically off center
