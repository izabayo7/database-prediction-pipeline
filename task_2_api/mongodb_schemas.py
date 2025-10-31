from datetime import datetime
from typing import Optional, Dict
from bson import ObjectId
from pydantic import BaseModel, Field, ConfigDict

class PyObjectId(str):
    @classmethod
    def __get_pydantic_core_schema__(cls, _source_type, _handler):
        from pydantic_core import core_schema
        return core_schema.no_info_after_validator_function(
            cls.validate, core_schema.str_schema()
        )

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return str(v)


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

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "age": 34,
                "gender": "Female",
                "marital_status": "Single",
                "education": 3,
                "education_field": "Life Sciences",
                "distance_from_home": 12,
                "over_18": "Y",
                "employee_count": 1,
                "attrition": "No",
                "department_name": "Development",
                "job_satisfaction": 4,
            }
        }
    )


class EmployeeCreate(EmployeeBase):
    """Used for POST (creating employees)."""
    pass


class Employee(EmployeeBase):
    """Used for GET/PUT (returning or updating employees)."""
    id: Optional[PyObjectId] = Field(default=None, alias="_id")

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
    )

class DepartmentBase(BaseModel):
    department_name: str
    employee_count: int
    attrition_count: int
    avg_attrition_rate: float
    avg_satisfaction: Dict[str, float] = Field(
        ...,
        example={
            "job": 2.75,
            "environment": 2.68,
            "relationship": 2.7,
            "work_life_balance": 2.82
        },
        description="Average satisfaction scores by category"
    )
    avg_monthly_income: float = Field(
        ...,
        example=6959.17,
        description="Average monthly income of employees in the department"
    )
    last_updated: Optional[datetime] = Field(
        default_factory=datetime.utcnow,
        description="Timestamp of the last update"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "department_name": "Sales",
                "employee_count": 446,
                "attrition_count": 92,
                "avg_attrition_rate": 0.206,
                "avg_satisfaction": {
                    "job": 2.75,
                    "environment": 2.68,
                    "relationship": 2.7,
                    "work_life_balance": 2.82
                },
                "avg_monthly_income": 6959.17,
                "last_updated": "2025-10-30T12:00:00Z"
            }
        }
    )


class DepartmentCreate(DepartmentBase):
    """Used for POST (creating departments)."""
    pass


class Department(DepartmentBase):
    """Used for GET/PUT (returning or updating departments)."""
    department_id: Optional[str] = Field(default=None, alias="_id")

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
    )


# JOB DETAILS MODELS

class JobDetailBase(BaseModel):
    employee_id: PyObjectId = Field(..., description="MongoDB ID of the employee")
    department_id: Optional[PyObjectId] = Field(None, description="MongoDB ID of the department")
    job_role: str
    job_level: int
    job_satisfaction: Optional[int] = Field(3, ge=1, le=5, description="Job satisfaction rating (1–5)")
    job_involvement: Optional[int] = Field(3, ge=1, le=5, description="Job involvement rating (1–5)")
    business_travel: Optional[str] = Field("Travel_Rarely", description="Travel frequency for the job")
    overtime: Optional[str] = Field("No", description="Whether the employee works overtime")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "employee_id": "6904ac56d9c49407108d277e",
                "department_id": "69025c53ee15d86054db580d",
                "job_role": "Software Engineer",
                "job_level": 2,
                "job_satisfaction": 4,
                "job_involvement": 3,
                "business_travel": "Travel_Rarely",
                "overtime": "No"
            }
        }
    )


class JobDetailCreate(JobDetailBase):
    """Used for POST (creating job details)."""
    pass


class JobDetail(JobDetailBase):
    """Used for GET/PUT (returning job details)."""
    job_id: Optional[PyObjectId] = Field(default=None, alias="_id")

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str}
    )