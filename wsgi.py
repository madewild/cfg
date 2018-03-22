"""Main web server logic"""

from flask import Flask, render_template
application = Flask(__name__)

@application.route("/")
def form():
    return render_template('form.html')

@application.route("/correction", methods=['GET', 'POST'])
def corr():
    return render_template('corr.html')

if __name__ == "__main__":
    application.run()