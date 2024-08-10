from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)


def get_db_connection():
    connection = mysql.connector.connect(host="sql12.freemysqlhosting.net",
                                         user="sql12725060",
                                         password="jqQaQEBwsH",
                                         database="sql12725060")
    return connection


@app.route('/')
def index():
    return render_template("login.html")


@app.route('/all_entries')
def other():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT * from test')
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return str(results)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
