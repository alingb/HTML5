"""djangoTest URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url


from linux import views

urlpatterns = [
    url(r"^$", views.index, name="index"),
    url(r'test/$', view=views.test, kwargs={"name": "ling"}, name="test"),
    url(r'hello/p1(\w+)p2(.+)/$', views.hello, name="hello"),
    url(r'keyword/(?P<ip>\S+)/$', views.keyword, name="keyword"),
    url(r'redirect/$', view=views.redirect, name="redirect"),
    url(r'teacher/list/$', view=views.teacherList, name="teacherList"),
]