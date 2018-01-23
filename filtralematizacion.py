import re
rx = re.compile("\d+")
save = open("lemaverbos2.txt","w")
with open("lemaverbos.txt") as f:
	for line in f:
		res = rx.search(line)
		if (not res):
			#print ("match")
			#print (line)
			save.write(line)
save.close()
