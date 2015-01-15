from django.core.management.base import BaseCommand

from accounts.models import Account

from rhyme.management.commands.w2pdec import word2phonemeseqdict
from rhyme.management.commands.p2rdec import phoneme2rhymedict
from rhyme.models import *
from rhyme.rhymer import Rhymer
from rhyme.management.commands.tables import cons_examples, sound_translate, \
        vowel_examples, vowel_list, vowel_dict, cons_family, cons_family_list, \
        vowel_family_list, vowel_family

class Command(BaseCommand):
    help = "generate family rhymes"

    def handle(self, *args, **options):
        self.user = Account.objects.get(email='adrian_nye@yahoo.com')
        self.generate_family_rhymes()
        #self.test()

    def test(self):
        #word = Word.objects.get(word='bond')
        word = Word.objects.get(word='sea')
        print word
        rhymer = Rhymer(word.phoneme_sequence)
        rhymer.make_rhymes()

    def generate_family_rhymes(self):
        counter = 0
        pss = PhonemeSequence.objects.all()
        for ps in pss:
            if not counter % 100:
                print counter

            counter += 1
            
            rhymer = Rhymer(ps)
            rhymer.make_rhymes()

