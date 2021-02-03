from RetroLang import RAM, CPU, PPU
from time import sleep
from os import system
from random import randint, choice

# CREATE RAM AND CPU
ram = RAM()
ppu = PPU()
cpu = CPU(ram, ppu)


def main():
    # COMMANDS
    while True:
        for i in range(cpu.hex("100"), cpu.hex("300")):
            cpu.ldx(choice([0, 1, 2, 3, 4, 5, 255]))
            cpu.stx(i)
            
        
        system("clear||cls")
        cpu.display()
        sleep(0.2)


if __name__ == "__main__":
    # Main script
    main()
    # ram.dumpMemory()
    # cpu.dumpRegisters()