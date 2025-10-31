from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)


# =========================
# Employee
# =========================
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


class Employee(EmployeeBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


# =========================
# Department
# =========================
class DepartmentBase(BaseModel):
    department_name: str


class Department(DepartmentBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


# =========================
# JobDetail
# =========================
class JobDetailBase(BaseModel):
    employee_id: str
    department_id: Optional[str] = None
    job_role: str
    job_level: int
    job_satisfaction: Optional[int] = 3
    job_involvement: Optional[int] = 3
    business_travel: Optional[str] = "Travel_Rarely"
    overtime: Optional[str] = "No"


class JobDetail(JobDetailBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
