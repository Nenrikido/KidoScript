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

### Base Keys :

- `,` : 				Scan from console to memory case at pointer position
- `.` : 				Print what's in memory case at pointer position in console
- `>` : 				Move pointer to right
- `<` : 				Move pointer to left
- `+` : 				Increment memory case at pointer position from 1
- `-` : 				Decrement memory case at pointer position from 1
- `\d` : 				(Any integer decimal) : Change value of memory case at pointer position
- `"Some String"` : 	Change value of memory case at pointer position by a string (store in the number of bytes in ASCII)

- `++` : 				Addition operator
- `--` : 				Substraction operator
- `*` : 				Multiplication operator
- `/` : 				Dividing operator
- `%` :					Modulo operator
- `#` :					Go to first memory case
- `;` :					Go to last memory case

### Structures :

- `[ PrintPointerOfStartEnd&Step ]{ CodeToLoop }` : 				For loop (End or Start and End or Start and End and Step) (Execute code until the 																		changing value from the for loop has ended what's the for loop has initialized it 																		to do; The memory case at where it has been initializated countains the changing 																		value from the for loop)

- `[ Condition ]?{ CodeToLoop }` : 									While loop (Execute code until the condition in the while loop arguments aren't 																		anymore resolved)

- `Condition ?{ CodeToExecutreIfTrue : CodeToExecuteIfFalse}` : 	If Else Elseif structure (else is optionnal). It uses a weak conditionnal system so 																	`0` and `''` are equivalents to `False` and all the other values are equivalent to 																		`True` 

- `{ PrintArgumentsPositionInMemory { CodeToExecuteAsFunction }` : 	Stores a function at memory case (memory is now a virtual memory local to the function and argument passed are stored in first cases of this virtual memory)

- `>{ PointerDeplacement }` :										Vector to move value of memory case at pointer position by PointerDeplacement (																			accept only loops and pointer deplacement keys), it can also be used in operations 																		to select another value than the one in the actual memory case. The pointer isn't 																		moving though

- `~{ PointerDeplacement }` :										Copy value of memory case at pointer position by PointerDeplacement (idem)
- `$` : 															Return value from function in memory case (need to be launched in another memory 																		case and is exactly like `^` if isn't in function)

- `^` :																Execute code from stored function (or do same as ,)
- `@` : 															Evaluate code in string in memory case at pointer position like a function

### Weak comparison (comparing with value processing) : 

- `( LeftMember = RightMember )` : 	Equality comparison
- `( LeftMember >= RightMember )` : 	Greater Than or Equal comparison
- `( LeftMember <= RightMember )` : 	Lesser Than or Equal comparison
- `( LeftMember != RightMember )` : 	Non equality comparison
- `( LeftMember *= RightMember )` :    Sum comparison (comparing global added values, `"hello"*="leohl"` => 1)

- `( LeftMember!RightMember )` : 	Non gate
- `( LeftMember&RightMember )` : 	And gate
- `( LeftMember|RightMember )` : 	Or gate

### Strong comparison (comparing ascii values and types) :

- `( LeftMember /= RightMember )` :   Equality comparison
- `( LeftMember >/= RightMember )` :  Greater Than or Equal comparison
- `( LeftMember </= RightMember )` :  Lesser Than or Equal comparison
- `( LeftMember !/= RightMember )` :  Non equality comparison
- `( LeftMember !/ RightMember )` :   Non gate
- `( LeftMember &/ RightMember )` :   And gate
- `( LeftMember |/ RightMember )` :   Or gate