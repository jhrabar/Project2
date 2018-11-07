#John Hrabar
#SSW555
#I Pledge My Honor That I Have Abided By The Stevens Honor System

import datetime
import sqlite3
from sqlite3 import Error
from dbcommands import *
# from dbcommands import translate_indis
# from dbcommands import translate_fams
# from dbcommands import addfams
# from dbcommands import addindis
# from dbcommands import create_tables
# from dbcommands import update_spousenames
# from dbcommands import list_deceased


zeroTags = ["INDI", "FAM", "HEAD", "TRLR", "NOTE"]
oneTags = ["NAME","SEX","BIRT","DEAT","FAMC","FAMS","MARR","HUSB","WIFE","CHIL","DIV"]
twoTags = ["DATE"]

Individuals = []
Families = []


#keeps track of the family or individual that's being updated
indiTag = ""
famTag = ""

# booleans that will help keep track of dates for birth, death, marriage, and divorce
birth = False
death = False
marriage = False
divorce = False


# Each individual and family is going to be a dictionary that will be added to a database
indiKeys = ['ID', 'name', 'gender', 'birthday', 'age', 'alive', 'death', 'child', 'spouse']
famKeys = ['ID', 'married', 'divorced', 'hID', 'hname', 'wID', 'wname', 'children']

months = {
	"JAN": 1,
	"FEB": 2,
	"MAR": 3,
	"APR": 4,
	"MAY": 5,
	"JUN": 6,
	"JUL": 7,
	"AUG": 8,
	"SEP": 9,
	"OCT": 10,
	"NOV": 11,
	"DEC": 12
}


def indDict():
	res = dict.fromkeys(indiKeys)
	res['child'] = []
	res['spouse'] = []
	return res
def famDict():
	res = dict.fromkeys(famKeys)
	res['children'] = []
	return res

def ageGetter(birthday):
	now = datetime.datetime.now()
	year = now.year
	month = now.month
	day = now.day
	birthdayList = birthday.split()
	if months[birthdayList[1]] > month or (months[birthdayList[1]] == month and int(birthdayList[0]) > day):
		return year - int(birthdayList[2]) - 1
	else:
		return year - int(birthdayList[2])

def main():
	fileName = input("Input name of GEDCOM file:\n")
	file = open(fileName)
	indi = False
	fam = False
	for gedLine in file:
		lineAsArray = gedLine.split()
		data = ""
		tag = ""

		# Checks if the tag given is in the list of acceptable 0 level tags and assigns validity accordingly
		if(lineAsArray[0] == "0"):
			for Tag in lineAsArray[1:]:
				if(Tag in zeroTags):
					tag = Tag
					validity = "Y"
			if(tag == ""):
				validity = "N"
				tag = lineAsArray[1]

		# Checks if the tag given is in the list of acceptable 1 level tags and assigns validity accordingly
		elif(lineAsArray[0] == "1"):
			for Tag in lineAsArray[1:]:
				if(Tag in oneTags):
					tag = Tag
					validity = "Y"
			if(tag == ""):
				validity = "N"
				tag = lineAsArray[1]

		# Checks if the tag given is in the list of acceptable 2 level tags and assigns validity accordingly
		elif(lineAsArray[0] == "2"):
			for Tag in lineAsArray[1:]:
				if(Tag in twoTags):
					tag = Tag
					validity = "Y"
			if(tag == ""):
				validity = "N"
				tag = lineAsArray[1]

		#if there is data this part determines what it is
		if (len(lineAsArray) > 1):
			#checks if the tag is something other than indi or fam
			if(tag != "INDI" and tag != "FAM"):
				data = " ".join(lineAsArray[2:])

				#if it is a valid tag that isn't indi or fam, the data will get added to the proper family or individual dictionary
				if(validity == "Y"):
					if(indi == True and fam == False):

						if(tag == "NAME"):
							Individuals[-1]["name"] = data
						elif(tag == "SEX"):
							Individuals[-1]["gender"] = data
						elif(tag == "BIRT"):
							birth = True
							death = False
							marriage = False
							divorce = False
						elif(tag == "DEAT"):
							birth = False
							death = True
							marriage = False
							divorce = False
						elif(tag == "DATE"):
							if(birth == True):
								Individuals[-1]["birthday"] = data
								Individuals[-1]["age"] = ageGetter(data)
							elif(death == True):
								Individuals[-1]["death"] = data
						elif(tag == "FAMC"):
							for char in '@':
								data = data.replace(char,'')
							Individuals[-1]["child"].append(data)
						elif(tag == "FAMS"):
							for char in '@':
								data = data.replace(char,'')
							Individuals[-1]["spouse"].append(data)



					elif(fam == True and indi == False):
						if(tag == "MARR"):
							birth = False
							death = False
							marriage = True
							divorce = False
						elif(tag == "DIV"):
							birth = False
							death = False
							marriage = False
							divorce = True
						elif(tag == "DATE"):
							if(marriage == True):
								Families[-1]["married"] = data
							elif(divorce == True):
								Families[-1]["divorced"] = data
						elif(tag == "HUSB"):
							for char in '@':
								data = data.replace(char,'')
							Families[-1]["hID"] = data
						elif(tag == "WIFE"):
							for char in '@':
								data = data.replace(char,'')
							Families[-1]["wID"] = data
						elif(tag == "CHIL"):
							for char in '@':
								data = data.replace(char,'')
							Families[-1]["children"].append(data)

			#If the tag is indi or fam, this will create a new family or individual dictionary to add data too from the next lines in the file
			else:
				data = lineAsArray[1]
				if(tag == "INDI"):
					indi = True
					fam = False
					for char in '@':
						data = data.replace(char,'')
					indiTag = data
					Individuals.append(indDict())
					Individuals[-1]["ID"] = indiTag
					famTag = ""
				else:
					indi = False
					fam = True
					for char in '@':
						data = data.replace(char,'')
					indiTag = ""
					famTag = data
					Families.append(famDict())
					Families[-1]["ID"] = famTag
	individs = translate_indis(Individuals)
	famils = translate_fams(Families)
	create_tables()
	addfams(Families)
	addindis(Individuals)
	update_spousenames()


if __name__ == '__main__':
	main()

	print("\nList Of Deceased:")
	print(list_deceased())
	print("\n")
	print(child_marriage_check())
	print(future_date_check())
	print(marriage_before_death())
	print(divorce_before_death())
	print(unique_spouses())
