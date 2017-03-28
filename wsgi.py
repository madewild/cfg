#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Python app for CFG grammar
"""

#pylint: disable = locally-disabled, invalid-name

import os
from cgi import parse_qs, escape

virtenv = os.environ['OPENSHIFT_PYTHON_DIR'] + '/virtenv/'
virtualenv = os.path.join(virtenv, 'bin/activate_this.py')
try:
    execfile(virtualenv, dict(__file__=virtualenv))
except IOError:
    pass
#
# IMPORTANT: Put any additional includes below this line.  If placed above this
# line, it's possible required libraries won't be in your searchable path
#

import nltk

def corr(string):
    '''Compute score based on CFG input'''
    pos = open(os.environ['OPENSHIFT_REPO_DIR']+'pos.txt').readlines()
    pos = [line.strip() for line in pos]

    neg = open(os.environ['OPENSHIFT_REPO_DIR']+'neg.txt').readlines()
    neg = [line.strip() for line in neg]

    lowstring = string.lower()
    gram = nltk.CFG.fromstring(lowstring)
    parser = nltk.ChartParser(gram)
    p = 0
    n = 0
    for text in pos:
        tokens = nltk.tokenize.wordpunct_tokenize(text.lower())
        try:
            trees = parser.parse(tokens)
        except ValueError:
            trees = []
        if len(list(trees)) > 0:
            p += 1
    for text in neg:
        tokens = nltk.tokenize.wordpunct_tokenize(text.lower())
        try:
            trees = parser.parse(tokens)
        except ValueError:
            trees = []
        for tree in trees:
            if tree:
                n += 1
    score = max(0, p-n)
    return score, p, n

def application(environ, start_response):
    '''Main app'''
    ctype = 'text/plain'
    if environ['PATH_INFO'] == '/health':
        response_body = "1"
    elif environ['PATH_INFO'] == '/env':
        response_body = ['%s: %s' % (key, value)
                         for key, value in sorted(environ.items())]
        response_body = '\n'.join(response_body)
    elif environ['PATH_INFO'] == '/correction':
        try:
            request_body_size = int(environ.get('CONTENT_LENGTH', 0))
        except ValueError:
            request_body_size = 0
        request_body = environ['wsgi.input'].read(request_body_size)
        d = parse_qs(request_body)
        cfg = d.get('cfg', [''])[0]
        #cfg = escape(cfg)
        try:
            score, p, n = corr(cfg)
            response_body = "Score partiel : " + str(score) + "/10 (" + str(p) + " bonnes phrases et " + str(n) + " mauvaises phrases reconnues)"
        except ValueError:
            response_body = "<html><head></head><body>Grammaire non-valide, veuillez vérifier la syntaxe :<br><br>" + cfg + "</body></html>"

    else:
        ctype = 'text/html'
        response_body = '''<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>TP CFG</title>
<style>

*, *:before, *:after {
    -moz-box-sizing: border-box;
    box-sizing: border-box;
}
aside,
footer,
header,
hgroup,
section{
  display: block;
}
body {
  color: #404040;
  font-family: "Helvetica Neue",Helvetica,"Liberation Sans",Arial,sans-serif;
  font-size: 14px;
  line-height: 1.4;
}
html {
  font-family: sans-serif;
  -ms-text-size-adjust: 100%;
  -webkit-text-size-adjust: 100%;
}
hgroup {
  margin-top: 50px;
}
h1, h2, h3 {
  color: #000;
  line-height: 1.38em;
  margin: 1.5em 0 .3em;
}
h1 {
  font-size: 25px;
  font-weight: 300;
  border-bottom: 1px solid #fff;
  margin-bottom: .5em;
}
h1:after {
  content: "";
  display: block;
  width: 100%;
  height: 1px;
  background-color: #ddd;
}
p {
  margin: 0 0 2em;
}
html {
  background: #f5f5f5;
  height: 100%;
}
</style>
</head>
<body>
    <hgroup>
        <h1>TP sur les grammaires CFG</h1>
    </hgroup>
    <div align="center">
        <form method="POST" action="/correction">
            <textarea rows="40" cols="100" name="cfg">Copiez ici votre grammaire</textarea><br>
            <input type="submit">
        </form>
    </div>
</body>
</html>'''

    status = '200 OK'
    response_headers = [('Content-Type', ctype), ('Content-Length', str(len(response_body)))]
    #
    start_response(status, response_headers)
    return [response_body]

#
# Below for testing only
#
if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    httpd = make_server('localhost', 8051, application)
    # Wait for a single request, serve it and quit.
    httpd.handle_request()
