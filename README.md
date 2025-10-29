# HR Employee Attrition Prediction Pipeline

A comprehensive machine learning pipeline for predicting employee attrition using IBM HR Analytics dataset. This project implements a full-stack solution with dual database systems (MySQL and MongoDB), API endpoints, and ML prediction capabilities.

---

## 🎯 Project Overview

This project aims to build an end-to-end machine learning pipeline that:

- Stores HR employee data in both SQL (MySQL) and NoSQL (MongoDB) databases
- Provides RESTful APIs for data operations (CRUD)
- Implements ML models for attrition prediction

### Key Features

- **Dual Database Implementation**: MySQL (normalized) and MongoDB (document-based)
- **Data Validation**: Constraints, triggers, and validation schemas
- **Risk Assessment**: Stored procedures for calculating attrition risk
- **Python Import Scripts**: Automated data loading from CSV
- **Comprehensive Documentation**: Detailed design and implementation guides

---

## 📊 Dataset Information

- **Name**: IBM HR Analytics Employee Attrition & Performance
- **Source**: Kaggle
- **Records**: 1,470 employees
- **Features**: 35 attributes including:
  - Personal information (age, gender, education, marital status)
  - Job details (role, department, level, satisfaction)
  - Compensation (salary, stock options, benefits)
  - Performance metrics (years at company, promotions, training)
  - Target variable: Attrition (Yes/No)

---

## 📚 Tasks Overview

### Task 1: Database Design

Implementation of dual database systems (MySQL and MongoDB) with complete schema design, stored procedures, triggers, and automated data import scripts.

**📖 [View Task 1 Documentation](./task_1_database_in_sql_and_mongo/README.md)**

#### Database Schema (ERD)

```mermaid
erDiagram
    EMPLOYEES ||--o{ JOB_DETAILS : "has"
    EMPLOYEES ||--|| COMPENSATION : "has"
    EMPLOYEES ||--|| PERFORMANCE_METRICS : "has"
    EMPLOYEES ||--|| SATISFACTION_SCORES : "has"
    DEPARTMENTS ||--o{ JOB_DETAILS : "contains"

    EMPLOYEES {
        int employee_number PK
        int age
        varchar gender
        varchar marital_status
        int education
        varchar education_field
        int distance_from_home
        char over_18
        int employee_count
        varchar attrition
        timestamp created_at
        timestamp updated_at
    }

    DEPARTMENTS {
        int department_id PK
        varchar department_name UK
        timestamp created_at
    }

    JOB_DETAILS {
        int job_id PK
        int employee_number FK
        int department_id FK
        varchar job_role
        int job_level
        int job_involvement
        int job_satisfaction
        int standard_hours
        varchar business_travel
        varchar overtime
        timestamp created_at
    }

    COMPENSATION {
        int compensation_id PK
        int employee_number FK "UNIQUE"
        int daily_rate
        int hourly_rate
        int monthly_income
        int monthly_rate
        int percent_salary_hike
        int stock_option_level
        timestamp last_salary_update
    }

    PERFORMANCE_METRICS {
        int performance_id PK
        int employee_number FK "UNIQUE"
        int performance_rating
        int years_at_company
        int years_in_current_role
        int years_since_last_promotion
        int years_with_curr_manager
        int total_working_years
        int num_companies_worked
        int training_times_last_year
        date last_evaluation_date
    }

    SATISFACTION_SCORES {
        int satisfaction_id PK
        int employee_number FK "UNIQUE"
        int environment_satisfaction
        int job_satisfaction
        int relationship_satisfaction
        int work_life_balance
        date survey_date
    }
```

**Key Tables:**

- **6 normalized tables** for MySQL implementation
- **3 collections** for MongoDB implementation
- **Stored procedures** for attrition risk calculation
- **Triggers** for automatic timestamp updates

### Task 2: API Development

RESTful API endpoints for CRUD operations on employee data with deployment.

### Task 3: ML Model Development

Machine learning models for predicting employee attrition.

---

### Installation

```bash
# Clone the repository
git clone https://github.com/izabayo7/database-prediction-pipeline.git
cd database-prediction-pipeline

# Set up Python environment
source .venv/bin/activate  # On macOS/Linux

```

---

## 🤝 Contributing

Each task has its own folder with dedicated documentation. When contributing:

1. Work in your assigned task folder
2. Create a README.md in your task folder with setup instructions
3. Follow the snake_case naming convention for folders
4. Update this main README with a link to your task's documentation

---

## 👥 Team

### Contributors

| Name               | GitHub                                               | Role                         |
| ------------------ | ---------------------------------------------------- | ---------------------------- |
| Cedric Izabayo     | [@izabayo7](https://github.com/izabayo7)             | Task 1: Database Design      |
| Peace Keza         | [@Peace3B](https://github.com/Peace3B)               | Task 1: Database Design      |
| Denyse Mutoni      | [@dmutoni](https://github.com/dmutoni)               | Task 2: API Development      |
| Patrick Niyogitare | [@thepatrickniyo](https://github.com/thepatrickniyo) | Task 3: ML Model Development |

---

## 📝 License

This project is part of an academic assignment at ALU (African Leadership University).

---

## 🔗 Resources

- [Kaggle Dataset](https://www.kaggle.com/datasets/pavansubhasht/ibm-hr-analytics-attrition-dataset)
- [MySQL Documentation](https://dev.mysql.com/doc/)
- [MongoDB Documentation](https://docs.mongodb.com/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)

---

**Happy Coding! 🚀**
