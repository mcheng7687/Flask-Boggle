from app import app, checkHighScore
from unittest import TestCase
from flask import session

app.config['TESTING'] = True

class GameTestCase(TestCase):
    """Test all functions in boggle's app.py"""

    def test_homepage(self):
        with app.test_client() as client:
            res = client.get("/")
            html = res.get_data(as_text = True)

            self.assertEqual(res.status_code,200)
            self.assertIn('id="start"',html)
    
    def test_gamepage(self):
        with app.test_client() as client:
            res = client.get("/game")
            html = res.get_data(as_text = True)

            self.assertEqual(res.status_code,200)
            self.assertIn('id="board"',html)
            self.assertIn('id="guess-word-div"',html)

    def test_new_game(self):
        with app.test_client() as client:
            res = client.get("/new-game")

            self.assertEqual(res.status_code,302)
            self.assertEqual(res.location, "http://localhost/")
    
    def test_new_game_followed(self):
        with app.test_client() as client:
            res = client.get("/new-game", follow_redirects=True)
            html = res.get_data(as_text = True)

            self.assertEqual(res.status_code,200)
            self.assertIn('id="start"',html)

    #FIX HERE
    def test_check_word(self):
        with app.test_client() as client:
            res = client.post("/test_word/apple")

            #value = res.get_data()
            val = res.get_json()
            print(f"here ---------> {val} <--------------")            
        
    def test_end_game_fail(self):
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['high_score'] = 5

            res = client.get("/game-over?score=0")
            html = res.get_data(as_text = True)

            self.assertEqual(res.status_code,200)
            self.assertIn('GAME OVER',html)
            self.assertIn('Sorry, you did not beat the high score.',html)

    def test_end_game_success(self):
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['high_score'] = 5

            res = client.get("/game-over?score=10")
            html = res.get_data(as_text = True)

            self.assertEqual(res.status_code,200)
            self.assertIn('GAME OVER',html)
            self.assertIn('Congratulations! You got a new high score!',html)

    def test_reset(self):
        with app.test_client() as client:
            res = client.get("/reset")

            self.assertEqual(res.status_code,302)
            self.assertEqual(res.location, "http://localhost/")
            self.assertEqual(session['high_score'], 0)
            self.assertEqual(session['visits'], 0)

    def test_reset_followed(self):
        with app.test_client() as client:
            res = client.get("/reset", follow_redirects=True)
            html = res.get_data(as_text = True)

            self.assertEqual(res.status_code,200)
            self.assertIn('id="start"',html)

    def test_checkHighScore(self):
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['high_score'] = 5
            
            self.assertTrue(checkHighScore(10))
            self.assertFalse(checkHighScore(1))
