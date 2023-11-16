# tests for the is_even() function
import unittest

#def is_even(a):
#    return False if a % 2 else True

class TestIsEven(unittest.TestCase):

    def test_when_output_true(self):
        # write your tests here
        for a in [2,46,14, 984]:
            self.assertTrue(is_even(a))

    def test_when_output_false(self):
        # write your tests here
        for a in [21,463,147, 9849]:
            self.assertFalse(is_even(a))


if __name__ == '__main__':
    unittest.main()