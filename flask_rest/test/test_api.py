import unittest


class APiTest(unittest.TestCase):
    def test_get(self):
        self.assertEqual(1,1)

    def test_get1(self):
        self.assertEqual(2,2)
    def test_only_master(self):
        self.assertEqual(3,3)
    def test_fail(self):
        self.assertEqual(1,1)



if __name__ == '__main__':
    unittest.main()
