"""
WSGI handler
============

WSGI server for handling dynamic reqeusts. The requests will be directly passed
on to the relevant python module to be executed and response will be in json.

The method to be called must be explicitly allowed by calling the @whitelist decorator.

method="package.module.method"

the query_string and environ will be passed to the method
"""

def handle():
	"""handle the request"""
	from lib.py import req, database
	import sys
		
	# execute a method
	if '_method' in req.params:
	
		parts = req.params['_method'].split('.')
		module = '.'.join(parts[:-1])
		method = parts[-1]
	
		# import the module
		__import__(module)
	
		from lib.py import whitelisted
					
		if module in sys.modules:
			# check if the method is whitelisted
			if getattr(sys.modules[module], method) not in whitelisted:
				return {"error":"Method `%s` not allowed" % method}

			# execute
			if req.method=='POST':
				database.conn.begin()
				
			t = getattr(sys.modules[module], method)(**req.params)

			if req.method=='POST':
				database.conn.commit()

			return t or {"message":"no response"}
		else:
			return {"error":"Unable to load method"}
	else:
		return {"error":"Request must have method"}

def json_type_handler(obj):
	"""convert datetime objects to string"""
	if hasattr(obj, 'strftime'):
		return str(obj)

def setup_request(environ):
	"""setup global req, res"""
	from webob import Request, Response
	import lib.py
	
	# clear session
	lib.py.out = {}
	lib.py.sess = {}
	lib.py.req = Request(environ)
	lib.py.res = Response()

def application(environ, start_response):
	import json

	setup_request(environ)
	
	import lib.py
	from lib.py import database, req, res
	# start db connection
	db = database.get()

	if '_method' in req.params and req.params['_method'] != 'lib.py.session.login':
		import lib.py.session
		lib.py.sess = lib.py.session.load()
	
	res.content_type = 'text/html'
	
	try:
		out = handle()
		lib.py.out.update(out)
	except Exception, e:
		from lib.py.common import traceback
		lib.py.out['error'] = str(traceback())
		
	if not res.body:
		if type(lib.py.out) is str:
			res.body = lib.py.out
		else:
			res.body = json.dumps(lib.py.out, default=json_type_handler)
		
	db.close()
	
	return res(environ, start_response)
	