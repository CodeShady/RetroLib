# RetroLib - *a 6502 CPU*

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
Although you shouldn't need to use the **RAM variable**, you can still use some of it's debugging tools in it. **The "Working RAM" only has 256 bytes of RAM! (255 + extra byte in the 0th place)**. That isn't a lot of memory, but remember that you have unlimited **PROM**/**ROM**.
```
ram.dumpMemory()	# Dump all memory to console (768 Values Total)
```

## Important Programmer Knowledge
RetroLib currently has **3** important classes.

**RAM** - This is your "Work Memory". You can use all 256 bytes freely.

**CPU** - This is your programs' actual brain. You call commands here.

**PPU** - This is your "Picture Processing Unit". This contains mainly colors.

**PPU RAM** - Each byte represents a pixel on the screen in the PPU RAM.

## Random-Access Memory (RAM)

## Work RAM
As the programmer, you get 256 bytes in memory called "Work RAM". Work RAM is free to use. You can save important data here (Player's health, Level names, Player's X and Y position).

**Work RAM start's at: $00**, and ends at **$FF**.

## PPU RAM
Unlike the Work RAM, the PPU RAM isn't for storing important information. You can use the PPU RAM to draw on the screen--it's pretty easy.

The PPU has 512 bytes of RAM. Each byte represents a pixel on the screen. Depending on the value of the byte, it will show a different color.

Each time ``cpu.display()`` is called, the PPU will reach each byte in the PPU RAM, then it'll display each pixel to the screen.

**The PPU RAM start's at: $00**, and ends at **$FF**.


### Showing RAM - *.dumpMemory()*
To view all the data in the program's memory. Use this command.

The result should look something like this:
```
0x0		00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 
0xa		00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 
0x14		00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 
0x1e		00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 
0x28		00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 
0x32		00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 
0x3c		00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 
0x46		00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 
0x50		00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 
0x5a		00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 
0x64		00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 
0x6e		00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 
0x78		00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 
0x82		00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 
0x8c		00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 
0x96		00, 00, 00, 00, 00, 00, 00, 00, 00, 00,
```
Each **number** in memory represents a one byte in memory.


## Writing To The Display


### PPU Colors
**0** - Black

**1** - Red

**2** - Green

**3** - Yellow

**4** - Purple

**5** - Cyan

**255** - White


------------

For example, let's display red onto the first pixel of the screen.
```
cpu.lda(1)	# Load number 2(red) into A register
cpu.sta("100")	# Store A register into memory location $100 ("$" means hex)

cpu.display()	# Turn on the screen
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

`cpu.beq()` - Branch if zero flag is set to 1.**( Z = 1 )**
`cpu.bne()` - Branch if zero flag is set to 0. **( Z = 0 )**


**.bne()** - **B**ranch if **N**ot **E**qual (Branch if ZFLAG is **not** set).

**.beq()** - **B**ranch if **E**qual (Branch if ZFLAG **is** set).

```
def loadPlayerLife():
	cpu.lda(100)

# Example Branching
cpu.bne(loadPlayerLife)	# Branch if ZFLAG is not set.
cpu.beq(loadPlayerLife)	# Branch if ZFLAG is set.
```

### Comparing
`cpu.cmp(VALUE)` - will compare the content of the **A register** with a value. If the result is "**equal**", the zero flag will be set (Z = 1). If the result is "**not equal**", the zero flag will be cleared (Z = 0).

`cpu.cpx(VALUE)` - will compare the content of the **X register** with a value. If the result is "**equal**", the zero flag will be set (Z = 1). If the result is "**not equal**", the zero flag will be cleared (Z = 0).

`cpu.cpy(VALUE)` - will compare the content of the **Y register** with a value. If the result is "**equal**", the zero flag will be set (Z = 1). If the result is "**not equal**", the zero flag will be cleared (Z = 0).

```
cpu.lda(100)
cpu.cmp(100)	# ZFlag will be set because 100 = 100. (Z = 1)
```

### Transferring Registers
`cpu.tax()` - Transfer **A register** into **X register**.
`cpu.tay()` - Transfer **A register** into **Y register**.
`cpu.txa()` - Transfer **X register** into **A register**.
`cpu.tya()` - Transfer **Y register** into **A register**.

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

### *.display()*
Turn on the display.
```
cpu.display()
```

### *.hex()*
Don't know the hex value of a number?

.hex() only accepts **strings** as an input. **If you try and load an int, it'll return FALSE**.

**cpu.hex("100")** - will return the number **256**.
```
cpu.hex("100")	# Returns number 256

if cpu.hex("100") == 256:
	# do stuff here
```

### *.clz()*
Clears the Zero Flag.
```
cpu.clz()	# Clear ZFlag
```

### *.dumpRegisters()*
Print all registers to the console. 
```
cpu.dumpRegisters()
```
Output:
```
A = 1
X = 0
Y = 255
Z = 0
```


------------

Thanks for using this program! It took me forever to write! I really hope you enjoy it! :)
-CodeShady

www.codeshady.com