from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


class Employee(Base):
    __tablename__ = "employees"

    employee_number = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String(10), nullable=False)
    marital_status = Column(String(20), nullable=False)
    education = Column(Integer, nullable=False)
    education_field = Column(String(50), nullable=False)
    distance_from_home = Column(Integer, nullable=False)
    over_18 = Column(String(1), nullable=False)
    employee_count = Column(Integer, nullable=False, default=1)
    attrition = Column(String(3), nullable=False)

    job_details = relationship(
        "JobDetail",
        back_populates="employee",
        uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True,
        lazy="joined",  # helps prefetch related record
    )


class Department(Base):
    __tablename__ = "departments"

    department_id = Column(Integer, primary_key=True, index=True)
    department_name = Column(String(100), unique=True, nullable=False)


class JobDetail(Base):
    __tablename__ = "job_details"

    job_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    employee_number = Column(
        Integer,
        ForeignKey("employees.employee_number", ondelete="CASCADE"),
        nullable=False,
    )
    department_id = Column(
        Integer,
        ForeignKey("departments.department_id", ondelete="SET NULL"),
        nullable=True,
    )
    job_role = Column(String(100))
    job_level = Column(Integer)
    job_satisfaction = Column(Integer, nullable=True, default=3) 
    job_involvement = Column(Integer, nullable=True, default=3)
    business_travel = Column(String(50), nullable=True, default="Travel_Rarely")
    employee = relationship("Employee", back_populates="job_details", lazy="joined")
    overtime = Column(String(3), nullable=True, default="No") 
