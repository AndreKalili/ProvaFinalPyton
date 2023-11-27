from fastapi import FastAPI
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy import Float
from datetime import datetime

app = FastAPI()

engine = create_engine('postgresql://postgres:root@localhost:6700/postgres')

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()

Base = declarative_base()

class Department(Base):
    __tablename__ = 'Department'

    DepartmentID = Column(Integer, primary_key=True)
    name = Column(String(255))
    region = Column(String(255))

class Employee(Base):
    __tablename__ = 'Employee'

    EmployeeID = Column(Integer, primary_key=True)
    name = Column(String(255))
    departmentID = Column(Integer, ForeignKey('Department.DepartmentID', ondelete='CASCADE'))
    department = relationship("Department", backref="employees")
    Birthday = Column(String(15))
    salary = Column(Float)
    Job = Column(String(255))

class JobHistory(Base):
    __tablename__ = 'JobHistory'

    JobHistoryID = Column(Integer, primary_key=True)
    EmployeeID = Column(Integer, ForeignKey('Employee.EmployeeID', ondelete='CASCADE')) 
    employee = relationship("Employee", backref="jobhistory")
    Job = Column(String(255))
    StartDate = Column(String(255), default="")
    EndDate = Column(String(255), default="")
    Title = Column(String(255))


Base.metadata.create_all(bind=engine)

@app.post("/Departments")
def create_Department(name: str, region: str):
    department = Department(name=name, region=region)
    session.add(department)
    session.commit()

    return JSONResponse(content={'id': department.DepartmentID, 'name': department.name, 'region': department.region})

@app.put("/Departments")
def put_Department(id: int, name: str, region: str):
    department = session.query(Department).filter(Department.DepartmentID == id).first()
    if department:
        department.name = name
        department.region = region
        session.commit()

    return JSONResponse(content={'id': department.DepartmentID, 'name': department.name, 'region': department.region})
    

@app.get("/Departments")
def get_Department():
    departments = session.query(Department).all()
    return JSONResponse(content=[{'id': department.DepartmentID, 'name': department.name, 'region': department.region} for department in departments])

@app.get("/DepartmentsAndEmployeesandjobhistory")
def get_DepartmentAndEmployeesandjobhistory():
    departments = session.query(Department).all()
    return JSONResponse(content=[{
        'id': department.DepartmentID,
        'name': department.name,
        'region': department.region,
        'employees': [{
            'id': employee.EmployeeID,
            'name': employee.name,
            'departmentID': employee.departmentID,
            'Birthday': employee.Birthday,
            'salary': employee.salary,
            'Job': employee.Job,
            'jobhistory': [{
                'id': jobhistory.JobHistoryID,
                'EmployeeID': jobhistory.EmployeeID,
                'Job': jobhistory.Job,
                'StartDate': jobhistory.StartDate,
                'EndDate': jobhistory.EndDate,
                'Title': jobhistory.Title
            } for jobhistory in employee.jobhistory]
        } for employee in department.employees]
    } for department in departments])

@app.delete("/Departments")
def delete_Department(id: int):
    department = session.query(Department).filter(Department.DepartmentID == id).first()
    session.delete(department)
    session.commit()

    return JSONResponse(content={'id': department.DepartmentID, 'name': department.name, 'region': department.region})

@app.post("/Employees")
def create_Employee(name: str, departmentID: int, Birthday: str, salary: float, Job: str):
    employee = Employee(name=name, departmentID=departmentID, Birthday=Birthday, salary=salary, Job=Job)
    session.add(employee)
    session.commit()

    return JSONResponse(content={'id': employee.EmployeeID, 'name': employee.name, 'departmentID': employee.departmentID, 'Birthday': employee.Birthday, 'salary': employee.salary, 'Job': employee.Job})

@app.put("/Employees")
def put_Employee(id: int, name: str, departmentID: int, Birthday: str, salary: float, Job: str):
    employee = session.query(Employee).filter(Employee.EmployeeID == id).first()
    if employee:
        employee.name = name
        employee.departmentID = departmentID
        employee.Birthday = Birthday
        employee.salary = salary
        employee.Job = Job
        session.commit()

        return JSONResponse(content={'id': employee.EmployeeID, 'name': employee.name, 'departmentID': employee.departmentID, 'Birthday': employee.Birthday, 'salary': employee.salary, 'Job': employee.Job})
    
@app.get("/Employees")    
def get_Employee():
    employees = session.query(Employee).all()

    return JSONResponse(content=[{'id': employee.EmployeeID, 'name': employee.name, 'departmentID': employee.departmentID, 'Birthday': employee.Birthday, 'salary': employee.salary, 'Job': employee.Job} for employee in employees])

@app.delete("/Employees")
def delete_Employee(id: int):
    employee = session.query(Employee).filter(Employee.EmployeeID == id).first()
    session.delete(employee)
    session.commit()

    return JSONResponse(content={'id': employee.EmployeeID, 'name': employee.name, 'departmentID': employee.departmentID, 'Birthday': employee.Birthday, 'salary': employee.salary, 'Job': employee.Job})

@app.post("/JobHistorys")
def create_JobHistory(EmployeeID: int, Job: str, StartDate: str, EndDate: str, Title: str):
    jobhistory = JobHistory(EmployeeID=EmployeeID, Job=Job, StartDate=StartDate, EndDate=EndDate, Title=Title)
    session.add(jobhistory)
    session.commit()

    return JSONResponse(content={'id': jobhistory.JobHistoryID, 'EmployeeID': jobhistory.EmployeeID, 'Job': jobhistory.Job, 'StartDate': jobhistory.StartDate, 'EndDate': jobhistory.EndDate, 'Title': jobhistory.Title})

@app.put("/JobHistorys")
def put_JobHistory(id: int, EmployeeID: int, Job: str, StartDate: str, EndDate: str, Title: str):
    jobhistory = session.query(JobHistory).filter(JobHistory.JobHistoryID == id).first()

    if jobhistory:
        jobhistory.EmployeeID = EmployeeID
        jobhistory.Job = Job
        jobhistory.StartDate = StartDate
        jobhistory.EndDate = EndDate
        jobhistory.Title = Title
        session.commit()

        return JSONResponse(content={'id': jobhistory.JobHistoryID, 'EmployeeID': jobhistory.EmployeeID, 'Job': jobhistory.Job, 'StartDate': jobhistory.StartDate, 'EndDate': jobhistory.EndDate, 'Title': jobhistory.Title})
    
    return JSONResponse(content={'error': 'JobHistory not found'})

@app.get("/JobHistorysandEmployees")
def get_JobHistorysandEmployees():
    jobhistorys = session.query(JobHistory).all()

    return JSONResponse(content=[{'id': jobhistory.JobHistoryID, 'EmployeeID': jobhistory.EmployeeID, 'Job': jobhistory.Job, 'StartDate': jobhistory.StartDate, 'EndDate': jobhistory.EndDate, 'Title': jobhistory.Title} for jobhistory in jobhistorys])

@app.delete("/JobHistorys")
def delete_JobHistory(id: int):
    jobhistory = session.query(JobHistory).filter(JobHistory.JobHistoryID == id).first()
    session.delete(jobhistory)
    session.commit()

    return JSONResponse(content={'id': jobhistory.JobHistoryID, 'EmployeeID': jobhistory.EmployeeID, 'Job': jobhistory.Job, 'StartDate': jobhistory.StartDate, 'EndDate': jobhistory.EndDate, 'Title': jobhistory.Title})

