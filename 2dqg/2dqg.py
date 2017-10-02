# 2d quiz generator
# 
# a bsd-licensed bidimensional quiz generator written in flask
# author: v0idpwn
# v0idpwn.github.io/2dqg

import os
import sqlite3
from flask import Flask, current_app, request, render_template, g

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, '/tmp/2dqg.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASK_SETTINGS', silent=True)


# database functions 
def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv
    
def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('initdb')
def initdb_command():
    init_db()
    print('Initialized the database.')    
    
def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db
    
@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()    

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
		#sending to db
		db = get_db()
		cursor = db.cursor()
		cursor.execute('insert into `questionary` (name, xAxis, yAxis) values (?, ?, ?)', [request.form['qName'], request.form['xAxis'], request.form['yAxis']])
		questionary_id = cursor.lastrowid
		for a in range (0, len(questions)):
			db.execute('insert into question (fk_id, qText, stronglyAgreeX, stronglyAgreeY, agreeX, agreeY, neutralX, neutralY, disagreeX, disagreeY, stronglyDisagreeX, stronglyDisagreeY) values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', [questionary_id, questions[a], opt[0][a], opt[1][a], opt[2][a], opt[3][a], opt[4][a], opt[5][a], opt[6][a], opt[7][a], opt[8][a], opt[9][a]])
		db.commit()
		
		return str(questions+opt)

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
	db = get_db()
	qNumber = db.execute('select count(qId) from question where fk_id=?', [str(quizId)])
	qNumber = qNumber.fetchone()
	data = request.form.getlist('opinion[]')
	return str(data)
	for a in range (0, qNumber):
		xAxis = xAxis + db.execute('select ' + data[a] + 'X from question where fk id = ? limit 1 offset ' + str(a), [str(quizId)])
		yAxis = yAxis + db.execute('select ' + data[a] + 'Y from question where fk_id = ? limit 1 offset ' + str(a), [str(quizId)]) 
	return(str(xAxis)+" e " +str(yAxis))
