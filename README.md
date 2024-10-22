# Spark, PostgreSQL, and Jupyter Notebook Docker Setup

This repository contains a Docker Compose setup for running an Apache Spark cluster, a PostgreSQL database, and a Jupyter Notebook environment. You can use this setup to run distributed data processing tasks, manage SQL databases, and work in a notebook-based Python environment with PySpark.

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

### Docker Services Summary:

- **Spark Master**: Web UI on `localhost:8080` and Spark Master listens on `localhost:7077`.
- **Spark Workers**: Automatically connect to Spark Master and participate in the cluster.
- **PostgreSQL**: Database accessible via `localhost:5432`.
- **Jupyter Notebook**: Web interface available on `localhost:8888`.

## Usage

### Step 1: Clone the repository

```bash
git clone <your-repo-url>
cd <your-repo-directory>
```

### Step 2: Start the Docker containers

To start all services, run the following command in the root directory (where the `docker-compose.yml` file is located):

```bash
docker-compose up -d
```

This command will pull the required Docker images (if they are not already on your system) and start the containers for Spark, PostgreSQL, and Jupyter Notebook.

### Step 3: Access the services

- **Jupyter Notebook**: Open your browser and go to `http://localhost:8888`. The notebook is running without a token, so you don't need a password.
- **Spark Master UI**: Available at `http://localhost:8080`.
- **PostgreSQL**: Access the PostgreSQL instance at `localhost:5432` using tools like `psql` or any SQL client. The credentials are:
  - Username: `admin`
  - Password: `admin123`
  - Database: `sparkdb`

### Step 4: Create a Table in PostgreSQL

Once the services are running, you can create a table in PostgreSQL using the following SQL query.

1. **Connect to PostgreSQL**:

   You can connect to the PostgreSQL container using `psql` or any SQL client (like DBeaver, pgAdmin, etc.). For example, to connect using `psql`, run:

   ```bash
   docker exec -it postgres-db psql -U admin -d sparkdb
   ```

   You will now be inside the PostgreSQL CLI, connected to the `sparkdb` database.

2. **Create a Table**:

   Once connected, you can create a table using the following SQL query:

   ```sql
   CREATE TABLE employees (
       id SERIAL PRIMARY KEY,
       name VARCHAR(100),
       position VARCHAR(50),
       salary INTEGER
   );
   ```

   This creates a simple `employees` table with columns for `id`, `name`, `position`, and `salary`.

### Step 5: Interact with the Spark Cluster

You can now interact with the Spark cluster using the PySpark environment in Jupyter Notebook.

1. Open the Jupyter Notebook at `http://localhost:8888`.
2. Create a new notebook and start coding with PySpark.
   
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

columns = ["name", "position", "salary"]
new_df = spark.createDataFrame(new_data, columns)

new_df.write.jdbc(url=url, table="employees", mode="append", properties=properties)
```

### Step 6: Stop the Containers

To stop and remove the containers, run:

```bash
docker-compose down
```

This will stop the running containers and remove them.

### Step 7: Persisting Data

The `./notebooks` folder is mounted into the Jupyter Notebook container, so any notebooks you create will be saved in this directory on your host machine. PostgreSQL data will persist in the Docker volumes even after the containers are stopped.

## Notes

- You can modify the `docker-compose.yml` file to adjust resource allocation or add additional services.
- The PostgreSQL data will be persisted across container restarts thanks to Docker volumes.

## Troubleshooting

- If you encounter any issues connecting to the Spark Master, ensure that the containers are up and running using the following command:

  ```bash
  docker-compose ps
  ```

- Ensure that your local ports `8080`, `7077`, `5432`, and `8888` are not being used by other services before running the containers.

---

This setup should allow you to easily run an Apache Spark cluster alongside PostgreSQL and a Jupyter Notebook for your data analysis and processing tasks.