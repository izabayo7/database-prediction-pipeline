from sqlalchemy import Integer
from pydantic import BaseModel
from typing import Optional 

class EmployeeBase(BaseModel):
    age: int
    gender: str
    marital_status: str
    education: int
    education_field: str
    distance_from_home: int
    over_18: str
    employee_count: int
    attrition: str
    department_name: Optional[str] = None
    job_satisfaction: Optional[int] = 3
    # job_involvement: Optional[int] = 3

class EmployeeCreate(EmployeeBase):
    pass

class Employee(EmployeeBase):
    employee_number: int
    class Config:
        from_attributes = True

# ---------------------------
# Department Schemas
# ---------------------------

class DepartmentBase(BaseModel):
    department_name: str

class DepartmentCreate(DepartmentBase):
    pass

class Department(DepartmentBase):
    department_id: int

    class Config:
        orm_mode = True


# ---------------------------
# JobDetail Schemas
# ---------------------------
class JobDetailBase(BaseModel):
    job_role: str
    job_level: int
    job_satisfaction: Optional[int] = None
    job_involvement: Optional[int] = None
    business_travel: Optional[str] = None
    overtime: Optional[str] = None

class JobDetailCreate(JobDetailBase):
    employee_number: int
    department_id: int

class JobDetail(JobDetailBase):
    job_id: int
    employee_number: int
    department_id: int

    class Config:
        orm_mode = True
