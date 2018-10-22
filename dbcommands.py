import sqlite3
from sqlite3 import Error
import datetime

dbname = 'gedcom.db'

createindi = '''CREATE TABLE IF NOT EXISTS individual
(ID text PRIMARY KEY, name text, gender text UNIQUE, birthday text, age int, alive int, death text, child text, spouse text)'''

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

def extract_individuals(individuals = []):
	#returns the ids and names of all individuals in the database in two arrays
	ids = []
	names = []
	conn = create_connection(dbname)
	curs = conn.cursor()
	if individuals == []:
		individuals = curs.execute('''SELECT * FROM individual''').fetchall()
	for individual in individuals:
		ids.append(individual[0])
		names.append(individual[1])
	conn.close()
	return ids, names

def extract_families(families = []):
	#returns the ids of all families in the database in an array
	ids = []
	conn = create_connection(dbname)
	curs = conn.cursor()
	if families ==[]:
		families = curs.execute('''SELECT * FROM family''').fetchall()
	for family in families:
		ids.append(family[0])
	conn.close()
	return ids

def find_duplicate_indices(arr):
	indices = set()
	for ind in range(len(arr)):
		current = arr[ind]
		if ind not in indices:
			for secind in range(len(arr)):
				if arr[secind] == current and secind!=ind:
					indices.add(current)
		else:
			continue
	return indices

def addindis(individuals):
	# existing_ids, existing_names = extract_individuals

	conn = create_connection(dbname)
	curs = conn.cursor()

	indis = translate_indis(individuals)
	input_ids, input_names = extract_individuals(indis)
	dupids = set()
	dupname= set()
	dupids = find_duplicate_indices(input_ids)
	dupnames = find_duplicate_indices(input_names)

	curs.executemany(indientry, indis)
	conn.commit()
	conn.close()

def addfams(families):
	conn = create_connection(dbname)
	curs = conn.cursor()

	fams = translate_fams(families)
	curs.executemany(famentry, fams)
	conn.commit()
	conn.close()

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
	curs.execute('''SELECT hId, wID, children FROM family''')
	result = curs.fetchall()
	conn.close()
	string = ""
	for tup in result:
		if tup[0] in tup[2] or tup[1] in tup[2]:
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


