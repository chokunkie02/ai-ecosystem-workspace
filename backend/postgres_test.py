from sqlalchemy import create_engine, text
from core.config import settings

url = f"postgresql+psycopg2://{settings.postgres_user}:{settings.postgres_password}@{settings.postgres_host}:{settings.postgres_port}/{settings.postgres_db}"
engine = create_engine(url)

def create_table():
    with engine.begin() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS students (
                id SERIAL PRIMARY KEY,
                student_id VARCHAR(50),
                name VARCHAR(100),
                age INT,
                major VARCHAR(100)
            )
        """))
    print("Table created.")

def show_data(label):
    with engine.begin() as conn:
        rows = conn.execute(text("SELECT * FROM students")).fetchall()
        print(f"--- {label} ---")
        for row in rows:
            print(row)

def insert_data():
    with engine.begin() as conn:
        conn.execute(text("INSERT INTO students (student_id, name, age, major) VALUES (:sid, :n, :a, :m)"),
                     {"sid": "6710110589", "n": "chokun", "a": 21, "m": "AI Engineering"})
    print("Data inserted.")

def update_data():
    with engine.begin() as conn:
        conn.execute(text("UPDATE students SET age = :a WHERE name = :n"), {"a": 22, "n": "chokun"})
    print("Data updated.")

def delete_data():
    with engine.begin() as conn:
        conn.execute(text("DELETE FROM students WHERE name = :n"), {"n": "chokun"})
    print("Data deleted.")

def drop_table():
    with engine.begin() as conn:
        conn.execute(text("DROP TABLE students"))
    print("Table dropped.")

if __name__ == "__main__":
    create_table()
    insert_data()
    show_data("After Insert")
    update_data()
    show_data("After Update")
    delete_data()
    show_data("After Delete")
    drop_table()
