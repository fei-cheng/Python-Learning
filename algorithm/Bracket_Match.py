def Bracket_Match(input, count):
    '''
        Only recurse, no loop
    '''
    if input == None or input == '':
        if count == 0:
            return True
        return False

    if input[0] == '(':
        count += 1
    elif input[0] == ')':
        if count > 0:
            count -= 1
        else:
            return False

    return Bracket_Match(input[1:], count)


if __name__ == '__main__':
    match = Bracket_Match('(a)(b)(a', 0)
    print match
