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
    def get(self, request, word=None):
        word = Word.objects.select_related('phoneme_sequence').get(word=word)
        rps = RhymePhonemeSequence.objects.select_related().filter(original_ps=word.phoneme_sequence).order_by('order')
        serializer = RhymePhonemeSequenceSerializer(rps, many=True)
        return Response(serializer.data)

class ListRhymes(APIView):
    """
    View to list rhymes for a phoneme sequence
    """
    permission_classes = (IsAuthenticatedOrReadOnly,)
    def get(self, request, ps=None):
        words = Word.objects.filter(phoneme_sequence__text=ps).prefetch_related('parts_of_speech')
        serializer = WordSerializer(words, many=True)
        return Response(serializer.data)

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
