import os
from flask import Flask, render_template, json, request, redirect, session
from flask.ext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash
from jinja2 import Environment, FileSystemLoader

app = Flask(__name__)
app.secret_key = 'ssh...Big secret!'
#MySQL configurations

mysql = MySQL()

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'tekken5'
app.config['MYSQL_DATABASE_DB'] = 'movieapp'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


# route to index.html
@app.route("/")
def main():
    return render_template('index.html')

# route to signup.html
@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')

# interact with MySQL for sign up
@app.route('/signUp',methods=['POST'])
def signUp():
    try:
        _name = request.form['inputName']
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']

        # validate the received values
        if _name and _email and _password:

            # All Good, let's call MySQL

            conn = mysql.connect()
            cursor = conn.cursor()
            _hashed_password = generate_password_hash(_password)
            cursor.callproc('sp_createUser',(_name,_email,_hashed_password))
            data = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
                return json.dumps({'message':'User created successfully !'})
            else:
                return json.dumps({'error':str(data[0])})
        else:
            return json.dumps({'html':'<span>Enter the required fields</span>'})

    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
        cursor.close()
        conn.close()

@app.route('/showSignin')
def showSignin():
    return render_template('signin.html')

@app.route('/validateLogin',methods=['POST'])
def validateLogin():
    try:
        _username = request.form['inputEmail']
        _password = request.form['inputPassword']

        # connect to mysql
        con = mysql.connect()
        cursor = con.cursor()
        cursor.callproc('sp_validateLogin',(_username,))
        data = cursor.fetchall()

        if len(data) > 0:
            if check_password_hash(str(data[0][3]),_password):
                session['user'] = data[0][0]
                return redirect('/userHome')
            else:
                return render_template('error.html',error = 'Wrong Email address or Password.')
        else:
            return render_template('error.html',error = 'Wrong Email address or Password.')

    except Exception as e:
        return render_template('error.html',error = str(e))
    finally:
        cursor.close()
        con.close()

@app.route('/userHome')
def userHome():
    if session.get('user'):
        con = mysql.connect()
        cursor = con.cursor()
        cursor.execute("SELECT * FROM Movie ORDER BY MovieID DESC");
        data = cursor.fetchall()

        data_dict = []
        for i in data:
            cursor.execute("SELECT TRUNCATE(avg(Rating), 1) FROM Review WHERE MovieID = %s", (i[0],))
            rating = cursor.fetchone()[0]
            data_dic = {
                    'MovieID': i[0],
                    'Title': i[1],
                    'ReleaseYear': i[2],
                    'MovieLength': i[3],
                    'GenreName': i[4],
                    'Synopsis': i[5],
                    'Rating' : rating
                    }

            data_dict.append(data_dic)

        #return json.dumps(data_dict)
        # generate template and assign variables
        loopdata = data_dict
        return render_template('userHome.html', loopdata=loopdata)

        # return the output
        return output
    else:
        return render_template('error.html',error = 'Unauthorized Access')

@app.route('/showAddMovie')
def showAddMovie():
    return render_template('addMovie.html')

@app.route('/logout')
def logout():
    session.pop('user',None)
    return redirect('/')

@app.route('/addMovie',methods=['POST'])
def addMovie():
    try:
        if session.get('user'):
            _title = request.form['inputTitle']
            _releaseYear = request.form['inputReleaseYear']
            _synopsis = request.form['inputSynopsis']
            _movieLength = request.form['inputMovieLength']
            _genre = request.form['inputGenre']
            _directorFirstName1 = request.form['inputDirectorFirstName1']
            _directorLastName1 = request.form['inputDirectorLastName1']
            _directorFirstName2 = request.form['inputDirectorFirstName2']
            _directorLastName2 = request.form['inputDirectorLastName2']
            _actorFirstName1 = request.form['inputActorFirstName1']
            _actorLastName1 = request.form['inputActorLastName1']
            _actorFirstName2 = request.form['inputActorFirstName2']
            _actorLastName2 = request.form['inputActorLastName2']
            _actorFirstName3 = request.form['inputActorFirstName3']
            _actorLastName3 = request.form['inputActorLastName3']
            _actorFirstName4 = request.form['inputActorFirstName4']
            _actorLastName4 = request.form['inputActorLastName4']
            _actorFirstName5 = request.form['inputActorFirstName5']
            _actorLastName5 = request.form['inputActorLastName5']

            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_addMovie',(_title,_releaseYear,_movieLength,_genre,_synopsis))
            data = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
                #return redirect('/userHome')
            else:
                return render_template('error.html',error = 'An error occurred!')

            cursor.execute("SELECT MovieID FROM Movie WHERE Title = %s", (_title,))
            data = cursor.fetchone()
            MovieID = data[0]

            cursor.callproc('sp_addDirectorName',(_directorFirstName1,_directorLastName1))
            data = cursor.fetchall()
            if len(data) is 0:
                conn.commit()
                #return redirect('/userHome')
                cursor.execute("SELECT DirectorID FROM Director WHERE FirstName = %s AND LastName = %s", (_directorFirstName1,_directorLastName1,))
                data = cursor.fetchone()
                DirectorID = data[0]
                cursor.callproc('sp_addDirectedBy',(DirectorID,MovieID))
                data = cursor.fetchall()
                if len(data) is 0:
                    conn.commit()
                    #return redirect('/userHome')
                else:
                    return render_template('error.html',error = 'An error occurred!')
            else:
                return render_template('error.html',error = 'An error occurred!')


            if _directorFirstName2 != '':
                cursor.callproc('sp_addDirectorName',(_directorFirstName2,_directorLastName2))
                data = cursor.fetchall()
                if len(data) is 0:
                    conn.commit()
                    #return redirect('/userHome')
                    cursor.execute("SELECT DirectorID FROM Director WHERE FirstName = %s AND LastName = %s", (_directorFirstName2,_directorLastName2,))
                    data = cursor.fetchone()
                    DirectorID = data[0]
                    cursor.callproc('sp_addDirectedBy',(DirectorID,MovieID))
                    data = cursor.fetchall()
                    if len(data) is 0:
                        conn.commit()
                        #return redirect('/userHome')
                    else:
                        return render_template('error.html',error = 'An error occurred!')

                else:
                    return render_template('error.html',error = 'An error occurred!')

            if _actorFirstName1 != '':
                cursor.callproc('sp_addActorName',(_actorFirstName1,_actorLastName1))
                data = cursor.fetchall()
                if len(data) is 0:
                    conn.commit()
                    #return redirect('/userHome')
                    cursor.execute("SELECT ActorID FROM Actor WHERE FirstName = %s AND LastName = %s", (_actorFirstName1,_actorLastName1,))
                    data = cursor.fetchone()
                    ActorID = data[0]
                    cursor.callproc('sp_addMovieActor',(ActorID,MovieID))
                    data = cursor.fetchall()
                    if len(data) is 0:
                        conn.commit()
                        #return redirect('/userHome')
                    else:
                        return render_template('error.html',error = 'An error occurred!')
                else:
                    return render_template('error.html',error = 'An error occurred!')

            if _actorFirstName2 != '':
                cursor.callproc('sp_addActorName',(_actorFirstName2,_actorLastName2))
                data = cursor.fetchall()
                if len(data) is 0:
                    conn.commit()
                    #return redirect('/userHome')
                    cursor.execute("SELECT ActorID FROM Actor WHERE FirstName = %s AND LastName = %s", (_actorFirstName2,_actorLastName2,))
                    data = cursor.fetchone()
                    ActorID = data[0]
                    cursor.callproc('sp_addMovieActor',(ActorID,MovieID))
                    data = cursor.fetchall()
                    if len(data) is 0:
                        conn.commit()
                        #return redirect('/userHome')
                    else:
                        return render_template('error.html',error = 'An error occurred!')
                else:
                    return render_template('error.html',error = 'An error occurred!')

            if _actorFirstName3 != '':
                cursor.callproc('sp_addActorName',(_actorFirstName3,_actorLastName3))
                data = cursor.fetchall()
                if len(data) is 0:
                    conn.commit()
                    #return redirect('/userHome')
                    cursor.execute("SELECT ActorID FROM Actor WHERE FirstName = %s AND LastName = %s", (_actorFirstName3,_actorLastName3,))
                    data = cursor.fetchone()
                    ActorID = data[0]
                    cursor.callproc('sp_addMovieActor',(ActorID,MovieID))
                    data = cursor.fetchall()
                    if len(data) is 0:
                        conn.commit()
                        #return redirect('/userHome')
                    else:
                        return render_template('error.html',error = 'An error occurred!')
                else:
                    return render_template('error.html',error = 'An error occurred!')

            if _actorFirstName4 != '':
                cursor.callproc('sp_addActorName',(_actorFirstName4,_actorLastName4))
                data = cursor.fetchall()
                if len(data) is 0:
                    conn.commit()
                    #return redirect('/userHome')
                    cursor.execute("SELECT ActorID FROM Actor WHERE FirstName = %s AND LastName = %s", (_actorFirstName4,_actorLastName4,))
                    data = cursor.fetchone()
                    ActorID = data[0]
                    cursor.callproc('sp_addMovieActor',(ActorID,MovieID))
                    data = cursor.fetchall()
                    if len(data) is 0:
                        conn.commit()
                        #return redirect('/userHome')
                    else:
                        return render_template('error.html',error = 'An error occurred!')
                else:
                    return render_template('error.html',error = 'An error occurred!')

            if _actorFirstName5 != '':
                cursor.callproc('sp_addActorName',(_actorFirstName5,_actorLastName5))
                data = cursor.fetchall()
                if len(data) is 0:
                    conn.commit()
                    #return redirect('/userHome')
                    cursor.execute("SELECT ActorID FROM Actor WHERE FirstName = %s AND LastName = %s", (_actorFirstName5,_actorLastName5,))
                    data = cursor.fetchone()
                    ActorID = data[0]
                    cursor.callproc('sp_addMovieActor',(ActorID,MovieID))
                    data = cursor.fetchall()
                    if len(data) is 0:
                        conn.commit()
                        return redirect('/userHome')
                    else:
                        return render_template('error.html',error = 'An error occurred!')
                else:
                    return render_template('error.html',error = 'An error occurred!')


            return redirect('/userHome')
            #return render_template('error.html',error = str(MovieID))
        else:
            return render_template('error.html',error = 'Unauthorized Access')
    except Exception as e:
        return render_template('error.html',error = str(e))
    finally:
        cursor.close()
        conn.close()


@app.route('/movie/<movie_name>/')
def movie(movie_name):
    if session.get('user'):
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Movie WHERE Title = %s", (movie_name,))
        data = cursor.fetchone()
        MovieID = data[0]
        cursor.execute("SELECT TRUNCATE(avg(Rating), 1) FROM Review WHERE MovieID = %s", (MovieID,))
        rating = cursor.fetchone()[0]
        data_dict = []
        data_dict = {
            'MovieID': data[0],
            'Title': data[1],
            'ReleaseYear': data[2],
            'MovieLength': data[3],
            'GenreName': data[4],
            'Synopsis': data[5],
            'Rating' : rating
        }

        UserID = session.get('user')
        cursor.execute("SELECT firstname, lastname, Director.DirectorID FROM Movie NATURAL JOIN DirectedBy, Director WHERE Director.DirectorID = DirectedBy.DirectorID and MovieID = %s",  (MovieID,))
        director_data = cursor.fetchall()
        cursor.execute("SELECT firstname, lastname, Actor.ActorID FROM Movie NATURAL JOIN MovieActor, Actor WHERE Actor.ActorID = MovieActor.ActorID and MovieID = %s",  (MovieID,))
        actor_data = cursor.fetchall()
        cursor.execute("SELECT Review, ReviewDate, UserName FROM Review NATURAL JOIN User WHERE MovieID = %s AND UserID <> %s ORDER BY ReviewID DESC",  (MovieID, UserID,))
        review_data = cursor.fetchall()
        cursor.execute("SELECT Review, ReviewDate, UserName FROM Review NATURAL JOIN User WHERE MovieID = %s AND UserID = %s ORDER BY ReviewID DESC",  (MovieID, UserID,))
        my_review_data = cursor.fetchall()
        return render_template('movieDetail.html', movieData = data_dict, director_name=director_data, actor_name=actor_data, review_data = review_data, my_review_data=my_review_data)

    else:
        return render_template('error.html',error = 'Unauthorized Access')

@app.route('/userHome', methods=['POST'])
def searchMovie():
    if session.get('user'):
        #return render_template('error.html',error = request.form['searchText'])
        con = mysql.connect()
        cursor = con.cursor()
        text = request.form['searchText']
        option = request.form['option']
        text = '%' + text + '%'
        try:
            if option == "opt1":
                print "sdsds"
                cursor.execute("SELECT * FROM Movie WHERE Title LIKE %s ORDER BY MovieID DESC",(text,))
            elif option == "opt2":
                cursor.execute("SELECT * FROM Movie WHERE ReleaseYear LIKE %s ORDER BY MovieID DESC",(text,))
            elif option == "opt3":
                cursor.execute("SELECT * FROM Movie WHERE GenreName LIKE %s ORDER BY MovieID DESC",(text,))
            else:
                return render_template('error.html',error = 'Invalid Input!')

        except Exception as e:
            return render_template('error.html',error = str(e))

        data = cursor.fetchall()

        data_dict = []
        for i in data:
            cursor.execute("SELECT TRUNCATE(avg(Rating), 1) FROM Review WHERE MovieID = %s", (i[0],))
            rating = cursor.fetchone()[0]

            data_dic = {
                    'MovieID': i[0],
                    'Title': i[1],
                    'ReleaseYear': i[2],
                    'MovieLength': i[3],
                    'GenreName': i[4],
                    'Synopsis': i[5],
                    'Rating' : rating
            }

            data_dict.append(data_dic)

        #return json.dumps(data_dict)
        # generate template and assign variables
        loopdata = data_dict
        return render_template('userHome.html', loopdata=loopdata)

        # return the output
        return output
    else:
        return render_template('error.html',error = 'Unauthorized Access')

@app.route('/movie/<movie_name>/', methods=['POST'])
def review(movie_name):
    if session.get('user'):
        review_text = request.form['inputReview']
        rating_text = request.form['inputRating']
        UserID = session.get('user')

        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Movie WHERE Title = %s", (movie_name,))
        data = cursor.fetchone()
        MovieID = data[0]

        if review_text != '':
            cursor.callproc('sp_addReview',(MovieID, UserID, review_text, rating_text))
            data = cursor.fetchall()
            if len(data) is 0:
                conn.commit()

                cursor.execute("SELECT TRUNCATE(avg(Rating), 1) FROM Review WHERE MovieID = %s", (MovieID,))
                rating = cursor.fetchone()[0]
                print rating
                cursor.execute("SELECT * FROM Movie WHERE Title = %s", (movie_name,))
                data = cursor.fetchone()
                data_dict = []
                data_dict = {
                    'MovieID': data[0],
                    'Title': data[1],
                    'ReleaseYear': data[2],
                    'MovieLength': data[3],
                    'GenreName': data[4],
                    'Synopsis': data[5],
                    'Rating' : rating
                }
            else:
                return render_template('error.html',error = 'An error occurred!')

        UserID = session.get('user')
        cursor.execute("SELECT firstname, lastname FROM Movie NATURAL JOIN DirectedBy, Director WHERE Director.DirectorID = DirectedBy.DirectorID and MovieID = %s",  (MovieID,))
        director_data = cursor.fetchall()
        cursor.execute("SELECT firstname, lastname FROM Movie NATURAL JOIN MovieActor, Actor WHERE Actor.ActorID = MovieActor.ActorID and MovieID = %s",  (MovieID,))
        actor_data = cursor.fetchall()
        cursor.execute("SELECT Review, ReviewDate, UserName FROM Review NATURAL JOIN User WHERE MovieID = %s AND UserID <> %s ORDER BY ReviewID DESC",  (MovieID, UserID,))
        review_data = cursor.fetchall()
        cursor.execute("SELECT Review, ReviewDate, UserName FROM Review NATURAL JOIN User WHERE MovieID = %s AND UserID = %s ORDER BY ReviewID DESC",  (MovieID, UserID,))
        my_review_data = cursor.fetchall()
        return render_template('movieDetail.html', movieData = data_dict, director_name=director_data, actor_name=actor_data, review_data = review_data, my_review_data=my_review_data)

    else:
        return render_template('error.html',error = 'Unauthorized Access')

@app.route('/showAddDirector')
def showAddDirector():
    return render_template('addDirector.html')

@app.route('/showAddActor')
def showAddActor():
    return render_template('addActor.html')

@app.route('/addDirector', methods=['POST'])
def addDirector():
    _inputNationality = request.form['inputNationality']
    _inputBirthPlace = request.form['inputBirthPlace']
    _inputDirectorFirstName = request.form['inputDirectorFirstName']
    _inputDirectorLastName = request.form['inputDirectorLastName']

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.callproc('sp_addDirector',(_inputDirectorFirstName,_inputDirectorLastName,_inputNationality,_inputBirthPlace))
    data = cursor.fetchall()
    if len(data) is 0:
        conn.commit()
        return redirect('/userHome')
    else:
        return render_template('error.html',error = 'An error occurred!')

@app.route('/addActor', methods=['POST'])
def addActor():
    _inputNationality = request.form['inputNationality']
    _inputBirthPlace = request.form['inputBirthPlace']
    _inputActorFirstName = request.form['inputActorFirstName']
    _inputActorLastName = request.form['inputActorLastName']

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.callproc('sp_addActor',(_inputActorFirstName,_inputActorLastName,_inputNationality,_inputBirthPlace))
    data = cursor.fetchall()
    if len(data) is 0:
        conn.commit()
        return redirect('/userHome')
    else:
        return render_template('error.html',error = 'An error occurred!')

@app.route('/actor/<actorid>/')
def actor(actorid):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Actor WHERE ActorID = %s",  (actorid,))
    data = cursor.fetchone()
    data_dict = []
    data_dict = {
        'firstname': data[1],
        'lastname': data[2],
        'nationality': data[3],
        'birthplace': data[4]
    }
    return render_template('actorDetail.html',data = data_dict)

@app.route('/director/<directorid>/')
def director(directorid):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Director WHERE DirectorID = %s",  (directorid,))
    data = cursor.fetchone()
    data_dict = []
    data_dict = {
        'firstname': data[1],
        'lastname': data[2],
        'nationality': data[3],
        'birthplace': data[4]
    }
    return render_template('directorDetail.html',data = data_dict)


if __name__ == "__main__":
    app.debug = True
    app.run()
