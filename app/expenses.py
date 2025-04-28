# app/expenses.py

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from .models import Expense,db
from .extensions import db            # Import db from extensions
from datetime import datetime
from flask import  send_file
from io import BytesIO
import base64
import random
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


exp_bp = Blueprint('expenses', __name__)


@exp_bp.route('/dashboard')
@login_required
def dashboard():
    """
    Show the logged-in user's list of expenses.
    """
    # Query only this user's expenses
    user_expenses = Expense.query.filter_by(user_id=current_user.id).all()
    user = current_user  # Get the logged-in user
    expenses = Expense.query.filter_by(user_id=user.id).all()  # Get all user's expenses
    
    # Calculate total expenses
    total_expenses = sum(expense.amount for expense in expenses)
    
    # Calculate the percentage for each category
    category_percentages = {}
    for expense in expenses:
        if expense.category not in category_percentages:
            category_percentages[expense.category] = 0
        category_percentages[expense.category] += expense.amount
    
    # Now calculate the percentage
    for category, amount in category_percentages.items():
        category_percentages[category] = (amount / total_expenses) * 100 if total_expenses > 0 else 0

    return render_template('dashboard.html',
                           user=user,
                           expenses=user_expenses, 
                           total_expenses=total_expenses, 
                           category_percentages=category_percentages)

@exp_bp.route('/add_expense', methods=['GET', 'POST'])
@login_required
def add_expense():
    if request.method == 'POST':
        description = request.form.get('description')
        amount = request.form.get('amount')
        date = request.form.get('date')
         # Get chosen category OR new category
        selected_category = request.form.get('category')
        new_category = request.form.get('new_category').strip()

        category = new_category if new_category else selected_category
       
        # Form validation
        if not all([description, amount, date, category]):
            flash('All fields are required.', 'error')
            return redirect(url_for('expenses.add_expense'))

        # Save to database
        new_expense = Expense(
            description=description,
            amount=float(amount),
            date=datetime.strptime(date, '%Y-%m-%d'),
            user_id=current_user.id,
            category = category
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



@exp_bp.route('/report')
@login_required
def report():
    user_expenses = Expense.query.filter_by(user_id=current_user.id).all()

    category_totals = {}
    for expense in user_expenses:
        if expense.category:
            category_totals[expense.category] = category_totals.get(expense.category, 0) + expense.amount
        else:
            category_totals['Uncategorized'] = category_totals.get('Uncategorized', 0) + expense.amount

    categories = list(category_totals.keys())
    amounts = list(category_totals.values())

    # Generate chart with matplotlib
    plt.figure(figsize=(8, 6))
    plt.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=140)
    plt.title('Expenses by Category')

    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    chart_data = base64.b64encode(img.getvalue()).decode()

    plt.close()

    return render_template('report.html', chart_data=chart_data)


