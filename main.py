import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QMainWindow,
    QLineEdit, QPushButton, QTextEdit
)
import sqlite3


class Student:
    def __init__(self, first, last, grade):
        self.first = first
        self.last = last
        self.grade = grade


class StudentDatabase:
    def __init__(self):
        self.conn = sqlite3.connect('student.db')
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS students (
            first TEXT,
            last TEXT,
            grade INTEGER
        )''')
        self.conn.commit()

    def insert(self, student):
        with self.conn:
            self.c.execute("INSERT INTO students VALUES (:first, :last, :grade)", {
                'first': student.first,
                'last': student.last,
                'grade': student.grade
            })

    def update(self, student, grade):
        with self.conn:
            self.c.execute("UPDATE students SET grade = :grade WHERE first = :first AND last = :last", {
                'first': student.first,
                'last': student.last,
                'grade': grade
            })

    def remove(self, student):
        with self.conn:
            self.c.execute("DELETE FROM students WHERE first = :first AND last = :last", {
                'first': student.first,
                'last': student.last
            })

    def fetch_all(self):
        self.c.execute("SELECT * FROM students")
        return self.c.fetchall()


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Database Manager")
        self.setGeometry(200, 200, 400, 400)
        self.db = StudentDatabase()
        layout = QVBoxLayout()

        self.first_input = QLineEdit()
        self.last_input = QLineEdit()
        self.grade_input = QLineEdit()

        layout.addWidget(self.first_input)
        layout.addWidget(self.last_input)
        layout.addWidget(self.grade_input)

        self.insert_btn = QPushButton("Insert")
        self.update_btn = QPushButton("Update")
        self.remove_btn = QPushButton("Remove")
        self.show_btn = QPushButton("Show All")

        layout.addWidget(self.insert_btn)
        layout.addWidget(self.update_btn)
        layout.addWidget(self.remove_btn)
        layout.addWidget(self.show_btn)

        self.output = QTextEdit()
        self.output.setReadOnly(True)
        layout.addWidget(self.output)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.insert_btn.clicked.connect(self.insert_student)
        self.update_btn.clicked.connect(self.update_student)
        self.remove_btn.clicked.connect(self.remove_student)
        self.show_btn.clicked.connect(self.show_students)

    def insert_student(self):
        try:
            student = Student(self.first_input.text(), self.last_input.text(), int(self.grade_input.text()))
            self.db.insert(student)
            self.output.append("Inserted successfully.")
        except Exception as e:
            self.output.append(f"Error: {e}")

    def update_student(self):
        try:
            student = Student(self.first_input.text(), self.last_input.text(), 0)
            new_grade = int(self.grade_input.text())
            self.db.update(student, new_grade)
            self.output.append("Updated successfully.")
        except Exception as e:
            self.output.append(f"Error: {e}")

    def remove_student(self):
        try:
            student = Student(self.first_input.text(), self.last_input.text(),0)
            self.db.remove(student)
            self.output.append("Removed successfully.")
        except Exception as e:
            self.output.append(f"Error: {e}")

    def show_students(self):
        students = self.db.fetch_all()
        self.output.clear()
        for s in students:
            self.output.append(f"{s[0]} {s[1]} - Grade: {s[2]}")


app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec_())