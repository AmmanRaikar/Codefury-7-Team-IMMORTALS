from flask import Flask, render_template

from app import create_app

app = create_app()

emp = [
    {"Empname": "Ashish", "Empid": "E1", "Empsalary": "50000"},
    {"Empname": "Aditya", "Empid": "E2", "Empsalary": "100000"}
]


@app.route('/')
def index():
    return render_template('index.html', emp=emp)

@app.route('/aditya')
def other():
    return render_template('other.html')

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000)

