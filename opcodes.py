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

def _u(reg, instr, vb=False):
    """
    U-type
    """
    if instr[0] == 'lui':
        ins = 'lui'
    elif instr[0] == 'auipc':
        ins = 'auipc'
    else:
        ins = 'unknown'

    im = reg[0:20]
    j_im = ''.join(im)
    dec_im = stoi(j_im, len(j_im))
    
    rd = ''.join(reg[20:25])

    res = ins + " x"+str(btoi(rd)) + ", " + str(dec_im)
    if vb:
        res += " (" + j_im + "; " + str(dec_im << 12) + " after shift)"
    return res

def _uj(reg, instr, vb=False):
    """
    UJ-type
    """
    im = []
    im.append(reg[0]) # imm[20]
    im += reg[12:20] # imm[19:12]
    im.append(reg[11]) # im[11]
    im += reg[1:11] # im[10:1]
    im.append('0')

    j_im = ''.join(im)
    dec_im = stoi(j_im, len(j_im))
    rd = ''.join(reg[20:25])

    res = instr[0] + " x"+str(rd) + ", " + str(dec_im)
    if vb:
        res += " (" + j_im + "; offset: " + str(dec_im//4) + ")"
    return res

def _i(reg, instr, vb=False):
    """
    I-type
    """
    if type(instr) == list:
        ins = instr[0]
    else:
        ins = instr.get(''.join(reg[17:20]))

        if ins is None:
            ins = "unknown"

    im = reg[0:12]
    rs1 = ''.join(reg[12:17])
    rd = ''.join(reg[20:25])

    j_im = ''.join(im)
    dec_im = stoi(j_im, len(j_im))

    res = ins + " x" + str(btoi(rd)) + ", x" + str(btoi(rs1)) + ", " + str(dec_im)
    if vb:
        res += " (" + j_im + ')'

    return res

def _sb(reg, instr, vb=False):
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

    res = ins + " x"+str(btoi(rs1)) + ", x"+str(btoi(rs2)) + ", " + str(dec_im)
    if vb:
        res += " (" + j_im + "; offset: " + str(dec_im//4) + ")"

    return res

def _s(reg, instr, vb=False):
    """
    S-type
    """
    ins = instr.get(''.join(reg[17:20]))

    if ins is None:
        ins = "unknown"

    im = reg[0:7] # im[11:5]
    im += reg[20:25] # im[4:0]

    rs2 = ''.join(reg[7:12])
    rs1 = ''.join(reg[12:17])

    j_im = ''.join(im)
    dec_im = stoi(j_im, len(j_im))

    res = ins + " x"+str(btoi(rs1)) + ", x"+str(btoi(rs2)) + ", " + str(dec_im)
    if vb:
        res += " (" + j_im + "; mem offset: " + str(dec_im//4) + ')'
    return res

def _r(reg, instr, vb=False):
    """
    R-type
    """
    f7 = ''.join(reg[0:7])
    if type(instr) == list and instr[0] == 'srl_i':
        if btoi(f7) == 0:
            ins = 'srli'
        else:
            ins = 'srai'
    else:
        ins_d = instr.get(''.join(reg[17:20]))
        if ins_d is None:
            ins = "unknown"
        elif type(ins_d) == str:
            ins = ins_d
        elif type(ins_d) == dict:
            if btoi(f7) == 0:
                ins = ins_d[0]
            else:
                ins = ins_d[1]

    rs2 = ''.join(reg[7:12])
    rs1 = ''.join(reg[12:17])
    rd = ''.join(reg[20:25])

    res = ins + " x"+str(btoi(rd)) + ", x"+str(btoi(rs1)) + ", x"+str(btoi(rs2))
    return res

def _r_i(reg, instr, vb=False):
    """
    R-type and I-type
    """
    ins = instr.get(''.join(reg[17:20]))

    if ins is None:
        ins = "unknown"
    elif ins in ['slli', 'srl_i']:
        return _r(reg, [ins], vb)

    return _i(reg, [ins], vb)

def _fence(reg, instr, vb=False):
    """
    Fence instruction
    """
    _not_impl("fence")
    pass

def _ec_br(reg, instr, vb=False):
    """
    Ecall/Ebreak instructions
    """
    if btoi(''.join(reg[0:12])) == 0:
        return "ecall"
    return "ebreak"

rv32m_opcodes = {btoi('0110111'): (_u, ['lui']), btoi('0010111'): (_u, ['auipc']),
                 btoi('1101111'): (_uj, ['jal']), btoi('1100111'): (_i, ['jalr']),
                 btoi('1100011'): (_sb, {'000': 'beq', '001': 'bne', '100': 'blt', '101': 'bge', '110': 'bltu', '111': 'bgeu'}),
                 btoi('0000011'): (_i, {'000': 'lb', '001': 'lh', '010': 'lw', '100': 'lbu', '101': 'lhu'}),
                 btoi('0100011'): (_s, {'000': 'sb', '001': 'sh', '010': 'sw'}),
                 btoi('0010011'): (_r_i, {'000': 'addi', '010': 'slti', '011': 'sltiu', '100': 'xori', '110': 'ori', '111': 'andi', '001': 'slli', '101': 'srl_i'}),
                 btoi('0110011'): (_r, {'000': {0: 'add', 1: 'sub'}, '001': 'sll', '010': 'slt', '011': 'sltu', '100': 'xor', '101': {0: 'srl', 1: 'sra'}, '110': 'or', '111': 'and'}),
                 btoi('0001111'): (_fence, ['fence']),
                 btoi('1110011'): (_ec_br, [])}


