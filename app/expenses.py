# app/expenses.py

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from .models import Expense
from .extensions import db            # Import db from extensions

from datetime import datetime

exp_bp = Blueprint('expenses', __name__)


@exp_bp.route('/dashboard')
@login_required
def dashboard():
    """
    Show the logged-in user's list of expenses.
    """
    # Query only this user's expenses
    user_expenses = Expense.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', expenses=user_expenses, user=current_user)

@exp_bp.route('/add_expense', methods=['GET', 'POST'])
@login_required
def add_expense():
    if request.method == 'POST':
        description = request.form.get('description')
        amount = request.form.get('amount')
        date = request.form.get('date')

        # Form validation
        if not all([description, amount, date]):
            flash('All fields are required.', 'error')
            return redirect(url_for('expenses.add_expense'))

        # Save to database
        new_expense = Expense(
            description=description,
            amount=float(amount),
            date=datetime.strptime(date, '%Y-%m-%d'),
            user_id=current_user.id,
            currency=current_user.currency  # Use the user's currency
        )

        db.session.add(new_expense)
        db.session.commit()
        flash('Expense added successfully!', 'success')
        return redirect(url_for('expenses.dashboard'))

    return render_template('add_expense.html')




@exp_bp.route('/edit/<int:expense_id>', methods=['GET', 'POST'])
@login_required
def edit_expense(expense_id):
    """
    GET:  Show form populated with the existing expense.
    POST: Update the expense in the DB and redirect back to dashboard.
    """
    # Lookup the expense or 404
    exp = Expense.query.get_or_404(expense_id)

    # Security check: only the owner can edit
    if exp.user_id != current_user.id:
        flash('Not authorized to edit this expense.', 'error')
        return redirect(url_for('expenses.dashboard'))

    if request.method == 'POST':
        # Update fields from the form
        exp.description = request.form.get('description')
        exp.amount      = float(request.form.get('amount'))
        db.session.commit()

        flash('Expense updated!', 'success')
        return redirect(url_for('expenses.dashboard'))

    # On GET, render form with existing data
    return render_template('edit_expense.html', expense=exp)
@exp_bp.route('/delete/<int:expense_id>')
@login_required
def delete_expense(expense_id):
    """
    Delete an existing expense by ID, only if it belongs to the current user.
    """
    exp = Expense.query.get_or_404(expense_id)

    # Security check: only owner can delete
    if exp.user_id != current_user.id:
        flash('You are not authorized to delete this expense.', 'error')
        return redirect(url_for('expenses.dashboard'))

    db.session.delete(exp)
    db.session.commit()
    flash('Expense deleted!', 'success')
    return redirect(url_for('expenses.dashboard'))
