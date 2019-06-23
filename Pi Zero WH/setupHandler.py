setupFile = open("setup.txt", "r")
fileArray = (setupFile.read()).split('\n')

def getSetupParamNo(position):
	return (fileArray[position])
