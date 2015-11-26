import string

def hasNumber(stringToCheck):
	if any(char.isdigit() for char in stringToCheck):
		return(True)
	else:
		return(False)

def rmPunct(dirtyStr):
	splitCleanStr = [ch for ch in dirtyStr if ch not in string.punctuation]
	cleanStr = ''.join(splitCleanStr)
	return(cleanStr)