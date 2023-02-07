import sys
import argparse
from opcodes import *

def decode_rv32(reg, verbose, jump):
    """
    Decode RV32 instruction
    """
    l = list(bin(int(reg, 16))[2:]) # convert to list

    l = ['0' for _ in range(32 - len(l))] + l # fill the beginning with 0s
    opcode = l[-7:] # last 7 bits

    handler, instr = rv32m_opcodes.get(int(''.join(opcode), 2), (None, None))
    if handler is None:
        print("Could not decode")
        if jump:
            return None, None
        return None

    return handler(l, instr, verbose, jump)

def main():
    parser = argparse.ArgumentParser(prog='decode.py', description='Simple RV32 decompiler')
    parser.add_argument('-v', '--verbose', action='store_true', help='verbose output')
    parser.add_argument('-l', '--nolabel', action='store_true', help='Do not insert labels')
    parser.add_argument('register', help='register to decode (or file)', metavar='register/file')
    args = parser.parse_args()

    if args.register[:2] == "0x":
        ans = decode_rv32(args.register, args.verbose, False)
        if ans is not None:
            print(ans)

    else:
        with open(args.register, 'r') as f:
            lines = f.readlines()

        res = []
        for l in lines:
            s = l.strip().split()
            if s[0][:2] == "0x":
                ans, jump = decode_rv32(s[0], args.verbose, not args.nolabel)
                if ans is not None:
                    if not s[1][0] == '#':
                        res.append(("\t" + ans + "  #" + ' '.join(s[1:]), jump))
                    else:
                        res.append(("\t" + ans + "  " + ' '.join(s[1:]), jump))
            elif not s == []:
                if args.nolabel:
                    res.append(l, None)
        

        if not args.nolabel:
            label_i = 0
            pc = 0
            while pc < len(res):
                l, jump = res[pc]

                if jump is not None:
                    addr = pc + jump
                    if addr > 0 and addr < len(res):
                        if res[addr][1] is None or not res[addr][1] == -1: # not a label
                            label_name = "label" + str(label_i)
                            res.insert(addr, (label_name + ":", -1))
                            if jump < 0:
                                pc += 1

                            label_i += 1
                        else:
                            label_name = res[addr][0][:-1]
                            
                        res[pc] = (l.replace("@", label_name, 1), None) # replace with label name
                pc += 1
            
            print("main:") # entry point
            
        for l in res:
            print(l[0])


if __name__ == "__main__":
    main()

