files = []
files.append("Evaluacion.docx")
import re
import docx
import dateparser
import nltk
from nltk.corpus import cess_esp as cess

from nltk import UnigramTagger as ut

output = open("sucesosout.txt","w")
cess_sents = cess.tagged_sents()
uni_tag = ut(cess_sents)
'''se crea el etiquetador de palabras'''
def extractDates(parrafo):
	'''detecta y extrae las fechas de un parrafo,  
		devuelve la fecha y el parrafo en una tupla'''
	unoadiez = "(uno|dos|tres|cuatro|cinco|seis|siete|ocho|nueve|diez|primero)"
	parrafos = []
	sincreticas = "(once|doce|trece|catorce|quince|dieciséis|diecisiete|dieciocho|diecinueve|veinte|veintiuno|veintidós|veintitrés|veinticuatro|veinticinco|veintiséis|veintisiete|veintiocho|veintinueve)"
	decenas="(veinte|treinta|cuarenta|cincuenta|sesenta|setenta|ochenta|noventa)"
	miles = "((mil novecientos)|(dos mil))"
	dates = []
	dianorm="((\d)|([0-2]\d)|([3][01]))"
	mesabr = "(ene|feb|mar|abr|may|jun|julio|ago|sep|oct|nov|dic)"
	meslargo="((enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|octubre|noviembre|diciembre)|{}\.?)".format(mesabr)
	mesnorm= "(([0]?\d)|(1[12])|{})".format(mesabr)
	anionorm= "(\d\d\d\d)"
	fechanormal= "({0}(/|-){1}(/|-){2})".format(dianorm,mesnorm,anionorm)
	dialargo ="({0}|{1}|(treinta y uno))".format(unoadiez,sincreticas)
	aniolargo = "({0} ?({1} )?(y )?{2}?)".format(miles,decenas,unoadiez)
	fechalarga="(({0}|{1}) de {2} de ({3}|{4}))".format(dianorm,dialargo,meslargo,anionorm,aniolargo)
	#print("fecha larga")
	#print(fechalarga)
	#print("fecha normal")
	#print(fechanormal)
	#print ("fecha")
	fecha = "{0}|{1}".format(fechalarga,fechanormal)
	rx = re.compile(fecha)
	res = rx.search(parrafo)
	if res:	
		#print ("match")
		#print(res.group())
		return res.group(0)	
	else :
		return ""	
def extractVerb(parrafo):
	''' devuelve el primer verbo que encuentra en fecha'''	
	palabras = parrafo.split()
	#print("palabras")
	#print(palabras)
	tags = uni_tag.tag(palabras)
	#print("tags")
	#print(tags)	
	for x in range(len(tags)):		
		word,tag = tags[x]
		#print("word:",word)
		if( tag is not None and word is not None):
			if(tag == "vmis3s0" or tag == "vmis3p0"):
				return word
			else:								
				if (tag =="vsis3s0" or tag =="vsis3p0" ):
					#buscar participio en seguida
					nextw,nextt = tags[x+1]				
					if( nextt is not None and nextw is not None and (nextt =="vmp00sM" or nextt =="vmp00pM" or nextt =="vmp00sf" or nextt =="vmp00pf"
						or ( nextt[0]=='a' and nextt[5]=='p'))):				
						return nextw					
	rx = re.compile("autorizó|otorgó|remitió")
	res =	rx.search(parrafo)
	if res:
		return "autorizó"


def getParrafos(files):
	lista =[]
	for file in files:
		'''se espera que los documentos a tratar se encuentren en la carpeta documentos 
		que esta en la misma carpeta que el script'''
		doc = docx.Document("{}".format(file))
		for paragraph in doc.paragraphs:
			lista.append(paragraph.text)
	return lista

def filtraSucesos(parrafos):	
	''' se identifica un suceso por la presencia de fecha seguida de un verbo'''
	fecha = ""
	verbo = ""
	que =""
	sucesos = []
	for parr in parrafos:
		fecha = extractDates(parr)
		if(fecha != "" ):
			verbo = extractVerb(parr)
			que = getSujeto(parr,fecha,verbo)
			sucesos.append((parr,fecha,verbo,que))

	return sucesos

def getSujeto(parrafo,fecha,verbo):
	''' El sujeto siempre se encuentra entre la fecha y el verbo y ocupa todo ese espacio
		con excepcion de las formulas mediante y de conformidad'''
	inicio = "(({0}.*mediante[^,]*)|({0}.*de conformidad[^,]*)|{0})".format(fecha)	
	st = "{0}(.*){1}".format(inicio,verbo)
	#print("regex")
	#print (st)
	#rx = re.compile(st)
	parrafo =parrafo.replace(inicio,"")
	parrafo = parrafo.replace("{}.*".format(verbo),"")

	
	#print(rx)
	#res = rx.search(parrafo)
	'''
	if(res):
		print("match sujeto:\n")
		#print("longitud:",len(res.groups))
		que = res.groups(3)
		if(que is not None):			
			print (que)
			return que
			print("ZZZZZZZZZZZZZ\n")
		else:
			print("is none")
			print("ZZZZZZZZZZZZZ\n")
			return "" 
					
	return ""
	'''
	print("parrafo")
	print(parrafo)
	return parrafo
def getAQuien(parrafo,fecha,verbo):
	'''siempre despues del verbo y puede ser introducido por preposicion a o ante
		articulos y ...termina donde un articulo no precedido por preposicon o una conjuncion que 
		o la palabra escrito'''
	inicio = "{0} ((a)|(ante))".format(verbo)
	exp = ""
def getDonde(lista):
	''' Siempre introducido por preposicion en y esta despues del verbo'''
def getQue(lista):
	''' Donde termina donde y a quien, en caso extremo sigue al verbo y termina con la palabra mediante, para , o el pronombre 
	relativo que, mismo/a que'''
def getParaQue(lista):
	'''comienza con mediante para  que, y se sigue '''
'''caso base es fecha verbo y que '''
parrafos = getParrafos(files)
extdates = filtraSucesos(parrafos)
'''for x,y,z,a in extdates:
	if(z is not None):
		output.write("fecha\n")
		output.write ("{}\n".format(y))
		output.write("verbo\n")
		output.write("{}\n".format(z))
		output.write("parrafo\n")
		output.write("{}\n".format(x))
		output.write("________________________")
	else:
		print ("fecha")
		print (y)
		print("verbo")
		print(z)
		print("parrafo")
		print(x)
		print("________________________")
		'''
suc = open("sucesos.csv","w")
suc.write("Contexto,Fecha,Lema,Quien\n")
for parrafo,fecha,verbo,que in extdates:	
	st='"{0}","{1}","{2}","{3}"\n'.format(parrafo,fecha,verbo,que)
	suc.write(st)
suc.close()