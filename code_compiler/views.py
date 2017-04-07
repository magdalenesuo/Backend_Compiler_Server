#!/usr/bin/env python


from django.shortcuts import render
from django.http import JsonResponse, HttpResponseForbidden

import requests, json, os

COMPILE_URL = "http://api.hackerearth.com/v3/code/compile/"
RUN_URL = "http://api.hackerearth.com/v3/code/run/"

# access config variable
DEBUG = True
# DEBUG = (os.environ.get('code_compiler_DEBUG') or "").lower() == "true"
CLIENT_SECRET = "f1f795118324bb2afbf0563caa25eac31eff5386"

permitted_languages = ["C", "CPP", "CSHARP", "CLOJURE", "CSS", "HASKELL", "JAVA", "JAVASCRIPT", "OBJECTIVEC", "PERL", "PHP", "PYTHON", "R", "RUBY", "RUST", "SCALA"]


"""
Check if source given with the request is empty
"""
def source_empty_check(source):
  if source == "":
    response = {
      "message" : "Source can't be empty!",
    }
    return JsonResponse(response, safe=False)


"""
Check if lang given with the request is valid one or not
"""
def lang_valid_check(lang):
  if lang not in permitted_languages:
    response = {
      "message" : "Invalid language - not supported!",
    }
    return JsonResponse(response, safe=False)


"""
Handle case when at least one of the keys (lang or source) is absent
"""
def missing_argument_error():
  response = {
    "message" : "ArgumentMissingError: insufficient arguments for compilation!",
  }
  return JsonResponse(response, safe=False)


"""
Method catering to AJAX call at /ide/compile/ endpoint,
makes call at HackerEarth's /compile/ endpoint and returns the compile result as a JsonResponse object
"""
def compileCode(request):
  if request.method == 'POST':
    try:
      source = request.POST['source']
      # Handle Empty Source Case
      source_empty_check(source)

      lang = request.POST['lang']
      # Handle Invalid Language Case
      lang_valid_check(lang)

    except KeyError:
      # Handle case when at least one of the keys (lang or source) is absent
      missing_argument_error()

    else:
      compile_data = {
        'client_secret': CLIENT_SECRET,
        'async': 0,
        'source': source,
        'lang': lang,
      }

      r = requests.post(COMPILE_URL, data=compile_data)
      return JsonResponse(r.json(), safe=False)
  else:
    return HttpResponseForbidden();


"""
Method catering to AJAX call at /ide/run/ endpoint,
makes call at HackerEarth's /run/ endpoint and returns the run result as a JsonResponse object
"""
def runCode(request):
  if request.method == 'POST':
    try:
      source = request.POST['source']
      # Handle Empty Source Case
      source_empty_check(source)

      lang = request.POST['lang']
      # Handle Invalid Language Case
      lang_valid_check(lang)

    except KeyError:
      # Handle case when at least one of the keys (lang or source) is absent
      missing_argument_error()

    else:
      # default value of 5 sec, if not set
      time_limit = request.POST.get('time_limit', 5)
      # default value of 262144KB (256MB), if not set
      memory_limit = request.POST.get('memory_limit', 262144)

      run_data = {
        'client_secret': CLIENT_SECRET,
        'async': 0,
        'source': source,
        'lang': lang,
        'time_limit': time_limit,
        'memory_limit': memory_limit,
      }

      # if input is present in the request
      code_input = ""
      if 'input' in request.POST:
        run_data['input'] = request.POST['input']
        code_input = run_data['input']

      """
      Make call to /run/ endpoint of HackerEarth API
      and save code and result in database
      """
      r = requests.post(RUN_URL, data=run_data)
      r = r.json()
      cs = ""
      rss = ""
      rst = ""
      rsm = ""
      rso = ""
      rsstdr = ""
      try:
        cs = r['compile_status']
      except:
        pass
      try:
        rss=r['run_status']['status']
      except:
        pass
      try:
        rst = r['run_status']['time_used']
      except:
        pass
      try:
        rsm = r['run_status']['memory_used']
      except:
        pass
      try:
        rso = r['run_status']['output_html']
      except:
        pass
      try:
        rsstdr = r['run_status']['stderr']
      except:
        pass

      return JsonResponse(r, safe=False)
  else:
    return HttpResponseForbidden()
