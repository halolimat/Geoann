
import os
#def wrt(file):
#	# Open a file
#	file= file.encode("utf-8")
#	path ="/home/dipnot/Desktop/sample/"+file
#	fo = open(path, "wb")
#	fo.write( "Python is a great language.\nYeah its great!!\n");
#
#	# Close opend file
#	fo.close()
#
#def read(file):
#	file= file.encode("utf-8")
#	path ="/home/dipnot/Desktop/sample/"+file
#	fo = open(path, "r+")
#	str = fo.read();
#	# Close opend file
#	fo.close()
#	print os.path.splitext(file)[0]
#	return str
def remov(path,id):
	f = open(path,"r")
	lines = f.readlines()
	f.close()
	f = open(path,"w")
	for line in lines:
		l=line
		l = l.replace("\n", "").split("\t")
		if "G" not in l[0]:
			f.write(line)
		elif id != l[1]:
			f.write(line)
	f.close()


