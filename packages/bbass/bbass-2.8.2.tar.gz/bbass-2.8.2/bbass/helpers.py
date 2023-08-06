import re
import json
import os.path



def dispose(string, *patterns, remove_edges=True):
	# remove_firsts=False, remove_lasts=False
	loop_count = 0
	if loop_count == len(patterns):
		return string
	
	p = re.compile(patterns[loop_count])
	parts = re.split(p, string)
	parts2 = [*filter(lambda part: len(part) > 1, parts)]
	parts3 = []

	if remove_edges:
		for part in parts2:
			part = part[1:] if part[0] == ' ' else part
			part = part[:-1] if part[-1] == ' ' else part
			parts3.append(part)

	string = ''.join(parts2) if parts3 == [] else ''.join(parts3)	
	loop_count += 1
	return dispose(string, *patterns[loop_count:], remove_edges=remove_edges)

def reduce_spaces(string):
	new_string = re.sub(r'\s\s', ' ', string)
	return new_string if new_string == string else reduce_spaces(new_string)

def present(path, name):
	from glob import iglob, glob
	sign = '/' if '/' in path else '\\'
	path = path[:-1] if path[-1] == sign else path
	songs_paths = iglob(f'{path}{sign}*')
	return any(filter(lambda file: f'{file.split(sign)[-1]}' == name, songs_paths))