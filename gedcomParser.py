#John Hrabar
#SSW555
#I Pledge My Honor That I Have Abided By The Stevens Honor System

fileName = input("Input name of GEDCOM file:\n")
file = open(fileName)

zeroTags = ["INDI", "FAM", "HEAD", "TRLR", "NOTE"]
oneTags = ["NAME","SEX","BIRT","DEAT","FAMC","FAMS","MARR","HUSB","WIFE","CHIL","DIV"]
twoTags = ["DATE"]

dict Individuals = {}
dict Families = {}

#specifies whether an individual's data or a family's data is being parsed
indi = False
fam = False

#keeps track of the family or individual that's being updated
indiTag = ""
famTag = ""

# booleans that will help keep track of dates for birth, death, marriage, and divorce
birth = False
death = False
marriage = False
divorce = False




indiKeys = ['ID', 'name', 'gender', 'birthday', 'age', 'alive', 'death', 'child', 'spouse']
famKeys = ['ID', 'married', 'divorced', 'hID', 'hname', 'wID', 'wname', 'children']
def indDict():
	res = dict.fromkeys(indiKeys)
	res['child'] = []
	res['spouse'] = []
	return res
def famDict():
	res = dict.fromkeys(famKeys)
	res['children'] = []
	return res



for gedLine in file:
	print("--> " + gedLine)
	lineAsArray = gedLine.split()
	data = ""
	tag = ""


	if(lineAsArray[0] == "0"):
		for Tag in lineAsArray[1:]:
			if(Tag in zeroTags):
				tag = Tag
				validity = "Y"
		if(tag == ""):
			validity = "N"
			tag = lineAsArray[1]



	elif(lineAsArray[0] == "1"):
		for Tag in lineAsArray[1:]:
			if(Tag in oneTags):
				tag = Tag
				validity = "Y"
		if(tag == ""):
			validity = "N"
			tag = lineAsArray[1]




	elif(lineAsArray[0] == "2"):
		for Tag in lineAsArray[1:]:
			if(Tag in twoTags):
				tag = Tag
				validity = "Y"
		if(tag == ""):
			validity = "N"
			tag = lineAsArray[1]





	if (len(lineAsArray) > 1):
		if(tag != "INDI" and tag != "FAM"):
			data = " ".join(lineAsArray[2:])
			if(validity == "Y"):
				if(indi == True and fam == False):
					if(tag == "")
				

				elif(fam == True and indi == False):
					Families[famTag][tag] = data
			


		else:
			data = lineAsArray[1]
			if(tag == "INDI"):
				indi = True
				fam = False
				indiTag = data
				Individuals[indiTag] = indDict()
				Individuals[indiTag]["ID"] = indiTag
				famTag = ""
			else:
				indi = False
				fam = True
				indiTag = ""
				famTag = data
				Families[famTag] = famDict()
				Families[famTag]["ID"] = famTag


	#print("<--" + lineAsArray[0] + "|" + tag + "|" + validity + "|" + data + "\n" + "\n")