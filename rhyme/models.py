from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class PeerReview(models.Model):
    """
    Represents review status of a word.
    Views that modify this require login.
    """
    user_added = models.BooleanField(default=False)
    flagged = models.BooleanField(default=False)
    reviewed = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
    added_date = models.DateTimeField(auto_now_add=True)
    added_by = models.ForeignKey(User)

    def __unicode__(self):  # Python 3: def __str__(self):
        return "user_added: %s flagged: %s reviewed: %s paid: %s" % \
                (self.user_added, self.flagged, self.reviewed, self.paid)

class PhonemeSequence(models.Model):
    """
    Represents the sounds of a word.   Used in two contexts - for the word being rhymed, and 
    also for the wordlists that are rhymes.

    The sound field is used as a heading when displaying the rhyme lists.
    """
    text = models.CharField(max_length=255) 

    def __unicode__(self):  # Python 3: def __str__(self):
        return self.text


class RhymePhonemeSequence(models.Model):
    """
    Represents an ordered list of rhyme phoneme sequences for a particular phoneme sequence
    """
    FAMILY = 'FAMILY'
    ADDITIVE = 'ADDITIVE'
    SUBTRACTIVE = 'SUBTRACTIVE'
    RHYME_TYPES = (
        (FAMILY, 'Family'),
        (ADDITIVE, 'Additive'),
        (SUBTRACTIVE, 'Subtractive'),
    )

    sound = models.CharField(max_length=30) # user-visible description of sound
    original_ps = models.ForeignKey(PhonemeSequence, related_name='original_phoneme_sequences')
    rhyme_ps = models.ForeignKey(PhonemeSequence, related_name='rhyme_phoneme_sequences')
    rhyme_type = models.CharField(max_length=20, choices=RHYME_TYPES)
    order = models.IntegerField() 

    def __unicode__(self):  # Python 3: def __str__(self):
        return "%s-%s: %s" % (self.rhyme_type, self.sound, self.order)


class PartOfSpeech(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name_plural = 'Parts of Speech'

    def __unicode__(self):  # Python 3: def __str__(self):
            return self.name

class Word(models.Model):
    """
    Represents a word
    """
    word = models.CharField(max_length=255, unique=True, db_index=True)
    phoneme_sequence = models.ForeignKey(PhonemeSequence)
    parts_of_speech = models.ManyToManyField(PartOfSpeech)
    peer_review = models.OneToOneField(PeerReview)

    def __unicode__(self):  # Python 3: def __str__(self):
            return self.word

"""
To get rhyme lists:
1.  word = Word.objects.select_related('rhyme_phoneme_sequences').get(word=word)
3. rhyme_lists = []
     for rhyme_phoneme_sequence in word.rhyme_phoneme_sequences:
        rhymes = Word.objects.select_related('phoneme_sequence')\
            .filter(phoneme_sequence=rhyme_phoneme_sequence.phoneme_sequence)\
            .prefetch_related('rhyme_phoneme_sequence')

        rhyme_lists.append({
            'sound': rhyme_phoneme_sequence.sound,
            'rhyme_type': rhyme_phoneme_sequence.rhyme_type,
            'order': rhyme_phoneme_sequence.order,
            'rhymes': rhymes,
        })
"""
