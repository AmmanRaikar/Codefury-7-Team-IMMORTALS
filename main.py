import mysql.connector
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__,
            template_folder="templates",
            static_folder="static",
            static_url_path='/')
app.secret_key = "IMMORTALS"


def get_db_connection():
    connection = mysql.connector.connect(host="sql12.freemysqlhosting.net",
                                         user="sql12725060",
                                         password="jqQaQEBwsH",
                                         database="sql12725060")
    return connection


@app.route('/', methods=["GET", "POST"])
def index():

    if request.method == "GET":
        return render_template("index.html")

    elif request.method == "POST":
        connection = get_db_connection()
        cursor = connection.cursor()
        check_pass = 1
        email_auth = 1
        username = request.form["name"]
        password = request.form["password"]
        email = request.form["email"]
        number = int(request.form["MobileNo"])
        c_password = request.form["confirm-password"]
        if password == c_password:
            cursor.execute("SELECT email FROM users")
            emails = cursor.fetchall()

            def check_email(email, emails):
                for i in emails:
                    if email in i:
                        return False
                return True

            if check_email(email, emails):
                print(f'{email} not in {list(emails)}')
                cursor.execute(
                    "INSERT INTO users (pname, password, email, phone) VALUES (%s, %s, %s, %s)",
                    (username, password, email, number))
                connection.commit()
                connection.close()
                return render_template('login.html')

            elif not check_email(email, emails):
                email_auth = 0
                err_text = "Email already signed up, please login"
                connection.close()
                return render_template("login.html",
                                       err_text=err_text,
                                       email_auth=email_auth)

        else:
            check_pass = 0
            err_text = "Passwords do not match"
            connection.close()
            return render_template("signup.html",
                                   err_text=err_text,
                                   check_pass=check_pass)

    return "<h1>Something went wrong</h1>"


@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template("login.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    return render_template("signup.html")


@app.route('/main', methods=['GET', 'POST'])
def main():
    # Page after Login
    username = request.args.get('email')
    password = request.args.get('password')
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT pid FROM users WHERE email=%s AND password=%s",
                   (username, password))
    pid = cursor.fetchone()
    print(pid)
    if pid is not None:
        return render_template("edu.html", pid=pid)

    elif pid is None:
        return "<h1>Invalid Credentials</h1>"

    return '<h1>Something went wrong</h1>'


@app.route('/location')
def location():
    return render_template("location.html")


# EDUCATION page links
@app.route('/edu', methods=['GET', 'POST'])
def edu():
    return render_template("edu.html")


@app.route('/edu/avalanche', methods=['GET', 'POST'])
def avalanche():
    return render_template("/edu_pages/Avalanches.html")


@app.route('/edu/blizzard', methods=['GET', 'POST'])
def blizzard():
    return render_template("/edu_pages/Blizzards.html")


@app.route('/edu/drought', methods=['GET', 'POST'])
def drought():
    return render_template("/edu_pages/droughts.html")


@app.route('/edu/earthquake', methods=['GET', 'POST'])
def earthquake():
    return render_template("/edu_pages/Earthquakes.html")


@app.route('/edu/flood', methods=['GET', 'POST'])
def flood():
    return render_template("/edu_pages/floods.html")


@app.route('/edu/hurricane', methods=['GET', 'POST'])
def hurricane():
    return render_template("/edu_pages/Hurricanes.html")


@app.route('/edu/landslide', methods=['GET', 'POST'])
def landslide():
    return render_template("/edu_pages/landslide.html")


@app.route('/edu/sandstorm', methods=['GET', 'POST'])
def sandstorm():
    return render_template("/edu_pages/Sandstorms.html")


@app.route('/edu/tornado', methods=['GET', 'POST'])
def tornado():
    return render_template("/edu_pages/Tornadoes.html")


@app.route('/edu/tsunami', methods=['GET', 'POST'])
def tsunami():
    return render_template("/edu_pages/Tsunamis.html")


@app.route('/edu/volcano', methods=['GET', 'POST'])
def volcano():
    return render_template("/edu_pages/volcanic.html")


@app.route('/edu/wildfire', methods=['GET', 'POST'])
def wildfire():
    return render_template("/edu_pages/Wildfires.html")


@app.route('/all')
def other():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT * from users')
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template("all.html", results=results)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
