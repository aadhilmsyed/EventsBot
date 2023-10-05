import unittest
import subprocess

class TestEventsBot(unittest.TestCase):
    def test_run_events_bot(self):
        # Use subprocess to run events_bot.py
        result = subprocess.run(["python", "events_bot.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Check if the process completed without errors
        self.assertEqual(result.returncode, 0, f"Error: {result.stderr}")

if __name__ == "__main__":
    unittest.main()

