# -*- coding: utf-8 -*-

# the imports
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
#from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

# configuration should go in a separate file
app.config.from_pyfile('app.cfg')
#toolbar = DebugToolbarExtension(app)

# the model
db = SQLAlchemy(app)

class App(db.Model):
    
    __tablename__ = 'todos'
    id  = db.Column('todo_id',db.Integer, primary_key = True)#, sqlite_autoincrement=True)
    title    = db.Column(db.String(60))
    text     = db.Column(db.String)
    done     = db.Column(db.Boolean)
    pub_date = db.Column(db.DateTime)
    
    def __init__(self, title, text):
        self.title      = title
        self.text       = text
        self.done       = False
        self.pub_date   = datetime.utcnow()

# the controler
@app.route("/")
def index():
    return render_template('index.html', todos = App.query.order_by(App.pub_date.desc()).all())
    

@app.route("/new", methods = ["GET", "POST"])
def new():
    if request.method == 'POST':
        if not request.form['title']:
            flash('Give it a title or something ...', category = 'error')
        elif not request.form['text']:
            flash('How are you suppose to know what to do ??? ', category = 'error')
        else:
            todo = App(request.form['title'], request.form['text'])
            db.session.add(todo)
            db.session.commit()
            flash(u'Successfully CREATED',category = 'success')
            return redirect(url_for('index'))
    return render_template('new.html')


@app.route('/todos/<int:todo_id>', methods = ['GET', 'POST'])
def update(todo_id):
    todo_item = App.query.get(todo_id)
    if request.method == 'GET':
        return render_template('view.html', todo = todo_item)
    todo_item.title     = request.form['title']
    todo_item.text      = request.form['text']
    todo_item.done      = ('done.%d' % todo_id) in request.form
    db.session.commit()
    flash(u'Successfully UPDATED',category = 'success')
    return redirect(url_for('index'))
    
if __name__ == "__main__":
    app.run()