from dbcommands import *
import unittest
#These Unit Tests assume that gedcomParser has been run
#and so the db has been created by the parser.

class Test(unittest.TestCase):
    def test_list_deceased(self):
        passer = "[('I2', 'Mario /Stevens/'), ('I5', 'Bella /Stan/'), ('I6', 'William /Stevens/'), ('I7', 'Stanley /Stan/'), ('I8', 'Mary /Leslie/')]"
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

if __name__ == "__main__":
    unittest.main()