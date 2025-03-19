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

# ---- / & /index ---- #

@app.route('/')                                                             # if route is '/'
@app.route('/index')
@app.route('/index.html')                                                   # if route is '/index.html'
def displayBoats():
    boatsRow = conn.execute(text('SELECT * FROM boats;')).all()             # select everything from table boats in boatdb
    return render_template('index.html', boats = boatsRow[:10])             # display boats.html including each boat from selection

# ---- /create ---- #

@app.route('/create.html', methods = ['GET', 'POST'])                       # /create.html redirects to /create
def redirectCreate():
    return redirect('/create')
@app.route('/create', methods = ['GET', 'POST'])                            # if route is '/create'
def displayCreate():
    if request.method == 'GET':                                             # if method is get
        return render_template('create.html')                               # load create.html
    elif request.method == 'POST':                                          # if method is post
        try:
            conn.execute(text('INSERT INTO boats '
            'values(:id, :name, :type, :owner_id, :rental_price)'), 
            request.form)
            conn.commit()                                                   # insert form data into table
            return redirect('/index')                                       # redirect to /boats
        except IntegrityError:
            errorMessage = 'Integrity error, cannot have duplicates.'
            return render_template('create.html', errorMessage = errorMessage)
        except:
            errorMessage = 'An error occured.'
            return render_template('create.html', errorMessage = errorMessage)

# ---- /search ---- #

@app.route('/search.html', methods = ['GET', 'POST'])
def redirectSearch():
    return redirect('/search')
@app.route('/search', methods = ['GET', 'POST'])
def displaySearch():
    if request.method == 'GET':
        return render_template('search.html')
    elif request.method == 'POST':
        try:
            boatID = request.form.get('id')
            result = conn.execute(text('SELECT * FROM boats WHERE id = :id'), {'id': boatID})
            boatRow = result.fetchall()
            if boatRow == '' or boatRow == []:
                return render_template('search.html', errorMessage = 'No items with this ID exist.')
            return render_template('boats.html', boats = boatRow)
        except:
            errorMessage = 'An error occured.'
            return render_template('search.html', errorMessage = errorMessage)

# ---- /update ---- #

@app.route('/update', methods=['GET', 'POST'])
@app.route('/update.html', methods=['GET', 'POST'])
def displayUpdate():
    if request.method == 'GET':
        return render_template('update.html')
    elif request.method == 'POST':
        try:
            boatID = request.form.get('id')
            result = conn.execute(text('SELECT * FROM boats WHERE id = :id'), {'id': boatID})
            boatRow = result.fetchone()

            if not boatRow:
                return render_template('update.html', errorMessage = 'Boat with this ID does not exist.')
            
            else: 
                conn.execute(
                text('UPDATE boats SET name = :name, type = :type, '
                'owner_id = :owner_id, rental_price = :rental_price '
                'WHERE id = :id'), 
                request.form)
                conn.commit()
                return redirect('/index')
                
        except:
            return render_template('update.html', errorMessage = 'An error occured.')

# ---- /delete ---- #

@app.route('/delete', methods=['GET', 'POST'])
@app.route('/delete.html', methods=['GET', 'POST'])
def displayDelete():
    if request.method == 'GET':
        return render_template('delete.html')
    elif request.method == 'POST':
        try:
            boatID = request.form.get('id')
            result = conn.execute(
                text('SELECT * FROM boats WHERE id = :id'),
                {'id': boatID})
            boatRow = result.fetchone()

            if not boatRow:
                return render_template(
                    'delete.html', 
                    errorMessage = 'Boat with this ID does not exist.'
                    )
            
            else: 
                conn.execute(
                text('DELETE FROM boats WHERE id = :id'), 
                {'id': boatID}
                )
                conn.commit()
                return redirect('/')
                
        except Exception as e:
            return render_template('delete.html', errorMessage = f'An error occured: {str(e)}.')



if __name__ == '__main__':                                                  # runs when not imported
    app.run(debug=True)