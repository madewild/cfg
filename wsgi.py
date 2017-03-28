#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Python app for CFG grammar
"""

#pylint: disable = locally-disabled, invalid-name, line-too-long

import os
from cgi import parse_qs

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
        h1 {
        color: #000;
        line-height: 1.38em;
        margin: 1.5em 0 .3em;
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
        pre {
            background-color: #ccc
        }
        </style>
        <script>
        function clearContents(element) {
            element.value = '';
        }
        </script>
        </head>
        '''
    if environ['PATH_INFO'] == '/correction':
        try:
            request_body_size = int(environ.get('CONTENT_LENGTH', 0))
        except ValueError:
            request_body_size = 0
        request_body = environ['wsgi.input'].read(request_body_size)
        d = parse_qs(request_body)
        cfg = d.get('cfg', [''])[0]
        try:
            score, p, n = corr(cfg)
            body = '''<body><h1>Grammaire valide</h1><p>Score partiel : <b>" + str(score) + "/10</b></p>
                      <p>" + str(p) + " bonnes phrases et " + str(n) + " mauvaises phrases reconnues</p>
                      <h2>Faux négatifs (bonnes phrases non reconnues)<h2>
                      <h2>Faux positifs (mauvaises phrases reconnues par erreur</h2>
                      </body></html>'''
        except ValueError:
            body = '''<body><h1>Grammaire non-valide</h1><p>Veuillez vérifier la syntaxe :<br></p>
                      <pre>" + cfg + "</pre>
                      <form method="POST" action="/">
                        <input type="submit" value="Retour">
                      </form>  
                      </body></html>'''
        response_body += body
    else:
        response_body += '''
<body>
    <div align="center">
        <h1>TP sur les grammaires CFG</h1>
        <br>
        <form method="POST" action="/correction">
            <textarea rows="40" cols="100" name="cfg" onfocus="clearContents(this);">Copiez ici votre grammaire...</textarea><br><br>
            <input type="submit" value="Envoyer">
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
