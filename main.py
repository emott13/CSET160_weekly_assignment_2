# -------------------------------------- #
# ---- CSET 160 Weekly Assignment 2 ---- #
# -------------------------------------- #


from flask import Flask, render_template, request, redirect
from sqlalchemy import create_engine, text
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
connectionString = "mysql://root:cset155@localhost/boatdb"                  # connection string
engine = create_engine(connectionString, echo = True)                       # engine
conn = engine.connect()                                                     # connection

@app.route('/')                                                             # if route is '/'
def display():
    return render_template('index.html')                                    # load index

@app.route('/boats.html')                                                   # if route is '/boats'
def displayBoats():
    boatsRow = conn.execute(text('SELECT * FROM boats;')).all()             # select everything from table boats in boatdb
    return render_template('boats.html', boats = boatsRow[:10])             # display boats.html including each boat from selection

@app.route('/create.html', methods = ['GET', 'POST'])                       # if route is '/create.html'
def displayCreate():
    if request.method == 'GET':                                             # if method is get
        return render_template('create.html')                               # load create.html
    elif request.method == 'POST':                                          # if method is post
        errorMessage = ''                                                   
        try:
            conn.execute(text('INSERT INTO boats values(:id, :name, :type, :owner_id, :rental_price)'), request.form)
            return redirect('/boats')
        except IntegrityError:
            errorMessage = 'Integrity error, cannot have duplicates.'
            return render_template('createBoat.html', errorMessage = errorMessage)
        except:
            errorMessage = 'An error occured.'
            return render_template('createBoat.html', errorMessage = errorMessage)

@app.route('/search.html', methods = ['GET', 'POST'])
def displaySearch():
    if request.method == 'GET':
        return render_template('create.html')
    elif request.method == 'POST':
        errorMessage = ''
        try:
            conn.execute(text('INSERT INTO boats values(:id, :name, :type, :owner_id, :rental_price)'), request.form)
            return redirect('/boats')
        except IntegrityError:
            errorMessage = 'Integrity error, cannot have duplicates.'
            return render_template('createBoat.html', errorMessage = errorMessage)
        except:
            errorMessage = 'An error occured.'
            return render_template('createBoat.html', errorMessage = errorMessage)

@app.route('/update.html')
def displayUpdate():
    return render_template('update.html')

@app.route('/delete.html')
def displayDelete():
    return render_template('delete.html')

if __name__ == '__main__':                                                  # runs when not imported
    app.run(debug=True)