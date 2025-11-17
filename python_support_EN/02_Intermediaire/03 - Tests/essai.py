

def moyenne(*args):
    return sum(args) / len(args)


import unittest

class TestFonctionMoyenne(unittest.TestCase):
    def test_moyenne_nombres_differents(self):
        self.assertEqual(moyenne(8, 10, 12), 10)

    def test_moyenne_nombres_egauxs(self):
        self.assertEqual(moyenne(10, 10, 10), 10)

    def test_moyenne_sans_nombres(self):
        with self.assertRaises(ZeroDivisionError):
            moyenne()

if __name__ == "__main__":
    unittest.main()
