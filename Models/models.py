from utils.db import db
from datetime import date
import json


class Contract(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    start_date = db.Column(db.Date, default=date.today)
    end_date = db.Column(db.Date, nullable=True)

    state = db.Column(db.String(10), default="active")
    salary = db.Column(db.String(250), nullable=False)

    employee_id = db.Column(db.Integer, db.ForeignKey("employee.id"))
    project_id = db.Column(db.Integer, db.ForeignKey("project.id"))

    def __init__(self, salary, employee_id, project_id):
        self.salary = salary
        self.employee_id = employee_id
        self.project_id = project_id

    def to_json(self):
        return {
            'id': self.id,
            'start_date': str(self.start_date),
            'end_date': str(self.end_date),
            'salary': self.salary,
            'state': self.state,
            'employee_id': self.employee_id,
            'project_id': self.project_id,
            'project': self.project
        }

    @property
    def project(self):
        project = Project.query.get(self.project_id)
        return project.to_json()


class Employee(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    rut = db.Column(db.String(250))
    name = db.Column(db.String(250))

    contracts = db.relationship("Contract")

    def __init__(self, rut, name):
        self.rut = rut
        self.name = name

    def to_json(self):
        contracts = [c.to_json() for c in self.contracts]
        return {
            'id': self.id,
            'rut': self.rut,
            'name': self.name,
            'contracts': contracts,
            'total_salary': self.total_salary,
            'active_contracts': self.active_contracts
        }

    @property
    def total_salary(self):
        return sum([int(c["salary"]) for c in self.active_contracts])

    @property
    def active_contracts(self):
        return [c.to_json() for c in self.contracts if c.state == "active"]


class Project(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(250), unique=True)

    contracts = db.relationship("Contract")

    def __init__(self, name):
        self.name = name

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name
        }

    @staticmethod
    def from_string(serialized_project: str) -> object:
        json_dct = json.loads(serialized_project)
        return Project(name=json_dct['Name'])
