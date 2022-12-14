from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import sys

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://rs@localhost:5432/todoapp2'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class TodoList(db.Model):
    __tablename__ = 'todolists'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(), nullable=False)
    todos = db.relationship('Todo', backref='list', lazy=True)


class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key = True)
    description = db.Column(db.String(), nullable = False)
    completed = db.Column(db.Boolean, nullable=True)
    list_id = db.Column(db.Integer, db.ForeignKey('todolists.id'), nullable=False)

    def __repr__(self):
        return f'<Todo {self.id} {self.description}>'


db.create_all()

@app.route('/todos/create', methods=['POST'])
def create_todo():
    error = False
    body={}
    try:
        description = request.get_json()['description']
        list_id = request.get_json()['list_id']
        print(request.get_json())
        todo = Todo(description=description, list_id=list_id)
        
        db.session.add(todo)
        
        db.session.commit()
        body['description'] = todo.description
    except:
        
        error = True
        db.session.rollback()
        
        print(sys.exc_info())
    finally:
        db.session.close()
    if not error:
        return jsonify(body)

@app.route('/todos/<todo_id>/set-completed', methods=['POST'])
def set_completed_todo(todo_id):
    try:    
        completed = request.get_json()['completed']
        todo = Todo.query.get(todo_id)
        todo.completed=completed
        print('test1')
        db.session.commit()
    except:
        print('rollback ')

        db.session.rollback()
    finally:
        db.session.close()
    return redirect(url_for('index'))

@app.route('/todos/<todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
  try:
    Todo.query.filter_by(id=todo_id).delete()
    db.session.commit()
  except:
    db.session.rollback()
  finally:
    db.session.close()
  return jsonify({ 'success': True })

@app.route('/lists/<list_id>')
def get_list_todos(list_id):
    return render_template('index.html', 
    lists=TodoList.query.all(),   
    active_list=TodoList.query.get(list_id),
    todos=Todo.query.filter_by(list_id=list_id).order_by('id').all())
    # html and parameters are passed to render_template together,
    # render_template will combine them and decide how they work together

@app.route('/')
def index():
    return redirect(url_for('get_list_todos', list_id=1))