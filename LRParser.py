import lex
import string
import random
import math
import copy
tokens = []   # token is the parsing object. We use LR parsing algorithm to interpret the tokens. token[-1] is the top tokens on the stack.
namespaces = [{}] # namespaces is a stack store the namespace, namespace is a dict which map a word to a value.
pc_stack = [] # pc_stack store the program counter before call a funtion.
test_stack = [] # test_stack store the result of test.
ArithmeticOP = ('add', 'sub', 'mul', 'div', 'mod','equ', 'gt', 'lt','and', 'or')

def isArithOP(token):
	for op in ArithmeticOP:
		if token == op:
			return True
	return False

def getValue(word):
	i = 1
	while i <= len(namespaces):
		if namespaces[-i].has_key(word):
			return namespaces[-i][word]
		else:
			i = i + 1
	return None


def parse(index): # main function for parsing, call it recursively
	c_token = tokens[-1][index]
	tp = type(c_token)
	print 'token:',c_token,'index',index
	if tp == type(True) or tp == type(1.0) or tp == type([]):
		return c_token

	if tp == type('abc'):
		if c_token[0] == '"':
			return c_token

		elif c_token == 'make':
			word = parse(index + 1)
			word = word[1:]  # remove "
			val = parse(index + 2)
			print 'word:',word,'val:',val
			del tokens[-1][index + 2]
			del tokens[-1][index + 1]
			namespaces[-1][word] = val

		elif c_token == 'test':
			flag = parse(index + 1)
			test_stack.append(flag)
			del tokens[-1][index + 1]

		elif c_token == ':' or c_token == 'thing':
			val = getValue(tokens[-1][index + 1])
			del tokens[-1][index + 1]
			print 'val',val
			if val == None:
				print 'undefined name',c_token
				exit(0)
			else:
				return val

		elif c_token == 'iftrue':
			flag = test_stack.pop()
			tokenlist = parse(index + 1)
			
			del tokens[-1][index + 1]
			if type(tokenlist) != type([]):
				print 'iftrue can only excute list'
				exit(0)
			if flag == True:
				tokenlist.reverse() # reverse the list for calling insert with a correct order.
				for x in tokenlist:
						tokens[-1].insert(index + 1,x)
						#print tokens[-1]


		elif c_token == 'output':
			output = parse(index + 1)
			del tokens[-1][index + 1]
			tokens[-1][0] = output

		elif c_token == 'stop':
			del tokens[-1][index:]

		elif c_token == 'print':

			val = parse(index + 1)
			del tokens[-1][index + 1]
			print 'print!!!'
			print val

		elif getValue(c_token) != None:   # function
			code = copy.deepcopy(getValue(c_token))
			argc = len(code[0]) # the number of argument.
			new_space = {}
			arg = []       #store argument
			for i in range(argc):
				arg.append(parse(index+i+1))  # code[0] is the parameter list, while code[1] is the code to run.

			i = argc
			while i > 0:
				del tokens[-1][index+i]   
				i = i - 1

			i = 0
			for para in code[0]:
				new_space[para] = arg[i]
				i = i + 1
			namespaces.append(new_space) # push the local namespace onto stack.
			tokens.append(code[1]) # push the local program onto stack.
			# excute code
			i = 0
			while i < len(tokens[-1]):
				parse(i)
				i = i + 1
			# receive return value
			return_value = tokens[-1][0]
			namespaces.pop()   # maintain the stack by caller
			tokens.pop()
			return return_value




		# arithmetic op
		elif isArithOP(c_token):
			op1 = parse(index + 1)
			op2 = parse(index + 2)
			del tokens[-1][index + 2]
			del tokens[-1][index + 1]
			if c_token == 'equ':
				if op1 == op2:
					return True
				else:
					return False
			elif c_token == 'add':
				return op1 + op2
			elif c_token == 'sub':
				return op1 - op2
			elif c_token == 'mul':
				return op1 * op2
			elif c_token == 'div':
				return op1 / op2
			elif c_token == 'mod':
				return float(int(op1)%int(op2))
			elif c_token == 'gt':
				return op1 > op2
			elif c_token == 'lt':
				return op1 < op2
			elif c_token == 'and':
				return op1 and op2
			elif c_token == 'or':
				return op1 or op2
	

def execute():
	i = 0
	while i < len(tokens[0]):
		parse(i)
		i = i + 1


file_obj = open('aa.mua')
code = file_obj.read()
code = lex.lex(code)
tokens.append(code)
execute()
print code
