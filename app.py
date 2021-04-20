
from flask import Flask, redirect, render_template, request, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey


app = Flask(__name__)
app.config['SECRET_KEY'] = 'survey_app'
debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
RESPONSE_KEY = 'responses'


@app.route('/')
def home_page():
    session[RESPONSE_KEY] = []
    return render_template('start_survey.html', survey=satisfaction_survey)


@app.route('/question/<int:id>')
def question_page(id):

    responses = session.get(RESPONSE_KEY)

    if (responses is None):
        return redirect('/')

    if (len(responses) == len(satisfaction_survey.questions)):
        return redirect('/complete')

    if (len(responses) != id):
        flash(f'Invalid Question Id :{id}')
        return redirect(f'/question/{len(responses)}')

    question = satisfaction_survey.questions[id]
    return render_template('question.html', question=question, ques_num=id)


@app.route('/answer', methods=['POST'])
def answer_page():

    choice = request.form['answer']
    responses = session[RESPONSE_KEY]
    responses.append(choice)
    session[RESPONSE_KEY] = responses

    if (len(responses) == len(satisfaction_survey.questions)):
        return redirect('/complete')

    else:
        return redirect(f'question/{len(responses)}')


@app.route('/complete')
def complete_survey():
    return render_template('complete.html')
