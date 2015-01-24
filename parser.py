import string
import namespace
import random
import math
import lex
import copy
token=[]
test_stack=[]
pc_stack=[]
BinaryOP = ('add','sub','mul','div','mod','eq','gt','lt','and','or','word','list','join')
UnaryOP = ('not','isnumber','isword','random','sqrt','islist','isbool','isempty','test','save','load','first','last','butfirst','butlast')
def isBinaryOP(token):
	for op in BinaryOP:
		if token == op:
			return True
	return False

def isUnaryOP(token):
	for op in UnaryOP:
		if token == op:
			return True
	return False

def getType(obj):
	tp = type(obj)
	if tp == type([]):
		return 'list'
	elif tp == type(0.3):
		return 'number'
	elif tp == type('s'):
		return 'word'
	elif tp == type(True):
		return 'bool'

def getIndexFromNamespace(var_name):
	for var in namespace.var_namespace:
		#print "varname",var.name,var_name
		if var.name == var_name:
			return namespace.var_namespace.index(var)

	return -1

def execute():
	i = 0
	while i < len(token[-1]):
		parse(i)
		i = i + 1
	


def parse(index):
	
	print "parse!",index,token[-1][index],"namespace:",namespace.var_namespace
	tp = type(token[-1][index])
	name_id = getIndexFromNamespace(token[-1][index])
	"""print "name_id:",name_id,tp
	if type(name_id) != bool:
		print "get!"
		token[-1][index] = namespace.var_namespace[name_id].value"""
	

	if tp == type(1.0) or tp == type(False) or tp == type([]):
		return token[-1][index]


	elif token[-1][index][0].isdigit() or token[-1][index][0]=='-':
		return string.atof(token[-1][index])
	# if token is string
	elif token[-1][index][0] == '"':
		return token[-1][index][1:]
	#if token is list
	elif token[-1][index][0] == '[':
		pass#parse the quote ,convert string to list

	#if token is arithmetic operation

	elif isBinaryOP(token[-1][index]):
		op1 = parse(index+1)	
		op2 = parse(index+2)

		del token[-1][index+2]
		del	token[-1][index+1]
		if token[-1][index] == 'add':
			token[-1][index] = op1 + op2
		elif token[-1][index] == 'sub':
			token[-1][index] = op1 - op2

		elif token[-1][index] == 'mul':
			token[-1][index] = op1 * op2

		elif token[-1][index] == 'div':
			token[-1][index] = op1/op2

		elif token[-1][index] == 'mod':
			token[-1][index] = float(int(op1)%int(op2))

		elif token[-1][index] == 'eq':
			token[-1][index] = (op1 == op2)

		elif token[-1][index] == 'gt':
			token[-1][index] = (op1 > op2)


		elif token[-1][index] == 'lt':
			token[-1][index] = (op1 < op2)


		elif token[-1][index] == 'and':
			token[-1][index] = op1 and op2


		elif token[-1][index] == 'or':
			token[-1][index] = op1 or op2

		elif token[-1][index] == 'word':
			token[-1][index] = str(op1)+str(op2)

		elif token[-1][index] == 'join':
			if getType(op1) == 'list':
				op1.append(op2)
				token[-1][index] = True
			else :
				print "semantic error:" + op1.name + "is not list"
				exit(0)


		elif token[-1][index] == "list":
			tmp = []
			for elem in op1:
				tmp.append(elem)
			for elem in op2:
				tmp.append(elem)

			token[-1][index] = tmp

		elif token[-1][index] == 'item':
			token[-1][index] = op2[op1]

	# other command
	
	elif token[-1][index] == "make":
		a = namespace.Varible()
		a.name = parse(index+1)
		op = parse(index+2)
		a.type = getType(op)
		a.value = op
		#print "1",namespace.var_namespace
		namespace.var_namespace.append(a)
		#print "2",namespace.var_namespace
		del token[-1][index+2]
		del token[-1][index+1]
		token[-1][index] = True
		

	elif token[-1][index] == "thing" or token[-1][index] == ':':
		token[-1][index] = parse(index+1)
		del token[-1][index+1]

	elif token[-1][index] == "erase":
		#print token[-1][index+1]
		del_id = getIndexFromNamespace(token[-1][index+1])
		#print del_id
		del token[-1][index+1]
		if del_id == -1:
			print "undefined Varible"
			exit(0)
		del namespace.var_namespace[del_id]
		token[-1][index] = True


	elif token[-1][index] == "isname":
		op = parse(index+1)
		del token[-1][index+1]
		flag = False
		for var in namespace.var_namespace:
			if op == var.name:
				flag = True
				break
		token[-1][index] = flag

	elif token[-1][index] == "print":
		op = parse(index+1)
		del token[-1][index+1]
		print op
		token[-1][index] = True

	elif token[-1][index] == "read":
		op = raw_input()
		if op[0] == '"':
			token[-1][index] = op[1:]
		else :
			token[-1][index] = string.atof(op)

	elif token[-1][index] == "readlinst":
		op = raw_input()
		returnlist = []
		elements = op.split()
		for element in elements:
			if element[0] == '"': #is word
				returnlist.append(element[1:])
			else :
				returnlist.append(string.atof(element))
		token[-1][index] = returnlist

	elif token[-1][index] == "iftrue":
		testflag = test_stack.pop()
		op = parse(index+1)
		if testflag == True:
		 	pc_stack.append(index)
		 	token.append(op)
		 	index = 0
		 	execute()
		 	index = pc_stack.pop()
		 	token.pop()
		else:
		 	token[-1][index] = False

	elif token[-1][index] == "iffalse":
		testflag = test_stack.pop()
		op = parse(index+1)
		if testflag == False:
			pc_stack.append(index)
			token.append(op)
			index = 0
			execute()
			index = pc_stack.pop()
			token.pop()
		else:
			token[-1][index] = False

	elif isUnaryOP(token[-1][index]):

		op = parse(index+1)
		del token[-1][index+1]

		if token[-1][index] == "random":	
			token[-1][index] = random.random() * op

		elif token[-1][index] == "sqrt":
			token[-1][index] = math.sqrt(op)

		elif token[-1][index] == 'not':
			token[-1][index] = not op1

		elif token[-1][index] == "isnumber":
			if getType(op) == 'number':
				token[-1][index] = True
			else :
				token[-1][index] = False

		elif token[-1][index] == "isword":
			if getType(op) == "word":
				token[-1][index] = True
			else :
				token[-1][index] = False

		elif token[-1][index] == "islist":
			if getType(op) == "list":
				token[-1][index] = True
			else :
				token[-1][index] = False

		elif token[-1][index] == "isbool":
			if getType(op) == "bool":
				token[-1][index] = True
			else :
				token[-1][index] = False

		elif token[-1][index] == "isempty":
			if op == "" or op == []:
				token[-1][index] = True
			else:
				token[-1][index] = False

		elif token[-1][index] == "test":
			if getType(op) != "bool":
				print "semantic error: "+str(op)+ "is not bool"
				exit(0)
			else :
				if op:
					test_stack.append(True)
					token[-1][index] = True
				else :
					test_stack.append(False)
					token[-1][index] = False

		elif token[-1][index] == "save":
			file_obj = open(op+'.m','w')
			for var in namespace.var_namespace:
				file_obj.write(var.name+" "+var.type+" "+str(var.value))
			file_obj.close()

		elif token[-1][index] == "load":
			pass
			#wait for implement

		elif token[-1][index] == "first":
			token[-1][index] = op[0]

		elif token[-1][index] == "last":
			token[-1][index] = op[-1]

		elif token[-1][index] == 'butfirst':
			token[-1][index] = op[1:]

		elif token[-1][index] == 'butlast':
			token[-1][index] = op[:-1]
	#if index < len(token[-1])-1:
	#	parse(index+1)
	for var in namespace.var_namespace:
		if token[-1][index] == var.name:
			return var.value

	for func in namespace.func_namespace:
		if token[-1][index] == func.name:
			the_fun = copy.deepcopy(func)
			op = []
			for c in range(func.argc):
				op.append(parse(index+c+1))

			#pass by value
	return token[-1][index]




code = 'make "f 123 print add : f 1'
token.append(lex.lex(code))
execute()

"""
token.append(lex.splitword(code))
print code
print token[-1]

print namespace.var_namespace"""
