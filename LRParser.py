import lex
import string
import random
import math
import copy
import time
tokens = []   # token is the parsing object. We use LR parsing algorithm to interpret the tokens. token[-1] is the top tokens on the stack.
namespaces = [{}] # namespaces is a stack store the namespace, namespace is a dict which map a word to a value.
pc_stack = [] # pc_stack store the program counter before call a funtion.
test_stack = [] # test_stack store the result of test.
ArithmeticOP = ('add', 'sub', 'mul', 'div', 'mod','eq', 'gt', 'lt','and', 'or')

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
	#print 'token:',c_token,'index',index
	if tp == type(True) or tp == type(1.0) or tp == type([]):
		return c_token

	if tp == type('abc'):
		if c_token[0] == '"':
			return c_token

		elif c_token == 'make':
			word = parse(index + 1)
			word = word[1:]  # remove "
			val = parse(index + 2)
			#print 'word:',word,'val:',val
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
			#print 'val',val
			if val == None:
				print 'undefined name',c_token
				exit(0)
			else:
				return val

		elif c_token == 'iftrue':
			flag = test_stack.pop()
			tokenlist = parse(index + 1)
			#print 'flag:',flag
			del tokens[-1][index + 1]
			if type(tokenlist) != type([]):
				print 'iftrue can only excute list'
				exit(0)
			if flag == True:
				tokenlist.reverse() # reverse the list for calling insert with a correct order.
				for x in tokenlist:
						tokens[-1].insert(index + 1,x)
						#print tokens[-1]

		elif c_token == 'iffalse':
			flag = test_stack.pop()
			tokenlist = parse(index + 1)
			
			del tokens[-1][index + 1]
			if type(tokenlist) != type([]):
				print 'iffalse can only excute list'
				exit(0)
			if flag == False:
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
			#print '*********************************print***********************'
			print val

		elif c_token == 'erase':
			word = parse(index+1)
			del tokens[-1][index+1]
			word = word[1:]
			del namespaces[-1][word]


		elif c_token == 'isname':
			word = parse(index+1)
			del tokens[-1][index+1]
			ans = getValue(word)
			if ans == None:
				return False
			else:
				return True

		elif c_token == 'read':
			a = raw_input()
			if a[0] == '-' or a[0].isdigit():
				return float(a)
			else:
				return a

		elif c_token == 'random':
			rag = parse(index+1)
			del tokens[-1][index+1]
			return random.random()*rag

		elif c_token == 'sqrt':
			num = parse(index+1)
			del tokens[-1][index+1]
			return math.sqrt(num)

		elif c_token == 'isnumber':
			num = parse(index+1)
			del tokens[-1][index+1]
			if type(num) == type(1.0):
				return True
			else:
				return False

		elif c_token == 'isword':
			wd = parse(index+1)
			del tokens[-1][index+1]
			if type(wd) == type('abc'):
				return True
			else:
				return False

		elif c_token == 'islist':
			wd = parse(index+1)
			del tokens[-1][index+1]
			if type(wd) == type([]):
				return True
			else:
				return False

		elif c_token == 'isbool':
			wd = parse(index+1)
			del tokens[-1][index+1]
			if type(wd) == type(True):
				return True
			else:
				return False

		elif c_token == 'isempty':
			op = parse(index+1)
			del tokens[-1][index+1]
			if op:
				return False
			else:
				return True

		elif c_token == 'word':
			op1 = parse(index+1)
			op2 = parse(index+2)
			del tokens[-1][index+2]
			del tokens[-1][index+1]
			return op1 + str(op2)

		elif c_token == 'list':
			op1 = parse(index+1)
			op2 = parse(index+2)
			del tokens[-1][index+2]
			del tokens[-1][index+1]
			if op1 and op2:
				return op1 + op2
			elif op1:
				return op1
			else:
				return op2

		elif c_token == 'join':
			op1 = parse(index+1)
			op2 = parse(index+2)
			del tokens[-1][index+2]
			del tokens[-1][index+1]
			op1.append(op2)
			#print 'join result:',op1
			return op1

		elif c_token == 'first':
			op = parse(index+1)
			del tokens[-1][index+1]
			return op[0]

		elif c_token == 'last':
			op = parse(index+1)
			del tokens[-1][index+1]
			return op[-1]

		elif c_token == 'butfirst':
			op = parse(index+1)
			del tokens[-1][index+1]
			return op[1:]

		elif c_token == 'butlast':
			op = parse(index+1)
			del tokens[-1][index+1]
			return op[:-1]

		elif c_token == 'item':
			op1 = parse(index+1)
			op2 = parse(index+2)
			del tokens[-1][index+2]
			del tokens[-1][index+1]
			return op2[op1]

		elif c_token == 'repeat':
			repeattime = parse(index+1)
			codelist = parse(index+2)
			del tokens[-1][index+2]
			del tokens[-1][index+1]
			codelist.reverse()
			for i in range(int(repeattime)):
				for x in codelist:
					tokens[-1].insert(index + 1,x)

		elif c_token == 'wait':
			num = parse(index+1)
			del tokens[-1][index+1]
			time.sleep(num/1000)

		elif c_token == 'save':
			filename = parse(index+1)
			del tokens[-1][index+1]
			filename = filename[1:] + '.namespace'
			ff = open(filename,'w')
			for key in namespaces[-1]:
				ff.write(str(key)+':'+str(namespaces[-1][key])+' ')
			ff.close()

		elif c_token == 'load':
			filename = parse(index+1)
			del tokens[-1][index+1]
			filename = filename[1:] + '.namespace'
			ff = open(filename)
			text = ff.read()
			text = text.split()
			for elem in text:
				pair = elem.split(':')
				if pair[1][0] == '-' or pair[1][0].isdigit():
					pair[1] = float(pair[1])
				#print pair[0],pair[1]
				namespaces[-1][pair[0]] = pair[1]

		elif c_token == 'erall':
			namespaces[-1].clear()

		elif c_token == 'poall':
			for key in namespaces[-1]:
				print str(key)+':'+str(namespaces[-1][key])

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
			if c_token == 'eq':
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
	namespaces[0]['pi'] = 3.14159
	namespaces[0]['run'] = [['code'],['repeat',1,':','code']]
	while i < len(tokens[0]):
		parse(i)
		i = i + 1



def run(code):
	code = lex.lex(code)
	tokens.append(code)
	execute()
"""
file_obj = open('sort.mua')
code = file_obj.read()
code = lex.lex(code)
tokens.append(code)
execute()
file_obj.close()
"""

