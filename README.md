# RetroLang - *a 6502 CPU*

## Setup
To start a RetroLang CPU, **first create a RAM and PPU object**, then **"attach"** both of them to the **CPU** object.
```
ram = RAM()
ppu = PPU()
cpu = CPU(ram, ppu)
```
That's it!
Now, you can use the **CPU** variable to run commands.
For example:
```
cpu.lda("ff")	# Store the hex code "FF" into A register
cpu.sta("00")	# Store the A register into memory location "00"
```
Although you shouldn't need to use the **RAM variable**, you can still use some of it's debugging tools in it. **The RetroLang CPU only has 256 bytes of RAM! (255 + extra byte in the 0th place)**. That isn't a lot of memory, but remember that you have unlimited **PROM**/**ROM**.
```
ram.dumpMemory()	# Dump all memory to console (256 Values Total)
```

## Important Programmer Knowledge
RetroLib currently has **3** important classes.

**RAM** - This is your "Work Memory". You can use all 256 bytes freely.

**CPU** - This is your programs' actual brain. You call commands here.

**PPU** - This is your "Picture Processing Unit". This contains mainly screen colors.

**PPU RAM** - This is the information that will be showed on the screen.

## PPU RAM
You can edit the PPU RAM values to show different colored pixels on the screen!
The PPU has 512 bytes of RAM. Each byte represents a pixel on the screen. Depending on the value of the byte, it will show a different color.

### PPU Colors
**0** - Black

**1** - Red

**2** - Green

**3** - Yellow

**4** - Purple

**5** - Cyan

**255** - White

```


```


## CPU Commands

### The Zero Flag
**The Zero Flag is very useful!** Without it, doing math operations would be useless.
You can use the zero flag to test if the last math operation's result was a zero.
The Zero flag is set to the **number ZERO** by default. When the zero flag is "**set**", it'll be the number **1**.

For example, this program will print "Hello, World!" 10 times with the help of the zero flag.
```
def main():
	cpu.ldy(10)	# Load number 10 into A register
    cpu.jmp(loop)	# Jump to "loop()" function

def loop():
    print("Hello, World!")	# Print "Hello, World"
    cpu.dey()	# Decrement the Y register
    cpu.bne(loop)	# Branch if Not Equal to Zero ( if Z != 1 )

```

Being able to **clear** the Zero Flag is important for future operations.
```
cpu.clz()	# Clear Z Flag
```

### *.jmp()*
Jump to a "**label**"(function). Only put the function name, **not the "()"**.
```
def firstFunc():
	cpu.lda("ff")
	cpu.jmp(secondFunc)

def secondFunc():
	cpu.sta(0)

cpu.jmp()
```



### Branching
Branching is just like **.jmp()**, but uses conditions. Branching is important for making your program doing *this* if *that*.

**.bne()** - **B**ranch if **N**ot **E**qual (Branch if ZFLAG is **not** set).

**.beq()** - **B**ranch if **E**qual (Branch if ZFLAG **is** set).

```
def loadPlayerLife():
	cpu.lda(100)

# Example Branching
cpu.bne(loadPlayerLife)	# Branch if ZFLAG is not set.
cpu.beq(loadPlayerLife)	# Branch if ZFLAG is set.
```

### Incrementing & Decrementing 
You can increment and decrement the **X and Y** register. Because the **A** register is almost only used for math, it shouldn't need this feature.
```
# Increment
cpu.inx()
cpu.iny()

# Decrement
cpu.dex()
cpu.dey()
```

### *.ld_()*
**L**oa**d** data into **_** register. The data can either be a **int** or a **hex code**.
```
cpu.lda(100)
cpu.ldx(255)
cpu.ldy("ff")
```

### *.st_()*
**St**ore register into memory location. The location can be an **int** or a **hex code**.
```
cpu.sta(100)
cpu.stx("00")
cpu.sty("2E")
```

## RAM Commands

### *.dumpMemory()*
Dump memory to the console. The result should look something like this:
```
[5, 100, 30, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
```
Each **number** in memory represents a one byte in memory.

