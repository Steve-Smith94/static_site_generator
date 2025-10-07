# python
import unittest
from gencontent import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_h1_simple(self):
        self.assertEqual(extract_title("# Hello"), "Hello")

    def test_h1_strips_whitespace(self):
        md = "#   Tolkien Fan Club   "
        self.assertEqual(extract_title(md), "Tolkien Fan Club")

    def test_raises_without_h1(self):
        with self.assertRaises(Exception):
            extract_title("## Not a title\nNo h1 here")

if __name__ == "__main__":
    unittest.main()