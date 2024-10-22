from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)

# Database connection parameters
DB_CONFIG = {
    "dbname": "sparkdb",
    "user": "admin",
    "password": "admin123",
    "host": "postgres",  # Docker service name for PostgreSQL
    "port": "5432"
}

# Function to connect to the database
def connect_db():
    conn = psycopg2.connect(**DB_CONFIG)
    return conn

# Route to insert data into employees table
@app.route('/add_employee', methods=['POST'])
def add_employee():
    data = request.get_json()
    name = data.get('name')
    department = data.get('department')

    if not name or not department:
        return jsonify({"error": "Name and department are required!"}), 400

    try:
        conn = connect_db()
        cur = conn.cursor()
        
        insert_query = '''
        INSERT INTO employees (name, department)
        VALUES (%s, %s);
        '''
        cur.execute(insert_query, (name, department))
        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"message": "Employee added successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to read all employees from the table
@app.route('/employees', methods=['GET'])
def get_employees():
    try:
        conn = connect_db()
        cur = conn.cursor()
        
        select_query = 'SELECT id, name, department FROM employees;'
        cur.execute(select_query)
        rows = cur.fetchall()
        
        # Create a list of dictionaries to hold employee data
        employees = []
        for row in rows:
            employees.append({
                "id": row[0],
                "name": row[1],
                "department": row[2]
            })

        cur.close()
        conn.close()

        return jsonify(employees), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Health check route
@app.route('/')
def index():
    return "Flask API is running!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)




# from flask import Flask, request, jsonify
# import psycopg2

# app = Flask(__name__)

# # Database connection parameters
# DB_CONFIG = {
#     "dbname": "sparkdb",
#     "user": "admin",
#     "password": "admin123",
#     "host": "postgres",  # Docker service name for PostgreSQL
#     "port": "5432"
# }

# # Function to connect to the database
# def connect_db():
#     conn = psycopg2.connect(**DB_CONFIG)
#     return conn

# # Route to insert data into employees table
# @app.route('/add_employee', methods=['POST'])
# def add_employee():
#     data = request.get_json()
#     name = data.get('name')
#     department = data.get('department')

#     if not name or not department:
#         return jsonify({"error": "Name and department are required!"}), 400

#     try:
#         conn = connect_db()
#         cur = conn.cursor()
        
#         insert_query = '''
#         INSERT INTO employees (name, department)
#         VALUES (%s, %s);
#         '''
#         cur.execute(insert_query, (name, department))
#         conn.commit()
#         cur.close()
#         conn.close()

#         return jsonify({"message": "Employee added successfully!"}), 201
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# # Health check route
# @app.route('/')
# def index():
#     return "Flask API is running!"

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)
