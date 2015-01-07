from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class PhonemeSequence(models.Model):
    """
    Represents the sequence of sounds that end a word.
    """
    text = models.CharField(max_length=255, db_index=True) 

    def __unicode__(self):  # Python 3: def __str__(self):
        return self.text

    class Meta:
        ordering = ['text']


class RhymePhonemeSequence(models.Model):
    """
    Represents a phoneme sequence that rhymes in a certain way with
    the phoneme sequence for a word

    Essentially this relates a list of rhyme phoneme sequences to the one for the word.
    We relate to the phonemesequence, not the word, because more that one word may have the same phoneme sequence.
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
        return "%s %s-%s: %s" % (self.original_ps, self.rhyme_type, self.sound, self.order)


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

    def __unicode__(self):  # Python 3: def __str__(self):
            return self.word

    class Meta:
        ordering = ['word']


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
    word = models.OneToOneField(Word)

    def __unicode__(self):  # Python 3: def __str__(self):
        return "user_added: %s flagged: %s reviewed: %s paid: %s" % \
                (self.user_added, self.flagged, self.reviewed, self.paid)
