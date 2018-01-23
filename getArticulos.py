"""
	Programa que analiza un documento de Word (.docx) que contenga un texto jurídico y lo estructura en una tabla .csv con los datos ordenados en las columnas "Contexto", "Ley", "Artículos" y "Fracciones". El programa utiliza expresiones regulares –escritas de acuerdo a estructuras lingüísticas– para obtener los datos deseados.

	@author: Jorge Galindo, Absalón Castañón e Ivan Salgado

	@company: GILkatón - Grupo de Ingeniería Lingüística, UNAM.

"""

import docx
import re
docs = []
docs.append("Evaluacion.docx")



#prefiltrado


lista =[]
contextos = []
licon=[]
tosave= open("output2.csv", "w")

def getArticulos():
	"""
	Función que selecciona y almacena los párrafos según si contienen una estructura de "artículo + ley que lo contiene". Además de almacenar la estructura, almacena el párrafo que la contiene como contexto

	"""
	articulos =[]
	contextos =[]
	rxentidad = re.compile("(en el |en los |del |de los |en su |en sus |los |al |el |En el |En los |Del |De los |En su |En sus |Los |Al |El )*(artículo|artículos|art.|Artículo|Artículos|Art.) [0-9]+(º|o\.)*(-[a-zA-Z])*((,)+ [0-9]+(º|o\.)*(-[a-zA-Z])*)*(( y )+[0-9]+(º|o\.)*(-[a-zA-Z])*)*((,)* (fracción |fracciones )+(I|V|X|L|C|D|M)+)*((,)+ (I|V|X|L|C|D|M)+)*(( y )+(I|V|X|L|C|D|M)+)*( inciso [a-z]\))*((, | y )+[0-9]+(º|o\.)*(-[a-zA-Z])*)*((,)* (fracción |fracciones )+(I|V|X|L|C|D|M)+)*((,)+ (I|V|X|L|C|D|M)+)*(( y )+(I|V|X|L|C|D|M)+)*( inciso [a-z]\))*( del | de la | de los | de las )+",re.UNICODE)
	for x in range(0,len(docs)):
			document=docx.Document("{}".format(docs[x]))
			for paragraph in document.paragraphs:
				res = rxentidad.search(paragraph.text)
				if res:
					var=re.sub("[[a-záéíóéúñ]*]$","",res.group())
					articulos.append(var)
					contextos.append(paragraph.text)
	return zip(articulos,contextos)

def getLey(articulos_contextos):
	"""
	Función que busca, en los párrafos del contexto, el nombre del texto legal que contiene los artículos seleccionados en la función anterior. Almacena el contexto completo, el nombre de la ley y la estructura que contiene el número y fracción de los artículos correspondientes.

	"""
	rxley = re.compile("((de la |del |de los )((Constitución|Ley|Estatuto|Lineamientos|[A-Z]{2,})(( [A-Z][a-záéíóéúñ]+)*( (a|del|las|,|sobre la|de los|de las|de||el|la|los|para|y|e) +)*){2,}(([A-Z][a-záéíóéúñ]*)*)(( (a|del|las|,|sobre la|de los|de las|de||el|la|los|para|y|e) +)*){2,}(([A-Z][a-záéíóéúñ]*)*)(( [A-Z][a-záéíóéúñ]*)*)))",re.UNICODE)

	resContextos = []
	resContLeyes = []
	resLeyes =[]

	for art,cont in articulos_contextos:
		res =  rxley.finditer(cont)
		for match in res:
			resContLeyes.append(art)
			resContextos.append(cont)
			resLeyes.append(match.group(3))

	return zip(resContextos, resLeyes, resContLeyes)

def getNumArt(contextos_leyes_contleyes):
	"""
	Función que busca, en la estructura que contiene el número y fracción de los artículos, el número correspondiente a los artículos citados del texto legal. Almacena el contexto completo, el nombre de la ley, el número del artículo y, una vez más, la estructura que contiene el número y fracción de los artículos correspondientes.

	"""
	rx ="([0-9]{1,}(º|o)*(-[a-zA-Z])*)+"

	rxnumarticulo=re.compile(rx)
	resContextos =[]
	resLeyes = []
	resNumArt = []
	resContLeyes = []
	for cont, ley, art in contextos_leyes_contleyes:
		res =  rxnumarticulo.finditer(art)
		for match in res:
			resContextos.append(cont)
			resLeyes.append(ley)
			resContLeyes.append(art)
			resNumArt.append(match.group(0))

	return zip(resContextos, resLeyes, resNumArt, resContLeyes)

def getNumFracciones(contextos_leyes_art_contleyes):
	"""
	Función que busca, en la estructura que contiene el número y fracción de los artículos, el número correspondiente a las fracciones citadas de los artículos del texto legal. Almacena el contexto completo, el nombre de la ley, el número del artículo y, finalmente, el número de fracción correspondiente.

	"""
	rx ="((I|V|X|L|C|D|M)+)"

	rxnumfracciones=re.compile(rx)

	resContextos =[]
	resLeyes = []
	resNumArt = []
	resNumFracciones = []

	for cont, ley, art, fracc in contextos_leyes_art_contleyes:
		res = rxnumfracciones.search(fracc)
		if res:
			resContextos.append(cont)
			resLeyes.append(ley)
			resNumArt.append(art)
			resNumFracciones.append(res.group(0))
		else:
			resContextos.append(cont)
			resLeyes.append(ley)
			resNumArt.append(art)
			resNumFracciones.append("")

	return zip(resContextos, resLeyes, resNumArt, resNumFracciones)

""" Se ejecutan las funciones y se obtienen los datos correspondientes """

licon = getArticulos()
licon = getLey(licon)
licon = getNumArt(licon)
licon = getNumFracciones(licon)

""" Se escriben los datos obtenidos en un tabla .csv """

tosave.write("Contexto,Ley,Artículos,Fracciones\n")
for cont,ley,art,fracc in licon:
	tosave.write('"{}","{}","{}","{}"\n'.format(cont,ley,art,fracc))

tosave.close()
