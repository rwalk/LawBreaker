#!/usr/bin/env python
from flask import Flask, render_template, request
import random

app = Flask(__name__)

SHAKESPEARE_START = 176
SHAKESPEARE_LINES = 124787
WINDOW_SIZE = 31

thank_yous = ["Thanks. I'm much smarter now!", "Awesome. Don't worry, I'm not skynet.", "Cool. That helps", "Thanks. I'm 1% smarter now.", "Wow, I learned so much from you.", "Cool. You get a gold star."] 

def get_some_text():
    start = random.randint(SHAKESPEARE_START, SHAKESPEARE_LINES-WINDOW_SIZE)
    end = start + WINDOW_SIZE
    count = 0
    text = []
    with open("data/shakespeare.txt") as f:
        for l in f:
            count+=1
            if count>=start and count<end:
                text.append(l.strip())
    return("\n".join(text))

def digest_submission(result_text):
    with open("data/training.out", "a") as f:
        for line in result_text.split("\n"):
            line = line.strip()
            if len(line)>5:
                f.write(line + "\n\n")
    return True    

@app.route("/")
def modules_home():
    return render_template("index.html")

@app.route("/sentences", methods=["GET","POST"])
def sentence_breaker():
    thank, message = False,None
    if request.form is not None and 'submit' in request.form:
        thank = digest_submission(request.form['text'])
        message = message=random.choice(thank_yous)  + " Want to do some more?"
    return render_template("sentences.html", input_text=get_some_text(), thank=thank, message=message)

if __name__ == "__main__":
    app.run(debug=True)
