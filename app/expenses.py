# app/expenses.py

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from .extensions import db            # Import db from extensions
from .models import Expense

exp_bp = Blueprint('expenses', __name__)

@exp_bp.route('/dashboard')
@login_required
def dashboard():
    """
    Show the logged-in user's list of expenses.
    """
    # Query only this user's expenses
    user_expenses = Expense.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', expenses=user_expenses)


@exp_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_expense():
    """
    GET: Show the add-expense form.
    POST: Validate & save the new expense, then redirect back.
    """
    if request.method == 'POST':
        description = request.form.get('description')
        amount      = request.form.get('amount')

        # Basic validation
        if not description or not amount:
            flash('All fields are required.', 'error')
            return redirect(url_for('expenses.add_expense'))

        # Save new expense
        new_exp = Expense(
            description=description,
            amount=float(amount),
            user_id=current_user.id
        )
        db.session.add(new_exp)
        db.session.commit()

        flash('Expense added!', 'success')
        return redirect(url_for('expenses.dashboard'))

    # If GET, just render the form
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
