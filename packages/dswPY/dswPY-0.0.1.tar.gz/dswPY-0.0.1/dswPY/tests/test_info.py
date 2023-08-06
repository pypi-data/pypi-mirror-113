import unittest
from dswPY import info

class TestInfo(unittest.TestCase):
    def test_help(self):
        general_info = "help"
        self.assertEqual(info.help(), general_info, "Test should pass")

if __name__ == '__main__':
    unittest.main()