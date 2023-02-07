import sys
import argparse
from opcodes import *

def decode_rv32(reg, verbose):
    """
    Decode RV32 instruction
    """
    l = list(bin(int(reg, 16))[2:]) # convert to list

    l = ['0' for _ in range(32 - len(l))] + l # fill the beginning with 0s
    opcode = l[-7:] # last 7 bits

    handler, instr = rv32m_opcodes.get(int(''.join(opcode), 2), (None, None))
    if handler is None:
        print("Could not decode")
        return None

    return handler(l, instr, verbose)

def main():
    parser = argparse.ArgumentParser(prog='decode.py', description='Simple RV32 decompiler')
    parser.add_argument('-v', '--verbose', action='store_true', help='verbose output')
    parser.add_argument('register', help='register to decode (or file)', metavar='register/file')
    args = parser.parse_args()

    if args.register[:2] == "0x":
        ans = decode_rv32(args.register, args.verbose)
        if ans is not None:
            print(ans)

    else:
        with open(args.register, 'r') as f:
            lines = f.readlines()

        for l in lines:
            s = l.strip().split()
            if s[0][:2] == "0x":
                ans = decode_rv32(s[0], args.verbose)
                if ans is not None:
                    print(ans, ' '.join(s[1:]))
            elif not s == []:
                print(l)


if __name__ == "__main__":
    main()

