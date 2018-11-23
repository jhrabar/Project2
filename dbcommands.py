import sqlite3
from sqlite3 import Error
import datetime
import re
from collections import Counter
from ast import literal_eval

dbname = 'gedcom.db'

createindi = '''CREATE TABLE IF NOT EXISTS individual
(ID text PRIMARY KEY, name text, gender text, birthday text, age int, alive int, death text, child text, spouse text, 
UNIQUE(name, birthday))'''

createfam = '''CREATE TABLE IF NOT EXISTS family
(ID text PRIMARY KEY, married text, divorced text, hID text, hname text, wID text, wname text, children text)'''

indiKeys = ['ID', 'name', 'gender', 'birthday', 'age', 'alive', 'death', 'child', 'spouse']
famKeys = ['ID', 'married', 'divorced', 'hID', 'hname', 'wID', 'wname', 'children']

indientry = "INSERT OR IGNORE INTO individual VALUES(?,?,?,?,?,?,?,?,?)"
famentry = "INSERT OR IGNORE INTO family VALUES(?,?,?,?,?,?,?,?)"

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

def create_connection(db_file):
	try:
		conn = sqlite3.connect(db_file)
	except Error as e:
		print(e)
	return conn

def create_tables():
	conn = create_connection(dbname)
	curs = conn.cursor()
	curs.execute(createindi)
	curs.execute(createfam)
	conn.close()

def translate_indis(individuals):
	indis = []
	for indi in individuals:
		arrindi = []
		for key in indiKeys:
			if key in ['ID', 'name', 'gender', 'birthday', 'death']:
				if indi[key] == None:
					arrindi.append('NA')
				else:
					arrindi.append(indi[key])
			elif key == 'age':
				arrindi.append(indi[key])
			elif key in ['child', 'spouse']:
				if indi[key] == []:
					arrindi.append('NA')
				else:
					arrindi.append(str(indi[key]))
			elif key == 'alive':
				if indi['death'] != None:
					arrindi.append(0)
				else:
					arrindi.append(1)
		indis.append(arrindi)
	#nindis = [tuple(l) for l in indis]
	return indis

def translate_fams(families):
	fams = []
	for fam in families:
		arrfam = []
		for key in famKeys:
			if key in ['ID', 'married', 'divorced', 'hID', 'hname', 'wID', 'wname']:
				if fam[key] == None:
					arrfam.append('NA')
				else:
					arrfam.append(fam[key])
			elif key == 'children':
				if fam[key] == None:
					arrfam.append('NA')
				else:
					arrfam.append(str(fam[key]))
		fams.append(arrfam)
	#nfams = [tuple(l) for l in fams]
	return fams

def find_duplicates(arr):
	items = set()
	counts = Counter(arr)
	for item in arr:
		if counts[item] >1:
			items.add(item)
		else:
			continue
	return items

def find_dupe_pairs(arr):
	items = set()
	counts = Counter(arr)
	for item in arr:
		if counts[item] >1:
			items.add(item)
		else:
			continue
	return items

def addindis(individuals):
	# existing_ids, existing_names = extract_individuals

	conn = create_connection(dbname)
	curs = conn.cursor()

	indis = translate_indis(individuals)
	idlist = [individual[0] for individual in indis]
	name_date_list = [(individual[1],individual[3]) for individual in indis]
	duplicated_ids = list(find_duplicates(idlist))
	duplicated_name_dates = list(find_duplicates(name_date_list))
	if len(duplicated_ids) ==0 and len(duplicated_name_dates) == 0:
		dupestring = "No duplicated individual ids or (name, date) pairs."
	else:
		dupestring = "ERROR: You have duplicate ids or (name,date) pairs, only one individual associated with each will appear in the database\n"
		dupestring = dupestring + str(duplicated_ids) + "\n" + str(duplicated_name_dates)

	curs.executemany(indientry, indis)
	conn.commit()
	conn.close()
	return dupestring

def addfams(families):
	conn = create_connection(dbname)
	curs = conn.cursor()

	fams = translate_fams(families)
	idlist = [family[0] for family in fams]
	duplicated_ids = list(find_duplicates(idlist))
	if len(duplicated_ids) ==0:
		dupestring = "No duplicated family ids."
	else:
		dupestring = "ERROR: You have duplicate ids, only one family associated with each will appear in the database\n"
		dupestring = dupestring + str(duplicated_ids)

	curs.executemany(famentry, fams)
	conn.commit()
	conn.close()
	return dupestring

def update_spousenames():
	conn = create_connection(dbname)
	curs = conn.cursor()
	curs.execute('''UPDATE family SET hname = (SELECT name FROM individual WHERE ID = hID)''')
	curs.execute('''UPDATE family SET wname = (SELECT name FROM individual WHERE ID = wID)''')
	conn.commit()
	conn.close()


#returns 0 if date1 is after date2 and 1 otherwise
def dateCompare(date1, date2):
	date1List = date1.split()
	date2List = date2.split()
	if (int(date1List[2]) > int(date2List[2])) or (int(date1List[2]) == int(date2List[2]) and months[date1List[1]] > months[date2List[1]]) or (int(date1List[2]) == int(date2List[2]) and months[date1List[1]] == months[date2List[1]] and int(date1List[0]) > int(date2List[0])):
		return 0
	else:
		return 1

def list_deceased():
	conn = create_connection(dbname)
	curs = conn.cursor()
	curs.execute('''SELECT ID, name FROM individual WHERE alive = 0''')
	result = curs.fetchall()
	return(str(result))
	conn.close()

def get_id_from_name(ind_name):
	conn = create_connection(dbname)
	curs = conn.cursor()
	curs.execute('''SELECT ID, name FROM individual where name = ?''', (ind_name,))
	result = curs.fetchall()
	conn.close()
	return result[0][0]

def get_individual_families(ind_id):
	conn = create_connection(dbname)
	curs = conn.cursor()
	curs.execute('''SELECT spouse FROM individual WHERE ID = ? ''', (ind_id,))
	result = curs.fetchall()
	conn.close()
	return result[0][0]

def child_marriage_check():
	conn = create_connection(dbname)
	curs = conn.cursor()
	curs.execute('''SELECT ID, hId, wID, children FROM family''')
	result = curs.fetchall()
	conn.close()
	string = ""
	for tup in result:
		if tup[3] != "None":
			children = ''.join(c for c in tup[3] if c not in "\"'[] ")
			childrenList = children.split(',')
			if tup[1] in childrenList or tup[2] in childrenList:
				string += "ERROR: FAMILY: US17: Family {famid} has a marriage to a descendant\n".format(famid = tup[0])
	if len(string) == 0:
		string = "US17: No marriages to descendants.\n"
	return string

def marriage_before_death():
	#Checks whether a person has died before their marriage 
	conn = create_connection(dbname)
	curs = conn.cursor()
	curs.execute('''SELECT ID, death FROM individual''')
	result = curs.fetchall()
	curs.execute('''SELECT ID, hID, wID, married FROM family''')
	result2 = curs.fetchall()
	conn.close()
	string =""
	for tup in result:
		if tup[1] != "NA":
			for tup2 in result2:
				if(tup2[3] != "NA"):
					if tup[0] == tup2[1] or tup[0] == tup2[2]:
						if dateCompare(tup[1], tup2[3]) == 1:
							string+="ERROR: INDIVIDUAL: US05: {ID}: Marriage {Marriage} occurs after death: {Death}\n".format(ID = tup[0], Marriage = tup2[3], Death = tup[1])
	if len(string) == 0:
		string = "US05: No marriages occur after death\n"
	return string	


def divorce_before_death():
	#Checks whether a person has died before their divorcce
	conn = create_connection(dbname)
	curs = conn.cursor()
	curs.execute('''SELECT ID, death FROM individual''')
	result = curs.fetchall()
	curs.execute('''SELECT ID, hID, wID, divorced FROM family''')
	result2 = curs.fetchall()
	conn.close()
	string =""
	for tup in result:
		if tup[1] != "NA":
			for tup2 in result2:
				if(tup2[3] != "NA"):
					if tup[0] == tup2[1] or tup[0] == tup2[2]:
						if dateCompare(tup[1], tup2[3]) == 1:
							string+="ERROR: INDIVIDUAL: US06: {ID}: Divorce {Divorce} occurs after death: {Death}\n".format(ID = tup[0], Divorce = tup2[3], Death = tup[1])
	if len(string) == 0:
		string = "US06: No divorces occur after death\n"
	return string		


def future_date_check():
	now = datetime.datetime.now()
	currDate = str(now.day) + " " + list(months.keys())[now.month - 1] + " " + str(now.year)
	conn = create_connection(dbname)
	curs = conn.cursor()
	curs.execute('''SELECT ID, birthday, death FROM individual''')
	result = curs.fetchall()
	curs.execute('''SELECT ID, married, divorced FROM family''')
	result2 = curs.fetchall()
	conn.close()
	string = ""
	for tup in result:
		if tup[1] != "NA":
			if dateCompare(tup[1], currDate) == 0:
				string += "ERROR: INDIVIDUAL: US01: {ID}: Birthday {Birthday} occurs in future\n".format(ID = tup[0], Birthday = tup[1])
		if tup[2] != "NA":
			if dateCompare(tup[2], currDate) == 0:
				string += "ERROR: INDIVIDUAL: US01: {ID}: Death {Death} occurs in future\n".format(ID = tup[0], Death= tup[2])
	for tup in result2:
		if tup[1] != "NA":
			if dateCompare(tup[1], currDate) == 0:
				string += "ERROR: FAMILY: US01: {ID}: Marriage {Marriage} occurs in future\n".format(ID = tup[0], Marriage= tup[1])
		if tup[2] != "NA":
			if dateCompare(tup[2], currDate) == 0:
				string += "ERROR: FAMILY: US01: {ID}: Divorce {Divorce} occurs in future\n".format(ID = tup[0], Divorce= tup[2])
	if len(string) == 0:
		string = "US01: No dates occur in future\n"
	return string

def dateDifference(date1, date2):
	date1List = date1.split()
	date2List = date2.split()
	if months[date1List[1]] > months[date2List[1]] or (months[date1List[1]] == months[date2List[1]] and int(date1List[0]) > int(date2List[0])):
		return int(date2List[2]) - int(date1List[2]) - 1
	else:
		return int(date2List[2]) - int(date1List[2])

def hundredfifty_years_old():
	#checks whether someone is younger than 150
	now = datetime.datetime.now()
	currDate = str(now.day) + " " + list(months.keys())[now.month - 1] + " " + str(now.year)
	conn = create_connection(dbname)
	curs = conn.cursor()
	curs.execute('''SELECT ID, birthday, death FROM individual''')
	individualResult = curs.fetchall()
	conn.close()
	resultString=""
	for tup in individualResult:
		if tup[2] == "NA":
			if dateDifference(tup[1], currDate) >= 150:
				resultString += "ERROR: INDIVIDUAL: US07: {ID}: has an age greater than 150 years old\n".format(ID = tup[0])
		else:
			if dateDifference(tup[1], tup[2]) >= 150:
				resultString += "ERROR: INDIVIDUAL: US07: {ID}: had an age greater than 150 years old\n".format(ID = tup[0])
	if len(resultString) == 0:
		resultString = "US07: No people older than 150 years old\n"
	return resultString		

def sibling_marriage():
	#checks whether or not siblings are married
	conn = create_connection(dbname)
	curs = conn.cursor()
	curs.execute('''SELECT ID, hID, wID FROM family''')
	familyResult = curs.fetchall()
	resultString=""
	for tup in familyResult:
		curs.execute('''SELECT ID, child FROM individual WHERE ID = ? OR ID = ?''', (tup[1],tup[2],))
		individuals = curs.fetchall()
		if individuals[0][1] == individuals[1][1] and individuals[0][1] != "NA":
			resultString += "ERROR: FAMILY: US18: {ID}: husband and wife are siblings\n".format(ID = tup[0])
	if len(resultString) == 0:
		resultString = "US18: No siblings married here! \n"
	return resultString

def orphan_checker():
	#checks for orphans
	conn = create_connection(dbname)
	curs = conn.cursor()
	curs.execute('''SELECT ID, name, age, child FROM individual''')
	individualResult = curs.fetchall()
	resultString="US33: List of Orphans: \n["
	for tup in individualResult:
		if(tup[2] < 18):
			fID = ''.join(c for c in tup[3] if c not in "\"'[] ")
			curs.execute('''SELECT ID, hID, wID FROM family WHERE ID = ?''', (fID,))
			family = curs.fetchone()
			curs.execute('''SELECT ID, alive FROM individual WHERE ID = ? OR ID = ?''', (family[1], family[2],))
			parents = curs.fetchall()
			if(parents[0][1] == 0 and parents[1][1] == 0):
				resultString += str(tup[0:2])
	resultString += "]"
	return resultString


def parents_too_old():
	conn = create_connection(dbname)
	curs = conn.cursor()
	curs.execute('''SELECT ID, hID, wID FROM family''')
	familyResult = curs.fetchall()
	resultString=""
	for tup in familyResult:
		curs.execute('''SELECT birthday FROM individual WHERE ID = ? ''', (tup[1],))
		hBirthday = curs.fetchone()
		curs.execute('''SELECT birthday FROM individual WHERE ID = ? ''', (tup[2],))
		wBirthday = curs.fetchone()
		family = "['" + tup[0] + "']"
		curs.execute('''SELECT ID, birthday FROM individual WHERE child = ? ''', (family,))
		individualResult = curs.fetchall()
		for tup2 in individualResult:
			if dateDifference(hBirthday[0], tup2[1]) >= 80:
				resultString += "ERROR: FAMILY: US12: {ID}: Father {hID} is greater than 80 years older than child {cID}\n".format(ID = tup[0], hID = tup[1], cID = tup2[0])
			if dateDifference(wBirthday[0], tup2[1]) >= 60:
				resultString += "ERROR: FAMILY: US12: {ID}: Mother {hID} is greater than 60 years older than child {cID}\n".format(ID = tup[0], hID = tup[2], cID = tup2[0])
	conn.close()
	if len(resultString) == 0:
		resultString = "US12: No parents are too old\n"
	return resultString		

def gender_roles():
	conn = create_connection(dbname)
	curs = conn.cursor()
	curs.execute('''SELECT ID, gender FROM individual''')
	individualResult = curs.fetchall()
	curs.execute('''SELECT ID, hID, wID FROM family''')
	familyResult = curs.fetchall()
	conn.close()
	resultString = ""
	for tup in individualResult:
		for tup2 in familyResult:
			if tup[0] == tup2[1]:
				if tup[1] != "M":
					resultString += "ERROR: FAMILY: US21: {fID}: Husband {hID} has incorrect gender\n".format(fID = tup2[0], hID = tup[0])#needs to update husband gender
			elif tup[0] == tup2[2]:
				if tup[1] != "F":
					resultString += "ERROR: FAMILY: US21: {fID}: Wife {wID} has incorrect gender\n".format(fID = tup2[0], wID = tup[0])
	if len(resultString) == 0:
		resultString = "US21: All Husbands and Wives Have Correct Gender\n"
	return resultString

def fifteen_siblings():
	conn = create_connection(dbname)
	curs = conn.cursor()
	curs.execute('''SELECT ID, children FROM family''')
	familyResult = curs.fetchall()
	conn.close()
	resultString = ""
	for tup in familyResult:
		if tup[1] != "None":
			childrenList = tup[1].split(",")
			if len(childrenList) >= 15:
				resultString += "ERROR: FAMILY: US15: {fID}: Family has 15 or more children\n".format(fID = tup[0])
	if len(resultString) == 0:
		resultString = "US15: All Families Have Fewer than 15 Children\n"
	return resultString

def unique_spouses():
	conn = create_connection(dbname)
	curs = conn.cursor()
	curs.execute('''SELECT ID, hID, wID FROM family''')
	fam_spouses = curs.fetchall()
	#we already know fam IDs are unique
	families_to_eliminate = []
	for i in range(len(fam_spouses)):
		husband = fam_spouses[i][1]
		wife = fam_spouses[i][2]
		for j in range(i+1, len(fam_spouses)):
			if fam_spouses[j][1] == husband and fam_spouses[j][2] == wife:
				families_to_eliminate.append((fam_spouses[j][0]))
	resultstring = 'No duplicated families.'
	eliminate_list = [(fam,) for fam in families_to_eliminate]
	curs.executemany('''DELETE FROM family WHERE ID = ?''', eliminate_list)
	conn.commit()
	conn.close()
	if len(families_to_eliminate)>0:
		resultstring = 'The following families have duplicate husband-wife pairs and have been eliminated from the database:\n' + str(families_to_eliminate)
	return resultstring

def uniform_male_surnames():
	conn = create_connection(dbname)
	curs = conn.cursor()
	curs.execute('''SELECT ID, hID, children FROM family''')
	fams = curs.fetchall()
	families = [[fam[0],fam[1],literal_eval(fam[2])] for fam in fams]
	curs.execute('''SELECT ID, name FROM individual WHERE gender = \'M\'''')
	men = curs.fetchall()
	conn.close()
	mendict = dict()
	bad_families = []
	for man in men:
		mendict[man[0]]=man[1]
	for man in list(mendict.keys()):
		mendict[man] = mendict[man].split('/')[1].strip()
	for family in families:
		if family[1] in list(mendict.keys()):
			family_name = mendict[family[1]]
		else:
			continue
		for child in family[2]:
			if child in list(mendict.keys()):
				if mendict[child]!=family_name:
					bad_families.append(family[0])
			else:
				continue
	result_string = 'US16: No families with inconsistent male surnames.'
	if len(bad_families) >0 :
		result_string = 'ERROR: US16: Some families have inconsistent male surnames:\n'+str(bad_families)	
	return result_string
	
def list_living_married():
	conn = create_connection(dbname)
	curs = conn.cursor()
	curs.execute('''SELECT ID, hID, wID FROM family WHERE divorced = \'NA\'''')
	familyResult = curs.fetchall()
	resultString = ""
	for family in familyResult:
		curs.execute('''SELECT ID, name FROM individual WHERE (ID = ? OR ID = ?) AND alive = 1''', (family[1], family[2],) )
		result = curs.fetchall()
		if len(result) > 0:
			resultString += str(result)
	conn.close()
	return resultString

def list_living_single():
	conn = create_connection(dbname)
	curs = conn.cursor()
	curs.execute('''SELECT ID, name FROM individual WHERE alive = 1 AND age >= 30 AND spouse = \'NA\'''')
	individualResult = curs.fetchall()
	conn.close()
	return str(individualResult)

def birth_before_marriage():
	conn = create_connection(dbname)
	curs = conn.cursor()
	curs.execute('''SELECT married, hID, wID FROM family''')
	familyResult = curs.fetchall()
	resultString = ""
	for fam in familyResult:
		curs.execute('''SELECT ID, name, birthday FROM individual WHERE (ID = ? OR ID = ?)''', (fam[1], fam[2],))
		result = curs.fetchall()
		for indi in result:
			if dateCompare(indi[2], fam[0]) == 0:
				resultString += "ERROR: INDIVIDUAL: US02: {ID}: Marriage {marriage} occurs before birth {birth}\n".format(ID = indi[0], marriage = fam[0], birth = indi[2])
	if len(resultString) == 0:
		resultString += "USO2: No individuals married before birth\n"
	conn.close()
	return resultString

def first_cousin_marriage():
	conn = create_connection(dbname)
	curs = conn.cursor()
	#get individuals who have parents in the db and have been married
	curs.execute('''SELECT ID, child, spouse FROM individual WHERE NOT spouse = \'NA\' AND NOT child = \'NA\'''')
	individualResult = curs.fetchall()
	resultString = ""
	for individual in individualResult:
		spouseIDs = []
		fID = ''.join(c for c in individual[2] if c not in "\"'[] ")
		fList = fID.split(",")
		for f in fList:
			curs.execute('''SELECT hID, wID FROM family WHERE hID = ? OR wID = ?''', (individual[0], individual[0], ))
			families = curs.fetchall()
			for fam in families:
				if fam[0] == individual[0]:
					spouseIDs.append(fam[1])
				elif fam[1] == individual[0]:
					spouseIDs.append(fam[0])
		fID = ''.join(c for c in individual[1] if c not in "\"'[] ")
		#get the family of the individual's parents
		curs.execute('''SELECT ID, hID, wID FROM family WHERE ID = ?''', (fID,))
		parentFamily = curs.fetchone()
		#get the individual parents
		curs.execute('''SELECT ID, child FROM individual WHERE ID = ? OR ID = ?''', (parentFamily[1], parentFamily[2], ))
		parents = curs.fetchall()
		for parent in parents:
			if parent[1] != "NA":
				#get the family the parent is a child of
				fID = ''.join(c for c in parent[1] if c not in "\"'[] ")
				curs.execute('''SELECT ID, children FROM family WHERE ID = ?''', (fID, ))
				grandParentFamily = curs.fetchone()
				AuntAndUncleIDs = ''.join(c for c in grandParentFamily[1] if c not in "\"'[] ")
				listOfAuntsAndUncles = AuntAndUncleIDs.split(',')
				for AuntOrUncle in listOfAuntsAndUncles:
					if AuntOrUncle != parent[0]:
						curs.execute('''SELECT children FROM family WHERE hID = ? or wID = ?''', (AuntOrUncle, AuntOrUncle, ))
						cousinFamilies = curs.fetchall()
						for cousinFamily in cousinFamilies:
							cousinIDs = ''.join(c for c in cousinFamily[0] if c not in "\"'[] ")
							listOfCousins = cousinIDs.split(',')
							for spouse in spouseIDs:
								if spouse in listOfCousins:
									resultString += "ERROR: US19: Individual {ID} is married to their first cousin {ID2}\n".format(ID = individual[0], ID2 = spouse)
	if len(resultString) == 0:
		resultString += "US19: No first cousin marriages\n"
	conn.close()
	return resultString

def marriage_before_divorce():
	conn = create_connection(dbname)
	curs = conn.cursor()
	curs.execute('''SELECT married, divorced, ID FROM family''')
	familyResult = curs.fetchall()
	resultString = ''
	for fam in familyResult:
		if fam[1] == 'NA':
			continue
		else:
			if dateDifference(fam[0],fam[1])<0:
				resultString+=str(fam[2])+','
	if len(resultString)>0:
		resultString = 'ERROR: US04: The following families have divorces before marriages:\n' + resultString
	else:
		resultString = 'US04: No families with divorce before marriage.'
	conn.close()
	return resultString

def list_children(family):
	children = literal_eval(family[1])
	kids = [(kid,) for kid in children]
	# print(kids)
	conn = create_connection(dbname)
	curs = conn.cursor()
	progeny = []
	for kid in kids:
		curs.execute('''SELECT ID, age, name FROM individual WHERE ID = ?''', kid)
		progeny += curs.fetchall()
	progeny.sort(key = lambda kid: kid[1])
	child_list = str(family[0]) + "\n"
	child_list += str([(child[0], child[2], child[1]) for child in progeny]) + "\n"
	conn.close()
	return child_list


def list_children_age_order():
	conn = create_connection(dbname)
	curs = conn.cursor()
	curs.execute('''SELECT ID, children FROM family''')
	fams = curs.fetchall()
	conn.close()
	result = ''
	for fam in fams:
		result += list_children(fam)
	return result