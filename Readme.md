Life is Short, I use MUA#


#MUA#

MUA interpreter V1.0 

`Developer`: DarkTango

`useage`:python mua.py [filename]

what is MUA?

# MakeUp Programming Language

## Basic Value Type



* `number`: begin with `[0~9]` or `-`, no difference between float and int.
* `word`: start with `"`, unicode encoding.
* `list`：start with `[]` , use `,` to split element；elements in list can be any and different type.

## Basic Operation


###Basic Format
[operator] [arguments]

Operator is a word without space. Each operator can have any numbers of arguments, arguments split by space.

###Basic Funtion

* `//`: comments
* `make <word> <value>`： assign value to word and add word to namespace.
* `thing <word>`: return the value of word.
* `: <word>`: the same as `thing`.
* `erase <word>`: erase "word" from namespace.
* `isname <word>`: return the bool value that if word is exist in namespace.
* `print <value>`: print the value.
* `read`: read a value or string from stdin.
* `readlinst`: read a line from stdin and combine them to a list.
* arithmatic operator
    * `add`, `sub`, `mul`, `div`, `mod`：`<operator> <number> <number>`
	* `eq`, `gt`, `lt`：`<operator> <number|word> <number|word>`
	* `and`, `or`：`<operator> <bool> <bool>`
	* `not`：`not <bool>`
* `random <number>`: return a random number from [0, number).
* `sqrt <number>`: return sqrt(number)
* `isnumber <value>`": return a bool value that if the value is a number 
* `isword <value>`: is a word?
* `islist <value>` is a list?
* `isbool <value>` is a boolean?
* `isempty <word|list>`: is a list empty?
* `test <value>`：return the bool of value
* `iftrue <list>`: if last test is true, excute the code in list.
* `iffalse <list>`: if last test if false, excute the code in list.
* `word <word> <word|number|bool>`: combine two word into one word.
* `list <list1> <list2>`: combine two list into one list.
* `join <list> <value>`: append value into the end of list.
* `first <word|list>`: return the first element of list/word.
* `last <word|list>`: return the last element of list/word.
* `butfirst <word|list>`: return the whole word/list except the first element.
* `butlast <word|list>`: return the whole word/list except the last element. 
* `item <number> <word|list>`: return the number's index element of word/list.
* `repeat <number> <list>`: excute the code in list number times.
* `stop`: stop the excution in a list.
* `wait <number>`: wait number second.
* `save <word>`: save the namespace in filesystem.
* `load <word>`: load the namespace from filesystem.
* `erall`: clear namespace.
* `poall`: list the namespace.

## Define and Call a Function

### Define

		make <word> [<list1> <list2>]
			word: function name
			list1: arguments list
			list2: operation list

### Call

		<functionName> <arglist>
			<functionName> name of funtion
			<arglist>arguments list 


## Built-in value


* `pi`：3.14159
* `if <bool> <list1> <list2>`: if bool is true, then excute list1, otherwise excute list2.
* `run <list>`: run code in list.


