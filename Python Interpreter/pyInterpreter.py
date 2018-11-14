import traceback, sys


class Interpreter:
    def __init__(self):
        self.memory = [] * 2000

    def verify(self, codestring):
        quotesCheck = -1
        closablesKeys = {'[': 0, '(': 0, '{': 0, '"': 0}
        closingKeys = {']': '[', ')': '(', '}': '{', '"': '"'}
        needingValueKeys = ['++', '--', '*', '/', '%', '?', ':', '=', '>=', '<=', '!=', '!', '&', '|', '/=', '>/=',
                            '</=',
                            '!', '&']
        otherKeys = [',', '.', '>', '<', '+', '-', '#', ';', '$', '^', '@']
        temp = ''
        for i, x in enumerate(list(codestring)):
            testNeedingValueKeys = [(temp + x).endswith(n) for n in needingValueKeys]
            testOtherKeys = [(temp + x).endswith(n) for n in otherKeys]
            if any(testNeedingValueKeys):
                key = ''.join(
                    needingValueKeys[n] if testNeedingValueKeys[n] else '' for n in range(len(needingValueKeys)))
                if not (codestring[i + 1] in '"0123456789' and codestring[
                    i - len(key)] in '"0123456789') and quotesCheck == -1:
                    try:
                        raise SyntaxError
                    except SyntaxError:
                        etype, value, tb = sys.exc_info()
                        message = ''.join(traceback.format_exception(etype, value, tb))
                        print(message.split('\n')[0] + '\n  ' + '...' + codestring[
                                                                        i - 3:i + 3] + '...' + '\n' + ' ' * 8 + '^' + '\nSyntaxError: invalid syntax (pos ' + str(
                            i) + ')', file=sys.stderr)
                        sys.exit(1)
                else:
                    key = ''.join(otherKeys[n] if testOtherKeys[n] else '' for n in range(len(otherKeys)))
            elif x in list(closablesKeys.keys()) and (x == '"' and quotesCheck == 1):
                closablesKeys[x] += 2 if any(x.endswith(j) for j in '("') else 1
            elif (temp + x).endswith('?['):
                closablesKeys['['] += 2
            elif x in list(closingKeys.keys()):
                closablesKeys[closingKeys[x]] -= 2
            else:
                pass
            if x == '"':
                quotesCheck *= -1
            temp = temp + x if len(temp) < 2 else temp[1] + x
        for i, x in closablesKeys.items():
            if x != 0:
                try:
                    raise SyntaxError
                except SyntaxError:
                    etype, value, tb = sys.exc_info()
                    message = ''.join(traceback.format_exception(etype, value, tb))
                    print(message.split('\n')[0] + '\n  ' + codestring + '\nSyntaxError: inconsistent use of "' + str(
                        i) + '" (' + str(abs(int(x / 2) if (x > 0 or i in '("') else x)) + (
                              ' too much' if x > 0 else ' missing') + ')',
                          file=sys.stderr)
                    sys.exit(1)

    def interpret(self, codestring):
        codestring += ' '
        self.verify(codestring)


codestring = '"Hello World !".'

i = Interpreter()
i.interpret(codestring)
