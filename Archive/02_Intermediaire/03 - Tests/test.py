
import unittest
from unittest.mock import patch

from ecran import afficher

class TestModuleEcran(unittest.TestCase):

    @patch("ecran.moyenne", return_value=42)
    def test_afficher(self, mock_moyenne):
        afficher(1, 2, 3)
        mock_moyenne.assert_called_once_with(1, 2, 3)

if __name__ == "__main__":
    unittest.main()
