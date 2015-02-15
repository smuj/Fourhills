import sys,os

MUSIC = False

if MUSIC:
    import musicpd

def cls():
    os.system(['clear','cls'][os.name == 'nt'])

TEXT_SEPARATOR_MAJOR = "\n===============================================\n"
TEXT_SEPARATOR_MINOR = "\n-----------------------------------------------\n"

CHARACTER_DESIGNATOR = "C"
LOCATION_DESIGNATOR = "L"
BATTLE_DESIGNATOR = "B"
QUIT_DESIGNATOR = "Q"

class Location:
    """Represents a location or settlement"""
    def __init__(self,name,description,battlescreen,playlistname):
        #name and description of location
        self.name = name
        self.description = description
        #what should be printed if a battle happens at this location
        if battlescreen == "":
            self.battlescreen = "No battle screen set up here"
        else:
            self.battlescreen = battlescreen
        #the position of the music file in the playlist that should play when we're at this location
        self.playlistname = playlistname
        #will contain a list of characters
        self.characters = []
        #will contain a list of locations navigatable from here. The "parent" will end up in index 0.
        self.children = []
        #whether this location has had its parent set yet
        self.parentSet = False
    def AddCharacter(self,character):
        #add a character to the end of the list
        self.characters.append(character)
    def AddChild(self,loc):
        #add a child to the list, and set its parent to this location
        self.children.append(loc)
        loc.SetParent(self)
    def SetParent(self,parent):
        if self.parentSet:
            raise Exception("Parent already set")
        self.children.insert(0,parent)
        self.parentSet = True
    def ToString(self):
        return self.name + TEXT_SEPARATOR_MAJOR + self.description

class Character:
    """Represents an character"""
    def __init__(self,name,text):
        self.name=name
        self.text=text
    def ToString(self):
        return self.name + TEXT_SEPARATOR_MAJOR + self.text

class LocationHandler:
    """Allows naviation through settlements and locations"""
    def __init__(self,startLoc):
        self.loc = startLoc
    def move(self,index):
        self.loc = self.loc.children[index]
    def ShowLocations(self):
        print(self.loc.ToString()+TEXT_SEPARATOR_MINOR)
        print("NPCs:")
        NPCrange = range(len(self.loc.characters))
        locrange = range(len(self.loc.children))
        for j in NPCrange:
            print(CHARACTER_DESIGNATOR,j,". ",self.loc.characters[j].name, sep='')
        print("Options:")
        for i in locrange:
            print(LOCATION_DESIGNATOR,i,". ",self.loc.children[i].name, sep='')
            
        return (NPCrange,locrange)

class SoundWrapper:
    """Wrapper for musicpd"""
    def __init__(self):
        self.client = musicpd.MPDClient()
        #stores current playlist name
        self.currentPlaylistName = "None"
    def setLoc(self,loc):
        #don't do anything if the playlist is the same
        if loc.playlistname != self.currentPlaylistName:
            self.currentPlaylistName=loc.playlistname
            self.client.connect('localhost',6600)
            self.client.stop()
            if loc.playlistname != "None":
                self.client.clear()
                self.client.load(loc.playlistname)
                self.client.play()
            self.client.close()
            self.client.disconnect()

def loadCharacter(filename):
    state = "Begin"
    charname = "Not Defined"
    chardescription = ""
    with open(filename,'r') as f:
        for line in f:
            if state == "Begin":
                lineparts = line.rstrip().split(":")
                if lineparts[0]=="##NAME":
                    charname = lineparts[1]
                    state = "GotNameTag"
            elif state =="GotNameTag":
                if line.rstrip()=="##DESCRIPTION":
                    state  = "GotDescriptionTag"
            elif state =="GotDescriptionTag":
                if line.rstrip() == "##END":
                    break
                else:
                    chardescription = chardescription+line
    return Character(charname,chardescription)

#this could do with some validation, plus tidying up a bit
def loadLocation(filename):
    state = "Begin"
    locname = "Not defined"
    locplaylistname = "Not defined"
    locdescription = ""
    locbattlescreen = ""
    with open(filename,'r') as f:
        for line in f:
            if state == "Begin":
                lineparts = line.rstrip().split(":")
                if lineparts[0]=="##NAME":
                    locname = lineparts[1]
                    state = "GotNameTag"
            elif state == "GotNameTag":
                lineparts = line.rstrip().split(":")
                if lineparts[0]=="##PLAYLISTNAME":
                    locplaylistname = lineparts[1]
                    state = "GotPlaylistTag"
            elif state == "GotPlaylistTag":
                if line.rstrip() == "##DESCRIPTION":
                    state = "GotDescriptionTag"
            elif state == "GotDescriptionTag":
                if line.rstrip() == "##BATTLESCREEN":
                    state = "GotBattlescreenTag"
                else:
                    locdescription = locdescription + line
            elif state == "GotBattlescreenTag":
                if line.rstrip() == "##END":
                    break
                else:
                    locbattlescreen = locbattlescreen + line
    return Location(locname,locdescription,locbattlescreen,locplaylistname)

def LoadWorld(path = 'World',parent = None):
    #if this is the first function call, we need to create the top-level world location
    if parent is None:
        parent = Location('World','Top-level world','None','BleakWilderness')
        #the top-level world's parent should be itself
        parent.SetParent(parent)
    #get list of files and subdirectories
    dirListing = os.listdir(path)
    #extract a list of subdirectories
    subDirs = [d for d in dirListing if os.path.isdir(os.path.join(path,d))]
    #extract a list of files
    files = [f for f in dirListing if os.path.isfile(os.path.join(path,f))]
    #from the file list, extract lists of character files and location files
    chaFiles = [f for f in files if os.path.splitext(f)[1].lower()=='.cha']
    locFiles = [f for f in files if os.path.splitext(f)[1].lower()=='.loc']
    #load the character files and add them to the parent
    for characterFile in chaFiles:
        parent.AddCharacter(loadCharacter(os.path.join(path,characterFile)))
    for locationFile in locFiles:
        thisLoc = loadLocation(os.path.join(path,locationFile))
        #load location files and add them to the parent
        parent.AddChild(thisLoc)
        #get the name of the file without the extensions
        locFileName = os.path.splitext(locationFile)[0]
        #see if there is a subdirectory with the same name - if so, recurse into it
        if locFileName in subDirs:
            LoadWorld(os.path.join(path,locFileName),parent = thisLoc)
    return parent

World = LoadWorld()

#Set initial location
glh = LocationHandler(World)

if MUSIC:
    #set up the playlist handler
    gsw = SoundWrapper()
    #start the first song playing
    gsw.setLoc(glh.loc)

#Main loop
quit = False
while quit == False:
    #clear the screen
    cls()
    #display the NPCs and locations, and get the ranges of the possible commands
    (NPCrange,locrange) = glh.ShowLocations()

    #whether the user has yet entered a valid input
    validInput = False
    #used to store what action the user makes
    actionType = ""
    #used to store any numbers associated with the action
    actionNumber = 0

    #keep going until the user enters valid input
    #this would ideally be in a function or something
    while validInput == False:
        #get input from the user and convert to uppercase
        cmd = input(">").upper()
        #if there's nothing at all, just ask again
        if len(cmd) == 0:
            continue
        #if it's length 1, its either battle or quit
        elif len(cmd) == 1:
            if cmd == BATTLE_DESIGNATOR:
                actionType = "Battle"
                validInput = True
            elif cmd == QUIT_DESIGNATOR:
                actionType = "Quit"
                validInput = True
            else:
                print("Invalid command")
        else:
            #if it's longer than 1, try and grab the integer after the letter
            try:
                actionNumber = int(cmd[1:])
                #if that worked, see whether it was a character or location
                if cmd[0]==CHARACTER_DESIGNATOR:
                    actionType = "Character"
                    #check it's within range
                    if actionNumber in NPCrange:
                        validInput = True
                    else:
                        print("Invalid character number")
                elif cmd[0] == LOCATION_DESIGNATOR:
                    actionType = "Location"
                    if actionNumber in locrange:
                        validInput = True
                    else:
                        print("Invalid location number")
                else:
                    print("Invalid command")
            except ValueError:
                #if the integer didn't make sense, print and keep asking
                print("Invalid number")

    #we've got a valid command now
    if actionType == "Quit":
        print("Quitting")
        quit = True
    elif actionType == "Battle":
        cls()
        print("Battle",TEXT_SEPARATOR_MAJOR,glh.loc.battlescreen)
        input("Press enter to exit battle")
    elif actionType == "Character":
        cls()
        print("Character description",TEXT_SEPARATOR_MAJOR,glh.loc.characters[actionNumber].ToString())
        input("Press enter to exit character description")
    elif actionType == "Location":
        glh.move(actionNumber)
        if MUSIC:
            gsw.setLoc(glh.loc)
    else:
        print("Error - actionType was unknown value. Accidental modification to code?")
        input("Press enter to continue")

