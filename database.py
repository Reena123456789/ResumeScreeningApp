import mysql.connector
import bcrypt

# Database connection
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        port=3308,
        database="resume_db"
    )

# Create Users Table (Run once)
def create_users_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            username VARCHAR(100) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()

# Register User
def registerUser(name, username, password):
    conn = get_connection()
    cursor = conn.cursor()

    # Hash the password before storing
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    try:
        query = "INSERT INTO users (name, username, password) VALUES (%s, %s, %s)"
        cursor.execute(query, (name, username, hashed_password.decode('utf-8')))
        conn.commit()
        cursor.close()
        conn.close()
        return True  # Registration successful
    except mysql.connector.Error as e:
        cursor.close()
        conn.close()
        return False  # Registration failed

# Login User
def loginUser(username, password):
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT password FROM users WHERE username = %s"
    cursor.execute(query, (username,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if user:
        hashed_password = user[0]
        if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
            return True  # Login successful
    return False  # Login failed
