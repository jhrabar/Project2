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
        self.assertEqual(list_living_married(), "[('I3', 'Stephanie /Alton/')][('I3', 'Stephanie /Alton/')][('I21', 'Me /STeve/'), ('I22', 'Mel /STeve/')]")

    def test_list_orphans(self):
        self.assertEqual(orphan_checker(), "US33: List of Orphans: \n[('I25', 'Steve /Swerve/')]")

    def test_sibling_marriage(self):
        self.assertEqual(sibling_marriage(), "ERROR: FAMILY: US18: F21: husband and wife are siblings\n")

    def test_uniform_male_surnames(self):
        self.assertEqual(uniform_male_surnames(), "ERROR: US16: Some families have inconsistent male surnames:\n['F3']")

    # def test_duplicate_id_checker(self):
    #     passer = "ERROR: You have duplicates ids or (name,date) pairs, only one individual associated with each will appear in the database\n['I2']\n[]"
    #     self.assertEqual(passer, )

if __name__ == "__main__":
    unittest.main()