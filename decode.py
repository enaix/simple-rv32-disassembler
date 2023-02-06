import sys
from opcodes import *

def decode_rv32(reg):
    """
    Decode RV32 instruction
    """
    l = list(bin(int(reg, 16))[2:]) # convert to list

    l = ['0' for _ in range(32 - len(l))] + l # fill the beginning with 0s
    opcode = l[-7:] # last 7 bits

    handler, instr = rv32m_opcodes.get(int(''.join(opcode), 2))
    if handler is None:
        print("Could not decode")
        return

    handler(l, instr)

def main():
    if len(sys.argv) == 1:
        print("Usage: decode.py 0x...")
        print("Will add reading from file option later")
        return
    instr = sys.argv[1]
    
    decode_rv32(instr)


if __name__ == "__main__":
    main()

