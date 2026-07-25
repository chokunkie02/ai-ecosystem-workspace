import sys
import time
import psycopg2

sys.stdout.reconfigure(encoding='utf-8')

def run_tests():
    # Database connection parameters
    conn_params = {
        "host": "localhost",
        "port": 5433,
        "user": "postgres",
        "password": "mysecretpassword",
        "dbname": "student_db"
    }
    
    print("[Process] Attempting to connect to PostgreSQL...")
    conn = None
    # Retry logic to wait for the database container to fully start up and accept connections
    for attempt in range(1, 6):
        try:
            conn = psycopg2.connect(**conn_params)
            break
        except Exception as e:
            print(f"[Warning] Connection attempt {attempt} failed: {e}")
            time.sleep(2)
            
    if not conn:
        print("[Error] Failed to connect to PostgreSQL database after 5 attempts.")
        return
        
    print("[Process] Connected successfully to PostgreSQL database!")
    cursor = conn.cursor()
    
    try:
        # i. คำสั่งสร้าง table
        create_query = """
        DROP TABLE IF EXISTS students;
        CREATE TABLE students (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            age INT,
            major VARCHAR(100)
        );
        """
        print("\n=== i. CREATE TABLE ===")
        print(f"Executing Query:\n{create_query.strip()}")
        cursor.execute(create_query)
        conn.commit()
        print("Table 'students' created successfully.")
        
        # ii. คำสั่งเพิ่มข้อมูลเข้า table
        insert_query = """
        INSERT INTO students (name, age, major) VALUES
        ('chokun', 21, 'วิศวะเอไอ'),
        ('chompoo', 20, 'พยาบาล'),
        ('jack', 22, 'วิศวะเคมี');
        """
        print("\n=== ii. INSERT INTO TABLE ===")
        print(f"Executing Query:\n{insert_query.strip()}")
        cursor.execute(insert_query)
        conn.commit()
        print(f"Inserted {cursor.rowcount} records successfully.")
        
        # iii. คำสั่งแสดงข้อมูลใน table
        select_query = "SELECT * FROM students;"
        print("\n=== iii. SELECT FROM TABLE ===")
        print(f"Executing Query:\n{select_query.strip()}")
        cursor.execute(select_query)
        rows = cursor.fetchall()
        print("Results:")
        for row in rows:
            print(row)
            
        # iv. คำสั่งแก้ไขข้อมูลใน table
        update_query = "UPDATE students SET age = 23 WHERE name = 'chokun';"
        print("\n=== iv. UPDATE TABLE ===")
        print(f"Executing Query:\n{update_query.strip()}")
        cursor.execute(update_query)
        conn.commit()
        print(f"Updated {cursor.rowcount} record(s) successfully.")
        
        # Verify update
        cursor.execute("SELECT * FROM students WHERE name = 'chokun';")
        print("Updated Row:")
        print(cursor.fetchone())
        
        # v. คำสั่งลบข้อมูลใน table
        delete_query = "DELETE FROM students WHERE name = 'jack';"
        print("\n=== v. DELETE FROM TABLE ===")
        print(f"Executing Query:\n{delete_query.strip()}")
        cursor.execute(delete_query)
        conn.commit()
        print(f"Deleted {cursor.rowcount} record(s) successfully.")
        
        # Verify delete
        cursor.execute("SELECT * FROM students;")
        print("Remaining Rows:")
        for row in cursor.fetchall():
            print(row)
            
        # vi. คำสั่งลบ table
        drop_query = "DROP TABLE students;"
        print("\n=== vi. DROP TABLE ===")
        print(f"Executing Query:\n{drop_query.strip()}")
        cursor.execute(drop_query)
        conn.commit()
        print("Table 'students' dropped successfully.")
        
    except Exception as err:
        print(f"[Error] SQL Execution failed: {err}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()
        print("\n[Process] Database connection closed.")

if __name__ == "__main__":
    run_tests()
