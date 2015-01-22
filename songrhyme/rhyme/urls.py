from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from django.conf import settings

from rest_framework import routers

from rhyme.views import *

#router = routers.DefaultRouter()
#router.register(r'ps', PhonemeSequenceViewSet)
#router.register(r'rps', RhymePhonemeSequenceViewSet)

urlpatterns = patterns('rhyme.views',

    # json data sources
    url(r'^api/accounts/', include('authemail.urls')),
    url('^api/ps_for_word/(?P<word>.+)/$', ListRhymePhonemeSequences.as_view()),
    url('^api/rhymes_for_ps/(?P<ps>.+)/$', ListRhymes.as_view()),
    url('^api/rhymes_for_word/(?P<word>.+)/$', ListRhymesForWord.as_view()),

    # main angular view
    url(r'^$', IndexView.as_view(), name='index'),
    )

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
