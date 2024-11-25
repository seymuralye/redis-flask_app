from flask import Flask, jsonify
import psycopg2
import redis
import os
import json

app = Flask(__name__)

# Fetch database and Redis connection details from environment variables
DB_NAME = os.getenv("DB_NAME", "my_database")
DB_USER = os.getenv("DB_USER", "admin")
DB_PASSWORD = os.getenv("DB_PASSWORD", "admin123")
DB_HOST = os.getenv("DB_HOST", "postgres")
DB_PORT = int(os.getenv("DB_PORT", 5432))

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

# Redis client
redis_client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=0)

# PostgreSQL connection
def get_postgres_connection():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )

# Check if the table exists and create it if it doesn't
def ensure_table_exists_and_insert_data():
    try:
        conn = get_postgres_connection()
        cursor = conn.cursor()

        # Check if the table exists
        cursor.execute("""
        SELECT EXISTS (
            SELECT FROM information_schema.tables
            WHERE table_name = 'countries_capitals'
        );
        """)
        table_exists = cursor.fetchone()[0]

        if not table_exists:
            print("Table does not exist. Creating table...")
            # Create the table
            cursor.execute("""
            CREATE TABLE countries_capitals (
                id SERIAL PRIMARY KEY,
                country VARCHAR(100) UNIQUE NOT NULL,
                capital VARCHAR(100) NOT NULL
            );
            """)
            conn.commit()

            # Insert data from the text file
            print("Inserting data into the table...")
            with open("countries_capitals.txt", "r") as file:
                for line in file:
                    if ":" in line:
                        country, capital = line.strip().split(":")
                        cursor.execute("""
                        INSERT INTO countries_capitals (country, capital)
                        VALUES (%s, %s)
                        ON CONFLICT DO NOTHING; -- Skip duplicates
                        """, (country.strip(), capital.strip()))
            conn.commit()
            print("Data inserted successfully.")
        else:
            print("Table already exists.")
    except Exception as e:
        print(f"Error ensuring table exists: {e}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

# API endpoint to fetch countries and capitals
@app.route("/countries", methods=["GET"])
def get_countries():
    cache_key = "countries_data"

    # Check if data exists in Redis
    cached_data = redis_client.get(cache_key)
    if cached_data:
        print("Fetching data from Redis...")
        data = json.loads(cached_data)
        return jsonify({"source": "redis", "data": data})

    # Fetch from PostgreSQL if not in Redis
    try:
        print("Fetching data from PostgreSQL...")
        conn = get_postgres_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT country, capital FROM countries_capitals;")
        rows = cursor.fetchall()
        data = [{"country": row[0], "capital": row[1]} for row in rows]

        # Cache data in Redis
        redis_client.set(cache_key, json.dumps(data), ex=300)  # Cache expires in 300 seconds

        return jsonify({"source": "postgres", "data": data})
    except Exception as e:
        return jsonify({"error": str(e)})
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

# Initialize the application by ensuring the table exists and is populated
ensure_table_exists_and_insert_data()

# Start the Flask application
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

