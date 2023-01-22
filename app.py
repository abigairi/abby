from flask import Flask, redirect, render_template, request

import speech_recognition as sr
import os
from pydub import AudioSegment
from pydub.silence import split_on_silence



app = Flask(__name__)

app.secret_key = 'your secret key'


r = sr.Recognizer()

def get_large_audio_transcription(path):
    """
    Splitting the large audio file into chunks
    and apply speech recognition on each of these chunks
    """
    # open the audio file using pydub
    sound = AudioSegment.from_wav(path)
    # split audio sound where silence is 700 miliseconds or more and get chunks
    chunks = split_on_silence(sound,
        # experiment with this value for your target audio file
        min_silence_len = 500,
        # adjust this per requirement
        silence_thresh = sound.dBFS-14,
        # keep the silence for 1 second, adjustable as well
        keep_silence=500,
    )
    folder_name = "audio-chunks"
    # create a directory to store the audio chunks
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    whole_text = ""
    # process each chunk
    for i, audio_chunk in enumerate(chunks, start=1):
        # export audio chunk and save it in
        # the `folder_name` directory.
        chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")
        # recognize the chunk
        with sr.AudioFile(chunk_filename) as source:
            audio_listened = r.record(source)
            # try converting it to text
            try:
                text = r.recognize_google(audio_listened, language="sw-TZ")
            except sr.UnknownValueError as e:
                return "We failed to know what you sayed, repeat again"
            else:
                text = f"{text.capitalize()}. "
                print(chunk_filename, ":", text)
                whole_text += text
    # return the text for all chunks detected
    return " " + whole_text

@app.route('/')
@app.route('/student')
def home():
    return render_template('student/home.html')


@app.route('/student/levelone')
def levelone():
    return render_template('student/levelone.html')


@app.route('/student/leveltwo')
def leveltwo():
    return render_template('student/leveltwo.html')


@app.route('/student/levelthree')
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


@app.route('/student/adjective')
def adjective():
    return render_template('student/level2/ADJECTIVE.html')


@app.route('/student/adverb')
def adverb():
    return render_template('student/level2/ADVERB.html')


@app.route('/student/link')
def link():
    return render_template('student/level2/LINK.html')


@app.route('/student/noun')
def noun():
    return render_template('student/level2/NOUN.html')


@app.route('/student/preposition')
def preposition():
    return render_template('student/level2/PREPOSITION.html')


@app.route('/student/pronoun')
def pronoun():
    return render_template('student/level2/PRONOUN.html')


@app.route('/student/verb')
def verb():
    return render_template('student/level2/VERB.html')


@app.route('/student/bodyparts')
def bodyparts():
    return render_template('student/level3/BODY PARTS.html')


@app.route('/student/greetings')
def greetings():
    return render_template('student/level3/GREETINGS.html')


@app.route('/student/colors')
def colors():
    return render_template('student/level3/COLORS.html')


@app.route('/student/days')
def days():
    return render_template('student/level3/DAYS.html')


@app.route('/student/month')
def month():
    return render_template('student/level3/MONTH.html')


@app.route('/levelone/selflearn')
def levelone_selflearn():
    workingdir = os.path.abspath(os.getcwd())
    filepath = workingdir + '/mysite/static/'
    path = filepath + 'A.wav'
    path2 = filepath + 'Recording.wav'
    # startConvertion(path)
    # w_one = wave.open(path, 'r')
    # w_two = wave.open(path2, 'r')
    # rs=audiodiff.audio_equal(path, path2)
    # print('results', rs)

    return render_template('student/level1/self.html')

@app.route("/selfone", methods=['POST', 'GET'])
def selfone():
    if request.method == "POST":
        f = request.files['audio_data']
        with open('audio.wav', 'wb') as audio:
            f.save(audio)
        # check
        rs = get_large_audio_transcription('audio.wav')
        print(rs)
        # if rs == 'baba' or rs== 'Baba' or rs=='BABA':
        #     sms = 'you pronounce correct' + ' ' + rs
        #     return sms
        # else:
        #     sms = 'you have pronounce wrong ' + ' ' +  rs
        #     return sms
        return rs


    else:
        rs = get_large_audio_transcription('audio.wav')
        return render_template('student/level1/self.html',rs=rs)

@app.route("/self2", methods=['POST', 'GET'])
def self2():
    if request.method == "POST":
        f = request.files['audio_data']
        with open('audio.wav', 'wb') as audio:
            f.save(audio)
        # check
        rs = get_large_audio_transcription('audio.wav')
        print(rs)
        # if rs == 'mama' or rs== 'Mama' or rs=='MAMA':
        #     sms = 'you pronounce correct' + ' ' + rs
        #     return sms
        # else:
        #     sms = 'you have pronounce wrong ' + ' ' +  rs
        #     return sms
        return rs


    else:
        rs = get_large_audio_transcription('audio.wav')
        return render_template('student/level1/self2.html',rs=rs)


@app.route("/level2/next2", methods=['POST', 'GET'])
def self2next2():
    if request.method == "POST":
        f = request.files['audio_data']
        with open('audio.wav', 'wb') as audio:
            f.save(audio)
        # check
        rs = get_large_audio_transcription('audio.wav')
        print(rs)
        # if rs == 'mama' or rs== 'Mama' or rs=='MAMA':
        #     sms = 'you pronounce correct' + ' ' + rs
        #     return sms
        # else:
        #     sms = 'you have pronounce wrong ' + ' ' +  rs
        #     return sms
        return rs


    else:
        rs = get_large_audio_transcription('audio.wav')
        return render_template('student/level2/next2.html',rs=rs)



@app.route("/level2/next3", methods=['POST', 'GET'])
def self2next3():
    if request.method == "POST":
        f = request.files['audio_data']
        with open('audio.wav', 'wb') as audio:
            f.save(audio)
        # check
        rs = get_large_audio_transcription('audio.wav')
        print(rs)
        # if rs == 'mama' or rs== 'Mama' or rs=='MAMA':
        #     sms = 'you pronounce correct' + ' ' + rs
        #     return sms
        # else:
        #     sms = 'you have pronounce wrong ' + ' ' +  rs
        #     return sms
        return rs


    else:
        rs = get_large_audio_transcription('audio.wav')
        return render_template('student/level2/next3.html',rs=rs)



@app.route("/self3", methods=['POST', 'GET'])
def self3():
    if request.method == "POST":
        f = request.files['audio_data']
        with open('audio.wav', 'wb') as audio:
            f.save(audio)
        # check
        rs = get_large_audio_transcription('audio.wav')
        print(rs)
        if rs == 'dada' or rs== 'Dada' or rs=='DADA':
            sms = 'you pronounce correct' + ' ' + rs
            return sms
        else:
            sms = 'you have pronounce wrong ' + ' ' +  rs
            return sms


    else:
        rs = get_large_audio_transcription('audio.wav')
        return render_template('student/level1/self3.html',rs=rs)


@app.route("/level3/next2", methods=['POST', 'GET'])
def self3next2():
    if request.method == "POST":
        f = request.files['audio_data']
        with open('audio.wav', 'wb') as audio:
            f.save(audio)
        # check
        rs = get_large_audio_transcription('audio.wav')
        print(rs)
        # if rs == 'mama' or rs== 'Mama' or rs=='MAMA':
        #     sms = 'you pronounce correct' + ' ' + rs
        #     return sms
        # else:
        #     sms = 'you have pronounce wrong ' + ' ' +  rs
        #     return sms
        return rs


    else:
        rs = get_large_audio_transcription('audio.wav')
        return render_template('student/level3/next2.html',rs=rs)


@app.route("/level3/next3", methods=['POST', 'GET'])
def self3next3():
    if request.method == "POST":
        f = request.files['audio_data']
        with open('audio.wav', 'wb') as audio:
            f.save(audio)
        # check
        rs = get_large_audio_transcription('audio.wav')
        print(rs)
        # if rs == 'mama' or rs== 'Mama' or rs=='MAMA':
        #     sms = 'you pronounce correct' + ' ' + rs
        #     return sms
        # else:
        #     sms = 'you have pronounce wrong ' + ' ' +  rs
        #     return sms
        return rs


    else:
        rs = get_large_audio_transcription('audio.wav')
        return render_template('student/level3/next3.html',rs=rs)



@app.route("/self4", methods=['POST', 'GET'])
def self4():
    if request.method == "POST":
        f = request.files['audio_data']
        with open('audio.wav', 'wb') as audio:
            f.save(audio)
        # check
        rs = get_large_audio_transcription('audio.wav')
        print(rs)
        if rs == 'kaka' or rs== 'Kaka' or rs=='KAKA':
            sms = 'you pronounce correct' + ' ' + rs
            return sms
        else:
            sms = 'you have pronounce wrong ' + ' ' +  rs
            return sms


    else:
        rs = get_large_audio_transcription('audio.wav')
        return render_template('student/level1/self4.html',rs=rs)



@app.route('/leveltwo/selflearn')
def leveltwo_selflearn():
    workingdir = os.path.abspath(os.getcwd())
    filepath = workingdir + '/mysite/static/'
    path = filepath + 'A.wav'
    path2 = filepath + 'Recording.wav'
    # startConvertion(path)
    # w_one = wave.open(path, 'r')
    # w_two = wave.open(path2, 'r')
    # rs=audiodiff.audio_equal(path, path2)
    # print('results', rs)

    return render_template('student/level2/self.html')


@app.route('/levelthree/selflearn')
def levelthree_selflearn():
    workingdir = os.path.abspath(os.getcwd())
    filepath = workingdir + '/mysite/static/'
    path = filepath + 'A.wav'
    path2 = filepath + 'Recording.wav'

    return render_template('student/level3/self.html')

@app.route('/level4/selflearn')
def level4_selflearn():
    if request.method == "POST":
        f = request.files['audio_data']
        with open('audio.wav', 'wb') as audio:
            f.save(audio)
        # check
        rs = get_large_audio_transcription('audio.wav')

        return rs
    else:
        return render_template('student/level3/self.html')




if __name__ == '__main__':
    app.run()