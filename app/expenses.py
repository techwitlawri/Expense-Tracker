#  for expense tracking logic and routes(add, edit, delete)


# app/expenses.py

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from . import db
from .models import Expense

# Create the Blueprint object named exp_bp
exp_bp = Blueprint(
    'expenses',            # Blueprint name for routing (url_prefix can be added here)
    __name__,              # This module
    template_folder='../templates'  # where to find templates
)

@exp_bp.route('/dashboard')
@login_required
def dashboard():
    """
    Show the logged-in user their list of expenses.
    """
    # Query only this user's expenses
    my_expenses = Expense.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', expenses=my_expenses)

@exp_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_expense():
    """
    Add a new expense for the logged-in user.
    GET: Show the form; POST: process the form data.
    """
    if request.method == 'POST':
        # Pull data from form
        desc = request.form['description']
        amt  = float(request.form['amount'])
        # Create and save the expense
        new_exp = Expense(description=desc, amount=amt, user_id=current_user.id)
        db.session.add(new_exp)
        db.session.commit()
        flash('Expense added successfully!', 'success')
        return redirect(url_for('expenses.dashboard'))
    # On GET, just render the add_expense form
    return render_template('add_expense.html')

@exp_bp.route('/delete/<int:expense_id>')
@login_required
def delete_expense(expense_id):
    """
    Delete an existing expense by ID, only if it belongs to the current user.
    """
    exp = Expense.query.get_or_404(expense_id)
    # Security check: ensure this expense belongs to the current user
    if exp.user_id != current_user.id:
        flash('You are not authorized to delete this expense.', 'danger')
        return redirect(url_for('expenses.dashboard'))

    db.session.delete(exp)
    db.session.commit()
    flash('Expense deleted.', 'success')
    return redirect(url_for('expenses.dashboard'))
