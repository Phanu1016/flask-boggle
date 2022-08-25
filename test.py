from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    def setUp(self):
        """ Setup client """
        self.client = app.test_client()

    def test_main_page(self):
        """ Test for board in session and main page HTML """
        with self.client:
            response = self.client.get('/')
            html = response.get_data(as_text=True)
            self.assertIn('board', session)
            self.assertIn('Timer: <span id="timer"></span>', html)
            self.assertIn('Score: <span id="score">0</span>', html)
            self.assertIn('Highest Score:', html)
            self.assertIn("You've played", html)

    def test_check(self):
        """ Test for word validity """
        with self.client:
            with self.client.session_transaction() as change_session:
                change_session['board'] = [["A", "N", "T", "H", "E"], 
                                           ["D", "O", "G", "A", "N"], 
                                           ["H", "U", "M", "A", "N"], 
                                           ["H", "A", "T", "I", "O"], 
                                           ["C", "I", "P", "D", "T"]]

        self.assertEqual(self.client.post('/check', json=({'guess':'ant'})).json['response'], 'ok')
        self.assertEqual(self.client.post('/check', json=({'guess':'dafdafasfafa'})).json['response'], 'not-word')
        self.assertEqual(self.client.post('/check', json=({'guess':'HE'})).json['response'], 'ok')
        self.assertEqual(self.client.post('/check', json=({'guess':'cap'})).json['response'], 'ok')
        self.assertEqual(self.client.post('/check', json=({'guess':'she'})).json['response'], 'not-on-board')
        self.assertEqual(self.client.post('/check', json=({'guess':'hide'})).json['response'], 'not-on-board')

    def test_update(self):
        """ Test sending score and getting nplay and highest score back"""
        with self.client:          
            response = self.client.post('/update', json=({'score':20}))
            self.assertEqual(response.json['nplay'], 1)
            self.assertEqual(response.json['highest'], 20)
