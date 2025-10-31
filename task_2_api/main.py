from fastapi import FastAPI
from .mysql_routers import employees_router, departments_router, job_details_router 
from .mongo_routers import mongo_departments_router, mongo_employees_router, mongo_job_details_router, mongo_predictions_router
# from mongo_database import mongo_db

app = FastAPI(
    title="Employee Attrition API",
    description="CRUD operations for employees, departments, job details, and predictions",
)

app.include_router(employees_router.router)
app.include_router(departments_router.router)
app.include_router(job_details_router.router)
app.include_router(mongo_departments_router.router)
app.include_router(mongo_employees_router.router)
app.include_router(mongo_job_details_router.router)
app.include_router(mongo_predictions_router.router)




