import unittest

class APiTest(unittest.TestCase):
    def test_get(self):
        self.assertEqual(1,2)

    def test_get1(self):
        self.assertEqual(2,3)
    def test_only_master(self):
        self.assertEqual(3,3)



if __name__ == '__main__':
    unittest.main()
