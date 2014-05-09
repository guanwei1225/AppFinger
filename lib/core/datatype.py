 # -*- coding: utf-8 -*
 #按照sqlmap写的，大概意思就是这样吧
"""
 	>>> foo = AttribDict()
    >>> foo.bar = 1
    >>> foo.bar
    1
"""

class advancedDict(dict):
	"""
	This class defines the sqlmap object, inheriting from Python data
	type dictionary.
	"""

	def __init__(self, indict=None, attribute=None):
		if indict is None:
			indict = {}

		# Set any attributes here - before initialisation
		# these remain as normal attributes
		self.attribute = attribute
		dict.__init__(self, indict)
		self.__initialised = True

		# After initialisation, setting attributes
		# is the same as setting an item

	def __getattr__(self, item):
		"""
		Maps values to attributes
		Only called if there *is NOT* an attribute with this name
		"""
		return self.__getitem__(item)

	def __setattr__(self, item, value):
		"""
		Maps attributes to values
		Only if we are initialised
		"""

		# This test allows attributes to be set in the __init__ method
		if not self.__dict__.has_key('_advancedDict__initialised'):
			return dict.__setattr__(self, item, value)

		# Any normal attributes are handled normally
		elif self.__dict__.has_key(item):
			dict.__setattr__(self, item, value)

		else:
			self.__setitem__(item, value)

