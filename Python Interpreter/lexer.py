code = ""

methods = [',', '.', '>', '<', '++', '--', '+', '-', '*', '/', '**', '//', '%', '#', ';', '(', '[', ']{', ']?{', '?{', '{', '>{', '~{', '$', '^', '@', '==', '>=', '<=', '!=', '*=', '>*=', '<*=', '!*=', '!', '&', '|', '/=', '>/=', '</=', '!/=', '!/', '&/', '|/']

methodChars = [list(filter(lambda x: len(x) == i, methods)) for i in range(4)]

def lexing(code):
    temp = ""
    tokenList = {}
    position = 0
    quoteStatus = False
    lookup = False
    for pos,i in enumerate(code):
        char = i
        if i.isnumeric() and len(temp) == 0 or i.isnumeric() and len(temp) > 0 and not temp[-1].isnumeric():
            lookup = False
            position += 1
        elif i.isnumeric():
            pass
        elif i == '"':
            lookup = False
            if not quoteStatus and position > 0 or quoteStatus and len(temp) > 0 and temp[-1] != '"':
                position += 1
            char = ""
            quoteStatus = not quoteStatus
        elif any(n.startswith(i) for n in methodChars[2]) and not lookup or any(n.startswith(i) for n in methodChars[3]) and not lookup:
            lookup = True
            position += 1
        elif len(temp) > 0 and any(n.startswith(temp[-1] + i) for n in methodChars[3]) and lookup or quoteStatus:
            lookup = True
        elif len(temp) > 0 and (temp[-1] + i) in methodChars[2]:
            lookup = False
            tokenList[position] = ""
            char = temp[-1] + i
        elif temp + i in methodChars[3]:
            lookup = False
            tokenList[position] = ""
            char = temp + i
        elif i in methodChars[1]:
            lookup = False
            position += 1
        else:
            char = ""
        if position not in tokenList:
            tokenList[position] = ''
        tokenList[position] += char
        if not (len(temp) > 0 and temp[-1] == '"') and tokenList[position] == '':
            del tokenList[position]
        if len(temp) == 2:
            temp = temp[1]
        temp += i
    return list(tokenList.values())


print(lexing(code))