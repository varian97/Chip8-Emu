from chip8.cpu import CPU

if __name__ == '__main__':
    cpu = CPU(None, None, None)
    cpu.load_rom_into_memory('./roms/Blitz.ch8')

    print(cpu.memory)
