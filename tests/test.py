import unittest
from unittest.mock import MagicMock, patch
import tkinter as tk
import tweepy
from minimalist_x_ui import MinimalistUI

class MyTestCase(unittest.TestCase):
    def setUp(self):
        # Initialize Tkinter window
        self.root = tk.Tk()
        self.app = MinimalistUI(self.root)
        self.root.withdraw()  # Hide the GUI during tests

    def tearDown(self):
        # Demo Tkinter window
        self.root.destroy()

    def test_ui(self):
        # Test the initial configuration of the UI components
        self.app.root.update()  # Force the Tkinter window to update
        self.assertEqual(self.app.root.geometry(), '677x400+0+0')
        self.assertTrue(self.app.text_input)
        self.assertTrue(self.app.progress_bar)
        self.assertTrue(self.app.root.overrideredirect())
        # Window should have no border/title

    def test_input_limit(self):
        # Ensure that the text input does not accept more than 280 characters
        self.app.text_input.insert('1.0', 'a' * 300)  # Exceed the limit
        self.app.update_progress(None)
        self.assertEqual(len(
            self.app.text_input.get("1.0", tk.END).strip()), 280)

    @patch('tweepy.Client.create_tweet')
    def test_send_tweet(self, mock_create_tweet):
        # Validate send_tweet function via Python's unittest.mock.patch
        # Mock Tweepy API create_tweet method.
        # Set up the mock to return a predefined response, then stimulate
        # entering a tweet and call send_tweet to evaluate API interaction
        mock_create_tweet.return_value = {'id': 123, 'text': 'Hello, World!'}
        self.app.text_input.insert('1.0', 'Testing, testing 1... 2... 3...')
        self.app.send_tweet()
        mock_create_tweet.assert_called_once_with(text='Testing, testing 1... 2... 3...')

    @patch('tweepy.Client.create_tweet',
           side_effect=tweepy.TweepyException("Failed to tweet"))
    # Validate send_tweet function exception management
    # via Python's unittest.mock.patch
    def test_send_tweet_failure(self, mock_create_tweet):
        self.app.text_input.insert('1.0', 'Another test')
        with self.assertRaises(tweepy.TweepyException):
            self.app.send_tweet()

    def test_progress_bar_update(self):
        # Evaluate progress bar functionality
        self.app.text_input.insert('1.0', 'Hello')
        self.app.update_progress(None)
        self.assertEqual(self.app.progress_bar['value'], 5)

if __name__ == '__main__':
    unittest.main()