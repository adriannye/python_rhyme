from django.conf.urls import patterns, include, url
from django.views.generic.base import RedirectView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),
    url(r'^rhyme/', include('rhyme.urls')),

    # visit to / should go to /rhyme
    url(r'^.*$', RedirectView.as_view(url='rhyme/', permanent=True), name='index')
)

