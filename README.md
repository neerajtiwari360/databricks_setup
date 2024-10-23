# Spark, PostgreSQL, and Jupyter Notebook Docker Setup

This repository contains a Docker Compose setup for running an Apache Spark cluster, a PostgreSQL database, a Jupyter Notebook environment, and a Flask API for data insertion and retrieval. You can use this setup to run distributed data processing tasks, manage SQL databases, and work in a notebook-based Python environment with PySpark.

## Prerequisites

Make sure you have the following installed:

- Docker
- Docker Compose

## Services

This setup consists of the following services:

1. **Spark Master**: The master node for managing the Spark cluster.
2. **Spark Workers**: Two Spark workers for running Spark jobs.
3. **PostgreSQL Database**: A PostgreSQL database instance to store data.
4. **Jupyter Notebook**: A Jupyter Notebook environment with PySpark installed.
5. **Flask API**: A Flask application for inserting and retrieving data from the PostgreSQL database.

### Docker Services Summary:

- **Spark Master**: Web UI on `http://localhost:8080` and Spark Master listens on `http://localhost:7077`.
- **Spark Workers**: Automatically connect to Spark Master and participate in the cluster.
- **PostgreSQL**: Database accessible via `http://localhost:5432`.
- **Jupyter Notebook**: Web interface available on `http://localhost:8888`.
- **Flask API**: API endpoint available at `http://localhost:5000`.

## Usage

### Step 1: Clone the repository

```bash
git clone <your-repo-url>
cd <your-repo-directory>
```

### Step 2: Start the Docker containers

To start all services, run the following command in the root directory (where the `docker-compose.yml` file is located):

```bash
docker-compose build
docker-compose up -d
```

This command will pull the required Docker images (if they are not already on your system) and start the containers for Spark, PostgreSQL, Jupyter Notebook, and Flask API.

### Step 3: Access the services

- **Jupyter Notebook**: Open your browser and go to `http://localhost:8888`. The notebook is running without a token, so you don't need a password.
- **Spark Master UI**: Available at `http://localhost:8080`.
- **PostgreSQL**: Access the PostgreSQL instance at `localhost:5432` using tools like `psql` or any SQL client. The credentials are:
  - Username: `admin`
  - Password: `admin123`
  - Database: `sparkdb`
- **Flask API**: You can interact with the Flask API at `http://localhost:5000`.

### Step 4: Create a Table in PostgreSQL

Once the services are running, you can create a table in PostgreSQL using either a Python script or directly running SQL commands.

#### Option 1: Using Python to Create the Table

You can run the following Python script to create the `employees` table in PostgreSQL. Make sure you have the `psycopg2` package installed. You can install it in your Jupyter Notebook or any Python environment as follows:

```bash
!pip install psycopg2-binary
```

Then, use the following Python code to create the table:

```python
import psycopg2

# Define connection parameters
conn_params = {
    "dbname": "sparkdb",
    "user": "admin",
    "password": "admin123",
    "host": "postgres",  # Use the service name defined in Docker Compose
    "port": "5432"
}

# Establish connection and create a table
try:
    conn = psycopg2.connect(**conn_params)
    cur = conn.cursor()
    
    # Create a table called "employees"
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS employees (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100),
        department VARCHAR(100)
    );
    '''
    cur.execute(create_table_query)
    conn.commit()  # Commit changes
    print("Table 'employees' created successfully!")
except Exception as e:
    print(f"Error: {e}")
finally:
    cur.close()
    conn.close()
```

#### Option 2: Directly Running SQL Code in PostgreSQL

You can connect to the PostgreSQL database using the `psql` command line interface to create the table directly. Here’s how to do it:

1. **Connect to PostgreSQL**:

   You can connect to the PostgreSQL container using `psql`. Run the following command:

   ```bash
   docker exec -it postgres-db psql -U admin -d sparkdb
   ```

   This command opens the PostgreSQL command line interface connected to the `sparkdb` database.

2. **Create the Table**:

   Once connected to the PostgreSQL CLI, you can create the `employees` table by running the following SQL command:

   ```sql
   CREATE TABLE IF NOT EXISTS employees (
       id SERIAL PRIMARY KEY,
       name VARCHAR(100),
       department VARCHAR(100)
   );
   ```

3. **Exit the psql interface**:

   After you have created the table, you can exit the PostgreSQL CLI by typing:

   ```bash
   \q
   ```

### Step 5: Using the Flask API to Feed and Read Data

The Flask API is set up to allow you to add and retrieve employee data from the PostgreSQL database. 

#### Inserting Data

To insert data, you can use `curl` or Postman.

##### Using cURL

Here’s how you can add an employee using cURL:

```bash
curl -X POST http://localhost:5000/add_employee \
-H "Content-Type: application/json" \
-d '{"name": "John Doe", "department": "Engineering"}'
```

##### Using Postman

1. Open Postman and create a new POST request.
2. Enter the URL: `http://localhost:5000/add_employee`.
3. Set the request body to JSON format and use the following:

```json
{
    "name": "John Doe",
    "department": "Engineering"
}
```

4. Send the request. If successful, you will receive a confirmation message.

#### Retrieving Data

To retrieve all employees from the `employees` table, you can use another `curl` command or Postman.

##### Using cURL

```bash
curl -X GET http://localhost:5000/employees
```

##### Using Postman

1. Create a new GET request.
2. Enter the URL: `http://localhost:5000/employees`.
3. Send the request. You should receive a JSON array of all employee records.

### Step 6: Interact with the Spark Cluster

You can now interact with the Spark cluster using the PySpark environment in Jupyter Notebook.

1. Open the Jupyter Notebook at `http://localhost:8888`.
2. Create a new notebook and start coding with PySpark.
3. Install the necessary libraries:

```bash
!pip install psycopg2-binary sqlalchemy
```

For example, you can use the following code in a Jupyter Notebook to interact with your PostgreSQL database:

```python
from pyspark.sql import SparkSession

# Create a Spark session
spark = SparkSession.builder \
    .appName("PostgresExample") \
    .master("spark://spark-master:7077") \
    .config("spark.jars.packages", "org.postgresql:postgresql:42.2.23") \
    .getOrCreate()

# PostgreSQL connection properties
url = "jdbc:postgresql://postgres-db:5432/sparkdb"
properties = {
    "user": "admin",
    "password": "admin123",
    "driver": "org.postgresql.Driver"
}

# Read data from PostgreSQL
df = spark.read.jdbc(url=url, table="employees", properties=properties)
df.show()

# Write data back to PostgreSQL
new_data = [("John Doe", "Software Engineer", 90000),
            ("Jane Doe", "Data Scientist", 95000)]

columns = ["name", "department", "salary"]
new_df = spark.createDataFrame(new_data, columns)

new_df.write.jdbc(url=url, table="employees", mode="append", properties=properties)
```

### Step 7: Stop the Containers

To stop and remove the containers, run:

```bash
docker-compose down
```

This will stop the running containers and remove them.

### Step 8: Persisting Data

The `./notebooks` folder is mounted into the Jupyter Notebook container, so any notebooks you create will be saved in this directory on your host machine. PostgreSQL data will persist in the Docker volumes even after the containers are stopped.

## Notes

- You can modify the `docker-compose.yml` file to adjust resource allocation or add additional services.
- The PostgreSQL data will be persisted across container restarts thanks to Docker volumes.

## Troubleshooting

- If you encounter any issues connecting to the Spark Master, ensure that the containers are up and running using the following command:

  ```bash
  docker-compose ps
  ```

- Ensure that your local ports `8080`, `7077`, `5432`, `8888`, and `5000` are not being used by other services before running the containers.

---

This setup should allow you to easily run an Apache Spark cluster alongside PostgreSQL, a Jupyter Notebook, and a Flask API for your data analysis and processing tasks.
```

### Summary of Changes in the Updated README.md
- **Project Overview**: Updated to include both data insertion and retrieval functionality through the Flask API

.
- **Usage Section**: Added detailed steps for retrieving data using the API.
- **Clear Instructions**: Enhanced clarity and flow in the instructions for ease of use.
- **Example Commands**: Included examples for both inserting and retrieving data via cURL and Postman.