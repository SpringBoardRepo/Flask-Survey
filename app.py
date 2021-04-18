
from flask import Flask, redirect, render_template, request, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey


app = Flask(__name__)
app.config['SECRET_KEY'] = 'survey_app'
debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

response = []


@app.route('/')
def home_page():
    return render_template('start_survey.html', survey=satisfaction_survey)


@app.route('/question/<int:id>')
def question_page(id):

    if (response is None):
        return redirect('/')

    if (len(response) == len(satisfaction_survey.questions)):
        return redirect('/complete')

    if (len(response) != id):
        flash('Invalid Question Id :' + id)
        return redirect(f'/question/{len(response)}')

    question = satisfaction_survey.questions[id]
    return render_template('question.html', question=question, ques_num=id)


@app.route('/answer', methods=['POST'])
def answer_page():

    choice = request.form['answer']
    response.append(choice)

    if (len(response) == len(satisfaction_survey.questions)):
        return redirect('/complete')

    else:
        return redirect(f'question/{len(response)}')


@app.route('/complete')
def complete_survey():
    return render_template('complete.html')
