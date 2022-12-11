from utils.db import db
from utils.validate import validate_run

from flask import Blueprint, render_template, redirect, \
    request, flash, url_for
from models.models import Employee

employees = Blueprint('employees', __name__)


@employees.route('/new', methods=['POST'])
def store():
    if request.method == 'POST':
        rut = validate_run(request.form.get("rut"))
        if not rut:
            flash('Rut del trabajador inválido', 'warning')
            return redirect(url_for('index'))

        employee = Employee.query.filter_by(rut=rut).first()
        if employee:
            flash('El trabajador ya existe', 'warning')
            return redirect(url_for('index'))

        new_employee = Employee(
            rut=rut,
            name=request.form.get("name")
        )

        db.session.add(new_employee)
        db.session.commit()

        flash('Trabajador añadido exitosamente!', 'info')

        return redirect(url_for('index'))


@employees.route("/update/<int:employee_id>", methods=["GET", "POST"])
def update(employee_id):
    employee = Employee.query.get(employee_id)

    if request.method == "POST":

        name = request.form.get("name")

        if name != employee.name:
            employee.name = name
            db.session.commit()
            flash('Trabajador actualizado exitosamente!', 'info')

    return render_template("update.html", employee=employee, contracts=employee.contracts)


@employees.route("/delete/<int:employee_id>", methods=["GET"])
def delete(employee_id):
    employee = Employee.query.get(employee_id)

    db.session.delete(employee)
    db.session.commit()

    flash('Trabajador eliminado exitosamente!', 'info')

    return redirect(url_for('index'))
