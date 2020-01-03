from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)


def __repr__(self):
    return '<task %r' % self.id


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        taskContent = request.form['content']
        newTask = Todo(content=taskContent)

        db.session.add(newTask)
        db.session.commit()
        return redirect('/')

    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']
        db.session.commit()
        return redirect('/')

    else:
        return render_template('update.html', task=task)


@app.route('/delete/<int:id>')
def delete(id):
    task = Todo.query.get_or_404(id)

    db.session.delete(task)
    db.session.commit()
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)
