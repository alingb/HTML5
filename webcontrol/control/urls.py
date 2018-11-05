from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'index', index, name='index'),
    url(r'serverdetail', serverDetail, name='index'),
    url(r'bios', bios, name='index'),
    url(r'ipmi', ipmi, name='index'),
]
