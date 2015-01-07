import logging

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from rhyme.management.commands.w2pdec import word2phonemeseqdict
from rhyme.management.commands.p2rdec import phoneme2rhymedict
from rhyme.models import *
from rhyme.management.commands.tables import cons_examples, sound_translate, \
        vowel_examples, vowel_list, vowel_dict, cons_family, cons_family_list, \
        vowel_family_list, vowel_family

logger = logging.getLogger(__name__)

class Rhymer(object):
    """
    Generate rhymes for a phoneme sequence
    """
    def __init__(self, ps):
        self.original_ps = ps
        self.original_ps_text = ps.text
        print ps.text

        # list of Word objects for perfect rhymes (all words that have the same phoneme sequence).
        self.words = Word.objects.filter(phoneme_sequence=ps)

    def remove_cons(self, ps, index):
        """
        remove consonant at index in ps
        """
        return ps[0:index]+ps[index+1:]

    def replace_cons(self, ps, index, char):
        """
        replace consonant at index in ps with char
        """
        ps = self.get_text(ps)
        stringlist = list(ps)
        stringlist[index] = char
        return ''.join(stringlist)

    def add_cons(self, ps, char):
        """
        add char to end of ps
        """
        return ps + char

    def get_text(self, ps):
        if isinstance(ps, PhonemeSequence):
            return ps.text
        else:
            return ps

    def find_consonants(self, ps):
        """
        Scan phoneme seq and detect consonants.

        Returns two values:
        consecutive: index of first of consecutive consonants (or None)
        consonant_indexes: list of integer indexes of all consonants
        """

        text = self.get_text(ps)
        consecutive = None
        consonant_indexes = [] # list of integer positions of consonants in rhyme phoneme sequence
        previous_was_consonant = False
        for i in range(len(text)):  # scan sequence from left
            if text[i] in cons_family:
                if previous_was_consonant:
                    consecutive = i-1
                consonant_indexes.append(i)
                previous_was_consonant = True
            else:
                previous_was_consonant = False

        return consecutive, consonant_indexes

    def make_rhymes(self):
        self._make_rhymes(self.original_ps.text)

    def _make_rhymes(self, ps_text):
        """
        vowel sounds stay the same.
        categorize consonant after stressed vowel and replace with relatives,
        then see if we generated a phoneme sequence that matches real words.
        if so, add those rhymes to database.

        ps_text is a text string, not PhonemeSequence object.  It has to be this way because we're trying
        phoneme sequences that don't have any rhymtes so they are not in the db.
        """

        consecutive_consonant_index, consonant_indexes = self.find_consonants(ps_text)
        #print('consecutive: %s' % (consecutive_consonant_index))
        #print('consonant_indexes: %s' % (consonant_indexes))

        self.rhyme_type = RhymePhonemeSequence.ADDITIVE
        if not consonant_indexes:
            # no consonants, only additive rhymes possible
            self.additive_rhymes(ps_text)
            return
        
        rhyme_list = []
        self.rhyme_type = RhymePhonemeSequence.FAMILY
        self.replace_each_consonant(ps_text, consonant_indexes)

        self.rhyme_type = RhymePhonemeSequence.SUBTRACTIVE
        consonants = cons_examples.keys()
        if ps_text[-1] == 'S':
            new_ps_text = self.remove_cons(ps_text, len(ps_text)-1)
            consecutive_consonant_index, consonant_indexes = self.find_consonants(new_ps_text)
            self.replace_each_consonant(new_ps_text, consonant_indexes)

        if consecutive_consonant_index:
            # remove first of each set of consecutive consonants, and try the whole rhyming
            # algorithm again.
            # Note: this removes the first consonant then 
            # tries to rhyme the result.  Because it's recursive it will sequentially remove 
            # all but the last consecutive consonant.
            new_ps_text = self.remove_cons(ps_text, consecutive_consonant_index)
            print 'CONSECUTIVE, ps now %s' % new_ps_text
            consecutive_consonant_index, consonant_indexes = self.find_consonants(new_ps_text)
            self.replace_each_consonant(new_ps_text, consonant_indexes)

    def replace_each_consonant(self, ps_text, consonant_indexes):
        for consonant_index in consonant_indexes:
            self.try_rhyme_categories(ps_text, consonant_index)

    def try_rhyme_category(self, ps, consonant_index, category, char, order):
        """
        Try replacing consonant with all other consonants in its category.
        """
        print('rhyme category %s, char %s\n' % (category, char))
        for trial_cons in cons_family_list[category]:
            if trial_cons != char: #skip self
                rhyming_sequence = self.replace_cons(ps, consonant_index, trial_cons)
                self.create_rhyme(trial_cons, rhyming_sequence, order)

    def final_order(self, order):
        """
        Give each rhyming mode a different order precedence
        """
        if self.rhyme_type == RhymePhonemeSequence.ADDITIVE:
            return order
        elif self.rhyme_type == RhymePhonemeSequence.FAMILY:
            return 10 + order
        elif self.rhyme_type == RhymePhonemeSequence.SUBTRACTIVE:
            return 20 + order
        else:
            raise Exception('unexpected rhyme type')

    def create_rhyme(self, trial_cons, pstext, order):
        """
        Create record of rhyme in database
        """
        try:
            ps = PhonemeSequence.objects.get(text=pstext)
        except PhonemeSequence.DoesNotExist:
            return

        print 'creating %s rhyme for original %s: sound %s, rhyme %s, order %s' % (self.rhyme_type,   
            self.original_ps,
            sound_translate[trial_cons],
            ps,
            self.final_order(order),
            )
        rps, created = RhymePhonemeSequence.objects.get_or_create(
            sound=sound_translate[trial_cons],
            original_ps=self.original_ps,
            rhyme_ps=ps,
            rhyme_type=self.rhyme_type,
            order=self.final_order(order),
        )

    def ps_has_rhymes(self, ps):
        """
        Does phoneme sequence have words?
        """
        # TODO: replace with query once we have user added words
        if ps in phoneme2rhymedict:
            return True
        return False

    def try_rhyme_categories(self, ps, consonant_index):
        """
        Determine family of consonant at consonant_index.
        Generate phoneme sequence by varying that consonant according to algorithm.
        See if there are any words rhyming with that phoneme sequence.
        ps - sequence in word to be rhymed
        consonant_index - index in phoneme sequence of consonant sound to be modified
        """
        pstext = self.get_text(ps)
        char = pstext[consonant_index] # current value of char to be modified
        # now build list of replacements according to family
        if cons_family[char] == "voiced_fricative":
            print 'voiced_fricative'
            # try companions, then unvoiced
            self.try_rhyme_category(ps, consonant_index, "voiced_fricative", char, 1)
            self.try_rhyme_category(ps, consonant_index, "unvoiced_fricative", char, 2)
                
            self.try_rhyme_category(ps, consonant_index, "voiced_plosive", char, 3)
            self.try_rhyme_category(ps, consonant_index, "unvoiced_plosive", char, 4)

            self.try_rhyme_category(ps, consonant_index, "nasal", char, 5)

        elif cons_family[char] == "unvoiced_fricative":
            print 'unvoiced_fricative'
            # try companions, then voiced
            self.try_rhyme_category(ps, consonant_index, "unvoiced_fricative", char, 1)
            self.try_rhyme_category(ps, consonant_index, "voiced_fricative", char, 2)

            self.try_rhyme_category(ps, consonant_index, "voiced_plosive", char, 3)
            self.try_rhyme_category(ps, consonant_index, "unvoiced_plosive", char, 4)

            self.try_rhyme_category(ps, consonant_index, "nasal", char, 5)
        elif cons_family[char] == "voiced_plosive":
            print 'voiced_plosive'
            i = cons_family_list["voiced_plosive"].index(char)  # index of first char
            # first try item i in other plosive list
            partner = cons_family_list["unvoiced_plosive"][i] # used later to skip

            # try partner
            trial_cons = cons_family_list["unvoiced_plosive"][i]
            new_seq = self.replace_cons(ps, consonant_index, trial_cons)
            self.create_rhyme(trial_cons, new_seq, 1)

            self.try_rhyme_category(ps, consonant_index, "voiced_plosive", char, 2)
            self.try_rhyme_category(ps, consonant_index, "unvoiced_plosive", partner, 3)

            self.try_rhyme_category(ps, consonant_index, "voiced_fricative", char, 4)
            self.try_rhyme_category(ps, consonant_index, "unvoiced_fricative", char, 5)

            self.try_rhyme_category(ps, consonant_index, "nasal", char, 6)

            # try partner, then companions, then other 2
            # for g can be long a,e,o u or short u
        elif cons_family[char] == "unvoiced_plosive":
            print 'unvoiced_plosive'
            # try partner, then companions, then other 2
            # for g can be long a,e,o u or short u

            # find partner
            i = cons_family_list["unvoiced_plosive"].index(char)  # index of first char
            # first try item i in other plosive list
            partner = cons_family_list["voiced_plosive"][i] # used later to skip

            # try partner
            trial_cons = cons_family_list["voiced_plosive"][i]
            new_seq = self.replace_cons(ps, consonant_index, trial_cons)
            self.create_rhyme(trial_cons, new_seq, 1)

            self.try_rhyme_category(ps, consonant_index, "unvoiced_plosive", char, 2)
            self.try_rhyme_category(ps, consonant_index, "voiced_plosive", partner, 3)

            self.try_rhyme_category(ps, consonant_index, "voiced_fricative", char, 4)
            self.try_rhyme_category(ps, consonant_index, "unvoiced_fricative", char, 5)

            self.try_rhyme_category(ps, consonant_index, "nasal", char, 6)

        elif cons_family[char] == "nasal":
            print 'nasal'
            self.try_rhyme_category(ps, consonant_index, "nasal", char, 1)

            self.try_rhyme_category(ps, consonant_index, "voiced_plosive", char, 2)
            self.try_rhyme_category(ps, consonant_index, "unvoiced_plosive", char, 3)

            self.try_rhyme_category(ps, consonant_index, "voiced_fricative", char, 4)
            self.try_rhyme_category(ps, consonant_index, "unvoiced_fricative", char, 5)

        elif cons_family[char] == "unique":
            print 'unique'
            self.try_rhyme_category(ps, consonant_index, "voiced_fricative", char, 1)
            self.try_rhyme_category(ps, consonant_index, "unvoiced_fricative", char, 2)

            self.try_rhyme_category(ps, consonant_index, "unique", char, 3)

            self.try_rhyme_category(ps, consonant_index, "voiced_plosive", char, 4)
            self.try_rhyme_category(ps, consonant_index, "unvoiced_plosive", char, 5)

            self.try_rhyme_category(ps, consonant_index, "nasal", char, 6)
            # for L and R in pair, keep first and replace second.
            # if alone, try others in this group
        else:
            pass #shouldn't happen
        
    def additive_rhymes(self, ps):
        """
        # first add s
        # second add plosive, voiced first
        # then add fricatives
        """
        char = "Z"
        newseq = self.add_cons(ps, char)
        index = len(newseq)-1   #last char is len-1

        self.try_rhyme_categories(newseq, index)

        # try unique, then plosives, fricatives, and nasals

        self.try_rhyme_category(newseq, index, "unique", char, 1)
        self.try_rhyme_category(newseq, index, "voiced_plosive", char, 2)
        self.try_rhyme_category(newseq, index, "unvoiced_plosive", char, 3)
        self.try_rhyme_category(newseq, index, "voiced_fricative", char, 4)
        self.try_rhyme_category(newseq, index, "unvoiced_fricative", char, 5)
        self.try_rhyme_category(newseq, index, "nasal", char, 6)
