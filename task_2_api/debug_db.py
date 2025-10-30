from sqlalchemy import text
from database import engine

def run():
    with engine.connect() as conn:
        print("DATABASE():", conn.execute(text("SELECT DATABASE()")).scalar())
        print("USER():", conn.execute(text("SELECT USER()")).scalar())
        print("session sql_mode:", conn.execute(text("SELECT @@session.sql_mode")).scalar())

        print("\nSHOW CREATE TABLE employees:")
        row = conn.execute(text("SHOW CREATE TABLE employees")).fetchone()
        print(row[1] if row else "No table info returned")

        print("\nSHOW TRIGGERS FOR employees (if any):")
        trig = conn.execute(text("SHOW TRIGGERS LIKE 'employees'")).fetchall()
        print(trig or "No triggers")

        print("\nAttempting INSERT using engine.begin() ...")
        ins = text("""
            INSERT INTO employees
            (age, gender, marital_status, education, education_field, distance_from_home, over_18, employee_count, attrition)
            VALUES (:age, :gender, :marital_status, :education, :education_field, :distance_from_home, :over_18, :employee_count, :attrition)
        """)
        try:
            with conn.begin():  # safe way to start a new transaction
                conn.execute(ins, {
                    "age": 99,
                    "gender": "Female",
                    "marital_status": "Single",
                    "education": 1,
                    "education_field": "Test",
                    "distance_from_home": 0,
                    "over_18": "Y",
                    "employee_count": 1,
                    "attrition": "No"
                })
            print("Manual INSERT succeeded via SQLAlchemy connection.")
        except Exception as e:
            print("Manual INSERT failed via SQLAlchemy connection.")
            print("Exception:", repr(e))

if __name__ == "__main__":
    run()