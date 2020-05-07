"""Main web server logic"""

import logging
from flask import Flask, render_template, request
from toolbox import test_cfg, eval_sent
app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def form():
    try:
        data = request.form
        gram = data['gram']
        return render_template('gram.html', gram=gram)
    except:
        return render_template('form.html')

@app.route("/correction", methods=['GET', 'POST'])
def corr():
    data = request.form
    gram = data['cfg']
    sent = data['sent']
    if sent and sent != "Testez ici une seule phrase (optionnel)":
        try:
            success = eval_sent(gram, sent)
            msg = "a bien" if success else "n'a pas"
            return render_template('corr2.html', sent=sent, msg=msg, gram=gram)
        except ValueError as e:
            print(e)
            return render_template('wrong.html', gram=gram)
    else:
        try:
            score, p, n, fneg, fpos, = test_cfg(gram)
            correct = 'phrase correcte' if p == 1 else 'phrases correctes'
            incorrect = 'phrase incorrecte' if n == 1 else 'phrases incorrectes'
            return render_template('corr.html', score=str(score), p=str(p), n=str(n), correct=correct, incorrect=incorrect, fneg=fneg, fpos=fpos, gram=gram)
        except ValueError as e:
            print(e)
            return render_template('wrong.html', gram=gram)

@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500

if __name__ == "__main__":
    app.run()
