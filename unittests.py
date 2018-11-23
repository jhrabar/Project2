from dbcommands import *
import unittest
#These Unit Tests assume that gedcomParser has been run
#and so the db has been created by the parser.

class Test(unittest.TestCase):
    def test_list_deceased(self):
        passer = "[('I2', 'Mario /Stevens/'), ('I5', 'Bella /Stan/'), ('I6', 'William /Stevens/'), ('I7', 'Stanley /Stan/'), ('I8', 'Mary /Leslie/'), ('I23', 'Martin /Swerve/'), ('I24', 'Barbara /Swerve/')]"
        self.assertEqual(passer, list_deceased())
    
    def test_child_marriage_check(self):
        passer = "ERROR: FAMILY: US17: Family F1 has a marriage to a descendant\n"
        self.assertEqual(passer, child_marriage_check())

    def test_future_date_check(self):
    	self.assertEqual("ERROR: INDIVIDUAL: US01: I1: Birthday 10 MAR 2336 occurs in future\nERROR: INDIVIDUAL: US01: I4: Birthday 8 DEC 5326 occurs in future\n", future_date_check())

    def test_marriage_before_death(self):
    	self.assertEqual("ERROR: INDIVIDUAL: US05: I2: Marriage 8 OCT 2013 occurs after death: 9 DEC 2012\n", marriage_before_death())

    def test_divorce_before_death(self):
    	self.assertEqual("ERROR: INDIVIDUAL: US06: I5: Divorce 9 APR 2000 occurs after death: 7 MAR 2000\n", divorce_before_death())

    def test_gender_roles(self):
        self.assertEqual("ERROR: FAMILY: US21: F1: Husband I2 has incorrect gender\n", gender_roles())

    def test_fifteen_siblings(self):
        self.assertEqual("ERROR: FAMILY: US15: F3: Family has 15 or more children\n", fifteen_siblings())

    def test_date_comparison(self):
        self.assertEqual(1, dateCompare("15 NOV 2018", "16 NOV 2018"))
        self.assertEqual(1, dateCompare("15 NOV 2018", "15 NOV 2018"))
        self.assertEqual(0, dateCompare("15 NOV 2018", "14 NOV 2018"))

    def test_date_difference(self):
        self.assertEqual(20, dateDifference("15 NOV 1998", "15 NOV 2018"))
        self.assertEqual(19, dateDifference("16 NOV 1998", "15 NOV 2018"))

    def test_parents_too_old(self):
        self.assertEqual("ERROR: FAMILY: US12: F1: Father I2 is greater than 80 years older than child I1\nERROR: FAMILY: US12: F1: Mother I3 is greater than 60 years older than child I1\nERROR: FAMILY: US12: F1: Father I2 is greater than 80 years older than child I4\nERROR: FAMILY: US12: F1: Mother I3 is greater than 60 years older than child I4\n", parents_too_old())

    def test_hundredfifty_years_old(self):
        self.assertEqual("ERROR: INDIVIDUAL: US07: I2: had an age greater than 150 years old\n", hundredfifty_years_old())

    def test_list_living_single(self):
        self.assertEqual("[('I9', 'James /Stan/')]", list_living_single())

    def test_list_living_married(self):
        self.assertEqual(list_living_married(), "[('I3', 'Stephanie /Alton/')][('I21', 'Me /STeve/'), ('I22', 'Mel /STeve/')][('I150', 'Henry /Jones/'), ('I151', 'Lily /Brain/')][('I200', 'Jerry /Small/'), ('I201', 'Henriette /Jones/')][('I220', 'Vincent /Jones/'), ('I222', 'Kristen /Money/')][('I204', 'Gabby /Small/'), ('I225', 'Gilbert /Jones/')]")

    def test_list_orphans(self):
        self.assertEqual(orphan_checker(), "US33: List of Orphans: \n[('I25', 'Steve /Swerve/')]")

    def test_unique_spouses(self):
        #This unittest will always have this answer because unique_spouses always cleans up when it runs in main,
        #So when it is run again in unittests, it will always say this. Comment out the call to unique_spouses in testParser
        #and comment out the pass case here while uncommenting the second testcase here to see the other functionality in action.
        self.assertEqual(unique_spouses(),"No duplicated families.")
        #self.assertEqual(unique_spouses(),"The following families have duplicate husband-wife pairs and have been eliminated from the database:\n[\'F20\']")

        

    def test_sibling_marriage(self):
        self.assertEqual(sibling_marriage(), "ERROR: FAMILY: US18: F21: husband and wife are siblings\n")

    def test_uniform_male_surnames(self):
        self.assertEqual(uniform_male_surnames(), "ERROR: US16: Some families have inconsistent male surnames:\n['F3']")

    def test_birth_before_marriage(self):
        self.assertEqual(birth_before_marriage(), "ERROR: INDIVIDUAL: US02: I24: Marriage 8 NOV 1980 occurs before birth 7 JUN 1981\n")

    def test_first_cousin_marriage(self):
        self.assertEqual(first_cousin_marriage(), "ERROR: US19: Individual I204 is married to their first cousin I225\nERROR: US19: Individual I225 is married to their first cousin I204\n")

    def test_marriage_before_divorce(self):
        self.assertEqual(marriage_before_divorce(), "ERROR: US04: The following families have divorces before marriages:\nF30,")

    def test_list_children_in_age_order(self):
        self.assertEqual(list_children_age_order(), "F1\n[('I4', 'Boy /Stevens/', -3309), ('I1', 'Steven /Stevens/', -318), ('I2', 'Mario /Stevens/', 222)]\nF2\n[('I2', 'Mario /Stevens/', 222)]\nF3\n[('I5', 'Bella /Stan/', 58), ('I9', 'James /Stan/', 59), ('I22', 'Mel /STeve/', 69), ('I21', 'Me /STeve/', 73)]\nF21\n[]\nF30\n[('I25', 'Steve /Swerve/', 17)]\nF34\n[('I201', 'Henriette /Jones/', 48), ('I220', 'Vincent /Jones/', 55)]\nF35\n[('I203', 'Jess /Small/', 17), ('I202', 'Helen /Small/', 18), ('I204', 'Gabby /Small/', 19)]\nF36\n[('I226', 'Luigi /Jones/', 6), ('I225', 'Gilbert /Jones/', 18)]\nF37\n[]\n")

    # def test_duplicate_id_checker(self):
    #     passer = "ERROR: You have duplicates ids or (name,date) pairs, only one individual associated with each will appear in the database\n['I2']\n[]"
    #     self.assertEqual(passer, )

if __name__ == "__main__":
    unittest.main()