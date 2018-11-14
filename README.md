# KidoScript

A smooth and fast writing language based on BrainFuck (but much simpler dw)

## Docs :

- Values are directly attributed to the memory case at pointer position
- Pointer is by default at first memory case
- There's no `null`, `undefined` or `None` equivalents are 0 and "" is weakly equal to 0
- Here's an Hello World ! : `"Hello World !".`
- There's no real booleans, results of comparison are 1 if `True` and 0 if `False`
- All other characters not in the keys below (basically all characters not enclosed in double quotes) won't be used and will be like commentaries

- KidoScript isn't yet supporting Floating Values, Value Structures, Unicode and Object Oriented Programmation but that's to go (except for Value Structures 'cause it's already using a big one)
- Virtual Memories can also be a way to go (and a replacement for advanced Value Structures)

### Base Keys :

- `,` : 				Scan from console to memory case at pointer position
- `.` : 				Print what's in memory case at pointer position in console
- `>` : 				Move pointer to right
- `<` : 				Move pointer to left
- `+` : 				Increment memory case at pointer position from 1
- `-` : 				Decrement memory case at pointer position from 1
- `\d` : 				(Any decimal) : Change value of memory case at pointer position
- `"Some String"` : 	Change value of memory case at pointer position by a string (store in the number of bytes in ASCII) (care to reserved word `func:`)
- `++` : 				Addition operator
- `--` : 				Substraction operator
- `*` : 				Multiplication operator
- `/` : 				Dividing operator
- `%` :					Modulo operator
- `#` :					Go to first memory case
- `;` :					Go to last memory case

### Structures :

- `[ PrintPointerOfStartEnd&Step ]{ CodeToLoop }` : 				For loop (End or Start and End or Start and End and Step)
- `[ Condition ]?{ CodeToLoop }` : 									While loop
- `Condition ?{ CodeToExecutreIfTrue : CodeToExecuteIfFalse}` : 	If Else Elseif structure (else is optionnal)
- `{ PrintArgumentsPositionInMemory { CodeToExecuteAsFunction }` : 	Store a function at memory case (as string starting by `func:`)
- `( PointerDeplacement )` :										Vector to move value of memory case at pointer position by PointerDeplacement (																			accept only loops and pointer deplacement keys), it can also be used in operations 																		to select another value than the one in the actual memory case. The pointer isn't 																		moving though
- `~( PointerDeplacement )` :										Copy value of memory case at pointer position by PointerDeplacement (idem)
- `$` : 															Return value from function in memory case (need to be launched in another memory 																		case and is exactly like `^` if isn't in function)
- `^` :																Execute code from stored function (or do same as ,)
- `@` : 															Evaluate code in string in memory case at pointer position like a function

### Weak comparison (comparing with value processing) : 

- `=` : 	Equality comparison
- `>=` : 	Greater Than or Equal comparison
- `<=` : 	Lesser Than or Equal comparison
- `!=` : 	Non equality comparison
- `!` : 	Non gate
- `&` : 	And gate
- `|` : 	Or gate

### Strong comparison (comparing ascii or global values) :

- `*=` : 	Sum comparison (comparing global added values)
- `/=` : 	Equality comparison
- `>/=` : Greater Than or Equal comparison
- `</=` : Lesser Than or Equal comparison
- `!/=` : Non equality comparison
- `!/` : 	Non gate
- `&/` : 	And gate
- `|/` : 	Or gate