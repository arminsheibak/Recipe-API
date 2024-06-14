from unittest.mock import patch
from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import TestCase

class TestCommand(TestCase):

    def test_wait_for_db_ready(self):
        """ test waiting for postgresql db until it's available and then start django """
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            gi.return_value = True
            call_command('wait_for_db')
            self.assertEqual(gi.call_count, 1)
    
    @patch('time.sleep', return_value=True)
    def test_wait_for_db(self, ts):
        """
        if django starts before db is ready ConnectionHandler will throw a OperationalError exception.
        wait_for_db management command will check to see if ConnectionHandler raised the error and if it does try again
        """
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            gi.side_effect = [OperationalError] * 5 + [True]
            call_command('wait_for_db')
            self.assertEqual(gi.call_count, 6)


