#John Hrabar
#SSW555
#I Pledge My Honor That I Have Abided By The Stevens Honor System

import sqlite3
conn = sqlite3.connect('GEDCOM.db')

fileName = input("Input name of GEDCOM file:\n")
file = open(fileName)

zeroTags = ["INDI", "FAM", "HEAD", "TRLR", "NOTE"]
oneTags = ["NAME","SEX","BIRT","DEAT","FAMC","FAMS","MARR","HUSB","WIFE","CHIL","DIV"]
twoTags = ["DATE"]

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
		else:
			data = lineAsArray[1]
	print("<--" + lineAsArray[0] + "|" + tag + "|" + validity + "|" + data + "\n" + "\n")

conn.close()