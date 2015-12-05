

def get_val(obj, key):
	try:
		value = obj[key]
	except KeyError, e:
		return None
	else:
		return value



def search_dictionary_for_certain_keys(key, dictionary):
	for k, value in dictionary.iteritems():
		if k == key or k.__contains__(key) or key.__contains__(k):
			return value
			
		else:
			if isinstance(value, dict):
				item = search_dictionary_for_certain_keys(key, value)
				if item is not None:
					return item
			elif isinstance(value, list):
				for i in value:
					if isinstance(i, dict):
						item = search_dictionary_for_certain_keys(key, i)
						if item is not None:
							return item