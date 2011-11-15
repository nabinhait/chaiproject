import model

class User(model.Model):
	create_table = """
	create table `user` (
		name varchar(180) primary key,
		fullname, varchar(240),
		email varchar(180),
		_updated timestamp,
	) engine=InnoDB
	"""	
	
	def __init__(self, obj):
		super(User, self).__init__(obj)
		
	def before_post(self):
		"""save password as sha256 hash"""		
		import hashlib
		if 'password' in self.obj and len(self.obj['password']!=64):
			self.obj['password'] = hashlib.sha256(self.obj['password']).hexdigest()
		
		# clear re-entered password
		if 'password_again' in self.obj:
			del self.obj['password_again']
			
	def before_get(self):
		"""hide password"""
		if 'password' in self.obj:
			del self.obj['password']