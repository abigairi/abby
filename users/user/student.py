import os
from flask import Blueprint, render_template, request, current_app, session, redirect, flash
from werkzeug.utils import secure_filename
from database import mysql
# import librosa
# import matplotlib.pyplot as plt
import wave
import audiodiff

student = Blueprint('student', __name__)






@app.route('/')
def home():
    return render_template('student/home.html')


@app.route('/levelone')
def levelone():
    return render_template('student/levelone.html')


@app.route('/leveltwo')
def leveltwo():
    return render_template('student/leveltwo.html')


@app.route('/levelthree')
def levelthree():
    return render_template('student/levelthree.html')


@app.route('/alphabets')
def alphabets():
    return render_template('student/level1/ALPHABETS.html')


@app.route('/vowels')
def atou():
    return render_template('student/level1/VOWELS.html')


@app.route('/syllable')
def batoza():
    return render_template('student/level1/SYLLABLE.html')


@app.route('/word1')
def sentence1():
    return render_template('student/level1/WORDS1.html')


@app.route('/word2')
def numbers():
    return render_template('student/level1/WORDS2.html')


@app.route('/adjective')
def adjective():
    return render_template('student/level2/ADJECTIVE.html')


@app.route('/adverb')
def adverb():
    return render_template('student/level2/ADVERB.html')


@app.route('/link')
def link():
    return render_template('student/level2/LINK.html')


@app.route('/noun')
def noun():
    return render_template('student/level2/NOUN.html')


@app.route('/preposition')
def preposition():
    return render_template('student/level2/PREPOSITION.html')


@app.route('/pronoun')
def pronoun():
    return render_template('student/level2/PRONOUN.html')


@app.route('/verb')
def verb():
    return render_template('student/level2/VERB.html')


@app.route('/bodyparts')
def bodyparts():
    return render_template('student/level3/BODY PARTS.html')


@app.route('/greetings')
def greetings():
    return render_template('student/level3/GREETINGS.html')


@app.route('/colors')
def colors():
    return render_template('student/level3/COLORS.html')


@app.route('/days')
def days():
    return render_template('student/level3/DAYS.html')


@app.route('/month')
def month():
    return render_template('student/level3/MONTH.html')


@app.route('/levelone/selflearn')
def levelone_selflearn():
    workingdir = os.path.abspath(os.getcwd())
    filepath = workingdir + '/mysite/static/'
    path = filepath + 'Ada.wav'
    path2 = filepath + 'Ba.wav'
    # startConvertion(path)
    # w_one = wave.open(path, 'r')
    # w_two = wave.open(path2, 'r')
    rs=audiodiff.equal(path, path2)
    print('results', rs)

    return render_template('student/level1/self.html')