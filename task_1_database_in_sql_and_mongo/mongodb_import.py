"""
MongoDB Data Import Script for HR Employee Attrition Dataset
This script imports data from CSV into MongoDB database

Authentication Support:
- Supports both authenticated and non-authenticated connections
- Set MONGODB_USER and MONGODB_PASSWORD in .env for authentication
- Leave them empty/unset for connections without authentication
"""

import pandas as pd
from pymongo import MongoClient
from datetime import datetime
import logging
import os
from dotenv import load_dotenv
import numpy as np

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# MongoDB Configuration
MONGODB_CONFIG = {
    'host': os.getenv('MONGODB_HOST', 'localhost'),
    'port': int(os.getenv('MONGODB_PORT', 27017)),
    'database': os.getenv('MONGODB_DATABASE', 'hr_attrition_nosql'),
    'username': os.getenv('MONGODB_USER'),
    'password': os.getenv('MONGODB_PASSWORD'),
    'authSource': os.getenv('MONGODB_AUTH_SOURCE', 'admin')  # Default to 'admin' for authentication
}

# CSV file path
CSV_FILE_PATH = os.getenv('CSV_FILE_PATH', 'hr_employee_attrition.csv')


class MongoDBDataImporter:
    """Class to handle data import for HR Attrition dataset into MongoDB"""
    
    def __init__(self):
        """Initialize MongoDB connection"""
        self.client = None
        self.db = None
        
    def connect_mongodb(self):
        """Establish MongoDB connection"""
        try:
            # Build connection parameters
            connection_params = {
                'host': MONGODB_CONFIG['host'],
                'port': MONGODB_CONFIG['port']
            }
            
            # Add authentication if credentials are provided
            if MONGODB_CONFIG.get('username') and MONGODB_CONFIG.get('password'):
                connection_params['username'] = MONGODB_CONFIG['username']
                connection_params['password'] = MONGODB_CONFIG['password']
                connection_params['authSource'] = MONGODB_CONFIG.get('authSource', MONGODB_CONFIG['database'])
                logger.info(f"Connecting to MongoDB with authentication as user: {MONGODB_CONFIG['username']}")
            else:
                logger.info("Connecting to MongoDB without authentication")
            
            self.client = MongoClient(**connection_params)
            self.db = self.client[MONGODB_CONFIG['database']]
            
            # Test connection
            server_info = self.client.server_info()
            logger.info(f"Successfully connected to MongoDB (version {server_info['version']})")
            logger.info(f"Using database: {MONGODB_CONFIG['database']}")
            
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise
    
    def clean_collections(self):
        """Clear existing data from MongoDB collections"""
        try:
            collections = ['employees', 'departments', 'attrition_predictions']
            
            for collection in collections:
                result = self.db[collection].delete_many({})
                logger.info(f"Cleared collection '{collection}': {result.deleted_count} documents deleted")
                
        except Exception as e:
            logger.error(f"Error clearing MongoDB collections: {e}")
            raise
    
    def create_indexes(self):
        """Create indexes for better query performance"""
        try:
            # Employees collection indexes
            self.db.employees.create_index([("employee_number", 1)], unique=True)
            self.db.employees.create_index([("attrition_info.status", 1)])
            self.db.employees.create_index([("job_info.department", 1)])
            self.db.employees.create_index([("personal_info.age", 1)])
            self.db.employees.create_index([("compensation.monthly_income", 1)])
            
            # Departments collection index
            self.db.departments.create_index([("department_name", 1)], unique=True)
            
            logger.info("Created MongoDB indexes successfully")
            
        except Exception as e:
            logger.error(f"Error creating indexes: {e}")
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
        """Insert department statistics into MongoDB"""
        try:
            departments = []
            
            for dept_name in df['Department'].unique():
                dept_data = df[df['Department'] == dept_name]
                attrition_count = (dept_data['Attrition'] == 'Yes').sum()
                total_count = len(dept_data)
                attrition_rate = attrition_count / total_count if total_count > 0 else 0
                
                dept_doc = {
                    'department_name': dept_name,
                    'employee_count': total_count,
                    'attrition_count': int(attrition_count),
                    'avg_attrition_rate': round(attrition_rate, 3),
                    'avg_satisfaction': {
                        'job': round(dept_data['JobSatisfaction'].mean(), 2),
                        'environment': round(dept_data['EnvironmentSatisfaction'].mean(), 2),
                        'relationship': round(dept_data['RelationshipSatisfaction'].mean(), 2),
                        'work_life_balance': round(dept_data['WorkLifeBalance'].mean(), 2)
                    },
                    'avg_monthly_income': round(dept_data['MonthlyIncome'].mean(), 2),
                    'last_updated': datetime.now()
                }
                
                departments.append(dept_doc)
            
            # Insert all departments
            if departments:
                result = self.db.departments.insert_many(departments)
                logger.info(f"Inserted {len(result.inserted_ids)} departments")
            
        except Exception as e:
            logger.error(f"Error inserting departments: {e}")
            raise
    
    def insert_employees(self, df: pd.DataFrame):
        """Insert employee data into MongoDB"""
        try:
            documents = []
            batch_size = 100
            
            for idx, row in df.iterrows():
                # Create employee document with embedded structure
                doc = {
                    'employee_number': int(row['EmployeeNumber']),
                    'personal_info': {
                        'age': int(row['Age']),
                        'gender': row['Gender'],
                        'marital_status': row['MaritalStatus'],
                        'education': {
                            'level': int(row['Education']),
                            'field': row['EducationField']
                        },
                        'distance_from_home': int(row['DistanceFromHome']),
                        'over_18': row['Over18']
                    },
                    'job_info': {
                        'department': row['Department'],
                        'role': row['JobRole'],
                        'level': int(row['JobLevel']),
                        'involvement': int(row['JobInvolvement']),
                        'satisfaction': int(row['JobSatisfaction']),
                        'standard_hours': int(row['StandardHours']),
                        'business_travel': row['BusinessTravel'],
                        'overtime': row['OverTime']
                    },
                    'compensation': {
                        'daily_rate': int(row['DailyRate']),
                        'hourly_rate': int(row['HourlyRate']),
                        'monthly_income': int(row['MonthlyIncome']),
                        'monthly_rate': int(row['MonthlyRate']),
                        'percent_salary_hike': int(row['PercentSalaryHike']),
                        'stock_option_level': int(row['StockOptionLevel'])
                    },
                    'performance': {
                        'rating': int(row['PerformanceRating']),
                        'years_at_company': int(row['YearsAtCompany']),
                        'years_in_current_role': int(row['YearsInCurrentRole']),
                        'years_since_last_promotion': int(row['YearsSinceLastPromotion']),
                        'years_with_current_manager': int(row['YearsWithCurrManager']),
                        'total_working_years': int(row['TotalWorkingYears']),
                        'num_companies_worked': int(row['NumCompaniesWorked']),
                        'training_times_last_year': int(row['TrainingTimesLastYear'])
                    },
                    'satisfaction_scores': {
                        'environment': int(row['EnvironmentSatisfaction']),
                        'job': int(row['JobSatisfaction']),
                        'relationship': int(row['RelationshipSatisfaction']),
                        'work_life_balance': int(row['WorkLifeBalance'])
                    },
                    'attrition_info': {
                        'status': row['Attrition'],
                        'risk_score': None,  # To be calculated by ML model
                        'last_risk_assessment': None
                    },
                    'metadata': {
                        'created_at': datetime.now(),
                        'updated_at': datetime.now(),
                        'employee_count': int(row['EmployeeCount']),
                        'data_source': 'initial_import'
                    }
                }
                
                documents.append(doc)
                
                # Insert in batches for better performance
                if len(documents) >= batch_size:
                    result = self.db.employees.insert_many(documents)
                    logger.info(f"Inserted batch of {len(result.inserted_ids)} employees (total: {idx + 1})")
                    documents = []
            
            # Insert remaining documents
            if documents:
                result = self.db.employees.insert_many(documents)
                logger.info(f"Inserted final batch of {len(result.inserted_ids)} employees")
            
            total_count = self.db.employees.count_documents({})
            logger.info(f"Total employees in MongoDB: {total_count}")
            
        except Exception as e:
            logger.error(f"Error inserting employees: {e}")
            raise
    
    def verify_data(self):
        """Verify data insertion in MongoDB"""
        try:
            print("\n" + "="*60)
            print("MONGODB DATA VERIFICATION RESULTS")
            print("="*60)
            
            # Count documents in collections
            collections_info = [
                ('employees', {}),
                ('departments', {}),
                ('employees (with attrition)', {'attrition_info.status': 'Yes'}),
                ('employees (without attrition)', {'attrition_info.status': 'No'})
            ]
            
            print("\n--- Collection Counts ---")
            for collection_name, query in collections_info:
                if 'employees' in collection_name:
                    count = self.db.employees.count_documents(query)
                else:
                    count = self.db.departments.count_documents(query)
                print(f"{collection_name}: {count} documents")
            
            # Department statistics using aggregation
            print("\n--- Department Statistics (Aggregation) ---")
            pipeline = [
                {
                    "$group": {
                        "_id": "$job_info.department",
                        "count": {"$sum": 1},
                        "avg_income": {"$avg": "$compensation.monthly_income"},
                        "attrition_count": {
                            "$sum": {
                                "$cond": [{"$eq": ["$attrition_info.status", "Yes"]}, 1, 0]
                            }
                        },
                        "avg_satisfaction": {"$avg": "$satisfaction_scores.job"}
                    }
                },
                {"$sort": {"count": -1}}
            ]
            
            results = list(self.db.employees.aggregate(pipeline))
            for dept in results:
                attrition_rate = (dept['attrition_count'] / dept['count']) * 100
                print(f"\n{dept['_id']}:")
                print(f"  Employees: {dept['count']}")
                print(f"  Avg Income: ${dept['avg_income']:.2f}")
                print(f"  Attrition Rate: {attrition_rate:.1f}%")
                print(f"  Avg Job Satisfaction: {dept['avg_satisfaction']:.2f}")
            
            # Sample employee document
            print("\n--- Sample Employee Document ---")
            sample = self.db.employees.find_one({"employee_number": 1})
            if sample:
                print(f"Employee Number: {sample['employee_number']}")
                print(f"Department: {sample['job_info']['department']}")
                print(f"Role: {sample['job_info']['role']}")
                print(f"Attrition Status: {sample['attrition_info']['status']}")
                print(f"Monthly Income: ${sample['compensation']['monthly_income']}")
            
            # Index information
            print("\n--- Indexes Created ---")
            for index in self.db.employees.list_indexes():
                print(f"  {index['name']}: {index.get('key', {})}")
            
            print("="*60)
            
        except Exception as e:
            logger.error(f"Error verifying data: {e}")
    
    def close_connection(self):
        """Close MongoDB connection"""
        if self.client:
            self.client.close()
            logger.info("MongoDB connection closed")
    
    def run_import(self):
        """Main method to run the complete import process"""
        try:
            # Connect to MongoDB
            self.connect_mongodb()
            
            # Ask user if they want to clean existing data
            response = input("\nDo you want to clean existing data before import? (y/n): ").lower()
            if response == 'y':
                logger.info("Cleaning existing collections...")
                self.clean_collections()
            
            # Create indexes
            logger.info("Creating indexes...")
            self.create_indexes()
            
            # Load CSV data
            logger.info("Loading CSV data...")
            df = self.load_csv_data()
            
            # Insert departments
            logger.info("Inserting department statistics...")
            self.insert_departments(df)
            
            # Insert employees
            logger.info("Inserting employee documents...")
            self.insert_employees(df)
            
            # Verify insertion
            logger.info("Verifying data insertion...")
            self.verify_data()
            
            logger.info("\n✅ MongoDB data import completed successfully!")
            
        except Exception as e:
            logger.error(f"Import failed: {e}")
            raise
        
        finally:
            self.close_connection()


def main():
    """Main execution function"""
    print("=" * 60)
    print("MONGODB DATA IMPORT SCRIPT FOR HR EMPLOYEE ATTRITION")
    print("=" * 60)
    print("\nDataset: IBM HR Analytics Employee Attrition")
    print("Target: MongoDB NoSQL Database")
    print("-" * 60)
    
    # Check if CSV file exists
    if not os.path.exists(CSV_FILE_PATH):
        print(f"\n❌ ERROR: CSV file not found at '{CSV_FILE_PATH}'")
        print("Please download the dataset from Kaggle and place it in the current directory")
        print("URL: https://www.kaggle.com/pavansubhasht/ibm-hr-analytics-attrition-dataset")
        return
    
    # Create importer instance
    importer = MongoDBDataImporter()
    
    try:
        # Run import
        importer.run_import()
    except KeyboardInterrupt:
        print("\n\n⚠️  Import interrupted by user")
    except Exception as e:
        print(f"\n❌ Import failed with error: {e}")
        return
    
    print("\n" + "=" * 60)
    print("MONGODB IMPORT COMPLETED!")
    print("=" * 60)


if __name__ == "__main__":
    main()
