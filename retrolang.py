from RetroLang import RAM, CPU, PPU
import time
import sys

# CREATE RAM AND CPU
ram = RAM()
ppu = PPU()
cpu = CPU(ram, ppu)


def main():
    # COMMANDS
    cpu.ldx("00")
    cpu.ppu()
    ppu.display()
    # cpu.ppu()

if __name__ == "__main__":
    # Main script
    main()
    cpu.dumpRegisters()



