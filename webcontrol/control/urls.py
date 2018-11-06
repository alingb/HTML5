from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'index', index, name='index'),
    url(r'serverdetail', serverDetail, name='serverdetail'),
    url(r'bios', bios, name='bios'),
    url(r'ipmi', ipmi, name='ipmi'),
    url(r'serverinfo', serverInfo, name='serverinfo'),
]
