def remove_ac_and_b(instr):
    p = q = 0
    while p < len(instr):
        if instr[p] == 'b':
            p += 1
        elif p+1 < len(instr) and instr[p:p+2] == 'ac':
            p += 2
        else:
            instr = instr[:q] + instr[p] + instr[q+1:]
            p += 1
            q += 1
    return instr[:q]

if __name__ == '__main__':

    print remove_ac_and_b('bbbbd')
    
