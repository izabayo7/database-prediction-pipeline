# Database Prediction Pipeline API

## Overview
This project is a **FastAPI-based RESTful API** that connects to both **MySQL** and **MongoDB** databases.  
It provides unified CRUD operations for managing HR data — specifically:
- Employees  
- Departments  
- Job Details  

The API supports both SQL and NoSQL storage layers and is designed for flexibility and scalability.

---

## 🚀 Features
- Dual-database support:
  - `/mysql/...` → endpoints for MySQL
  - `/mongo/...` → endpoints for MongoDB
- Clean modular architecture (routers, CRUD, schemas separated)
- Swagger auto-documentation via FastAPI
- Consistent Pydantic v2 models with JSON schema examples
- Environment-based DB configuration
- ObjectId support for MongoDB
- Filters and pagination on GET endpoints

---

## 📁 Project Structure

```
task_2_api/
│
├── main.py # App entry point
├── database.py # MySQL connection
├── mongo_database.py # MongoDB connection
│
├── mysql_crud/ # CRUD logic for MySQL
│ ├── employees_crud.py
│ ├── departments_crud.py
│ └── job_details_crud.py
│
├── mongodb_crud/ # CRUD logic for MongoDB
│ ├── employees_crud.py
│ ├── departments_crud.py
│ └── job_details_crud.py
│
├── mysql_routers/ # MySQL API routes
│ ├── employees_router.py
│ ├── departments_router.py
│ └── job_details_router.py
│
├── mongodb_routers/ # MongoDB API routes
│ ├── employees_router.py
│ ├── departments_router.py
│ └── job_details_router.py
│
├── mongodb_schemas.py # Pydantic models (v2)
└── requirements.txt
```

## ⚙️ Setup Instructions

### 1️⃣ Clone the repository
```bash
git clone https://github.com/your-username/database-prediction-pipeline.git
cd database-prediction-pipeline

### 2️⃣ Create a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```
### 3️⃣ Install dependencies
```bash
pip install -r requirements.txt
``` 

### 4️⃣ Configure databases
- Set up your MySQL and MongoDB databases.
- Update connection settings in `database.py` and `mongo_database.py`.
- Ensure the necessary tables/collections are created.
- (Optional) Seed initial data if needed.
- ### 5️⃣ Run the FastAPI server
```bash
uvicorn task_2_api.main:app --reload
```
### 6️⃣ Access the API
- Open your browser and navigate to `http://localhost:8000/docs` for the Swagger UI.
- Explore and test the API endpoints for both MySQL and MongoDB.
- ### 7️⃣ API Endpoints
- **MySQL Endpoints**:
  - Employees: `/mysql/employees`
  - Departments: `/mysql/departments`
  - Job Details: `/mysql/job_details`       
- **MongoDB Endpoints**:
  - Employees: `/mongo/employees`
  - Departments: `/mongo/departments`
  - Job Details: `/mongo/job_details`   
- ## 🛠️ Customization
- Modify Pydantic models in `mongodb_schemas.py` to fit your data structure.
- Extend CRUD operations in the respective `*_crud.py` files.
- Add new routes in the `*_routers` directories as needed.
- ## Architecture Diagram
          ┌────────────────────────────┐
          │        FastAPI API         │
          │    (task_2_api/main.py)    │
          └────────────┬───────────────┘
                       │
        ┌──────────────┼──────────────┐
        │                             │
┌──────────────┐              ┌────────────────┐
│   MySQL DB   │              │   MongoDB DB   │
│ (SQL tables) │              │ (NoSQL docs)   │
└──────────────┘              └────────────────┘
        │                             │
        ▼                             ▼
  CRUD via SQLAlchemy          CRUD via PyMongo

- ## 🤝 Contributing
- Fork the repository.
- Create a new branch for your feature or bugfix.
- Commit your changes with clear messages.
- Push to your fork and open a pull request.
- ## 📄 License
- This project is licensed under the MIT License. See the `LICENSE` file for details.
- Thank you for using the Database Prediction Pipeline API!
- Happy coding!
- 
