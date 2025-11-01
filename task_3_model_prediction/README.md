# Task 3: Model Prediction Pipeline

This task implements a complete machine learning prediction pipeline that:
1. Trains a linear regression model on the HR Employee Attrition dataset
2. Fetches the latest employee entry from the API
3. Preprocesses the data for prediction
4. Makes predictions using the trained model
5. Logs prediction results to the database

---

## 📁 Directory Structure

```
task_3_model_prediction/
├── train_linear_regression_model.ipynb    # Training notebook
├── predict_employee_income.ipynb           # Prediction notebook
├── models/                                 # Saved models and preprocessing tools
│   ├── employee_income_model.joblib       # Trained model
│   ├── employee_income_scaler.joblib      # Feature scaler
│   ├── feature_names.json                  # Feature names
│   └── label_encoders.joblib              # Label encoders for categorical variables
├── requirements.txt                       # Python dependencies
└── README.md                              # This file
```

---

## 🚀 Getting Started

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Train the Model

Open and run `train_linear_regression_model.ipynb` cell by cell. This notebook will:
- Load the HR Employee Attrition dataset (`../hr_employee_attrition.csv`)
- Preprocess the data (handle missing values, encode categorical variables)
- Train a linear regression model to predict **MonthlyIncome**
- Evaluate the model performance
- Save the model and preprocessing tools to the `models/` directory

**Expected Output:**
- Model files saved in `models/` directory
- Evaluation metrics (MSE, RMSE, MAE, R² Score)
- Visualization of predictions vs actual values

### 3. Make Predictions

Open and run `predict_employee_income.ipynb` cell by cell. This notebook will:
- Fetch the latest employee entry from the API (must be running)
- Preprocess the employee data
- Load the trained model
- Make a prediction for the employee's monthly income
- Log the prediction results to the database

**Prerequisites:**
- The API server must be running (`task_2_api`)
- The model must be trained first (step 2)
- Database connection configured (uses `.env` from `task_2_api`)

---

## 📊 Model Details

### Target Variable
- **MonthlyIncome**: The monthly income of the employee (continuous variable)

### Features Used
The model uses all available features from the HR Employee Attrition dataset except:
- `EmployeeNumber` (ID column)
- `EmployeeCount` (constant)
- `Over18` (constant)
- `StandardHours` (constant)
- `MonthlyIncome` (target variable)

### Model Type
- **Linear Regression** (from scikit-learn)

### Preprocessing Steps
1. **Missing Data Handling**: Fill missing numeric values with median, categorical with mode
2. **Categorical Encoding**: Label encoding for all categorical variables
3. **Feature Scaling**: MinMaxScaler to scale features between 0 and 1

---

## 🔄 Prediction Pipeline

The prediction pipeline (`predict_employee_income.ipynb`) performs the following steps:

### Step 1: Fetch Latest Employee Entry
- Connects to the API at `https://ml.bwenge.rw/mysql/employees/latest/entry`
- Handles connection errors gracefully

### Step 2: Handle Missing Data
- Maps API employee data to model feature format
- Fills missing fields with default values from the original dataset
- Ensures all required features are present

### Step 3: Preprocess Input Data
- Encodes categorical variables using saved label encoders
- Scales features using the saved scaler
- Prepares data in the exact format expected by the model

### Step 4: Make Predictions
- Loads the trained linear regression model
- Makes prediction on the preprocessed employee data
- Displays prediction results

### Step 5: Log Results to Database
- Creates a `predictions` table in MySQL (if it doesn't exist)
- Logs the prediction with:
  - Employee number
  - Predicted monthly income
  - Prediction timestamp
  - Input features used
  - Model version

---

## 📋 Database Schema

The prediction results are stored in a `predictions` table:

```sql
CREATE TABLE predictions (
    prediction_id INT AUTO_INCREMENT PRIMARY KEY,
    employee_number INT NOT NULL,
    predicted_monthly_income FLOAT NOT NULL,
    prediction_date DATETIME NOT NULL,
    input_features TEXT,
    model_version VARCHAR(50) DEFAULT 'v1.0',
    FOREIGN KEY (employee_number) REFERENCES employees(employee_number)
);
```

---

## 🔧 Configuration

### API Configuration
Update the API base URL in `predict_employee_income.ipynb` if your API runs on a different host:
```python
API_BASE_URL = "https://ml.bwenge.rw"
```

### Database Configuration
The prediction script uses the same database configuration as `task_2_api`. Ensure you have a `.env` file in `task_2_api/` with:
```
MYSQL_USER=your_user
MYSQL_PASSWORD=your_password
MYSQL_HOST=host
MYSQL_PORT=3306
MYSQL_DATABASE=hr_attrition_db
```

---

## 📝 Usage Example

### Training the Model

1. Start Jupyter Notebook:
```bash
jupyter notebook
```

2. Open `train_linear_regression_model.ipynb`

3. Run all cells sequentially

4. Verify that model files are created in `models/` directory

### Making Predictions

1. Start the API server:
```bash
cd ../task_2_api
uvicorn main:app --reload
```

2. Open `predict_employee_income.ipynb` in Jupyter

3. Run all cells sequentially

4. Check the predictions table in the database for logged results

---

## 📈 Model Evaluation

After training, the model provides:
- **MSE (Mean Squared Error)**: Average squared difference between predicted and actual values
- **RMSE (Root Mean Squared Error)**: Square root of MSE, in the same units as the target
- **MAE (Mean Absolute Error)**: Average absolute difference
- **R² Score**: Coefficient of determination (higher is better, max 1.0)

---

## ⚠️ Troubleshooting

### Model Not Found
- **Error**: `FileNotFoundError: models/employee_income_model.joblib`
- **Solution**: Run `train_linear_regression_model.ipynb` first to create the model files

### API Connection Error
- **Error**: `ConnectionError: Could not connect to API`
- **Solution**: Ensure the API server is running on `https://ml.bwenge.rw` or `http://localhost:8000`

### Database Connection Error
- **Error**: `Error connecting to database`
- **Solution**: 
  - Check database credentials in `.env` file
  - Ensure MySQL server is running
  - Verify database exists

### Missing Features Error
- **Error**: `KeyError: 'FeatureName'`
- **Solution**: The preprocessing function handles missing features by using default values from the training dataset

---

## 🎯 Future Improvements

- [ ] Add support for batch predictions
- [ ] Implement model versioning
- [ ] Add prediction confidence intervals
- [ ] Create API endpoint for predictions
- [ ] Add prediction history visualization
- [ ] Implement model retraining pipeline
- [ ] Add prediction validation and monitoring

---

## 📚 References

- Scikit-learn Linear Regression: https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html
- Joblib for model persistence: https://joblib.readthedocs.io/
- FastAPI documentation: https://fastapi.tiangolo.com/

---

## ✅ Checklist

Before running predictions:
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Model trained (`train_linear_regression_model.ipynb` completed)
- [ ] Model files present in `models/` directory
- [ ] API server running (`cd task_2_api && uvicorn main:app --reload`)
- [ ] Database configured and accessible
- [ ] At least one employee entry exists in the database

