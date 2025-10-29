# Task 1: Database Design for HR Employee Attrition Dataset

## Dataset Information

- **Dataset Name**: IBM HR Analytics Employee Attrition & Performance
- **Source**: Kaggle
- **Purpose**: Predict employee attrition using machine learning
- **Total Columns**: 35 attributes per employee

---

## Part A: MySQL Database Design

### 1. Database Schema

```sql
-- Create Database
CREATE DATABASE IF NOT EXISTS hr_attrition_db;
USE hr_attrition_db;

-- Table 1: EMPLOYEES (Personal Information)
CREATE TABLE employees (
    employee_number INT PRIMARY KEY,
    age INT NOT NULL CHECK (age >= 18 AND age <= 100),
    gender VARCHAR(10) NOT NULL CHECK (gender IN ('Male', 'Female')),
    marital_status VARCHAR(20) NOT NULL CHECK (marital_status IN ('Single', 'Married', 'Divorced')),
    education INT NOT NULL CHECK (education BETWEEN 1 AND 5),
    education_field VARCHAR(50) NOT NULL,
    distance_from_home INT NOT NULL CHECK (distance_from_home >= 0),
    over_18 CHAR(1) NOT NULL CHECK (over_18 IN ('Y', 'N')),
    employee_count INT DEFAULT 1,
    attrition VARCHAR(3) NOT NULL CHECK (attrition IN ('Yes', 'No')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Table 2: DEPARTMENTS
CREATE TABLE departments (
    department_id INT AUTO_INCREMENT PRIMARY KEY,
    department_name VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table 3: JOB_DETAILS (Current Job Information)
CREATE TABLE job_details (
    job_id INT AUTO_INCREMENT PRIMARY KEY,
    employee_number INT NOT NULL,
    department_id INT NOT NULL,
    job_role VARCHAR(100) NOT NULL,
    job_level INT NOT NULL CHECK (job_level BETWEEN 1 AND 5),
    job_involvement INT NOT NULL CHECK (job_involvement BETWEEN 1 AND 4),
    job_satisfaction INT NOT NULL CHECK (job_satisfaction BETWEEN 1 AND 4),
    standard_hours INT DEFAULT 80,
    business_travel VARCHAR(50) NOT NULL CHECK (business_travel IN ('Non-Travel', 'Travel_Rarely', 'Travel_Frequently')),
    overtime VARCHAR(3) NOT NULL CHECK (overtime IN ('Yes', 'No')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (employee_number) REFERENCES employees(employee_number) ON DELETE CASCADE,
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
);

-- Table 4: COMPENSATION (All Pay-Related Data)
CREATE TABLE compensation (
    compensation_id INT AUTO_INCREMENT PRIMARY KEY,
    employee_number INT NOT NULL UNIQUE,
    daily_rate INT NOT NULL CHECK (daily_rate > 0),
    hourly_rate INT NOT NULL CHECK (hourly_rate > 0),
    monthly_income INT NOT NULL CHECK (monthly_income > 0),
    monthly_rate INT NOT NULL CHECK (monthly_rate > 0),
    percent_salary_hike INT NOT NULL CHECK (percent_salary_hike BETWEEN 0 AND 100),
    stock_option_level INT NOT NULL CHECK (stock_option_level BETWEEN 0 AND 3),
    last_salary_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (employee_number) REFERENCES employees(employee_number) ON DELETE CASCADE
);

-- Table 5: PERFORMANCE_METRICS (Experience & Performance)
CREATE TABLE performance_metrics (
    performance_id INT AUTO_INCREMENT PRIMARY KEY,
    employee_number INT NOT NULL UNIQUE,
    performance_rating INT NOT NULL CHECK (performance_rating BETWEEN 1 AND 4),
    years_at_company INT NOT NULL CHECK (years_at_company >= 0),
    years_in_current_role INT NOT NULL CHECK (years_in_current_role >= 0),
    years_since_last_promotion INT NOT NULL CHECK (years_since_last_promotion >= 0),
    years_with_curr_manager INT NOT NULL CHECK (years_with_curr_manager >= 0),
    total_working_years INT NOT NULL CHECK (total_working_years >= 0),
    num_companies_worked INT NOT NULL CHECK (num_companies_worked >= 0),
    training_times_last_year INT NOT NULL CHECK (training_times_last_year >= 0),
    last_evaluation_date DATE DEFAULT (CURRENT_DATE),
    FOREIGN KEY (employee_number) REFERENCES employees(employee_number) ON DELETE CASCADE
);

-- Table 6: SATISFACTION_SCORES (All Satisfaction Metrics)
CREATE TABLE satisfaction_scores (
    satisfaction_id INT AUTO_INCREMENT PRIMARY KEY,
    employee_number INT NOT NULL UNIQUE,
    environment_satisfaction INT NOT NULL CHECK (environment_satisfaction BETWEEN 1 AND 4),
    job_satisfaction INT NOT NULL CHECK (job_satisfaction BETWEEN 1 AND 4),
    relationship_satisfaction INT NOT NULL CHECK (relationship_satisfaction BETWEEN 1 AND 4),
    work_life_balance INT NOT NULL CHECK (work_life_balance BETWEEN 1 AND 4),
    survey_date DATE DEFAULT (CURRENT_DATE),
    FOREIGN KEY (employee_number) REFERENCES employees(employee_number) ON DELETE CASCADE
);

-- Create Indexes for Better Performance
CREATE INDEX idx_employee_attrition ON employees(attrition);
CREATE INDEX idx_job_department ON job_details(department_id);
CREATE INDEX idx_performance_rating ON performance_metrics(performance_rating);
CREATE INDEX idx_satisfaction_employee ON satisfaction_scores(employee_number);
```

### 2. Stored Procedure (MySQL Version)

```sql
-- Drop procedure if exists
DROP PROCEDURE IF EXISTS calculate_attrition_risk;

DELIMITER $$

-- Stored Procedure: Calculate Attrition Risk Score
CREATE PROCEDURE calculate_attrition_risk(IN emp_number INT)
BEGIN
    DECLARE risk_points INT DEFAULT 0;
    DECLARE risk_level VARCHAR(20);
    DECLARE risk_factors TEXT DEFAULT '';
    DECLARE job_sat INT;
    DECLARE env_sat INT;
    DECLARE work_balance INT;
    DECLARE years_no_promo INT;
    DECLARE is_overtime VARCHAR(3);
    DECLARE income_level INT;
    
    -- Get employee satisfaction scores
    SELECT 
        job_satisfaction,
        environment_satisfaction,
        work_life_balance
    INTO job_sat, env_sat, work_balance
    FROM satisfaction_scores
    WHERE employee_number = emp_number;
    
    -- Get performance metrics
    SELECT years_since_last_promotion
    INTO years_no_promo
    FROM performance_metrics
    WHERE employee_number = emp_number;
    
    -- Get job details
    SELECT overtime
    INTO is_overtime
    FROM job_details
    WHERE employee_number = emp_number;
    
    -- Get compensation
    SELECT monthly_income
    INTO income_level
    FROM compensation
    WHERE employee_number = emp_number;
    
    -- Calculate risk based on multiple factors
    IF job_sat <= 2 THEN
        SET risk_points = risk_points + 25;
        SET risk_factors = CONCAT(risk_factors, 'Low Job Satisfaction, ');
    END IF;
    
    IF env_sat <= 2 THEN
        SET risk_points = risk_points + 20;
        SET risk_factors = CONCAT(risk_factors, 'Low Environment Satisfaction, ');
    END IF;
    
    IF work_balance <= 2 THEN
        SET risk_points = risk_points + 20;
        SET risk_factors = CONCAT(risk_factors, 'Poor Work-Life Balance, ');
    END IF;
    
    IF years_no_promo >= 5 THEN
        SET risk_points = risk_points + 15;
        SET risk_factors = CONCAT(risk_factors, 'Long Time Without Promotion, ');
    END IF;
    
    IF is_overtime = 'Yes' THEN
        SET risk_points = risk_points + 10;
        SET risk_factors = CONCAT(risk_factors, 'Frequent Overtime, ');
    END IF;
    
    IF income_level < 3000 THEN
        SET risk_points = risk_points + 10;
        SET risk_factors = CONCAT(risk_factors, 'Below Average Income, ');
    END IF;
    
    -- Determine risk level
    IF risk_points >= 60 THEN
        SET risk_level = 'HIGH';
    ELSEIF risk_points >= 30 THEN
        SET risk_level = 'MEDIUM';
    ELSE
        SET risk_level = 'LOW';
    END IF;
    
    -- Remove trailing comma and space
    IF LENGTH(risk_factors) > 2 THEN
        SET risk_factors = SUBSTRING(risk_factors, 1, LENGTH(risk_factors) - 2);
    END IF;
    
    -- Return results
    SELECT 
        emp_number AS employee_id,
        risk_points AS risk_score,
        risk_level,
        risk_factors;
END$$

DELIMITER ;
```

### 3. Trigger (MySQL Version)

```sql
-- Drop trigger if exists
DROP TRIGGER IF EXISTS log_salary_changes;

DELIMITER $$

-- Trigger: Log Salary Changes
CREATE TRIGGER update_salary_timestamp
BEFORE UPDATE ON compensation
FOR EACH ROW
BEGIN
    -- Update the last_salary_update timestamp when salary changes
    IF NEW.monthly_income != OLD.monthly_income THEN
        SET NEW.last_salary_update = CURRENT_TIMESTAMP;
    END IF;
END$$

DELIMITER ;

-- Additional Trigger: Update employee timestamp
DROP TRIGGER IF EXISTS update_employee_timestamp;

DELIMITER $$

CREATE TRIGGER update_employee_timestamp
BEFORE UPDATE ON employees
FOR EACH ROW
BEGIN
    SET NEW.updated_at = CURRENT_TIMESTAMP;
END$$

DELIMITER ;
```

---