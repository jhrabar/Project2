from dbcommands import *
import unittest
#These Unit Tests assume that gedcomParser has been run
#and so the db has been created by the parser.

class Test(unittest.TestCase):
    def test_list_deceased(self):
        passer = "[('I1', 'Woodrow /McPherson/'), ('I7', 'Tom /McPherson/'), ('I8', 'Olga /Wall/'), ('I9', 'Tim /McPherson/'), ('I10', 'Nicole /Mackle/'), ('I11', 'Bryce /McPherson/')]"
        self.assertEqual(passer, list_deceased())
    
    def test_child_marriage_check(self):
        passer = "All good, no marriage with children."
        self.assertEqual(passer, child_marriage_check())

if __name__ == "__main__":
    unittest.main()