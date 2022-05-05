from flask import Flask, render_template, request, redirect
from flask_sqlalchemy   import SQLAlchemy
from datetime import datetime
app = Flask(__name__)

#DB connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

db = SQLAlchemy(app)

# create a model
class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)

#map a funtion to a url
@app.route('/', methods = ['POST','GET'])             # av'/'oid 404 app route decorator
def index():
    if request.method == 'POST':
        form_content = request.form['content']
        new_schd = Schedule(content = form_content)

        # Put it in database
        try:
            db.session.add(new_schd)
            db.session.commit()
            # after form submission print this
            #return "Form Submitted"
            return redirect('/')                #return back to index page
        except:
            return "Error commiting to database"


    else:
        schedules = Schedule.query.all()
        return render_template('index.html', schedules=schedules)

@app.route('/delete/<int:id>')
def delete(id):
    schedule_to_delete = Schedule.query.get_or_404(id)

    try:
        db.session.delete(schedule_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task.'

@app.route('/update/<int:id>', methods = ['GET', 'POST'])
def update(id):
    schedule = Schedule.query.get_or_404(id)

    if request.method == 'POST':
        schedule.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating.'
    else:
        return render_template('update.html', schedule=schedule)


if __name__ == "__main__":
    app.run(debug=True)

