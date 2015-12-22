import six




class StreamerException(Exception):

	def __init__(self, reason, response=None):
		self.reason = six.text_type(reason)
		self.response = response
		Exception.__init__(self, reason)

	def __str__(self):
		return self.reason

	@classmethod
	def handle_exception(e, func, *args, **kwargs):
		""" prints the exception along with the function name it occured in"""

		if type(func) == "instancemethod":
			func_name = func.__func__.__name__
		elif type(func) == "function":
			func_name = func.func_name
		else:
			func_name = "Uknown"
			print "handle_exception error. Dont know where this error occured. Error: {}".format(six.text_type(e))
		
		print "new exception {} in func {}".format(six.text_type(e), func_name)



