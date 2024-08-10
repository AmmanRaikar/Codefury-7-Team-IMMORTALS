import mysql.connector
from flask import Flask, render_template, request, session
from flask_cors import CORS

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
                cursor.execute(
                    "INSERT INTO users (pname, password, email, phone) VALUES (%s, %s, %s, %s)",
                    (username, password, email, number))
                connection.commit()
                connection.close()
                success_text = "Registration Successful, Please Login"
                return render_template('login.html', text = success_text, success = True)

            elif not check_email(email, emails):
                email_auth = 0
                err_text = "Email already registered, please login"
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
    if pid is not None:
        global pid_session  
        pid_session = int(''.join(map(str, pid)))
        cursor.execute(f"SELECT * FROM users WHERE pid={pid_session}")
        user_basic_information = cursor.fetchall()
        return render_template("userscree.html", info = user_basic_information)
        

    elif pid is None:
        return render_template("login.html",
                               err_text="Wrong Credentials",
                               email_auth=0)

    return '<h1>Something went wrong</h1>'


@app.route('/userscreen', methods=['GET', 'POST'])
def userscreen():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE pid=%s", (pid_session, ))
    user_basic_information : list = cursor.fetchall()
    # print(type(user_basic_information))
    name = user_basic_information[0][0]
    email = user_basic_information[0][1]
    location = user_basic_information[0][4]
    with open("logs.txt", "a") as f1:
        f1.write(str(user_basic_information))

    return render_template('userscree.html',
                           user_basic_information=user_basic_information)


@app.route('/location')
def location():
    return render_template("location.html")


# EDUCATION page links
@app.route('/edu', methods=['GET'])
def edu():
    return render_template("edu.html")


@app.route('/edu/avalanche', methods=['GET'])
def avalanche():
    return render_template("/edu_pages/Avalanches.html")


@app.route('/edu/blizzard', methods=['GET'])
def blizzard():
    return render_template("/edu_pages/Blizzards.html")


@app.route('/edu/drought', methods=['GET'])
def drought():
    return render_template("/edu_pages/droughts.html")


@app.route('/edu/earthquake', methods=['GET'])
def earthquake():
    return render_template("/edu_pages/Earthquakes.html")


@app.route('/edu/flood', methods=['GET'])
def flood():
    return render_template("/edu_pages/floods.html")


@app.route('/edu/hurricane', methods=['GET'])
def hurricane():
    return render_template("/edu_pages/Hurricanes.html")


@app.route('/edu/landslide', methods=['GET'])
def landslide():
    return render_template("/edu_pages/landslide.html")


@app.route('/edu/sandstorm', methods=['GET'])
def sandstorm():
    return render_template("/edu_pages/Sandstorms.html")


@app.route('/edu/tornado', methods=['GET'])
def tornado():
    return render_template("/edu_pages/Tornadoes.html")


@app.route('/edu/tsunami', methods=['GET'])
def tsunami():
    return render_template("/edu_pages/Tsunamis.html")


@app.route('/edu/volcano', methods=['GET'])
def volcano():
    return render_template("/edu_pages/volcanic.html")


@app.route('/edu/wildfire', methods=['GET'])
def wildfire():
    return render_template("/edu_pages/Wildfires.html")

@app.route('/personal', methods=['GET', 'POST'])
def personal_details():
    if request.method == "GET":
        return (f"enter a web page to enter personal details.\n" 
        f"Include- Name, Age, gender, 2 phone numbers of relatives and address, blood group"
        f", ")

    elif request.method == "POST":
        name = request.form["name"] #AutoFilled
        age = request.form["age"]
        gender = request.form["gender"]
        phone_no1 = request.form["phone_no1"]
        phone_no2 = request.form["phone_no2"]
        address_relative = request.form["address"]
        blood_group = request.form["blood_group"]
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO emergency (pid, age, gender, phone1, phone2, address_rel, blood_group) VALUES (%s, %s, %s, %s, %s, %s)", (pid_session, age, gender, phone_no1, phone_no2, address_relative, blood_group))
        return render_template("userscree.html")

    return '<h1>Something Went Wrong</h1>'
        
        
        

@app.route('/all')
def other():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT * from users where pid = 2')
    results = cursor.fetchall()
    print(type(results))
    cursor.close()
    connection.close()
    return render_template("all.html", results=results)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
