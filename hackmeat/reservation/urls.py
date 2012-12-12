from django.conf import settings
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template, redirect_to

urlpatterns = patterns('hackmeat.reservation.views',
    url(r'^processor_reserve/?$', r'processor_reserve'),
    url(r'^order/?$', r'order'),
    url(r'^confirmation/?$', r'confirmation'),
    url(r'^reservation_form/$', 'reservation', name='res_form'),
    url(r'^res_cut_step/$', 'cut_step', name='cut_form'),
    url(r'^res_complete/$', 'reservation_complete', name='res_complete'),
    #About URLs
    url(r'about/$', direct_to_template, {'template': 'base/about.html'}),
    #Contact URLs
    url(r'^contact/?$', r'contact', name='contact'),
    url(r'^reservation_form/contact/?$', r'contact', name='contact'),
    url(r'^res_cut_step/contact/?$', r'contact', name='contact'),
    url(r'^res_complete/contact/?$', r'contact', name='contact'),
)
