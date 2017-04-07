#!/usr/bin/env python

from django.conf.urls import url

from . import views

app_name = 'code_compiler'

urlpatterns = [
  # ex: /compile/
  url(r'^compile/$', views.compileCode, name='compile'),
  # ex: /run/
  url(r'^run/$', views.runCode, name='run'),
]
