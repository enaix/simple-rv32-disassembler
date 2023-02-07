def btoi(a):
    """
    bin to dec (unsigned)
    """
    return int(a, 2)

def stoi(a, l):
    """
    bin to dec (signed)
    """
    sign = 1 << (l - 1)
    uns = btoi(a)
    return (uns & sign - 1) - (uns & sign)

def _not_impl(t):
    print("Type " + t + " is not implemented")

def _u(reg):
    """
    U-type
    """
    _not_impl("U")
    pass

def _uj(reg):
    """
    UJ-type
    """
    _not_impl("UJ")
    pass

def _i(reg):
    """
    I-type
    """
    _not_impl("I")
    pass

def _sb(reg, instr):
    """
    SB-type
    """
    im = []
    im.append(reg[0]) # imm[12]
    im.append(reg[24]) # im[11]
    im += reg[1:7] # imm[10:5]
    im += reg[20:24] # imm[4:1]
    im.append('0') # imm[0]

    rs2 = ''.join(reg[7:12])
    rs1 = ''.join(reg[12:17])

    ins = instr.get(''.join(reg[17:20]))

    if ins is None:
        ins = "unknown"

    j_im = ''.join(im)
    dec_im = stoi(j_im, len(j_im))

    print(ins + " x"+str(btoi(rs1)) + ", x"+str(btoi(rs2)) + ", " + str(dec_im) + " (" + j_im + ", offset: " + str(dec_im//4) + ")")

def _s(reg):
    """
    S-type
    """
    _not_impl("S")
    pass

def _r(reg):
    """
    R-type
    """
    _not_impl("R")
    pass

def _r_i(reg):
    """
    R-type and I-type
    """
    _not_impl("R/I")
    pass

def _fence(reg):
    """
    Fence instruction
    """
    _not_impl("fence")
    pass

def _ec_br(reg):
    """
    Ecall/Ebreak instructions
    """
    _not_impl("ecall/ebreak")
    pass

rv32m_opcodes = {btoi('0110111'): (_u, ['lui']), btoi('0010111'): (_u, ['auipc']),
                 btoi('1101111'): (_uj, ['jal']), btoi('1100111'): (_i, ['jalr']),
                 btoi('1100011'): (_sb, {'000': 'beq', '001': 'bne', '100': 'blt', '101': 'bge', '110': 'bltu', '111': 'bgeu'}),
                 btoi('0000011'): (_i, []),
                 btoi('0100011'): (_s, []), btoi('0010011'): (_r_i, []),
                 btoi('0110011'): (_r, []), btoi('0001111'): (_fence, ['fence']),
                 btoi('1110011'): (_ec_br, [])}


