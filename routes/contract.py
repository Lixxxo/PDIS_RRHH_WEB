from utils.db import db
from datetime import date
from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.models import Contract, Employee, Project
contracts = Blueprint('contracts', __name__)


@contracts.route("/contracts/<employee_id>", methods=["GET"])
def index(employee_id):
    employee = Employee.query.get(employee_id)
    projects = Project.query.all()
    return render_template("contracts.html", employee=employee.to_json(), projects=projects)


@contracts.route("/contracts/hire/", methods=["POST", "GET"])
def hire():

    if request.method == 'POST':

        employee_id = request.form.get("employee_id")
        employee = Employee.query.get(employee_id)
        if not employee:
            return redirect(url_for('/'))

        project_id = request.form.get("project_id")
        project = Project.query.get(project_id)
        if not project:
            flash("No hay proyectos.", "warning")
            return redirect(url_for("contracts.index", employee_id=employee_id))

        # que que no haya mas de un contracto activo
        # en el mismo proyecto

        active_projects = Contract.query.filter_by(project_id=project_id, employee_id=employee_id, state="active")
        if active_projects.first():
            projects = [c.project for c in active_projects]
            flash(f"{employee.name} ya cuenta con un contrato activo en {projects[0]['name']}", 'warning')
            return redirect(url_for("contracts.index", employee_id=employee.id))

        new_contract = Contract(
            salary=request.form.get("salary"),
            project_id=project_id,
            employee_id=employee_id
        )

        db.session.add(new_contract)
        db.session.commit()

        # TODO: Publish a queue for rabbitMQ
        # Exchange RRHH_fire, send project, salary

        flash("Trabajador contratado exitosamente!", "info")
        return redirect(url_for("contracts.index", employee_id=employee_id))


@contracts.route("/contracts/fire/<int:employee_id>", methods=["POST"])
def fire(employee_id):
    if request.method == "POST":
        contract_id = request.form.get("contract_id")
        contract = Contract.query.get(contract_id)
        if not contract:
            flash('No hay contratos', 'warning')
            return redirect(url_for('contracts.index', employee_id=employee_id))

        contract.state = "inactive"
        contract.end_date = date.today()

        db.session.commit()

        # TODO: Publish a queue for rabbitMQ
        # Exchange RRHH_fire, send project, salary
        flash("Trabajador desvinculado exitosamente!", "info")
        return redirect(url_for("contracts.index", employee_id=contract.employee_id))
