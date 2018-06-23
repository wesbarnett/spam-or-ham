from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import SubmissionForm
from joblib import load
import requests

@app.route('/', methods=['GET', 'POST'])
def index():
    form = SubmissionForm()
    if form.validate_on_submit():
        clf = load('clf.gz')
        text = form.text.data
        print(text)
        prediction = clf.predict([text])
        if prediction[0] == 1:
            flash('SPAM')
        else:
            flash('HAM')
    return render_template('index.html', form=form)
