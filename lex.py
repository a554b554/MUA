import string
import copy
def splitword(code):
	code = code.replace('[',' [ ')
	code = code.replace(']',' ] ')
	code = code.replace(':',' : ')
	token = code.split()
	return token

def getnumber(inputlist):
	ans = []
	for elem in inputlist:
		if elem[0].isdigit() or elem[0]=='-':
			elem =  string.atof(elem)
		ans.append(elem)
	return ans
temp=[]

def resolve(inputlist):
	ans = []
	temp = []
	for elem in inputlist:
		if elem == '[':
			ans.append(elem)
		elif elem == ']':
			while 1:
				a = ans.pop()
				if a == '[':
					temp.reverse()
					ans.append(temp)
					temp = []
					break
				else:
					temp.append(a)
		else :
			ans.append(elem)
	return ans

def lex(code):
	token = splitword(code)
	token = getnumber(token)
	token = resolve(token)
	return token



""" E->EE
	E->[E]
	E->id






def parse_list(list):
	stack = [[]]
	depth = 0
	# Insert space
	token_set = list.replace('[',' [ ')
	token_set = token_set.replace(']',' ] ')
	token_set = token_set.split()
	# Implement Push Down Automata by using a explicit stack.
	for token in token_set:
		if token[0] == '[':
			stack.append([])
			depth = depth + 1
		elif token.isdigit() or token == '-':
			stack[depth].append(string.atof(token))
		elif token[0] == '"':
			stack[depth].append(token[1:])
		elif token[0] == ']':
			stack[depth-1].append(stack[depth])
			stack[depth]=[]
			depth = depth - 1

	return stack[0][0]"""
