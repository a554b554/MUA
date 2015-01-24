var_namespace = []
class Varible:
	def __init__(self):
		self.name = "nil"
		self.type = "nil"
		self.value = 0



class Function:
	def __init__(self):
		self.name = "nil"
		self.argc = 0
		self.argv = []
		self.codelist = []
import copy

a = [1,2,3,45,65,67,7]
b = ['a','b','c']
b.reverse()
print a
for x in b:
	a.insert(2,x)

print a