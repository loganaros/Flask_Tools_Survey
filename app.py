from flask import Flask, request, render_template, redirect, flash
from surveys import satisfaction_survey
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

app.config['SECRET_KEY'] = 'ajeifjaifjaeofjd'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
# debug = DebugToolbarExtension(app)

responses = []

@app.route("/")
def survey_page():
    return render_template("home.html",  title=satisfaction_survey.title, instructions=satisfaction_survey.instructions, questions=satisfaction_survey.questions)

@app.route("/start", methods=["POST"])
def start_survey():
    return redirect("/questions/0")

@app.route("/thank-you")
def end_page():
    return render_template("thank-you.html", responses=responses)

@app.route("/questions/<int:question_number>")
def questions_page(question_number):
    if len(responses) != question_number:
        flash("Invalid Response")
        return redirect(f"/questions/{len(responses)}")
    
    return render_template("questions.html", title=satisfaction_survey.title, instructions=satisfaction_survey.instructions, question=satisfaction_survey.questions[question_number])

@app.route("/answer", methods=["POST"])
def save_answer():
    responses.append(request.form["choice"])

    if len(responses) < len(satisfaction_survey.questions):
        return redirect(f"/questions/{len(responses)}")
    else:
        return redirect("/thank-you")