import unittest
from transcriptb2b import transcript


class TestStringMethods(unittest.TestCase):


    def test_transcript(self):
        self.assertEqual(transcript('ATG'), 'AUG')  # OK

    def test_with_spaces(self):
        self.assertEqual(transcript('A TG'), 'A UG')  # OK

    def test_other_letters(self):
        self.assertEqual(transcript('b2b'), '???')  # OK


if __name__ == '__main__':
    unittest.main()