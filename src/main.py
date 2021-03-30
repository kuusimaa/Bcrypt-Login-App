import mysql.connector
import bcrypt


# Checks if the username already exists in the database.
def check_username(user, cursor):
    cursor.execute(f"SELECT * FROM users WHERE username='{user}'")
    data = cursor.fetchall()

    if len(data) == 0:
        return False
    return True


# Checks if given username and password combination is correct.
def check_account(username, password, cursor):
    try:
        cursor.execute(
            f"SELECT passwd FROM users WHERE username  = '{username}'")
        passwd = cursor.fetchone()[0]
    except Exception:
        return False

    if bcrypt.checkpw(password, passwd.encode("utf-8")):
        return True
    return False


# Asks for the username and password and then calls function check_account() to see if given login details are correct.
def login(cursor):
    given_username = input("Please enter your username: ")
    given_password = input("Please enter your password: ").encode("utf-8")

    if check_account(given_username, given_password, cursor):
        print(f"Logged in as: {given_username}")
        return True
    else:
        print("Incorrect username or password")
        return False


# Asks for a Username, Password and email and checks whether username already exists in the database.
def register(cursor):
    while True:
        u = input("Please enter username you want to use: ")

        if not check_username(u, cursor):
            p = input("Please enter password you will remember: ").encode(
                "utf-8")
            e = input("Please enter your email address: ")

            passwd_hashed = bcrypt.hashpw(p, bcrypt.gensalt())
            cursor.execute(
                "INSERT INTO Users (username, passwd, email) VALUES (%s,%s,%s)", (u, passwd_hashed, e))
            print("Registration was successful!")
            return True
        print("Username is already in use!")
        return False


# Prints options at the start of the program.
def print_start():
    print("###Welcome to Login###")
    select = int(input("Options:\n"
                       "Login(1)\n"
                       "Register(2)\n"
                       "Quit(3)\n"))
    return select


def main():
    # table users contains: uid, username, passwd, email.
    # Default user login: default:default.
    db = mysql.connector.connect(
        host="YourHost",  # Enter your host address.
        database="loginSystems",
        user="YourUser",  # Enter your user.
        passwd="YourPassword"  # Enter your password.
    )
    c = db.cursor()

    while True:
        try:
            select = print_start()
        except ValueError:
            print("not a valid number. Try again...")
            continue
        if select == 1:
            if login(c):
                break
        elif select == 2:
            register(c)
            db.commit()
            break
        elif select == 3:
            quit()
        else:
            print("not a valid number. Try again...")


if __name__ == '__main__':
    main()
