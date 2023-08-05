__version__ = '0.1.1'


def timer(func):
	import time
	'''
	Decorator which prints the time it takes the function to run.
	@time
	def timed_function():
	'''
	def wrapper(*args, **kwargs):
		begin = time.time()
		run = func(*args, **kwargs)
		print("Time: " + str(begin-time.time()))
		return run
	
	return wrapper

class Recorder:
	def __init__(self, *args):
		self.clicks = {}
		for x in args:
			self.clicks[x] = 0

	
	def click(self, k=None): 
		if k == None:
			for y, x in self.clicks.items():
				x += 1
				self.clicks[y] = x
			return self.clicks
		try:
			self.clicks[k] += 1
		except ValueError:
			raise ValueError('The identifier which you listed was not correct.')
		return self.clicks[k]
		
	def clicks(self):
		return self.clicks

class Validate:
	def string(func):
		def wrapper(*args, **kwargs):
			function = func(*args, **kwargs)

			if not isinstance(function, str):
				raise TypeError("Function return should be string type instead it is " + str(type(function)))
			return function
		
		return wrapper

	def integer(func):
		def wrapper(*args, **kwargs):
			function = func(*args, **kwargs)

			if not isinstance(function, int):
				raise TypeError("Function return should be float type instead it is " + str(type(function)))
			return function
		
		return wrapper

	def decimal(func):
		def wrapper(*args, **kwargs):
			function = func(*args, **kwargs)

			if not isinstance(function, float):
				raise TypeError("Function return should be int type instead it is " + str(type(function)))
			return function
		
		return wrapper

	def none(func):
		def wrapper(*args, **kwargs):
			function = func(*args, **kwargs)

			if function != None:
				raise TypeError("Function return should be none type instead it is " + str(type(function)))
			return function
		
		return wrapper

	def true(func):
		def wrapper(*args, **kwargs):
			function = func(*args, **kwargs)

			if function != True:
				raise TypeError("Function return should be true instead it is " + str(type(function)))
			return function
		
		return wrapper

	def false(func):
		def wrapper(*args, **kwargs):
			function = func(*args, **kwargs)

			if function != True:
				raise TypeError("Function return should be false instead it is " + str(type(function)))
			return function
		
		return wrapper

def system():
	'''
	System. Returns mac, linux, win32, or win64
	'''
	from sys import platform as pf
	
	if pf == 'linux':
		return 'linux'
	elif pf == 'mac':
		return 'mac'
	elif pf == 'win32':
		return 'win32'
	elif pf == 'win64':
		return 'win64'


class DB:
	def __init__(self, db_type):
		if db_type == dict:
			self.db_type = dict
			self.db = {}
		elif db_type == list:
			self.db_type = list
			self.db = []
		else:
			raise TypeError('db_type cannot be used as database type. only working types are list type and dict type.')
	def add(self, *args, **kwargs):
		if self.db_type == dict:
			for k, v in kwargs.items():
				self.db[k] = v
		elif self.db_type == list:
			for v in args:
				self.db.append(v)
	def view(self, k):
		if self.db_type == dict:
			return self.db[k]
		elif self.db_type == list:
			return self.db[k]		

class Class2List:
	def dict(self):
		method_list = []
		for attribute in dir(self):
			if attribute[0:2] != '__' and attribute != 'dict':
				method_list.append(attribute)
		return method_list
