from django.core.context_processors import csrf
from django.conf.urls import url, patterns, include
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView
from django.views.decorators.csrf import ensure_csrf_cookie

from rest_framework import viewsets, routers, generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from rhyme.models import Word, RhymePhonemeSequence, PhonemeSequence
from rhyme.serializers import PhonemeSequenceSerializer, RhymePhonemeSequenceSerializer, WordSerializer


class ListRhymePhonemeSequences(APIView):
    """
    View to list all rhyme phoneme sequences for a word
    """
    permission_classes = (IsAuthenticatedOrReadOnly,)
    def get(self, request, word):
        word = Word.objects.select_related('phoneme_sequence').get(word=word)
        rps = RhymePhonemeSequence.objects.select_related().filter(original_ps=word.phoneme_sequence).order_by('order')
        serializer = RhymePhonemeSequenceSerializer(rps, many=True)
        return Response(serializer.data)

class ListRhymes(APIView):
    """
    View to list rhymes for a phoneme sequence
    """
    permission_classes = (IsAuthenticatedOrReadOnly,)
    def get(self, request, ps):
        words = Word.objects.filter(phoneme_sequence__text=ps).prefetch_related('parts_of_speech')
        serializer = WordSerializer(words, many=True)
        return Response(serializer.data)

class ListRhymesForWord(APIView):
    """
    View to list rhymes for a word.  

    Returns a nested list, outeer list is rhyme types,
    inner list is rhymes for that rhyme type. 
    """
    permission_classes = (IsAuthenticatedOrReadOnly,)
    def get(self, request, word):
        # first see if we know the word at all.
        try:
            word = Word.objects.get(word=word)
        except Word.DoesNotExist:
            return Response({'error': 'Word not found'})

        ps_id = word.phoneme_sequence_id

        # perfect rhymes first

        perfect = Word.objects.filter(phoneme_sequence_id=word.phoneme_sequence_id)\
                    .values('word', 'pos')

        perfect_rhymes_in_rps_format = [
            {
                "sound": "", 
                "rhymes": perfect,
                "order": 0, 
                "rhyme_type": "PERFECT"
            }, 
        ]

        # we could do this in two stages: get rps objects, then get rhymes
        # for each rps object.  But that ends up with multiple queries.
        # First attempt to do in a single query.

        rpses = RhymePhonemeSequence.objects\
                .filter(original_ps_id=ps_id)\
                .order_by('order')\
                .values('sound', 'rhyme_type', 'order', 'rhyme_ps_id')

        for rps in rpses:
            rps['rhymes'] = Word.objects\
                    .filter(phoneme_sequence_id=rps['rhyme_ps_id'])\
                    .values('word', 'pos')

        # because rpses is a ValuesQuerySet and we need it in list form to add
        rps_list = [rps for rps in rpses]
        return Response(perfect_rhymes_in_rps_format + rps_list)

class RhymePhonemeSequenceViewSet(viewsets.ModelViewSet):
    """
    """
    queryset = RhymePhonemeSequence.objects.all()
    serializer_class = RhymePhonemeSequenceSerializer

class PhonemeSequenceViewSet(viewsets.ModelViewSet):
    """
    """
    queryset = PhonemeSequence.objects.all()
    serializer_class = PhonemeSequenceSerializer


class IndexView(TemplateView):
    template_name = 'index.html'

    @method_decorator(ensure_csrf_cookie)
    def dispatch(self, *args, **kwargs):
        return super(IndexView, self).dispatch(*args, **kwargs)

class RedirectView(TemplateView):
    template_name = 'index.html'

    @method_decorator(ensure_csrf_cookie)
    def dispatch(self, *args, **kwargs):
        return super(IndexView, self).dispatch(*args, **kwargs)
