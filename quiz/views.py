from flask import request, render_template, redirect

from quiz import app
from quiz.db import get_db


@app.route('/')
def mainPage():
    return render_template('creationForm.html')


@app.route('/make', methods=['POST', 'GET'])
def make():
    if request.method == 'POST':
        questions = []
        opt = []
        questions = request.form.getlist('question[]')
        opt.append(request.form.getlist('stronglyAgreeX[]'))
        opt.append(request.form.getlist('stronglyAgreeY[]'))
        opt.append(request.form.getlist('agreeX[]'))
        opt.append(request.form.getlist('agreeY[]'))
        opt.append(request.form.getlist('neutralX[]'))
        opt.append(request.form.getlist('neutralY[]'))
        opt.append(request.form.getlist('disagreeX[]'))
        opt.append(request.form.getlist('disagreeY[]'))
        opt.append(request.form.getlist('stronglyDisagreeX[]'))
        opt.append(request.form.getlist('stronglyDisagreeY[]'))
        # sending to db
        db = get_db()
        cursor = db.cursor()
        cursor.execute('insert into `questionary` (name, xAxis, yAxis, maxX, maxY) values (?, ?, ?, ?, ?)',
                       [request.form['qName'], request.form['xAxis'], request.form['yAxis'], request.form['maxX'],
                        request.form['maxY']])
        questionaryId = cursor.lastrowid
        for a in range(0, len(questions)):
            db.execute \
                    (
                    'insert into question (fk_id, qText, stronglyAgreeX, stronglyAgreeY, agreeX, agreeY, neutralX, neutralY, disagreeX, disagreeY, stronglyDisagreeX, stronglyDisagreeY) values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                    [questionaryId, questions[a], opt[0][a], opt[1][a], opt[2][a], opt[3][a], opt[4][a], opt[5][a],
                     opt[6][a], opt[7][a], opt[8][a], opt[9][a]])
        db.commit()
        return redirect('/quiz/' + str(questionaryId))


@app.route('/quiz/<quizId>')
def showQuiz(quizId):
    db = get_db()
    data = db.execute('select qText from question where fk_id=?', [str(quizId)])
    data = data.fetchall()
    quizName = db.execute('select name from questionary where id=?', [str(quizId)])
    quizName = quizName.fetchone()
    return render_template('quiz.html', questions=data, name=quizName, quizid=str(quizId))


@app.route('/quiz/<quizId>/answer', methods=['POST', 'GET'])
def answerQuiz(quizId):
    if request.method == 'POST':
        db = get_db()
        qNumber = db.execute('select count(qId) from question where fk_id=?', [str(quizId)])
        qNumber = qNumber.fetchone()
        qName = db.execute('select name from questionary where id=?', [str(quizId)])
        qName = qName.fetchone()
        xName = db.execute('select xAxis from questionary where id=?', [str(quizId)])
        xName = xName.fetchone()
        yName = db.execute('select yAxis from questionary where id=?', [str(quizId)])
        yName = yName.fetchone()
        maxX = db.execute('select maxX from questionary where id=?', [str(quizId)])
        maxY = db.execute('select maxY from questionary where id=?', [str(quizId)])
        maxX = maxX.fetchone()
        maxY = maxY.fetchone()
        data = []
        xAxis = yAxis = 0.0
        for a in range(1, qNumber[0] + 1):  # starts at 1 because loop.index does
            data.append(request.form.get('opinion[' + str(a) + ']'))
        for a in range(0, qNumber[0]):
            x = db.execute('select ' + str(data[a]) + 'X from question where fk_id = ? limit 1 offset ' + str(a),
                           [str(quizId)])
            y = db.execute('select ' + str(data[a]) + 'Y from question where fk_id = ? limit 1 offset ' + str(a),
                           [str(quizId)])
            x = x.fetchone()
            y = y.fetchone()
            xAxis = xAxis + x[0]
            yAxis = yAxis + y[0]
            return (
                render_template('result.html', x=xAxis, y=yAxis, name=qName[0], maxX=maxX[0], maxY=maxY[0],
                                xAxis=xName[0], yAxis=
                                yName[0]))
