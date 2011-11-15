import model, http_request

class Page(model.Model):
	_name = 'page'
	_create_table = """
	create table `page` (
		name varchar(180) primary key,
		html text,
		markdown text,
		css text,
		js text,
		_updated timestamp
	) engine=InnoDB
	"""
	
	def __init__(self, obj):
		super(Page, self).__init__(obj)
		
	def after_post(self):
		"""generated html pages"""
		import pages
		ret = pages.make()
		if http_request.req:
			http_request.req.out['log'] = ret