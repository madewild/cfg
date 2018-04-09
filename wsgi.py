"""Main web server logic"""

from flask import Flask, render_template, request
from toolbox import test_cfg
application = Flask(__name__)

@application.route("/", methods=['GET', 'POST'])
def form():
    try:
        data = request.form
        gram = data['gram']
        return render_template('gram.html', gram=gram)
    except:
        return render_template('form.html')

@application.route("/correction", methods=['GET', 'POST'])
def corr():
    data = request.form
    gram = data['cfg']
    try:
        score, p, n, fneg, fpos, = test_cfg(gram)
        correct = 'phrase correcte' if p == 1 else 'phrases correctes'
        incorrect = 'phrase incorrecte' if n == 1 else 'phrases incorrectes'
        return render_template('corr.html', score=str(score), p=str(p), n=str(n), correct=correct, incorrect=incorrect, fneg=fneg, fpos=fpos, gram=gram)
    except ValueError as e:
        print(e)
        return render_template('wrong.html', gram=gram)

if __name__ == "__main__":
    application.run()
