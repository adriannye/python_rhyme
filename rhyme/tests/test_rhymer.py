from django.test import TestCase
from rhyme.models import *
from django.core.management import call_command


class RhymerTestCase(TestCase):
    def setUp(self):
        Word.objects.create(name="lion", sound="roar")
        call_command('loadperfect', test=True)

    def test_gen_rhyme_1(self):
        """Word with single consonant"""
        lion = Animal.objects.get(name="lion")
        cat = Animal.objects.get(name="cat")
        self.assertEqual(lion.speak(), 'The lion says "roar"')
        self.assertEqual(cat.speak(), 'The cat says "meow"')
