import mysql.connector
import bcrypt


# Setups database to be used.
def setup():

    # Default user is default:default.
    # But you can change these to your liking.
    DEFAULT_PASSWORD = bcrypt.hashpw(b"default", bcrypt.gensalt())
    DEFAULT_USERNAME = "default"
    DEFAULT_EMAIL = "default@default.com"
    DEFAULT_DATABASE = "loginDatabase"

    db = mysql.connector.connect(
        host="YourHost",  # Enter your host address.
        user="YourUser",  # Enter your user.
        passwd="YourPassword"  # Enter your password.
    )
    mycursor = db.cursor()
    mycursor.execute(f"CREATE DATABASE {DEFAULT_DATABASE}")
    mycursor.execute(f"USE {DEFAULT_DATABASE}")
    mycursor.execute(
        "CREATE TABLE Users (uid int primary KEY AUTO_INCREMENT NOT NULL,username VARCHAR(255) NOT NULL, passwd VARCHAR(255) NOT NULL, email VARCHAR(255) NOT NULL)")
    mycursor.execute("INSERT INTO Users (username, passwd, email) VALUES (%s,%s,%s)",
                     (DEFAULT_USERNAME, DEFAULT_PASSWORD, DEFAULT_EMAIL))

    db.commit()
    db.close()
    print(
        f"A database named {DEFAULT_DATABASE} with table users contains uid, username, passwd, email")


if __name__ == '__main__':
    setup()
