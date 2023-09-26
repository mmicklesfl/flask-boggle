import unittest
from app import app, session
from boggle import Boggle

class FlaskTests(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True
        # Set up a sample board in the session
        with self.client.session_transaction() as sess:
            sess['board'] = [["A", "B", "C", "D", "E"],
                             ["F", "G", "H", "I", "J"],
                             ["K", "L", "M", "N", "O"],
                             ["P", "Q", "R", "S", "T"],
                             ["U", "V", "W", "X", "Y"]]

    def test_home(self):
        with self.client:
            response = self.client.get('/')
            html = response.get_data(as_text=True)
            self.assertIn('<table', html)
            self.assertEqual(response.status_code, 200)

    def test_valid_guess(self):
        with self.client:
            # Using a word from the sample board
            response = self.client.post('/check-guess', json={"guess": "HI"})
            data = response.get_json()
            self.assertEqual(data["result"], "ok")
            self.assertEqual(response.status_code, 200)

    def test_invalid_guess(self):
        with self.client:
            # Using an invalid word
            response = self.client.post('/check-guess', json={"guess": "INVALIDWORD"})
            data = response.get_json()
            self.assertNotEqual(data["result"], "ok")
            self.assertEqual(response.status_code, 200)

    def test_end_game(self):
        with self.client:
            response = self.client.post('/end-game', json={"score": 10})
            data = response.get_json()
            self.assertIn("newRecord", data)
            self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()
