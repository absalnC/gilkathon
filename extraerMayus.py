import docx
import re
docs = []
docs.append("Evaluacion.docx")


#prefiltrado


lista =[]
contextos = []
licon=[]
#archivo con resultados
tosave= open("entidades.csv", "w")
#archivo auxiliar para revisar funcionamiento
test = open("output.txt","w")

def getSustantivos():
	'''funcion que lee los archivos y devuelve una tupla de sustantivos y parrafos'''
	sustantivos =[]
	contextos =[]
	rxentidad = re.compile(".*",re.UNICODE)
	for x in range(0,len(docs)):	
			document=docx.Document("{}".format(docs[x]))	
			for paragraph in document.paragraphs:
				res = rxentidad.search(paragraph.text)
				if res:
					#print("Match:")
					var=re.sub("[[a-záéíóéúñ]*]$","",res.group())
					sustantivos.append(var)
					contextos.append(paragraph.text)
					#print(var,"\n")
					#tosave.write("{}\n".format(var)
					#tosave.write("{}\n".format(paragraph.text))
					#print(paragraph.text)
	return zip(sustantivos,contextos)	
			
def getParentesis(sustantivos_contextos):
	''' funcion que identifica todos las entidades que estan seguidas de un 
		parentesis con abreviatura'''
	capitalized = "\"?(([A-Z][a-záéíóéúñ]+ ?)((a|del|las|,|sobre|de|el|la|los|para|y|e) ?)*){2,}\"?"
	decretos = "\“Decreto[^\(\)]*"
	acuerdos="\“Acuerdo[^\(\)]*"
	rx ="({0}((S.A. de C.V. ?)?|(S.A.B. de C.V. ?)?)|{1}|{2}) \([^\(\)]*\)".format(capitalized,decretos,acuerdos)

	rxparentesis=re.compile(rx)
	resContextos =[]
	resSustantivos = []
	for sust,cont in sustantivos_contextos:
		#print("searching:")
		#print(cont)
		res =  rxparentesis.finditer(cont)
		for match in res:
			print("match")
			print(match.group(0))
			resContextos.append(cont)
			resSustantivos.append(match.group(0))

	return zip(resSustantivos,resContextos)

def separar(licon):
	''' funcion que separa las cadenas obtenidas por getParentesis en entidad y abreviatura'''
	rxSust = re.compile("([^/(]+ ?)+")
	rxAbr = re.compile("\(.*\)")
	sustantivos = []
	contextos =[]
	abreviaturas =[]
	for sust,cont in licon:
		test.write("{}\n".format(sust))
		test.write("{}\n".format(cont))
		test.write("________________________\n")
		smatch = rxSust.search(sust)
		sustantivos.append(smatch.group())
		amatch = rxAbr.search(sust)
		abreviaturas.append(amatch.group())
		contextos.append(sust)
	return zip(sustantivos,abreviaturas,contextos)

def printLicon(licon):
	for sust,cont in licon:
		print(sust)
		print("CONTEXTO")
		print(cont)
		print("___________________________")
#obtener texto de archivos
licon =getSustantivos()
#obter entidad con parentesis con su contexto
licon=getParentesis(licon)
#obtener abreviatura con entidad
licon = separar(licon)
tosave.write("Contexto,Entidad,Abreviatura\n")
for sust,abr,cont in licon:
	sust = sust.replace("\"","")
	abr = abr.replace("\"","")
	cont = cont.replace("\"","")
	tosave.write('"{}","{}","{}"\n'.format(cont,sust,abr.replace("(","").replace(")","")))



'''for sust,cont in licon:
	#print("saving")
	#print(sust)
	tosave.write("{}\n".format(sust))
	tosave.write("{}\n".format(cont))'''
printLicon(licon)
test.close()
tosave.close()	