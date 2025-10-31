from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from bson import ObjectId

# ✅ Pydantic v2-compatible ObjectId type
class PyObjectId(str):
    @classmethod
    def __get_pydantic_core_schema__(cls, _source_type, _handler):
        from pydantic_core import core_schema
        # define how Pydantic should validate ObjectId
        return core_schema.no_info_after_validator_function(
            cls.validate, core_schema.str_schema()
        )

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return str(v)

# ✅ Employee Base Model
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
class Employee(EmployeeBase):
    id: Optional[PyObjectId] = Field(default=None, alias="_id")

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str}
    )
