from fastapi import FastAPI
from .mysql_routers import employees_router, departments_router, job_details_router
from .mongo_routers import mongo_router

app = FastAPI(
    title="Employee Attrition API",
    description="CRUD operations for employees, departments, and job details",
)

app.include_router(employees_router.router)
app.include_router(departments_router.router)
app.include_router(job_details_router.router)
app.include_router(mongo_router.router)


