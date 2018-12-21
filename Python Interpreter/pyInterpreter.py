# Copyright (C) 2018 Yoann Bernard
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

# -*- coding: utf-8 -*-
import sys
import traceback
import re
# noinspection PyCompatibility
from io import StringIO
import _io


# noinspection PyCompatibility,PyCallingNonCallable,PyPep8,PyBroadException,PyShadowingNames,PyShadowingNames,PyShadowingNames,PyShadowingNames,PyShadowingNames,PyShadowingNames,PyShadowingNames,PyShadowingNames,PyShadowingNames,PyShadowingNames,PyShadowingNames,PyShadowingNames,PyShadowingNames,PyShadowingNames,PyShadowingNames,PyShadowingNames,PyShadowingNames,PyShadowingNames,PyShadowingNames,PyShadowingNames,PyShadowingNames,PyShadowingNames,PyShadowingNames
class Interpreter:
    """Python Interpreter for KidoScript, developped by Nenrikido"""

    memory: list
    pointer: int
    tempvalue: object
    methods: dict
    priorities: list
    arguments: list
    i: int
    x: str
    codeString: str

    # noinspection PyCompatibility
    class Capturing(list):
        """Capturing prints for arguments"""

        _stdout: _io.TextIOWrapper
        _stringIo: StringIO

        def __enter__(self):
            self._stdout = sys.stdout
            sys.stdout = self._stringIo = StringIO()
            return self

        def __exit__(self, *args):
            self.extend(self._stringIo.getvalue().splitlines())
            del self._stringIo
            sys.stdout = self._stdout

    # noinspection PyCompatibility,PyShadowingNames,PyShadowingNames
    class Function:
        """Representating a function, arguments will be in first cases of memory"""

        arguments: list
        memory: list
        tempvalue: object
        pointer: int
        methods: dict
        priorities: list
        i: int
        x: str
        codeString: str
        returning: bool

        def __init__(self, arguments, codeString, interpreter):
            self.arguments = arguments
            self.codeString = codeString
            self.memory = []

            # Simulate inheritance
            self.interpret = interpreter.interpret
            for attribute in dir(interpreter):
                if attribute not in ['arguments', 'memory', 'codeString']:
                    setattr(self, attribute, getattr(interpreter, attribute))
            for key, method in self.methods.items():
                setattr(self, method.__name__(), method)

        def execute(self):
            for i, argument in enumerate(self.arguments):
                self.memory[i] = argument
            self.interpret(self.codeString)
            if self.returning:
                self.returning = False
                return self.memory[self.pointer]

    def buildFunction(self, arguments, code):
        """Builds a function object"""

        return self.Function(arguments, code, self)

    # noinspection PyCompatibility,PyShadowingNames
    class Vector:
        """Representating a vector"""

        memory: list
        tempvalue: object
        pointer: int
        methods: dict
        priorities: list
        i: int
        x: str
        codeString: str

        def __init__(self, codeString, interpreter):
            self.codeString = codeString

            # Simulate inheritance
            self.interpret = interpreter.interpret
            for attribute in dir(interpreter):
                if attribute not in ['arguments', 'codeString']:
                    setattr(self, attribute, getattr(interpreter, attribute))
            for key, method in self.methods.items():
                if key not in [',', '.', '+', '-', '~(', '$']:
                    setattr(self, method.__name__(), method)

        def getDeplacement(self):
            beginningPointer = self.pointer
            self.interpret(self.codeString)
            return self.pointer - beginningPointer

    def buildVector(self, code):
        """Builds a vector object"""

        return self.Vector(code, self)

    def __init__(self):
        self.memory = [0] * 2000
        self.pointer = 0
        self.tempvalue = self.memory[self.pointer]
        self.methods = {',': self.scan, '.': self.print, '>': self.moveRight, '<': self.moveLeft,
                        '++': self.incrementPointer, '--': self.decrementPointer, '0': self.putInt, '1': self.putInt,
                        '2': self.putInt, '3': self.putInt, '4': self.putInt, '5': self.putInt, '6': self.putInt,
                        '7': self.putInt,
                        '8': self.putInt, '9': self.putInt, '"': self.putString, '+': self.add, '-': self.negate,
                        '*': self.multiplicate, '/': self.divide, '**': self.power, '//': self.euclidianDivide,
                        '%': self.modulo, '#': self.firstIndex,
                        ';': self.lastIndex, '(': self.startGroupCode, '[': self.setArguments,
                        ']{': self.startInnerForCode,
                        ']?{': self.startInnerWhileCode, '?{': self.startInnerIfCode, '{': self.startFunctionCode,
                        '>{': self.startVectorCode,
                        '~{': self.startCopyVectorCode, '$': self.returnResult, '^': self.execute, '@': self.evaluate,
                        '==': self.isWeaklyEq, '>=': self.isWeaklyGe, '<=': self.isWeaklyLe, '!=': self.isWeaklyNe,
                        '*=': self.isSumEq, '>*=': self.isSumGe, '<*=': self.isSumLe, '!*=': self.isSumNe,
                        '!': self.weakNon, '&': self.weakAnd, '|': self.weakOr,
                        '/=': self.isStronglyEq, '>/=': self.isStronglyGe, '</=': self.isStronglyLe,
                        '!/=': self.isStronglyNe,
                        '!/': self.strongNon, '&/': self.strongAnd, '|/': self.strongOr}
        self.priorities = ['.\*\*|\/\/', '..%', '..\*|..\/', '..-|..+', '.&\/|..&', '..\|\/|.\|',
                           '.==|.!=|.>=|.<=|.\*=|>\*=|<\*=|!\*=|=\/=|!\/=|>\/=|<\/=']
        self.arguments = []
        self.i = 0
        self.x = ''
        self.vector = {"isVector": False, "deplacement": 0}
        self.returning = False

    def scan(self):
        """`,` : Scans from console to memory case at pointer position"""
        self.memory[self.pointer] = input()

    def print(self):
        """`.` : Prints what's in memory case at pointer position in console"""
        print(self.memory[self.pointer])

    def moveRight(self):
        """`>` : Moves pointer to right"""
        self.pointer = self.pointer + 1 if self.pointer < len(self.memory) - 1 else 0

    def moveLeft(self):
        """`<` : Moves pointer to left"""
        self.pointer = self.pointer - 1 if self.pointer > 0 else len(self.memory) - 1

    def incrementPointer(self):
        """`+` : Increments memory case at pointer position from 1"""
        n = self.memory[self.pointer]
        self.memory[self.pointer] = n + 1 if type(n) == int else chr(ord(n[-1]) + 1)

    def decrementPointer(self):
        """`-` : Decrements memory case at pointer position from 1"""
        n = self.memory[self.pointer]
        self.memory[self.pointer] = n - 1 if type(n) == int else chr(ord(n[-1]) - 1)

    def putInt(self):
        """`\d` : (Any integer decimal) : Changes value of memory case at pointer position"""
        intString = ''
        while self.codeString[self.i].isnumeric():
            intString += self.codeString[self.i]
            self.i += 1
        self.i -= 1
        self.memory[self.pointer] = int(intString)

    def putString(self):
        """`"Some String"` : Changes value of memory case at pointer position by a string (store in the number of bytes in ASCII) (care to reserved word `func:`)"""
        self.i += 1
        string = ''
        while self.codeString[self.i] != '"':
            string += self.codeString[self.i]
            self.i += 1
        self.memory[self.pointer] = string

    def add(self):
        """`++` : Addition operator"""
        intString = ''
        self.i += 1
        if self.codeString[self.i] != '(':
            while self.codeString[self.i].isnumeric():
                intString += self.codeString[self.i]
                self.i += 1
        else:
            intString = self.startVectorCode(True)
        self.i -= 1
        self.memory[self.pointer] += int(intString)

    def negate(self):
        """`--` : Substraction operator"""
        intString = ''
        self.i += 1
        if self.codeString[self.i] != '(':
            while self.codeString[self.i].isnumeric():
                intString += self.codeString[self.i]
                self.i += 1
        else:
            intString = self.startVectorCode(True)
        self.i -= 1
        self.memory[self.pointer] -= int(intString)

    def multiplicate(self):
        """`*` : Multiplication operator"""
        intString = ''
        self.i += 1
        if self.codeString[self.i] != '(':
            while self.codeString[self.i].isnumeric():
                intString += self.codeString[self.i]
                self.i += 1
        else:
            intString = self.startVectorCode(True)
        self.i -= 1
        self.memory[self.pointer] *= int(intString)

    def divide(self):
        """`/` : Division operator"""
        intString = ''
        self.i += 1
        if self.codeString[self.i] != '(':
            while self.codeString[self.i].isnumeric():
                intString += self.codeString[self.i]
                self.i += 1
        else:
            intString = self.startVectorCode(True)
        self.i -= 1
        self.memory[self.pointer] /= int(intString)

    def power(self):
        """`**` : Power operator"""
        intString = ''
        self.i += 1
        if self.codeString[self.i] != '(':
            while self.codeString[self.i].isnumeric():
                intString += self.codeString[self.i]
                self.i += 1
        else:
            intString = self.startVectorCode(True)
        self.i -= 1
        self.memory[self.pointer] **= int(intString)

    def euclidianDivide(self):
        """`//` : Euclidian divisio operator"""
        intString = ''
        self.i += 1
        if self.codeString[self.i] != '(':
            while self.codeString[self.i].isnumeric():
                intString += self.codeString[self.i]
                self.i += 1
        else:
            intString = self.startVectorCode(True)
        self.i -= 1
        self.memory[self.pointer] //= int(intString)

    def modulo(self):
        """`%` : Modulo operator"""
        intString = ''
        self.i += 1
        if self.codeString[self.i] != '(':
            while self.codeString[self.i].isnumeric():
                intString += self.codeString[self.i]
                self.i += 1
        else:
            intString = self.startVectorCode(True)
        self.i -= 1
        self.memory[self.pointer] %= int(intString)

    def firstIndex(self):
        """`#` : Goes to first memory case"""
        self.pointer = 0

    def lastIndex(self):
        """`;` : Goes to last memory case"""
        self.pointer = len(self.memory) - 1

    class LiteralToken:
        def __init__(self, value):
            self.value = int(value)

        def nud(self):
            return self.value

    @staticmethod
    def expression(rbp=0):
        """Builds the expression with priority"""
        # noinspection PyGlobalUndefined
        global token, nextToken
        t = token
        token = nextToken()
        left = t.nud()
        while rbp < token.lbp:
            t = token
            token = nextToken()
            left = t.led(left)
        return left

    def createToken(self, operator):
        """Creates a token"""

        # noinspection PyMethodParameters,PyShadowingNames
        class Operator:
            def __init__(this):
                for i, x in enumerate(self.priorities):
                    if re.match(x, operator):
                        this.lbp = i * 10
                        break

            @staticmethod
            def nud():
                if operator == '+':
                    return self.expression(100)
                elif operator == '-':
                    return -self.expression(100)

            @staticmethod
            def led(left):
                if operator in '+-//**%':
                    eval('return ' + left + operator + self.expression(10))
                else:
                    return self.methods[operator]

        return Operator()

    def tokenize(self, code):
        """Recursively checks for priority"""
        for number, operator in re.findall("\s*(?:(\d+)|(\*\*|.))", code):
            if number:
                yield self.LiteralToken(number)
            elif any(re.match(i, operator) for i in self.priorities):
                yield self.createToken(operator)
            else:
                raise SyntaxError("unknown operator: %r" % operator)

    def startGroupCode(self):
        """`( CodeToExecuteWithPriorityHandlingOrComparison )` : Group of code with operator and comparison priority (`Comparison` (`and` > `or` > `comparison operators`) > `**` > `//` > `%` > `/` > `*` > `-` > `+`)"""
        global token, nextToken

        # Get code to execute in group
        self.i += 1
        codeString = ''
        while self.codeString[self.i] != ')':
            codeString += self.codeString[self.i]
            self.i += 1
        nextToken = next(self.tokenize(codeString))
        token = nextToken()
        self.memory[self.pointer] = self.expression()

    def setArguments(self, endEnclosing=']'):
        """Method setting arguments for for and while loops and functions"""

        # Get code to execute to get arguments
        self.i += 1
        codeToExecute = ''
        while self.codeString[self.i] != endEnclosing:
            codeToExecute += self.codeString[self.i]
            self.i += 1

        # Execute code in capturing context to get printed values as arguments
        with self.Capturing() as output:
            self.interpret(codeToExecute)
        self.arguments = output

    def startInnerForCode(self):
        """`[ PrintPointerOfStartEnd&Step ]{ CodeToLoop }` : For loop (End or Start and End or Start and End and Step) (Execute code until the changing value from the for loop has ended what's the for loop has initialized it to do; The memory case at where it has been initializated countains the changing value from the for loop)"""

        # Check is there's no more than 3 arguments
        if len(self.arguments) > 3:
            try:
                raise TypeError
            except TypeError:
                etype, value, tb = sys.exc_info()
                message = ''.join(traceback.format_exception(etype, value, tb))
                print(message.split('\n')[0] + '\n  ' + '...' + codeString[
                                                                self.i - 3 if self.i - 3 > 0 else 0:self.i + 3] + '...' + '\n' + ' ' * (
                              self.i + (len(codeString) if len(
                          codeString) < 6 else 6)) + '^' + '\nTypeError: loop expected at most 3 arguments, got ' + str(
                    len(
                        self.arguments)),
                      file=sys.stderr)
                sys.exit(1)

        # Get code to loop
        self.i += 1
        codeToExecute = ''
        while self.codeString[self.i] != ']':
            codeToExecute += self.codeString[self.i]
            self.i += 1

        # Loop code execution
        forPointer = self.pointer
        for i in range(*self.arguments):
            self.memory[forPointer] = i
            self.interpret(codeToExecute)

        self.arguments = []

    def startInnerWhileCode(self):
        """`[ Condition ]?{ CodeToLoop }` : While loop (Execute code until the condition in the while loop arguments aren't anymore resolved)"""

        # Check is there's no more than 1 argument
        if len(self.arguments) > 1:
            try:
                raise TypeError
            except TypeError:
                etype, value, tb = sys.exc_info()
                message = ''.join(traceback.format_exception(etype, value, tb))
                print(message.split('\n')[0] + '\n  ' + '...' + codeString[
                                                                self.i - 3 if self.i - 3 > 0 else 0:self.i + 3] + '...' + '\n' + ' ' * (
                              self.i + (len(codeString) if len(
                          codeString) < 6 else 6)) + '^' + '\nTypeError: loop expected at most 3 arguments, got ' + str(
                    len(
                        self.arguments)),
                      file=sys.stderr)
                sys.exit(1)

        # Get code to loop
        self.i += 1
        codeToExecute = ''
        while self.codeString[self.i] != ']':
            codeToExecute += self.codeString[self.i]
            self.i += 1

        # Loop code execution
        while self.arguments[0]():
            self.interpret(codeToExecute)

        self.arguments = []

    def startInnerIfCode(self):
        """`Condition ?{ CodeToExecuteIfTrue : CodeToExecuteIfFalse}` : If Else Elseif structure (else is optionnal). It uses a weak conditionnal system so `0` and `''` are equivalents to `False` and all the other values are equivalent to `True`"""

        # Get code to execute
        self.i += 1
        colonPassed = False
        codeToExecuteIfTrue = ''
        codeToExecuteIfFalse = ''
        while self.codeString[self.i] != '}':
            if self.codeString[self.i] == ':':
                self.i += 1
                colonPassed = True
            if colonPassed:
                codeToExecuteIfFalse += self.codeString[self.i]
            else:
                codeToExecuteIfTrue += self.codeString[self.i]
            self.i += 1

        # Conditionnal code execution
        if self.memory[self.pointer] in [0, '']:
            if codeToExecuteIfFalse != '':
                self.interpret(codeToExecuteIfFalse)
        else:
            self.interpret(codeToExecuteIfTrue)

        self.arguments = []

    def startFunctionCode(self):
        """`{ PrintArgumentsPositionInMemory { CodeToExecuteAsFunction }` : Stores a function at memory case (memory is now a virtual memory local to the function and argument passed are stored in first cases of this virtual memory)"""

        # Set function arguments
        self.setArguments('{')
        passingArguments = self.arguments

        # Get code to loop
        self.i += 1
        codeToExecute = ''
        while self.codeString[self.i] != '}':
            codeToExecute += self.codeString[self.i]
            self.i += 1

        # Store function
        self.memory[self.pointer] = self.buildFunction(passingArguments, codeToExecute)
        self.arguments = []

    def startVectorCode(self, isSelectionning=False):
        """`( PointerDeplacement )` : Vector to move value of memory case at pointer position by PointerDeplacement (accept only loops and pointer deplacement keys), it can also be used in operations to select another value than the one in the actual memory case. The pointer isn't"""

        # Get Vector Deplacement (and errors with it)
        self.i += 1
        codeToExecute = 0
        while self.codeString[self.i] != '}':
            codeToExecute += self.codeString[self.i]
            self.i += 1
        vector = self.buildVector(codeString)
        deplacement = vector.getDeplacement()

        # Move or return deplacement if selectionning
        if isSelectionning:
            return deplacement
        else:
            self.memory[self.pointer + deplacement] = self.memory[self.pointer]
            self.memory[self.pointer] = 0

    def startCopyVectorCode(self):
        """`~{ PointerDeplacement }` :	Copies value of memory case at pointer position by PointerDeplacement (idem)"""

        # Get Vector Deplacement (and errors with it)
        self.i += 1
        codeToExecute = 0
        while self.codeString[self.i] != '}':
            codeToExecute += self.codeString[self.i]
            self.i += 1
        vector = self.buildVector(self.codeString)
        deplacement = vector.getDeplacement()

        # Copy value
        self.memory[self.pointer + deplacement] = self.memory[self.pointer]

    def returnResult(self):
        """`$` : Return value from function in memory case (need to be launched in another memory case and is exactly like `^` if isn't in function)"""

        self.returning = True

    def execute(self):
        """`^` : Execute code from stored function (or do same as ,)"""

        try:
            self.memory[self.pointer].execute()
        except AttributeError:
            etype, value, tb = sys.exc_info()
            message = ''.join(traceback.format_exception(etype, value, tb))
            print(message.split('\n')[0] + '\n  ' + '...' + self.codeString[
                                                            self.i - 3 if self.i - 3 > 0 else 0:self.i + 3] + '...' + '\n' + ' ' * (
                          self.i + (len(self.codeString) if len(
                      self.codeString) < 6 else 6)) + '^' + '\nTypeError: \'' + type(
                self.memory[self.pointer]) + '\' object is not callable',
                  file=sys.stderr)

    def evaluate(self):
        """`@` : Evaluate code in string in memory case at pointer position like a function"""

        try:
            eval(self.memory[self.pointer])
        except:
            print("Traceback (most recent call last):", file=sys.stderr)
            traceback.print_tb(sys.exc_info()[2])
            print(str(sys.exc_info()[0]).split("<class '")[1].split("'>")[0] + ' : ' + str(sys.exc_info()[1]),
                  file=sys.stderr)

    @staticmethod
    def isWeaklyEq(leftMember, rightMember):
        return leftMember == rightMember if type(leftMember) == type(rightMember) \
            else ord(leftMember) == rightMember if type(leftMember) == str and len(leftMember) == 1 and type(
            rightMember) == int \
            else leftMember == ord(rightMember) if type(rightMember) == int and type(rightMember) == int and len(
            rightMember) == 1 \
            else len(leftMember) == rightMember if type(leftMember) == str and type(rightMember) == int \
            else leftMember == len(rightMember)

    @staticmethod
    def isWeaklyGe(leftMember, rightMember):
        return leftMember >= rightMember if type(leftMember) == type(rightMember) \
            else ord(leftMember) >= rightMember if type(leftMember) == str and len(leftMember) == 1 and type(
            rightMember) == int \
            else leftMember >= ord(rightMember) if type(rightMember) == int and type(rightMember) == int and len(
            rightMember) == 1 \
            else len(leftMember) >= rightMember if type(leftMember) == str and type(rightMember) == int \
            else leftMember >= len(rightMember)

    @staticmethod
    def isWeaklyLe(leftMember, rightMember):
        return leftMember <= rightMember if type(leftMember) == type(rightMember) \
            else ord(leftMember) <= rightMember if type(leftMember) == str and len(leftMember) == 1 and type(
            rightMember) == int \
            else leftMember <= ord(rightMember) if type(rightMember) == int and type(rightMember) == int and len(
            rightMember) == 1 \
            else len(leftMember) <= rightMember if type(leftMember) == str and type(rightMember) == int \
            else leftMember <= len(rightMember)

    @staticmethod
    def isWeaklyNe(leftMember, rightMember):
        return leftMember != rightMember if type(leftMember) == type(rightMember) \
            else ord(leftMember) != rightMember if type(leftMember) == str and len(leftMember) == 1 and type(
            rightMember) == int \
            else leftMember != ord(rightMember) if type(rightMember) == int and type(rightMember) == int and len(
            rightMember) == 1 \
            else len(leftMember) != rightMember if type(leftMember) == str and type(rightMember) == int \
            else leftMember != len(rightMember)

    def isSumEq(self, leftMember, rightMember):
        return sum([ord(i) for i in leftMember]) == rightMember if type(leftMember) == str and type(rightMember) == int \
            else leftMember == sum([ord(i) for i in rightMember]) if type(rightMember) == str and type(
            leftMember) == int \
            else sum([ord(i) for i in leftMember]) == sum([ord(i) for i in rightMember]) if type(leftMember) == type(
            rightMember) == str \
            else self.isWeaklyEq(leftMember, rightMember)

    def isSumGe(self, leftMember, rightMember):
        return sum([ord(i) for i in leftMember]) >= rightMember if type(leftMember) == str and type(rightMember) == int \
            else leftMember >= sum([ord(i) for i in rightMember]) if type(rightMember) == str and type(
            leftMember) == int \
            else sum([ord(i) for i in leftMember]) >= sum([ord(i) for i in rightMember]) if type(leftMember) == type(
            rightMember) == str \
            else self.isWeaklyEq(leftMember, rightMember)

    def isSumLe(self, leftMember, rightMember):
        return sum([ord(i) for i in leftMember]) <= rightMember if type(leftMember) == str and type(rightMember) == int \
            else leftMember <= sum([ord(i) for i in rightMember]) if type(rightMember) == str and type(
            leftMember) == int \
            else sum([ord(i) for i in leftMember]) <= sum([ord(i) for i in rightMember]) if type(leftMember) == type(
            rightMember) == str \
            else self.isWeaklyEq(leftMember, rightMember)

    def isSumNe(self, leftMember, rightMember):
        return sum([ord(i) for i in leftMember]) != rightMember if type(leftMember) == str and type(rightMember) == int \
            else leftMember != sum([ord(i) for i in rightMember]) if type(rightMember) == str and type(
            leftMember) == int \
            else sum([ord(i) for i in leftMember]) != sum([ord(i) for i in rightMember]) if type(leftMember) == type(
            rightMember) == str \
            else self.isWeaklyEq(leftMember, rightMember)

    @staticmethod
    def weakNon(thing):
        return not bool(thing)

    @staticmethod
    def weakAnd(leftMember, rightMember):
        return bool(leftMember) and bool(rightMember)

    @staticmethod
    def weakOr(leftMember, rightMember):
        return bool(leftMember) or bool(rightMember)

    @staticmethod
    def isStronglyEq(leftMember, rightMember):
        return leftMember == rightMember and type(leftMember) == type(rightMember)

    @staticmethod
    def isStronglyGe(leftMember, rightMember):
        return leftMember >= rightMember and type(leftMember) == type(rightMember)

    @staticmethod
    def isStronglyLe(leftMember, rightMember):
        return leftMember <= rightMember and type(leftMember) == type(rightMember)

    @staticmethod
    def isStronglyNe(leftMember, rightMember):
        return leftMember != rightMember and type(leftMember) == type(rightMember)

    @staticmethod
    def strongNon(thing):
        return not thing

    @staticmethod
    def strongAnd(leftMember, rightMember):
        return leftMember and rightMember and type(leftMember) == type(rightMember)

    @staticmethod
    def strongOr(leftMember, rightMember):
        return leftMember or rightMember and type(leftMember) == type(rightMember)

    @staticmethod
    def verify(codeString):
        quotesCheck = -1
        closablesKeys = {'[': 0, '(': 0, '{': 0, '"': 0}
        closingKeys = {']': '[', ')': '(', '}': '{', '"': '"'}
        closablesState = []
        needingValueKeys = ['*', '/', '+', '-', '**', '//', '%', '?', ':', '=', '>=', '<=', '!=', '!', '&', '|', '/=', '>/=',
                            '</=',
                            '!', '&']
        temp = ''
        for i, x in enumerate(list(codeString)):
            testNeedingValueKeys = [(temp + x).endswith(n) for n in needingValueKeys]
            if x in closablesKeys.keys() and x != '"':
                closablesState.append((i, x))
            if x in closingKeys.keys() and x != '"':
                if closablesState[-1][1] == closingKeys[x]:
                    closablesState = closablesState[:-1]
                else:
                    try:
                        print('Closable : ' + x)
                        raise SyntaxError
                    except SyntaxError:
                        etype, value, tb = sys.exc_info()
                        message = ''.join(traceback.format_exception(etype, value, tb))
                        print(message.split('\n')[0] + '\n  ' + '...' + codeString[
                                                                        i - 3 if i - 3 > 0 else 0:i + 3] + '...' + '\n' + ' ' * (
                                      i + (len(codeString) if len(
                                  codeString) < 6 else 6)) + '^' + '\nSyntaxError: unexpected "' + x + '" at pos ' + str(
                            i),
                              file=sys.stderr)
                        sys.exit(1)
            if any(testNeedingValueKeys):
                j = 0
                while j < 3:
                    if codeString[i + 1:i + j] in '"0123456789' and quotesCheck == -1:
                        break
                    j += 1
                if j == 2:
                    try:
                        print('Needingvalue : ' + codeString[i + 1:i + 1 + len(needingValueKeys[testNeedingValueKeys.index(True)])])
                        raise SyntaxError
                    except SyntaxError:
                        etype, value, tb = sys.exc_info()
                        message = ''.join(traceback.format_exception(etype, value, tb))
                        print(message.split('\n')[0] + '\n  ' + '...' + codeString[
                                                                        i - 3:i + 3] + '...' + '\n' + ' ' * 8 + '^' + '\nSyntaxError: invalid syntax (pos ' + str(
                            i) + ')', file=sys.stderr)
                        sys.exit(1)
            elif x in list(closablesKeys.keys()) and quotesCheck == -1:
                closablesKeys[x] += 2 if any(x.endswith(j) for j in '("[') else 1
            elif (temp + x).endswith('?{') and quotesCheck == -1:
                closablesKeys['{'] += 2
            elif x in list(closingKeys.keys()) and quotesCheck == 1:
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
                    print(message.split('\n')[0] + '\n  ' + codeString + '\nSyntaxError: inconsistent use of "' + str(
                        i) + '" (' + str(abs(int(x / 2) if (x > 0 or i in '("{[') else x)) + (
                              ' too much' if x > 0 else ' missing') + ')',
                          file=sys.stderr)
                    sys.exit(1)

    def interpret(self, codeString):

        # Verifies if good syntax
        self.codeString = codeString + ' '
        self.verify(self.codeString)

        # Interprets
        while self.i < len(self.codeString):
            self.x = self.codeString[self.i]
            try:
                if self.codeString[self.i + 1] in '+-{(=/*':
                    self.i += 1
                    self.x = self.codeString[self.i - 1:self.i + 1]
                    if self.x in ['/=', '?{']:
                        self.i += 1
                        self.x = self.codeString[self.i - 2:self.i + 1]
                        if self.x not in ['>/=', '</=', '!/=', ']?{']:
                            self.i -= 1
                            self.x = self.codeString[self.i - 1:self.i + 1]
                    elif self.x not in ['++', '--', '//', '**', '?{', '~{', '>{', '>=', '<=', '!=', '*=',
                                        '/=', '!/', '&/', '|/']:
                        self.i -= 1
                        self.x = self.codeString[self.i]
            except IndexError:
                pass
            if self.x in self.methods.keys():
                self.tempvalue = self.memory[self.pointer]
                # noinspection PyPep8,PyBroadException
                try:
                    print(str(self.methods[self.x]))
                    self.methods[self.x]()
                except:
                    etype, value, tb = sys.exc_info()
                    message = ''.join(traceback.format_exception(etype, value, tb))
                    print(message.split('\n')[0] + '\n  ' + '...' + codeString[
                                                                    self.i - 3:self.i + 3] + '...' + '\n' + ' ' * 8 + '^\n' +
                          message.split('\n')[-2] + ' (pos ' +
                          str(self.i) + ')', file=sys.stderr)
                    sys.exit(1)
            self.i += 1


if __name__ == '__main__':
    # todo : GUI (or maybe IDE)
    # todo : Multiprocessing
    # todo : OOP
    # todo : Import
    # todo : read/write in file
    codeString = '3**2.'

    i = Interpreter()
    i.interpret(codeString)
