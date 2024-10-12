from django.test import SimpleTestCase

class TestsBerries(SimpleTestCase):
    
    def test_setup(self):
        self.assertEqual("Hello World!", "Hello World!")