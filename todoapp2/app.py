from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://rs@localhost:5432/todoapp2'
db = SQLAlchemy(app)

class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key = True)
    description = db.Column(db.String(), nullable = False)

    def __repr__(self):
        return f'<Todo {self.id} {self.description}>'
    
db.create_all()

@app.route('/todos/create', methods=['POST'])
def create_todo():
    #print(request)
    #print(request.form)
    print(request.get_json())
    description = request.get_json()['description']
    print(1)
    todo = Todo(description=description)
    print(2)

    db.session.add(todo)
    print(3)

    db.session.commit()
    print(4)
    print(todo.description)
    print(jsonify({
        'description': todo.description
    }))

    return jsonify({
        'description': todo.description
    })

@app.route('/')
def index():
    return render_template('index.html', data=Todo.query.all())
