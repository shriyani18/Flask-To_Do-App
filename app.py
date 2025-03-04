from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)  # Added max length
    desc = db.Column(db.String(500), nullable=False)  # Added max length
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

@app.route("/", methods=['GET', 'POST'])
def hello_world():
    if request.method == "POST":
        title = request.form.get("title")
        desc = request.form.get("desc")

        if title and desc:  # Ensure both fields have values
            todo = Todo(title=title, desc=desc)
            db.session.add(todo)
            db.session.commit()
            return redirect("/")  # Redirect to avoid duplicate form submission

    allTodo = Todo.query.all()  
    return render_template('index.html', allTodo=allTodo)  

@app.route("/show")
def show():
    allTodo = Todo.query.all()
    return render_template('index.html', allTodo=allTodo)  


@app.route("/update/<int:sno>", methods=['GET', 'POST'])
def update(sno):
    todo = Todo.query.filter_by(sno=sno).first()

    if request.method == "POST":
        todo.title = request.form["title"]
        todo.desc = request.form["desc"]
        db.session.commit()  # Save updates
        return redirect("/")  # Redirect to homepage

    return render_template('update.html', todo=todo)  



@app.route("/delete/<int:sno>")
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")
   
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Ensure the table exists before running the app
    app.run(debug=True, port=8000)
