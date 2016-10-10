from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
app = Flask(__name__)
mysql = MySQLConnector(app,'friendsdb')

app.secret_key = "GreaseIsTheWordIsTheTimeIsTheFeeling"

#DISPLAY ALL
@app.route('/')
def index():
	query = "SELECT * FROM friends"
	friends = mysql.query_db(query)
	print friends
	return render_template('index.html', all_friends = friends)

#SEARCH
@app.route('/friends/<friend_id>')
def show(friend_id):
	query = "SELECT * FROM friends WHERE id = :specific_id"
	data = {'specific_id': friend_id}
	friends = mysql.query_db(query, data)
	return render_template('index.html', all_friends = friends)


# CREATE
@app.route('/friends', methods=['POST'])
def create():

	query = "INSERT INTO friends (first_name, last_name, occupation, created_at, updated_at) VALUES (:first_name, :last_name, :occupation, NOW(), NOW())"
	data = {
			'first_name': request.form['first_name'],
			'last_name': request.form['last_name'],
			'occupation':  request.form['occupation']
	}
	mysql.query_db(query, data)
	return redirect('/')


# UPDATE
@app.route('/update_friend')
def update_form():
	return render_template('update.html')

@app.route('/process', methods=['POST'])
def process_update():
	session['first_name'] =  request.form['first_name']
	session['last_name'] =  request.form['last_name']
	session['occupation'] =  request.form['occupation']
	session['id'] =  request.form['id']
	return redirect('/update_friend/{}'.format(session['id']))


@app.route('/update_friend/<friend_id>')
def update(friend_id):
	query = "UPDATE friends SET first_name = :first_name, last_name = :last_name, occupation = :occupation WHERE id = :id"
	data = {
		'first_name': session['first_name'],
		'last_name': session['last_name'],
		'occupation':  session['occupation'],
		'id' : friend_id
	}
	mysql.query_db(query, data)
	return redirect('/')

# DELETE
#UNIMPLEMENTED
@app.route('/remove_friend/<friend_id>', methods=['POST'])
def delete(friend_id):
    query = "DELETE FROM friends WHERE id = :id"
    data = {'id': friend_id}
    mysql.query_db(query, data)
    return redirect('/')


app.run(debug=True)
