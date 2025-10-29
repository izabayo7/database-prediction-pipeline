"""
MySQL Data Import Script for HR Employee Attrition Dataset
This script imports data from CSV into MySQL database
"""

import pandas as pd
import mysql.connector
from mysql.connector import Error
from datetime import datetime
import logging
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# MySQL Configuration
MYSQL_CONFIG = {
    'host': os.getenv('MYSQL_HOST', 'localhost'),
    'database': os.getenv('MYSQL_DATABASE', 'hr_attrition_db'),
    'user': os.getenv('MYSQL_USER', 'root'),
    'password': os.getenv('MYSQL_PASSWORD', 'password'),
    'port': int(os.getenv('MYSQL_PORT', 3306))
}

# CSV file path
CSV_FILE_PATH = os.getenv('CSV_FILE_PATH', 'hr_employee_attrition.csv')


class MySQLDataImporter:
    """Class to handle data import for HR Attrition dataset into MySQL"""
    
    def __init__(self):
        """Initialize MySQL connection"""
        self.connection = None
        self.cursor = None
        self.departments_map = {}
        
    def connect_mysql(self):
        """Establish MySQL connection"""
        try:
            self.connection = mysql.connector.connect(**MYSQL_CONFIG)
            self.cursor = self.connection.cursor()
            logger.info(f"Successfully connected to MySQL database: {MYSQL_CONFIG['database']}")
        except Error as e:
            logger.error(f"Failed to connect to MySQL: {e}")
            raise
            
    def clean_tables(self):
        """Clear existing data from MySQL tables"""
        try:
            # Disable foreign key checks temporarily
            self.cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
            
            tables = [
                'satisfaction_scores',
                'performance_metrics',
                'compensation',
                'job_details',
                'employees',
                'departments'
            ]
            
            for table in tables:
                self.cursor.execute(f"TRUNCATE TABLE {table}")
                logger.info(f"Cleared table: {table}")
            
            # Re-enable foreign key checks
            self.cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
            self.connection.commit()
            
        except Error as e:
            self.connection.rollback()
            logger.error(f"Error clearing MySQL tables: {e}")
            raise
    
    def load_csv_data(self) -> pd.DataFrame:
        """Load and preprocess CSV data"""
        try:
            # Check if file exists
            if not os.path.exists(CSV_FILE_PATH):
                raise FileNotFoundError(f"CSV file not found: {CSV_FILE_PATH}")
                
            df = pd.read_csv(CSV_FILE_PATH)
            logger.info(f"Loaded {len(df)} records from {CSV_FILE_PATH}")
            
            # Handle any NaN values
            df = df.fillna({
                'NumCompaniesWorked': 0,
                'YearsInCurrentRole': 0,
                'YearsSinceLastPromotion': 0,
                'YearsWithCurrManager': 0,
                'TrainingTimesLastYear': 0
            })
            
            # Validate required columns
            required_columns = [
                'EmployeeNumber', 'Age', 'Gender', 'MaritalStatus', 'Education',
                'EducationField', 'DistanceFromHome', 'Over18', 'EmployeeCount',
                'Attrition', 'Department', 'JobRole', 'JobLevel', 'JobInvolvement',
                'JobSatisfaction', 'StandardHours', 'BusinessTravel', 'OverTime',
                'DailyRate', 'HourlyRate', 'MonthlyIncome', 'MonthlyRate',
                'PercentSalaryHike', 'StockOptionLevel', 'PerformanceRating',
                'YearsAtCompany', 'YearsInCurrentRole', 'YearsSinceLastPromotion',
                'YearsWithCurrManager', 'TotalWorkingYears', 'NumCompaniesWorked',
                'TrainingTimesLastYear', 'EnvironmentSatisfaction', 
                'RelationshipSatisfaction', 'WorkLifeBalance'
            ]
            
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                raise ValueError(f"Missing required columns: {missing_columns}")
            
            return df
            
        except Exception as e:
            logger.error(f"Error loading CSV file: {e}")
            raise
    
    def insert_departments(self, df: pd.DataFrame):
        """Insert unique departments into MySQL"""
        try:
            departments = df['Department'].unique()
            
            for dept_name in departments:
                # Insert department
                insert_query = """
                    INSERT INTO departments (department_name) 
                    VALUES (%s)
                    ON DUPLICATE KEY UPDATE department_id=LAST_INSERT_ID(department_id)
                """
                self.cursor.execute(insert_query, (dept_name,))
                
                # Get the department_id
                dept_id = self.cursor.lastrowid
                if dept_id == 0:
                    # Department already existed, fetch its ID
                    self.cursor.execute(
                        "SELECT department_id FROM departments WHERE department_name = %s",
                        (dept_name,)
                    )
                    dept_id = self.cursor.fetchone()[0]
                
                self.departments_map[dept_name] = dept_id
            
            self.connection.commit()
            logger.info(f"Inserted {len(departments)} departments")
            
        except Error as e:
            self.connection.rollback()
            logger.error(f"Error inserting departments: {e}")
            raise
    
    def insert_data(self, df: pd.DataFrame):
        """Insert data into MySQL tables"""
        try:
            success_count = 0
            error_count = 0
            
            for idx, row in df.iterrows():
                try:
                    # 1. Insert into employees table
                    employee_query = """
                        INSERT INTO employees (
                            employee_number, age, gender, marital_status, education,
                            education_field, distance_from_home, over_18, employee_count,
                            attrition
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        ON DUPLICATE KEY UPDATE employee_number=employee_number
                    """
                    employee_data = (
                        int(row['EmployeeNumber']),
                        int(row['Age']),
                        row['Gender'],
                        row['MaritalStatus'],
                        int(row['Education']),
                        row['EducationField'],
                        int(row['DistanceFromHome']),
                        row['Over18'],
                        int(row['EmployeeCount']),
                        row['Attrition']
                    )
                    self.cursor.execute(employee_query, employee_data)
                    
                    # 2. Insert into job_details table
                    job_query = """
                        INSERT INTO job_details (
                            employee_number, department_id, job_role, job_level,
                            job_involvement, job_satisfaction, standard_hours,
                            business_travel, overtime
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    job_data = (
                        int(row['EmployeeNumber']),
                        self.departments_map[row['Department']],
                        row['JobRole'],
                        int(row['JobLevel']),
                        int(row['JobInvolvement']),
                        int(row['JobSatisfaction']),
                        int(row['StandardHours']),
                        row['BusinessTravel'],
                        row['OverTime']
                    )
                    self.cursor.execute(job_query, job_data)
                    
                    # 3. Insert into compensation table
                    comp_query = """
                        INSERT INTO compensation (
                            employee_number, daily_rate, hourly_rate, monthly_income,
                            monthly_rate, percent_salary_hike, stock_option_level
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """
                    comp_data = (
                        int(row['EmployeeNumber']),
                        int(row['DailyRate']),
                        int(row['HourlyRate']),
                        int(row['MonthlyIncome']),
                        int(row['MonthlyRate']),
                        int(row['PercentSalaryHike']),
                        int(row['StockOptionLevel'])
                    )
                    self.cursor.execute(comp_query, comp_data)
                    
                    # 4. Insert into performance_metrics table
                    perf_query = """
                        INSERT INTO performance_metrics (
                            employee_number, performance_rating, years_at_company,
                            years_in_current_role, years_since_last_promotion,
                            years_with_curr_manager, total_working_years,
                            num_companies_worked, training_times_last_year
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    perf_data = (
                        int(row['EmployeeNumber']),
                        int(row['PerformanceRating']),
                        int(row['YearsAtCompany']),
                        int(row['YearsInCurrentRole']),
                        int(row['YearsSinceLastPromotion']),
                        int(row['YearsWithCurrManager']),
                        int(row['TotalWorkingYears']),
                        int(row['NumCompaniesWorked']),
                        int(row['TrainingTimesLastYear'])
                    )
                    self.cursor.execute(perf_query, perf_data)
                    
                    # 5. Insert into satisfaction_scores table
                    sat_query = """
                        INSERT INTO satisfaction_scores (
                            employee_number, environment_satisfaction, job_satisfaction,
                            relationship_satisfaction, work_life_balance
                        ) VALUES (%s, %s, %s, %s, %s)
                    """
                    sat_data = (
                        int(row['EmployeeNumber']),
                        int(row['EnvironmentSatisfaction']),
                        int(row['JobSatisfaction']),
                        int(row['RelationshipSatisfaction']),
                        int(row['WorkLifeBalance'])
                    )
                    self.cursor.execute(sat_query, sat_data)
                    
                    success_count += 1
                    
                    # Commit every 100 records for better performance
                    if success_count % 100 == 0:
                        self.connection.commit()
                        logger.info(f"Inserted {success_count} records...")
                        
                except Error as e:
                    error_count += 1
                    logger.warning(f"Error inserting row {idx} (Employee {row['EmployeeNumber']}): {e}")
                    self.connection.rollback()
                    continue
            
            # Final commit
            self.connection.commit()
            logger.info(f"Successfully inserted {success_count} records into MySQL")
            if error_count > 0:
                logger.warning(f"Failed to insert {error_count} records")
            
        except Error as e:
            self.connection.rollback()
            logger.error(f"Error inserting data into MySQL: {e}")
            raise
    
    def verify_data(self):
        """Verify data insertion in MySQL"""
        try:
            print("\n" + "="*60)
            print("MYSQL DATA VERIFICATION RESULTS")
            print("="*60)
            
            # Count records in each table
            tables = [
                'employees',
                'departments',
                'job_details',
                'compensation',
                'performance_metrics',
                'satisfaction_scores'
            ]
            
            for table in tables:
                self.cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = self.cursor.fetchone()[0]
                print(f"{table.upper()}: {count} records")
            
            # Test stored procedure
            print("\n--- Testing Stored Procedure ---")
            try:
                self.cursor.execute("CALL calculate_attrition_risk(1)")
                result = self.cursor.fetchone()
                if result:
                    print(f"Risk calculation for Employee 1:")
                    print(f"  Employee ID: {result[0]}")
                    print(f"  Risk Score: {result[1]}")
                    print(f"  Risk Level: {result[2]}")
                    print(f"  Risk Factors: {result[3]}")
                
                # Consume any remaining results from the stored procedure
                while self.cursor.nextset():
                    pass
                    
            except Error as e:
                logger.warning(f"Stored procedure not found or error: {e}")
            
            # Department statistics
            print("\n--- Department Statistics ---")
            self.cursor.execute("""
                SELECT d.department_name, COUNT(e.employee_number) as emp_count,
                       SUM(CASE WHEN e.attrition = 'Yes' THEN 1 ELSE 0 END) as attrition_count
                FROM departments d
                JOIN job_details j ON d.department_id = j.department_id
                JOIN employees e ON j.employee_number = e.employee_number
                GROUP BY d.department_name
            """)
            
            for dept_name, emp_count, attrition_count in self.cursor.fetchall():
                attrition_rate = (attrition_count / emp_count) * 100 if emp_count > 0 else 0
                print(f"{dept_name}: {emp_count} employees, {attrition_rate:.1f}% attrition rate")
            
            print("="*60)
            
        except Error as e:
            logger.error(f"Error verifying data: {e}")
    
    def close_connection(self):
        """Close MySQL connection"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
            logger.info("MySQL connection closed")
    
    def run_import(self):
        """Main method to run the complete import process"""
        try:
            # Connect to MySQL
            self.connect_mysql()
            
            # Ask user if they want to clean existing data
            response = input("\nDo you want to clean existing data before import? (y/n): ").lower()
            if response == 'y':
                logger.info("Cleaning existing data...")
                self.clean_tables()
            
            # Load CSV data
            logger.info("Loading CSV data...")
            df = self.load_csv_data()
            
            # Insert departments first
            logger.info("Inserting departments...")
            self.insert_departments(df)
            
            # Insert data into MySQL
            logger.info("Inserting data into MySQL tables...")
            self.insert_data(df)
            
            # Verify insertion
            logger.info("Verifying data insertion...")
            self.verify_data()
            
            logger.info("\n✅ MySQL data import completed successfully!")
            
        except Exception as e:
            logger.error(f"Import failed: {e}")
            raise
        
        finally:
            self.close_connection()


def main():
    """Main execution function"""
    print("=" * 60)
    print("MYSQL DATA IMPORT SCRIPT FOR HR EMPLOYEE ATTRITION")
    print("=" * 60)
    print("\nDataset: IBM HR Analytics Employee Attrition")
    print("Target: MySQL Database")
    print("-" * 60)
    
    # Check if CSV file exists
    if not os.path.exists(CSV_FILE_PATH):
        print(f"\n❌ ERROR: CSV file not found at '{CSV_FILE_PATH}'")
        print("Please download the dataset from Kaggle and place it in the current directory")
        print("URL: https://www.kaggle.com/pavansubhasht/ibm-hr-analytics-attrition-dataset")
        return
    
    # Create importer instance
    importer = MySQLDataImporter()
    
    try:
        # Run import
        importer.run_import()
    except KeyboardInterrupt:
        print("\n\n⚠️  Import interrupted by user")
    except Exception as e:
        print(f"\n❌ Import failed with error: {e}")
        return
    
    print("\n" + "=" * 60)
    print("MYSQL IMPORT COMPLETED!")
    print("=" * 60)


if __name__ == "__main__":
    main()
