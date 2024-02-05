from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
db = SQLAlchemy(app)


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    gender = db.Column(db.Integer)
    

    def __init__(self, name, gender):
        self.name = name
        self.gender = gender
        


@app.route('/')
def index():
    students = Student.query.all()
    return render_template('index.html', students=students)


@app.route('/add_student', methods=["POST"])
def add_student():
    name = request.form['name']
    gender = request.form['gender']
    student = Student(name, gender)
    db.session.add(student)
    db.session.commit()
    return redirect('/')


@app.route('/edit_student/<int:student_id>', methods=['GET', 'POST'])
def edit_student(student_id):
    student = Student.query.get(student_id)

    if request.method == 'POST':
        student.name = request.form['name']
        student.gender = request.form['gender']
        db.session.commit()
        return redirect('/')

    return render_template('edit_student.html', student=student)


@app.route('/delete_student/<int:student_id>', methods=['POST'])
def delete_student(student_id):
    student = Student.query.get(student_id)
    db.session.delete(student)
    db.session.commit()
    return redirect('/')


@app.route('/generate_groups', methods=['POST'])
def generate_groups():
    num_students = len(Student.query.all())
    num_groups = int(request.form['num_groups'])

    students = [student.name for student in Student.query.all()]
    random.shuffle(students)

    group_size = num_students // num_groups
    remaining_students = num_students % num_groups

    groups = []
    start_index = 0
    for i in range(num_groups):
        end_index = start_index + group_size
        if i < remaining_students:
            end_index += 1
        group = students[start_index:end_index]
        groups.append(group)
        start_index = end_index

    # Randomly shuffle the students within each group
    for group in groups:
        random.shuffle(group)

    return render_template('dashboard.html', groups=groups)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)     