#
#   ~~ RETROLANG ~~
#   A 6502 Processor
#      for Python
#
#   By: CodeShady

### RAM CLASS ###
class RAM:
    def __init__(self):
        self.PPU = PPU()
        self.MEM = []

        self.MEMORY_RANGE = 768
        # Load Zeros Into Memory
        [ self.MEM.append(0) for x in range(self.MEMORY_RANGE) ]

    def dumpMemory(self):
        lineBreakPoint = 10
        lineCount = 0
        lineNumber = 0

        print("\033[1;33m" + hex(lineNumber) + "\033[0m\t", end="")
        for byte in self.MEM:
            if lineCount >= lineBreakPoint:
                lineNumber += 10
                print("\n\033[1;33m" + hex(lineNumber) + "\033[0m\t", end="")
                lineCount = 0
            
            if len(hex(byte)) == 3:
                print(hex(byte)[2:] + "0", end=", ")
            else:
                print(hex(byte)[2:], end=", ")

            lineCount += 1
        print("")


### CPU CLASS ###
class CPU:
    # TODO: [X] Create PPU Class (For displaying Ascii art to console)
    # TODO: [ ] Create STACK Class (For adding variables to "The Stack")
    # TODO: [X] Rework the LDA & STA functions (AKA, remove the lfm() function).

    def __init__(self, memory, ppu):
        self.RAM = memory
        self.PPU = ppu
        self.A = 0
        self.X = 0
        self.Y = 0
        self.ZFLAG = 0
    
    ## COMMANDS ##
    def _realValue(self, value):
        # If char is "#$__" use HEX
        firstChar = value[:1]
        secondChar = value[1:2]
        
        if firstChar == "#":
            # Value is a NUMBER
            if secondChar == "$":
                # Retrun HEX VALUE
                hexNum = self.hex(value[2:])
                if hexNum > 255:
                    hexNum = 255
                return abs(hexNum)
            elif str.isnumeric(value[1:]):
                # Return DECIMAL VALUE
                return value[1:]
            elif secondChar == "%":
                # Return BINARY VALUE
                binNum = self.binary(value[2:])
                if binNum > 255:
                    binNum = 255
                return abs(binNum)

        elif firstChar == "$":
            # Value is HEX (GET MEMORY)
            value = self.hex(value[1:])
            memoryLength = len(self.RAM.MEM)-1
            if value > memoryLength:
                value = memoryLength
            return self.RAM.MEM[abs(value)]
        elif firstChar == "%":
            # Value is BINARY (GET MEMORY)
            value = self.binary(value[1:])
            memoryLength = len(self.RAM.MEM)
            if value > memoryLength:
                value = memoryLength
            return self.RAM.MEM[abs(value)]

        self._bug("Trying to load an unknown int into register.")
    def _bug(self, message):
        print("\033[41m[ERROR]\033[0m " + str(message))
    def _maxMemoryNum(self, char):
        if isinstance(char, str):
            char = int(char, 16) # Char is a string
        char = abs(char)
        if char > 767:
            char = 767
        return char
    def dumpRegisters(self):
        print("A = " + str(self.A))
        print("X = " + str(self.X))
        print("Y = " + str(self.Y))
        print("Z = " + str(self.ZFLAG))
    def hex(self, string):
        if isinstance(string, str):
            return int(string, 16)
        self._bug("Trying to convert a non-HEX value.")
    def binary(self, string):
        if isinstance(string, str):
            return int(string, 2)
        self._bug("Trying to convert a non-BINARY value.")
    def maxByteNum(self, char):
        if isinstance(char, str):
            char = int(char, 16) # Char is a string
        char = abs(char)
        if char > 255:
            char = 255
        return char

    ## DISPLAY PPU ##
    def display(self):
        # Send memory to PPU to display to console
        memory = self.RAM.MEM[256:]
        self.PPU.display(memory)

    ## ZFLAG ##
    def clz(self):
        # Clear the Z-FLAG
        self.ZFLAG = 0

    ## COMPARING A,X,Y ##
    def cmp(self, number):
        if self.A == self.maxByteNum(number):
            self.ZFLAG = 1
        else:
            self.ZFLAG = 0
    def cpx(self, number):
        if self.X == self.maxByteNum(number):
            self.ZFLAG = 1
        else:
            self.ZFLAG = 0
    def cpy(self, number):
        if self.Y == self.maxByteNum(number):
            self.ZFLAG = 1
        else:
            self.ZFLAG = 0

    ## TRANSFERRING A,X,Y ##
    def tax(self):
        self.X = self.A
    def tay(self):
        self.Y = self.A
    def txa(self):
        self.A = self.X
    def tya(self):
        self.A = self.Y

    ## JUMPING ##
    def jmp(self, labelName):
        labelName()

    ## BRANCHING ##
    def bne(self, labelName):
        if self.ZFLAG != 1:
            labelName()
    def beq(self, labelName):
        if self.ZFLAG == 1:
            labelName()

    ## DE-X,Y ##
    def dex(self):
        self.X -= 1
        if self.X == 0:
            self.ZFLAG = 1
        if self.X < 0:
            self.X = 255
    def dey(self):
        self.Y -= 1
        if self.Y == 0:
            self.ZFLAG = 1
        if self.Y < 0:
            self.Y = 255

    ## IN-X,Y ##
    def iny(self):
        self.Y += 1
        if self.Y > 255:
            self.ZFLAG = 1
            self.Y = 0
    def inx(self):
        self.X += 1
        if self.X > 255:
            self.ZFLAG = 1
            self.X = 0
    
    ## LD-A,X,Y ##
    def lda(self, char):
        self.A = int(self._realValue(char))
    def ldx(self, char):
        self.X = int(self._realValue(char))
    def ldy(self, char):
        self.Y = int(self._realValue(char))

    ## ST-A,X,Y ##
    def sta(self, location):
        self.RAM.MEM[self._maxMemoryNum(location)] = self.A
    def stx(self, location):
        self.RAM.MEM[self._maxMemoryNum(location)] = self.X
    def sty(self, location):
        self.RAM.MEM[self._maxMemoryNum(location)] = self.Y


## PICTURE PROCESSING UNIT ##
class PPU:
    def __init__(self):
        self.SCREEN_WIDTH = 32
        self.COLORS = {
            0: self.BLACK_BACKGROUND,
            1: self.RED_BACKGROUND,
            2: self.GREEN_BACKGROUND,
            3: self.YELLOW_BACKGROUND,
            4: self.PURPLE_BACKGROUND,
            5: self.CYAN_BACKGROUND,
            255: self.WHITE_BACKGROUND,
        }

    def display(self, MEMORY):
        counter = 0
        for byte in MEMORY:
            if counter == self.SCREEN_WIDTH:
                print(self.RESET + "")
                counter = 0
            print(self.COLORS[byte] + " ", end=" ")
            counter += 1
        print(self.RESET)

	# Reset
    RESET = "\033[0m";  # Text Reset

    # Regular Colors
    BLACK = "\033[0;30m";   # BLACK
    RED = "\033[0;31m";     # RED
    GREEN = "\033[0;32m";   # GREEN
    YELLOW = "\033[0;33m";  # YELLOW
    BLUE = "\033[0;34m";    # BLUE
    PURPLE = "\033[0;35m";  # PURPLE
    CYAN = "\033[0;36m";    # CYAN
    WHITE = "\033[0;37m";   # WHITE

    # Bold
    BLACK_BOLD = "\033[1;30m";  # BLACK
    RED_BOLD = "\033[1;31m";    # RED
    GREEN_BOLD = "\033[1;32m";  # GREEN
    YELLOW_BOLD = "\033[1;33m"; # YELLOW
    BLUE_BOLD = "\033[1;34m";   # BLUE
    PURPLE_BOLD = "\033[1;35m"; # PURPLE
    CYAN_BOLD = "\033[1;36m";   # CYAN
    WHITE_BOLD = "\033[1;37m";  # WHITE

    # Underline
    BLACK_UNDERLINED = "\033[4;30m";  # BLACK
    RED_UNDERLINED = "\033[4;31m";    # RED
    GREEN_UNDERLINED = "\033[4;32m";  # GREEN
    YELLOW_UNDERLINED = "\033[4;33m"; # YELLOW
    BLUE_UNDERLINED = "\033[4;34m";   # BLUE
    PURPLE_UNDERLINED = "\033[4;35m"; # PURPLE
    CYAN_UNDERLINED = "\033[4;36m";   # CYAN
    WHITE_UNDERLINED = "\033[4;37m";  # WHITE

    # Background
    BLACK_BACKGROUND = "\033[40m";  # BLACK
    RED_BACKGROUND = "\033[41m";    # RED
    GREEN_BACKGROUND = "\033[42m";  # GREEN
    YELLOW_BACKGROUND = "\033[43m"; # YELLOW
    BLUE_BACKGROUND = "\033[44m";   # BLUE
    PURPLE_BACKGROUND = "\033[45m"; # PURPLE
    CYAN_BACKGROUND = "\033[46m";   # CYAN
    WHITE_BACKGROUND = "\033[47m";  # WHITE

    # High Intensity
    BLACK_BRIGHT = "\033[0;90m";  # BLACK
    RED_BRIGHT = "\033[0;91m";    # RED
    GREEN_BRIGHT = "\033[0;92m";  # GREEN
    YELLOW_BRIGHT = "\033[0;93m"; # YELLOW
    BLUE_BRIGHT = "\033[0;94m";   # BLUE
    PURPLE_BRIGHT = "\033[0;95m"; # PURPLE
    CYAN_BRIGHT = "\033[0;96m";   # CYAN
    WHITE_BRIGHT = "\033[0;97m";  # WHITE

    # Bold High Intensity
    BLACK_BOLD_BRIGHT = "\033[1;90m"; # BLACK
    RED_BOLD_BRIGHT = "\033[1;91m";   # RED
    GREEN_BOLD_BRIGHT = "\033[1;92m"; # GREEN
    YELLOW_BOLD_BRIGHT = "\033[1;93m";# YELLOW
    BLUE_BOLD_BRIGHT = "\033[1;94m";  # BLUE
    PURPLE_BOLD_BRIGHT = "\033[1;95m";# PURPLE
    CYAN_BOLD_BRIGHT = "\033[1;96m";  # CYAN
    WHITE_BOLD_BRIGHT = "\033[1;97m"; # WHITE

    # High Intensity backgrounds
    BLACK_BACKGROUND_BRIGHT = "\033[0;100m";# BLACK
    RED_BACKGROUND_BRIGHT = "\033[0;101m";# RED
    GREEN_BACKGROUND_BRIGHT = "\033[0;102m";# GREEN
    YELLOW_BACKGROUND_BRIGHT = "\033[0;103m";# YELLOW
    BLUE_BACKGROUND_BRIGHT = "\033[0;104m";# BLUE
    PURPLE_BACKGROUND_BRIGHT = "\033[0;105m"; # PURPLE
    CYAN_BACKGROUND_BRIGHT = "\033[0;106m";  # CYAN
    WHITE_BACKGROUND_BRIGHT = "\033[0;107m";   # WHITE